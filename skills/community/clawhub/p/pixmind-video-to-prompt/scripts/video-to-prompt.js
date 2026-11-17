#!/usr/bin/env node

import { createHash } from "node:crypto"
import { createReadStream, createWriteStream } from "node:fs"
import { mkdir, readFile, rename, stat, unlink, writeFile } from "node:fs/promises"
import { homedir } from "node:os"
import path from "node:path"
import { Readable } from "node:stream"
import { pipeline } from "node:stream/promises"
import { spawn } from "node:child_process"
import { pathToFileURL } from "node:url"

const API_BASE = (process.env.PIXMIND_API_BASE || "https://aihub-admin.aimix.pro").replace(/\/$/, "")
const FFMPEG_MANIFEST =
  process.env.PIXMIND_FFMPEG_MANIFEST ||
  "https://cdn.pixmind.io/pixmind-builder/dependencies/ffmpeg/windows/x64/manifest.json"
const TERMINAL = new Set(["ready", "success", "completed", "failed", "error", "cancelled"])
const SUCCESS = new Set(["ready", "success", "completed"])

const HELP = `Pixmind video-to-prompt

Submit one video, poll the task, extract local storyboard frames, and emit a portable result.

Usage:
  Windows: powershell -NoProfile -ExecutionPolicy Bypass -File run.ps1 [options]
  macOS:   sh run.sh [options]

Inputs:
  --url <video-url> --yes --poll [options]
  --file <video-path> --yes --poll [options]
  --task-id <task-id> --poll [--file <video-path> | --url <video-url>] [options]

Options:
  --url <url>           Remote HTTP(S) video URL
  --file <path>         Local video file
  --task-id <id>        Resume an existing task without another paid submission
  --language <code>     Output language (default: zh-cn)
  --max-scenes <count>  Maximum scenes, 1-100 (default: 100)
  --yes                 Confirm the 100 credits/started-minute charge
  --poll                Wait until the task reaches a terminal state
  --interval <ms>       Poll interval, minimum 2000 (default: 5000)
  --timeout <seconds>   Maximum poll time (default: 1800)
  --output <directory>  Result directory (default: Downloads/pixmind-video-to-prompt/<taskId>)
  --ffmpeg <path>       Explicit FFmpeg executable
  --no-screenshots      Skip local frame extraction
  --help                Show this help
`

function parseArgs(argv) {
  const values = {}
  const flags = new Set(["--yes", "--poll", "--no-screenshots", "--help"])
  const names = new Map([
    ["--url", "url"],
    ["--file", "file"],
    ["--task-id", "taskId"],
    ["--language", "language"],
    ["--max-scenes", "maxScenes"],
    ["--interval", "interval"],
    ["--timeout", "timeout"],
    ["--output", "output"],
    ["--ffmpeg", "ffmpeg"],
  ])

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index]
    if (flags.has(arg)) {
      values[arg.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase())] = true
      continue
    }
    const name = names.get(arg)
    if (!name) throw new Error(`Unknown option: ${arg}`)
    const value = argv[index + 1]
    if (!value || value.startsWith("--")) throw new Error(`Missing value for ${arg}`)
    values[name] = value
    index += 1
  }
  return values
}

function integer(value, fallback, name, minimum, maximum) {
  if (value === undefined) return fallback
  const parsed = Number(value)
  if (!Number.isInteger(parsed) || parsed < minimum || parsed > maximum) {
    throw new Error(`${name} must be an integer from ${minimum} to ${maximum}.`)
  }
  return parsed
}

function record(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value)
}

function responseData(value) {
  if (!record(value)) return undefined
  return record(value.data) ? value.data : value
}

function taskStatus(value) {
  const valueStatus = responseData(value)?.status
  return typeof valueStatus === "string" ? valueStatus.toLowerCase() : "unknown"
}

async function request(pathname, key, init = {}) {
  const response = await fetch(`${API_BASE}${pathname}`, {
    ...init,
    headers: {
      Accept: "application/json",
      Authorization: `Bearer ${key}`,
      ...init.headers,
    },
    signal: AbortSignal.timeout(120_000),
  })
  const body = await response.text()
  const payload = parseJson(body)
  if (!payload) throw new Error(`Pixmind returned invalid JSON (HTTP ${response.status}).`)
  if (!response.ok || (typeof payload.code === "number" && payload.code !== 1000)) {
    const detail = typeof payload.message === "string" ? payload.message : JSON.stringify(payload)
    const hints = {
      400: "Check the video source and ensure the video is no longer than 10 minutes.",
      401: "Configure a valid PIXMIND_API_KEY.",
      402: "The Pixmind account has insufficient credits.",
    }
    throw new Error(
      `Pixmind API error (HTTP ${response.status}): ${detail}${hints[response.status] ? ` ${hints[response.status]}` : ""}`,
    )
  }
  return payload
}

async function submit(options, key) {
  if (options.url) {
    const url = new URL(options.url)
    if (url.protocol !== "http:" && url.protocol !== "https:") throw new Error("--url must use HTTP or HTTPS.")
    return request("/api-platform/v1/video-to-prompt", key, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ videoUrl: options.url, language: options.language, maxScenes: options.maxScenes }),
    })
  }

  const resolved = path.resolve(options.file)
  const info = await stat(resolved).catch(() => undefined)
  if (!info?.isFile()) throw new Error(`Video file not found: ${resolved}`)
  const form = new FormData()
  form.append("videoFile", new Blob([await readFile(resolved)]), path.basename(resolved))
  form.append("language", options.language)
  form.append("maxScenes", String(options.maxScenes))
  return request("/api-platform/v1/video-to-prompt", key, { method: "POST", body: form })
}

async function poll(taskId, options, key) {
  const deadline = Date.now() + options.timeout * 1000
  while (true) {
    const result = await request(`/api-platform/v1/tasks/${encodeURIComponent(String(taskId))}`, key)
    const status = taskStatus(result)
    if (TERMINAL.has(status)) return result
    if (Date.now() >= deadline) throw new Error(`Timed out waiting for Pixmind task ${taskId}.`)
    process.stderr.write(`Task ${taskId}: ${status}${progress(result) !== undefined ? ` ${progress(result)}%` : ""}\n`)
    await new Promise((resolve) => setTimeout(resolve, options.interval))
  }
}

function progress(value) {
  const result = responseData(value)?.progress
  if (typeof result === "number" && Number.isFinite(result)) return result
}

function storyboardData(value) {
  const parsed = typeof value === "string" ? parseJson(value.trim()) : value
  if (Array.isArray(parsed)) return parsed.map(storyboardData).find(Boolean)
  if (!record(parsed)) return undefined

  if (Array.isArray(parsed.data)) {
    const splits = Array.isArray(parsed.splits)
      ? parsed.splits.flatMap((item) => {
          if (!record(item)) return []
          const startTime = Number(item.startTime)
          const endTime = Number(item.endTime)
          if (!Number.isFinite(startTime) || !Number.isFinite(endTime) || startTime < 0 || endTime <= startTime) return []
          return [{ startTime, endTime }]
        })
      : []
    const scenes = parsed.data.flatMap((item, index) => {
      if (!record(item)) return []
      return [
        {
          no: finite(item.no) ?? index + 1,
          startTime: splits[index]?.startTime,
          endTime: splits[index]?.endTime,
          time: finite(item.time),
          view: text(item.view),
          scene: text(item.scence) || text(item.scene),
          script: text(item.text),
          description: text(item.description),
          prompt: text(item.prompt),
          camera: text(item.camera),
          colorTone: text(item.colorTone),
          dialogue: text(item.dialogue),
          soundEffect: text(item.soundEffect),
          transition: text(item.transition),
        },
      ]
    })
    if (scenes.length > 0) {
      return {
        videoDescription: text(parsed.videoDescription),
        videoSummary: text(parsed.videoSummary),
        videoPrompt: text(parsed.videoPrompt),
        fullStoryboardPrompt: text(parsed.fullStoryboardPrompt),
        splits,
        scenes,
      }
    }
  }

  return Object.values(parsed).map(storyboardData).find(Boolean)
}

async function screenshots(source, storyboard, taskId, options) {
  if (!source || options.noScreenshots || storyboard.splits.length === 0) return []
  const directory = path.resolve(options.output || path.join(homedir(), "Downloads", "pixmind-video-to-prompt", taskId))
  await mkdir(directory, { recursive: true })
  const ffmpeg = await resolveFfmpeg(options.ffmpeg)
  const results = await mapLimit(storyboard.splits, 4, async (split, index) => {
    const timestamp = (split.startTime + split.endTime) / 2
    const filename = `scene-${String(index + 1).padStart(3, "0")}_${timestamp.toFixed(3).replace(".", "-")}s.jpg`
    const output = path.join(directory, filename)
    try {
      await run(ffmpeg, [
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        String(timestamp),
        "-i",
        source,
        "-frames:v",
        "1",
        "-vf",
        "crop=min(iw\\,ih*9/16):min(ih\\,iw*16/9):(iw-ow)/2:(ih-oh)/2,scale=640:-2",
        "-q:v",
        "5",
        output,
      ])
      return { scene: index, path: output, filename, timestamp }
    } catch (error) {
      process.stderr.write(`Screenshot ${index + 1} failed: ${error instanceof Error ? error.message : String(error)}\n`)
      return undefined
    }
  })
  return results.filter(Boolean)
}

async function resolveFfmpeg(explicit) {
  const candidates = [explicit, process.env.PIXMIND_FFMPEG_PATH, "ffmpeg"].filter(Boolean)
  for (const candidate of candidates) {
    if (await works(candidate)) return candidate
  }
  if (process.platform !== "win32" || process.arch !== "x64") {
    throw new Error("FFmpeg was not found. Install FFmpeg or set PIXMIND_FFMPEG_PATH.")
  }

  const manifest = await fetchJson(FFMPEG_MANIFEST)
  if (!Array.isArray(manifest.versions)) throw new Error("Invalid Pixmind FFmpeg manifest.")
  const versions = [...manifest.versions].sort((left, right) => Number(right.version === manifest.preferred) - Number(left.version === manifest.preferred))
  const errors = []
  for (const version of versions) {
    try {
      return await installFfmpeg(version)
    } catch (error) {
      errors.push(error instanceof Error ? error.message : String(error))
    }
  }
  throw new Error(`Unable to install Pixmind FFmpeg: ${errors.join("; ")}`)
}

async function installFfmpeg(version) {
  if (!record(version) || typeof version.version !== "string" || typeof version.url !== "string") {
    throw new Error("Invalid FFmpeg version entry.")
  }
  const directory = path.join(cacheRoot(), "ffmpeg", "windows-x64", version.version)
  const executable = path.join(directory, "ffmpeg.exe")
  if (await validFfmpeg(executable, version)) return executable
  await mkdir(directory, { recursive: true })
  const temporary = `${executable}.${process.pid}.download`
  process.stderr.write(`Downloading FFmpeg ${version.version} from Pixmind R2...\n`)
  try {
    await download(version.url, temporary).catch(async (error) => {
      const fallback = version.url.replace("https://cdn.pixmind.io/dependencies/", "https://cdn.pixmind.io/pixmind-builder/dependencies/")
      if (fallback === version.url) throw error
      await download(fallback, temporary)
    })
    if (!(await validFile(temporary, version))) throw new Error(`FFmpeg ${version.version} failed size or SHA-256 validation.`)
    await rename(temporary, executable).catch(async () => {
      if (!(await validFfmpeg(executable, version))) throw new Error(`Unable to activate FFmpeg ${version.version}.`)
    })
  } finally {
    await unlink(temporary).catch(() => undefined)
  }
  if (!(await works(executable))) throw new Error(`FFmpeg ${version.version} is not executable.`)
  return executable
}

async function validFfmpeg(file, version) {
  return (await validFile(file, version)) && (await works(file))
}

async function validFile(file, version) {
  const info = await stat(file).catch(() => undefined)
  if (!info?.isFile()) return false
  if (typeof version.size === "number" && info.size !== version.size) return false
  if (typeof version.sha256 === "string" && (await sha256(file)) !== version.sha256.toLowerCase()) return false
  return true
}

async function works(command) {
  return run(command, ["-version"]).then(
    () => true,
    () => false,
  )
}

async function run(command, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] })
    const stderr = []
    child.stderr.on("data", (chunk) => stderr.push(chunk))
    child.on("error", reject)
    child.on("close", (code) => {
      if (code === 0) return resolve()
      reject(new Error(`${path.basename(command)} exited with code ${code}: ${Buffer.concat(stderr).toString("utf8").trim()}`))
    })
  })
}

async function download(url, destination) {
  const response = await fetch(url, { signal: AbortSignal.timeout(900_000) })
  if (!response.ok || !response.body) throw new Error(`Download failed (HTTP ${response.status}): ${url}`)
  await pipeline(Readable.fromWeb(response.body), createWriteStream(destination))
}

async function fetchJson(url) {
  const response = await fetch(url, { headers: { Accept: "application/json" }, signal: AbortSignal.timeout(120_000) })
  if (!response.ok) throw new Error(`Request failed (HTTP ${response.status}): ${url}`)
  return response.json()
}

async function sha256(file) {
  const hash = createHash("sha256")
  for await (const chunk of createReadStream(file)) hash.update(chunk)
  return hash.digest("hex")
}

function cacheRoot() {
  if (process.env.PIXMIND_CACHE_DIR) return path.resolve(process.env.PIXMIND_CACHE_DIR)
  if (process.platform === "win32") return path.join(process.env.LOCALAPPDATA || homedir(), "Pixmind", "cache")
  return path.join(homedir(), ".cache", "pixmind")
}

function presentation(storyboard, frames, language) {
  const zh = language.toLowerCase().startsWith("zh")
  const labels = zh
    ? ["序号", "参考图", "时长", "景别", "脚本", "场景描述", "视频提示词"]
    : ["Scene", "Reference image", "Duration", "Shot type", "Script", "Scene description", "Video prompt"]
  const frameIndexes = new Map(frames.map((frame, index) => [frame.scene, index]))
  return {
    type: "data-table",
    sections: [
      storyboard.videoDescription ? { title: zh ? "视频描述" : "Video description", content: storyboard.videoDescription } : undefined,
      storyboard.videoSummary ? { title: zh ? "视频总结" : "Video summary", content: storyboard.videoSummary } : undefined,
      storyboard.videoPrompt
        ? { title: zh ? "视频提示词" : "Video prompt", content: storyboard.videoPrompt, variant: "highlight", copy: true }
        : undefined,
      {
        title: zh ? "完整分镜提示词" : "Full storyboard prompt",
        content: storyboard.fullStoryboardPrompt || formatStoryboard(storyboard.scenes, zh),
        variant: "code",
        copy: true,
      },
    ].filter(Boolean),
    table: {
      columns: [
        { key: "scene", label: labels[0], width: "xs" },
        { key: "image", label: labels[1], width: "image" },
        { key: "duration", label: labels[2], width: "xs" },
        { key: "shot", label: labels[3], width: "sm" },
        { key: "script", label: labels[4], width: "md" },
        { key: "visual", label: labels[5], width: "md" },
        { key: "prompt", label: labels[6], width: "lg" },
      ],
      rows: storyboard.scenes.map((scene, index) => ({
        scene: scene.no,
        image: frameIndexes.has(index) ? { type: "attachment", index: frameIndexes.get(index), alt: `${labels[1]} ${scene.no}` } : "",
        duration: duration(scene),
        shot: { type: "badge", text: scene.view, detail: scene.scene },
        script: { type: "callout", text: scene.script },
        visual: scene.description || "",
        prompt: { type: "copy", text: scene.prompt },
      })),
    },
  }
}

function formatStoryboard(scenes, zh) {
  return scenes
    .map((scene) => {
      const values = zh
        ? [["景别", scene.view], ["场景", scene.scene], ["运镜", scene.camera], ["色调", scene.colorTone], ["画面", scene.description], ["台词", scene.dialogue], ["音效", scene.soundEffect], ["转场", scene.transition], ["提示词", scene.prompt]]
        : [["Shot Type", scene.view], ["Scene", scene.scene], ["Camera", scene.camera], ["Color Tone", scene.colorTone], ["Visual", scene.description], ["Dialogue", scene.dialogue], ["Sound Effect", scene.soundEffect], ["Transition", scene.transition], ["Prompt", scene.prompt]]
      return [`【${zh ? "分镜" : "No."} ${scene.no} | ${duration(scene)}】`, ...values.flatMap(([key, value]) => (value ? [`${key}：${value}`] : []))].join("\n")
    })
    .join("\n\n")
}

function duration(scene) {
  const value = scene.time ?? (scene.startTime !== undefined && scene.endTime !== undefined ? scene.endTime - scene.startTime : undefined)
  return value === undefined ? "-" : `${Number(value.toFixed(2))}s`
}

function finite(value) {
  const result = typeof value === "number" ? value : typeof value === "string" ? Number(value) : Number.NaN
  if (Number.isFinite(result)) return result
}

function text(value) {
  if (typeof value === "string" && value.trim()) return value
}

function parseJson(value) {
  try {
    return JSON.parse(value)
  } catch {
    return undefined
  }
}

async function mapLimit(items, concurrency, fn) {
  const results = Array(items.length)
  let next = 0
  await Promise.all(
    Array.from({ length: Math.min(concurrency, items.length) }, async () => {
      while (next < items.length) {
        const index = next
        next += 1
        results[index] = await fn(items[index], index)
      }
    }),
  )
  return results
}

async function main() {
  const args = parseArgs(process.argv.slice(2))
  if (args.help) return process.stdout.write(HELP)

  const sourceCount = [args.url, args.file].filter(Boolean).length
  if (sourceCount > 1) throw new Error("Provide only one of --url or --file.")
  if (!args.taskId && sourceCount !== 1) throw new Error("Provide one of --url or --file for a new task.")
  if (!args.taskId && !args.yes) {
    throw new Error("Paid submission not confirmed. Review the 100 credits per started minute charge, then add --yes.")
  }

  const key = process.env.PIXMIND_API_KEY?.trim()
  if (!key) throw new Error("PIXMIND_API_KEY is not configured.")
  const options = {
    ...args,
    language: args.language || "zh-cn",
    maxScenes: integer(args.maxScenes, 100, "--max-scenes", 1, 100),
    interval: integer(args.interval, 5000, "--interval", 2000, 300000),
    timeout: integer(args.timeout, 1800, "--timeout", 10, 86400),
  }
  const source = options.file ? path.resolve(options.file) : options.url
  const submitted = options.taskId ? undefined : await submit(options, key)
  const taskId = options.taskId ?? responseData(submitted)?.taskId
  if (taskId === undefined || taskId === null) throw new Error("Pixmind did not return a taskId.")
  if (!options.poll) {
    process.stdout.write(`${JSON.stringify({ type: "pixmind-video-to-prompt-task", taskId: String(taskId), submitted }, null, 2)}\n`)
    return
  }

  const result = await poll(taskId, options, key)
  const status = taskStatus(result)
  if (!SUCCESS.has(status)) throw new Error(`Pixmind task ${taskId} ended with status: ${status}.`)
  const storyboard = storyboardData(result)
  if (!storyboard) throw new Error(`Pixmind task ${taskId} did not contain structured storyboard data.`)
  const outputDirectory = path.resolve(options.output || path.join(homedir(), "Downloads", "pixmind-video-to-prompt", String(taskId)))
  const frames = await screenshots(source, storyboard, String(taskId), { ...options, output: outputDirectory })
  const attachments = frames.map((frame) => ({
    type: "file",
    mime: "image/jpeg",
    url: pathToFileURL(frame.path).href,
    filename: frame.filename,
  }))
  const output = {
    schemaVersion: 1,
    type: "pixmind-video-to-prompt",
    taskId: String(taskId),
    status,
    outputDirectory,
    storyboard,
    screenshots: frames,
    attachments,
    presentation: presentation(storyboard, frames, options.language),
    raw: result,
  }
  await mkdir(outputDirectory, { recursive: true })
  await writeFile(path.join(outputDirectory, "result.json"), `${JSON.stringify(output, null, 2)}\n`)
  process.stdout.write(`${JSON.stringify(output, null, 2)}\n`)
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`)
  process.exitCode = 1
})
