#!/usr/bin/env node
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdir, mkdtemp, readdir, readFile, copyFile, rm, stat } from 'node:fs/promises';
import { homedir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { markRunDir } from './safety.mjs';
import { STDIO_DISCARD, STDIO_PIPE } from './stdio-modes.mjs';

function parse(argv) {
  const o = { ratio: '1:1', video: false, timeout: 600000 };
  for (let i = 0; i < argv.length; i++) {
    const flag = argv[i];
    if (flag === '--video') { o.video = true; continue; }
    if (flag === '--json') continue;
    if (flag === '--help' || flag === '-h') {
      console.log('grok-image.mjs --prompt <text> --out <png|mp4> [--ref <image>] [--video] [--ratio 1:1|16:9|9:16|3:2|2:3|auto] [--timeout ms] [--json]');
      process.exit(0);
    }
    const keys = { '--prompt': 'prompt', '--prompt-file': 'promptFile', '--out': 'out', '--ref': 'ref', '--ratio': 'ratio', '--timeout': 'timeout' };
    if (!keys[flag] || !argv[i + 1] || argv[i + 1].startsWith('--')) throw new Error("invalid argument: " + (flag));
    if (o[keys[flag]] !== undefined && !['ratio', 'timeout'].includes(keys[flag])) throw new Error("duplicate argument: " + (flag));
    o[keys[flag]] = argv[++i];
  }
  if (!o.out || Boolean(o.prompt) === Boolean(o.promptFile)) throw new Error('require --out and exactly one of --prompt / --prompt-file');
  if (!['1:1', '16:9', '9:16', '3:2', '2:3', 'auto'].includes(o.ratio)) throw new Error('unsupported --ratio');
  if (o.video && (!o.ref || o.ratio === 'auto')) throw new Error('--video requires --ref and an explicit --ratio (default 1:1)');
  o.timeout = Number(o.timeout);
  if (!Number.isFinite(o.timeout) || o.timeout <= 0) throw new Error('--timeout must be positive milliseconds');
  o.out = path.resolve(o.out);
  if (path.extname(o.out).toLowerCase() !== (o.video ? '.mp4' : '.png')) throw new Error('--out extension must be .png, or .mp4 with --video');
  if (o.ref) o.ref = path.resolve(o.ref);
  return o;
}

function runProcess(bin, args, cwd, limitMs = 60000, details = false) {
  return new Promise((resolve, reject) => {
    const child = spawn(bin, args, { cwd, stdio: [STDIO_DISCARD, STDIO_PIPE, STDIO_PIPE], shell: false });
    let stdout = '', stderr = '', timedOut = false;
    child.stdout.on('data', d => { stdout += d; });
    child.stderr.on('data', d => { stderr += d; });
    let killTimer;
    const timer = setTimeout(() => {
      timedOut = true; child.kill('SIGTERM');
      killTimer = setTimeout(() => child.kill('SIGKILL'), 2000);
    }, limitMs);
    child.on('error', e => { clearTimeout(timer); reject(e); });
    child.on('close', code => {
      clearTimeout(timer); clearTimeout(killTimer);
      if (timedOut) reject(new Error((bin) + " timeout after " + (limitMs) + "ms"));
      else if (code !== 0) reject(new Error((bin) + " exited " + (code) + ": " + (stderr + "\n" + stdout)));
      else resolve(details ? { stdout, stderr } : stdout);
    });
  });
}

const digest = async file => createHash('sha256').update(await readFile(file)).digest('hex');
// 图片转换、尺寸、解码指纹都交给跨平台的 imgtool.py（Pillow）
const PY = process.env.PYTHON ?? (process.platform === 'win32' ? 'python' : 'python3');
const IMGTOOL = path.join(path.dirname(fileURLToPath(import.meta.url)), 'imgtool.py');
async function mediaFiles(root) {
  let entries;
  try { entries = await readdir(root, { withFileTypes: true }); }
  catch (e) { if (e.code === 'ENOENT') return []; throw e; }
  const files = [];
  for (const entry of entries) {
    const p = path.join(root, entry.name);
    if (entry.isDirectory()) files.push(...await mediaFiles(p));
    else if (entry.isFile() && /\.(png|jpe?g|webp|gif|bmp|heic|mp4|mov)$/i.test(p)) files.push(p);
  }
  return files;
}

export function grokModeFromEnv(env = process.env) {
  const mode = (env.IMAGE_GEN_GROK_MODE || "").trim();
  if (mode === "scoped" || mode === "legacy") return mode;
  return "auto";
}

export function grokCliArgs(tool, instruction, mode) {
  const denials = ["--deny", "Bash", "--deny", "WebFetch", "--deny", "WebSearch"];
  if (mode === "legacy") {
    return ["-p", instruction, "--output-format", "json", "--always-approve", "--sandbox", "workspace", ...denials];
  }
  return ["-p", instruction, "--output-format", "json", "--permission-mode", "dontAsk", "--sandbox", "workspace",
    "--tools", (tool) + ",Write", "--allow", tool, "--allow", "Write", ...denials];
}

export function grokLooksDenied(text) {
  const t = String(text || "").toLowerCase();
  return /not available|unavailable|permission denied|not allowed|not permitted|unknown tool|disallowed|tool .*denied|not in the (allowed )?tool/.test(t);
}

export function grokModeLabel(mode) {
  return mode === "legacy" ? "legacy-always-approve" : "scoped";
}

async function runGrokJob(tool, instruction, work, limitMs) {
  const setting = grokModeFromEnv();
  const mode = setting === "legacy" ? "legacy" : "scoped";
  const { stdout, stderr } = await runProcess("grok", grokCliArgs(tool, instruction, mode), work, limitMs, true);
  return { reply: stdout, stderr, grok_mode: grokModeLabel(mode) };
}

async function main() {
  const start = Date.now(), o = parse(process.argv.slice(2));
  const prompt = o.promptFile ? await readFile(o.promptFile, 'utf8') : o.prompt;
  if (!prompt.trim()) throw new Error('empty prompt');
  await mkdir(path.dirname(o.out), { recursive: true });
  const work = await mkdtemp(path.join(path.dirname(o.out), ".grok-image-" + (Date.now()) + "-"));
  await markRunDir(work);
  try {
    // 图片解码后再散列，防止把旧 JPEG 转成 PNG 冒充新图；视频按原文件散列。一次进程算完一批图
    const isVideo = file => /\.(mp4|mov)$/i.test(file);
    async function fingerprints(files) {
      const images = files.filter(f => !isVideo(f));
      const fps = images.length ? JSON.parse(await runProcess(PY, [IMGTOOL, 'fp', ...images], work)).fp : [];
      return [...fps, ...await Promise.all(files.filter(isVideo).map(digest))];
    }
    const sessions = path.join(homedir(), '.grok', 'sessions');
    const before = new Map(), oldHashes = new Set();
    const existing = await mediaFiles(sessions);
    for (const file of existing) before.set(file, true);
    for (const hash of await fingerprints(existing)) oldHashes.add(hash);
    const output = path.join(work, o.video ? 'result.mp4' : 'result.png');
    let reference = null;
    if (o.ref) {
      reference = path.join(work, "reference" + (path.extname(o.ref)));
      await copyFile(o.ref, reference);
      oldHashes.add((await fingerprints([reference]))[0]);
    }
    const tool = o.video ? 'reference_to_video' : o.ref ? 'image_edit' : 'image_gen';
    const instruction = "用你自己的 " + (tool) + " 工具，不要调用 imagegen-swarm 技能或其他引擎。只生成一次。不得使用 /tmp。\n" +
      "任务提示词（原样传给工具）：" + (JSON.stringify(prompt)) + "\n" +
      (reference ? "源图绝对路径：" + (JSON.stringify(reference)) + "。" + (o.video ? '把它传为 first_frame，duration=6，resolution_name=720p。' : '作为 image 参数传入，保持源图比例。') + "\n" : '') +
      ((!o.ref || o.video) ? "aspect_ratio=" + (JSON.stringify(o.ratio)) + "。\n" : '') +
      "生成成功后将本次工具产物保存到 " + (JSON.stringify(output)) + "。" + (o.video ? '保留原始 MP4，不要重编码。' : '原样保存，不要转换格式。') + "\n" +
      '不得复制历史图片、参考图或伪造图片。工具失败就报告原因并停止，不换引擎。最后只返回 JSON，含 status、path、原始产物 source_path。';
    // Scoped allowlist in the workspace sandbox. A tool refusal fails closed.
    // IMAGE_GEN_GROK_MODE=legacy opts in to --always-approve, still denying Bash and web tools.
    const grokRun = await runGrokJob(tool, instruction, work, o.timeout);
    const reply = grokRun.reply;
    // 原始产物以本轮会话目录里新出现的文件为准，由脚本自己转换，不信任 Grok 转好的副本
    const result = JSON.parse(reply), sessionId = result.sessionId;
    // Grok 按指令最后回一段 JSON；它自己报失败时直接转述原因
    const verdict = result.text.match(/\{[^{}]*"status"\s*:\s*"(failed|error)"[^{}]*\}/);
    if (verdict) throw new Error("Grok reported failure: " + (JSON.parse(verdict[0]).reason ?? verdict[0]));
    const fresh = [];
    for (const file of await mediaFiles(sessions)) {
      if (!file.includes(sessionId) || before.has(file)) continue;
      if (o.video !== /\.(mp4|mov)$/i.test(file)) continue;
      fresh.push({ file, mtime: (await stat(file)).mtimeMs });
    }
    if (!fresh.length) throw new Error("no newly generated " + (o.video ? 'video' : 'image') + " in this Grok session " + (sessionId) + "; reply: " + (reply.slice(-3000)));
    const source = fresh.sort((a, b) => b.mtime - a.mtime)[0].file;
    if (oldHashes.has((await fingerprints([source]))[0])) throw new Error('stale output: matches pre-existing session media or reference');
    if (o.video) await copyFile(source, o.out);
    else await runProcess(PY, [IMGTOOL, 'png', source, o.out], work);
    const data = await readFile(o.out);
    if (o.video ? data.toString('ascii', 4, 8) !== 'ftyp' : !data.subarray(0, 8).equals(Buffer.from('89504e470d0a1a0a', 'hex'))) throw new Error('invalid output media signature');
    console.log(JSON.stringify({ status: 'ok', path: o.out, engine: 'grok', source_path: source, bytes: (await stat(o.out)).size, elapsed_seconds: Math.round((Date.now() - start) / 1000), grok_mode: grokRun.grok_mode }));
  } finally {
    await rm(work, { recursive: true, force: true });
  }
}

main().catch(e => {
  console.log(JSON.stringify({ status: 'error', engine: 'grok', reason: e.message }));
  process.exitCode = 1;
});
