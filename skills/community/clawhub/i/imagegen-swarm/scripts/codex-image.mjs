#!/usr/bin/env node
import { spawn } from "node:child_process";
import { readFile, writeFile, open, stat, mkdir, readdir, unlink, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { homedir } from "node:os";
import path from "node:path";
import { markRunDir, sandboxMayWiden, userApprovedSandboxWiden } from "./safety.mjs";
import { isInvokedDirectly } from "./direct.mjs";
import { SHELL_METACHAR } from "./shell-meta.mjs";
import { STDIO_DISCARD } from "./stdio-modes.mjs";

function parseArgs(argv) {
  const o = {
    prompt: "", promptFile: null, out: "", aspect: "1:1", refs: [],
    sandbox: "workspace-write", escalateSandbox: false,
    timeoutMs: 300_000, retries: 2, codex: null, json: false, model: "gpt-6-luna", effort: "low",
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => argv[++i];
    switch (a) {
      case "--prompt": o.prompt = next(); break;
      case "--prompt-file": o.promptFile = next(); break;
      case "--out": case "--image": o.out = next(); break;
      case "--aspect": case "--ar": o.aspect = next(); break;
      case "--ref": o.refs.push(next()); break;
      case "--sandbox": o.sandbox = next(); break;
      case "--escalate-sandbox": o.escalateSandbox = true; break;
      case "--timeout": o.timeoutMs = Number(next()); break;
      case "--retries": o.retries = Number(next()); break;
      case "--codex": o.codex = next(); break;
      case "--model": o.model = next(); break;
      case "--effort": o.effort = next(); break;
      case "--json": o.json = true; break;
      case "-h": case "--help": printHelp(); process.exit(0);
      default: fail("invalid_args", "Unknown argument: " + (a));
    }
  }
  if (!o.out) fail("invalid_args", "--out is required");
  if (o.prompt && o.promptFile) fail("invalid_args", "--prompt and --prompt-file are mutually exclusive");
  if (!o.prompt && !o.promptFile) fail("invalid_args", "--prompt or --prompt-file required");
  const abs = (p) => (path.isAbsolute(p) ? p : path.resolve(process.cwd(), p));
  o.out = abs(o.out);
  if (o.promptFile) o.promptFile = abs(o.promptFile);
  o.refs = o.refs.map(abs);
  if (SHELL_METACHAR.test(o.out)) fail("invalid_args", "--out path has unsafe characters: " + (o.out));
  for (const r of o.refs) if (SHELL_METACHAR.test(r)) fail("invalid_args", "--ref path has unsafe characters: " + (r));
  return o;
}

function printHelp() {
  process.stdout.write("codex-image.mjs — image via Codex CLI image_gen\n\n" +
    "node codex-image.mjs --out <png> (--prompt <t> | --prompt-file <p>) [--aspect 1:1] [--ref f]... [--sandbox workspace-write] [--escalate-sandbox] [--timeout ms] [--retries n] [--codex path] [--model gpt-6-luna] [--effort low] [--json]\n\n" +
    "--escalate-sandbox: does not widen this process by itself. A later attempt\n" +
    "leaves workspace-write only when the log says the sandbox blocked the write\n" +
    "AND the user has set IMAGE_GEN_SANDBOX_ESCALATE=yes for that retry.\n" +
    "The agent must not set that variable. Other failures stay in workspace-write.\n");
}

let JSON_MODE = false;
function fail(kind, msg) {
  if (JSON_MODE) process.stdout.write(JSON.stringify({ status: "error", error: msg, error_kind: kind }) + "\n");
  else process.stderr.write("Error [" + (kind) + "]: " + (msg) + "\n");
  process.exit(kind === "invalid_args" ? 2 : 1);
}

function desktopAppCandidates() {
  if (process.platform === "darwin") {
    return [
      "/Applications/Codex.app/Contents/Resources/codex",
      path.join(homedir(), "Applications", "Codex.app", "Contents", "Resources", "codex"),
    ];
  }
  return [];
}

async function resolveCodex(explicit) {
  explicit = explicit || process.env.CODEX_BIN || null;
  if (explicit) {
    if (!existsSync(explicit)) fail("codex_not_installed", "codex path not found: " + (explicit));
    return explicit;
  }
  const onPath = await new Promise((res) => {
    const c = spawn("codex", ["--version"], { stdio: STDIO_DISCARD, shell: process.platform === "win32" });
    c.on("error", () => res(false));
    c.on("close", (code) => res(code === 0));
  });
  if (onPath) return "codex";
  for (const c of desktopAppCandidates()) if (existsSync(c)) return c;
  const binDir = path.join(homedir(), "AppData", "Local", "OpenAI", "Codex", "bin");
  if (existsSync(binDir)) {
    let best = null, bestMtime = 0;
    for (const d of await readdir(binDir)) {
      const exe = path.join(binDir, d, "codex.exe");
      try { const s = await stat(exe); if (s.mtimeMs > bestMtime) { bestMtime = s.mtimeMs; best = exe; } } catch {}
    }
    if (best) return best;
  }
  fail("codex_not_installed", "codex CLI not found: not a working codex on PATH, not in Codex.app (macOS), not under the user profile AppData/Local/OpenAI/Codex/bin (Windows). Install @openai/codex or the Codex app, then run codex login. If a broken npm shim is shadowing a good binary, point at it with --codex <path> or $CODEX_BIN.");
}

// image_gen 没有尺寸参数，画幅只由提示词决定：把比例写进交给它的提示词末尾
const FORMATS = { "1:1": "Square 1:1 image.", "3:2": "Landscape 3:2 image.", "2:3": "Portrait 2:3 image.", "4:3": "Landscape 4:3 image.",
  "3:4": "Portrait 3:4 image.", "16:9": "Wide landscape 16:9 image.", "9:16": "Tall portrait 9:16 image.", "2.35:1": "Cinematic ultra-wide 2.35:1 image." };

function buildInstruction(prompt, o) {
  const refHint = o.refs.length > 0
    ? "\nREFERENCE IMAGES (attached above): " + (o.refs.length) + " image(s) provided for style/composition guidance.\n"
    : "";
  return "You have an internal image generation tool, exposed as image_gen.imagegen (it may also be\nreferred to as image_gen). You MUST call it before doing anything else.\n\nTASK: Generate an image with the spec below, then save to disk.\n\nIMAGE_GEN PROMPT (pass it to image_gen exactly as written, character for character):\n" + (prompt.trim()) + "\n" + (FORMATS[o.aspect] ?? "Aspect ratio " + (o.aspect) + ".") + "\n\nOUTPUT PATH: " + (o.out) + "\n" + (refHint) + "\nSTEPS:\n1. Call image_gen once with the IMAGE_GEN PROMPT above as its prompt, unchanged" + (o.refs.length > 0 ? ", passing the attached reference images" : "") + ".\n2. Move or copy ONLY the image produced by that image_gen call from Codex default location ($CODEX_HOME/generated_images/...) to: " + (o.out) + "\n3. Verify with: ls -la " + (o.out) + "\n4. Reply with ONLY this JSON line (no markdown fences, no other text):\n   {\"status\":\"ok\",\"path\":\"" + (o.out) + "\",\"bytes\":<file_size_in_bytes>}\n\nHARD CONSTRAINTS:\n- Do NOT search for, find, inspect, reuse, or copy any pre-existing files from $CODEX_HOME/generated_images/ or any other directory.\n- Do NOT run ls/find/rg/grep/glob over $CODEX_HOME/generated_images/ before image_gen has been called.\n- You MUST call image_gen first. Only after image_gen completes may you copy the newly created file from this turn.\n- Do NOT use curl, wget, Python, or any external API.\n- Do NOT use bash to fabricate an image; only image_gen produces real pixels.\n- Use ONLY the image_gen internal tool.\n- If image_gen fails or is unavailable, do NOT substitute any other file. Reply with\n  {\"status\":\"error\",\"reason\":\"<what failed>\"} instead. Delivering an unrelated image is a\n  worse outcome than reporting failure, and the caller verifies this by content hash.";
}

function generatedImagesRoot() {
  return path.join(process.env.CODEX_HOME || path.join(homedir(), ".codex"), "generated_images");
}

// 拒绝把 generated_images 中的旧图当作本轮产物。
async function snapshotGeneratedImages() {
  const files = [];
  async function walk(dir) {
    let entries;
    try { entries = await readdir(dir, { withFileTypes: true }); } catch { return; }
    for (const e of entries) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) await walk(p);
      else if (e.isFile()) { try { files.push({ path: p, size: (await stat(p)).size }); } catch {} }
    }
  }
  await walk(generatedImagesRoot());
  return files;
}

async function sha256(file) {
  return createHash("sha256").update(await readFile(file)).digest("hex");
}

async function findStaleSource(outPath, snapshot) {
  let outSize;
  try { outSize = (await stat(outPath)).size; } catch { return null; }
  const candidates = snapshot.filter((f) => f.size === outSize);
  if (candidates.length === 0) return null;
  const outHash = await sha256(outPath).catch(() => null);
  if (!outHash) return null;
  for (const c of candidates) {
    const h = await sha256(c.path).catch(() => null);
    if (h && h === outHash) return c.path;
  }
  return null;
}

async function isPng(file) {
  try {
    const fh = await open(file, "r");
    const buf = Buffer.alloc(8);
    await fh.read(buf, 0, 8, 0);
    await fh.close();
    return buf.equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));
  } catch { return false; }
}

function sandboxBlocked(processResult) {
  const text = ((processResult.stderr || "") + "\n" + (processResult.stdout || "")).toLowerCase();
  if (text.includes("operation not permitted")) return true;
  return text.includes("sandbox") && /block|denied|not permitted|permission|eacces|eperm/.test(text);
}

export function extractCodexAgentError(stdout) {
  for (const line of String(stdout || "").split(/\n/).reverse()) {
    let event;
    try { event = JSON.parse(line); } catch { continue; }
    const item = event?.item;
    if (item?.type !== "agent_message" || typeof item.text !== "string") continue;
    const message = item.text.trim().replace(/^```(?:json)?\s*|\s*```$/gi, "");
    try {
      const result = JSON.parse(message);
      return result?.status === "error" && typeof result.reason === "string" ? result : null;
    } catch {
      return null;
    }
  }
  return null;
}

export function isImageGenUnavailable(reason) {
  const text = String(reason || "").toLowerCase();
  return /image_gen/.test(text) && /unavailable|not available/.test(text);
}

function runCodexExec(codex, instruction, o, cwd) {
  return new Promise((resolve) => {
    // 固定走 OpenAI 官方通道：config.toml 可能把 Codex 接到本机路由网关，网关不转发 image_gen
    const args = ["exec", "--json", "-c", 'model_provider="openai"', "-m", o.model, "-c", "model_reasoning_effort=\"" + (o.effort) + "\"",
      "--sandbox", o.sandbox, "--skip-git-repo-check", "-C", cwd];
    for (const r of o.refs) args.push("--image", r);
    args.push("-");
    let stdout = "", stderr = "", timedOut = false;
    const child = spawn(codex, args, { stdio: ["pipe", "pipe", "pipe"], shell: false, cwd });
    child.on("error", (e) => resolve({ code: -1, stdout, stderr: stderr + String(e), timedOut }));
    child.stdout.on("data", (c) => { stdout += c.toString(); });
    child.stderr.on("data", (c) => { stderr += c.toString(); });
    child.stdin.write(instruction);
    child.stdin.end();
    const t = setTimeout(() => { timedOut = true; child.kill("SIGTERM"); setTimeout(() => child.kill("SIGKILL"), 2000); }, o.timeoutMs);
    child.on("close", (code) => { clearTimeout(t); resolve({ code, stdout, stderr, timedOut }); });
  });
}

async function main() {
  const o = parseArgs(process.argv.slice(2));
  JSON_MODE = o.json;
  const codex = await resolveCodex(o.codex);
  const prompt = o.promptFile ? await readFile(o.promptFile, "utf-8").catch(() => fail("prompt_file_missing", "Prompt file not found: " + (o.promptFile))) : o.prompt;
  const outDir = path.dirname(o.out);
  await mkdir(outDir, { recursive: true });
  const instruction = buildInstruction(prompt, o);

  const logDir = path.join(outDir, ".codex-img-" + (Date.now()));
  await mkdir(logDir, { recursive: true }).catch(() => {});
  await markRunDir(logDir);
  const start = Date.now();
  let lastErr = "unknown";
  const preExisting = await snapshotGeneratedImages();
  const outPreExisted = existsSync(o.out);
  let outBefore = null;
  if (outPreExisted) {
    const info = await stat(o.out);
    outBefore = { size: info.size, mtimeMs: info.mtimeMs, hash: await sha256(o.out) };
  }
  for (let attempt = 1; attempt <= o.retries + 1; attempt++) {
    if (!o.json) process.stderr.write("[codex] attempt " + (attempt) + "/" + (o.retries + 1) + " (sandbox=" + (o.sandbox) + ") -> " + (o.out) + "\n");
    const processResult = await runCodexExec(codex, instruction, o, outDir);
    await writeFile(path.join(logDir, "attempt-" + (attempt) + ".log"), processResult.stdout + "\n--- stderr ---\n" + processResult.stderr).catch(() => {});
    if (processResult.timedOut) { lastErr = "timeout after " + (o.timeoutMs) + "ms"; continue; }
    if (processResult.code === -1 || processResult.stderr.includes("not found: codex") || processResult.stderr.includes("command not found")) fail("codex_not_installed", "codex could not be launched: " + (processResult.stderr.slice(0, 300)));
    const outputIsPng = existsSync(o.out) && await isPng(o.out);
    const outputUnchanged = outputIsPng && outPreExisted && await sha256(o.out) === outBefore.hash;
    if (outputIsPng && !outputUnchanged) {
      const stale = await findStaleSource(o.out, preExisting);
      if (stale) {
        lastErr = "rejected output: byte-identical to a pre-existing image (" + (stale) + ") — image_gen did not produce a new image this run";
        if (!o.json) process.stderr.write("[codex] attempt " + (attempt) + " REJECTED: " + (lastErr) + "\n");
        if (!outPreExisted) await unlink(o.out).catch(() => {});
        continue;
      }
      // 成功就删掉本轮日志；失败时日志留在输出目录供排查
      await rm(logDir, { recursive: true, force: true });
      const s = await stat(o.out);
      const result = { status: "ok", provider: "codex", path: o.out, bytes: s.size, aspect: o.aspect, attempts: attempt, elapsed_seconds: Math.round((Date.now() - start) / 1000) };
      if (o.json) process.stdout.write(JSON.stringify(result) + "\n");
      else process.stdout.write("OK  codex  " + (o.out) + "  (" + (s.size) + " bytes, " + (result.elapsed_seconds) + "s, attempt " + (attempt) + ")\n");
      process.exit(0);
    }
    const agentErr = extractCodexAgentError(processResult.stdout);
    if (agentErr && isImageGenUnavailable(agentErr.reason)) {
      fail("image_gen_unavailable", (agentErr.reason) + " — 这个 Codex 账号没有出图工具（免费套餐常见）");
    }
    lastErr = agentErr && agentErr.reason
      ? agentErr.reason
      : outputUnchanged
      ? "no new PNG at " + (o.out) + ": the file is unchanged from before this run (codex exec exited " + (processResult.code) + ": " + (processResult.stderr.slice(0, 200)) + ")"
      : processResult.code !== 0 ? "codex exec exited " + (processResult.code) + ": " + (processResult.stderr.slice(0, 200)) : "no valid PNG at " + (o.out) + " (agent may not have called image_gen, or sandbox blocked the write)";
    if (!o.json) process.stderr.write("[codex] attempt " + (attempt) + " failed: " + (lastErr) + "\n");
    const blocked = sandboxBlocked(processResult);
    const approved = userApprovedSandboxWiden();
    if (sandboxMayWiden({ escalateSandbox: o.escalateSandbox, approved, blocked, sandbox: o.sandbox })) {
      o.sandbox = "danger-full-access";
      if (!o.json) process.stderr.write("[codex] sandbox blocked the write and the user approved a wider sandbox -> retrying remaining attempts with danger-full-access\n");
    } else if (blocked && o.escalateSandbox && !approved) {
      lastErr += " — sandbox blocked the write. Not retrying with a wider sandbox. The user must set IMAGE_GEN_SANDBOX_ESCALATE=yes before a broader retry. The agent must not set it.";
      if (!o.json) process.stderr.write("[codex] not escalating: --escalate-sandbox is set but the user has not approved IMAGE_GEN_SANDBOX_ESCALATE=yes\n");
    } else if (blocked && o.sandbox === "workspace-write") {
      lastErr += " — sandbox blocked the write. Ask the user before a wider sandbox. They must set IMAGE_GEN_SANDBOX_ESCALATE=yes themselves.";
      if (!o.json) process.stderr.write("[codex] not escalating the sandbox; the user must set IMAGE_GEN_SANDBOX_ESCALATE=yes\n");
    } else if (o.escalateSandbox && !blocked) {
      if (!o.json) process.stderr.write("[codex] not escalating: this failure is not a sandbox block\n");
    }
  }
  fail("generation_failed", (lastErr) + " (logs: " + (logDir) + ")");
}

if (isInvokedDirectly(import.meta.url)) main().catch((e) => fail("spawn_failed", String(e?.stack || e)));
