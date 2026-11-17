import { spawn } from 'node:child_process';
import { mkdir, mkdtemp, readFile, copyFile, readdir, rm, stat } from 'node:fs/promises';
import { existsSync, statSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { markRunDir } from './safety.mjs';
import { STDIO_DISCARD, STDIO_PIPE } from './stdio-modes.mjs';
import { isInvokedDirectly } from './direct.mjs';

const RATIOS = ['1:1', '2:3', '3:2', '3:4', '4:3', '9:16', '16:9'];
const BRAIN = path.join(homedir(), '.gemini', 'antigravity-cli', 'brain');

function parse(argv) {
  const o = { aspect: '1:1', model: 'gemini-3.8-flash-low', timeout: 600000, refs: [] };
  for (let i = 0; i < argv.length; i++) {
    const flag = argv[i];
    if (flag === '--json') continue;
    if (flag === '--help' || flag === '-h') {
      console.log("gemini-image.mjs --prompt <text> --out <png> [--ref <image>]... [--aspect " + (RATIOS.join('|')) + "] [--model <agy model>] [--agy <path>] [--timeout ms] [--json]");
      process.exit(0);
    }
    const keys = { '--prompt': 'prompt', '--prompt-file': 'promptFile', '--out': 'out', '--ref': 'ref', '--aspect': 'aspect', '--model': 'model', '--agy': 'agy', '--timeout': 'timeout' };
    if (!keys[flag] || !argv[i + 1] || argv[i + 1].startsWith('--')) throw new Error("invalid argument: " + (flag));
    const value = argv[++i];
    if (keys[flag] === 'ref') { o.refs.push(path.resolve(value)); continue; }
    if (['prompt', 'promptFile', 'out', 'agy'].includes(keys[flag]) && o[keys[flag]] !== undefined) throw new Error("duplicate argument: " + (flag));
    o[keys[flag]] = value;
  }
  if (!o.out || Boolean(o.prompt) === Boolean(o.promptFile)) throw new Error('require --out and exactly one of --prompt / --prompt-file');
  if (!RATIOS.includes(o.aspect)) throw new Error("unsupported --aspect (generate_image accepts " + (RATIOS.join(', ')) + ")");
  if (o.refs.length > 3) throw new Error('generate_image accepts at most 3 --ref images');
  o.timeout = Number(o.timeout);
  if (!Number.isFinite(o.timeout) || o.timeout <= 0) throw new Error('--timeout must be positive milliseconds');
  o.out = path.resolve(o.out);
  if (path.extname(o.out).toLowerCase() !== '.png') throw new Error('--out extension must be .png');
  o.agy = o.agy ?? process.env.AGY_BIN ?? path.join(homedir(), '.local', 'bin', 'agy');
  if (!existsSync(o.agy)) throw new Error("agy not found: " + (o.agy) + " (install the Antigravity CLI or pass --agy)");
  return o;
}

function runProcess(bin, args, cwd, limitMs = 60000) {
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
      else if (code !== 0) reject(new Error((bin) + " exited " + (code) + ": " + (stderr || stdout)));
      else resolve(stdout);
    });
  });
}

// 图片转换、尺寸、解码指纹都交给跨平台的 imgtool.py（Pillow）
const PY = process.env.PYTHON ?? (process.platform === 'win32' ? 'python' : 'python3');
const IMGTOOL = path.join(path.dirname(fileURLToPath(import.meta.url)), 'imgtool.py');

// 会话日志会把很长的提示词截断。截断行不能让 JSON.parse 抛错，否则图已经生成也会被丢掉。
// 完整原文在同目录的 transcript_full.jsonl；没有完整文件时再读被截过的 transcript.jsonl。
export function transcriptFile(dir) {
  const full = path.join(dir, 'transcript_full.jsonl');
  const clipped = path.join(dir, 'transcript.jsonl');
  try {
    if (existsSync(full) && statSync(full).size > 0) return full;
  } catch { /* 完整日志不可读就退回截断的那份 */ }
  return clipped;
}

export function parseJsonValue(text) {
  try { return JSON.parse(text); } catch { /* 截断或夹杂了说明文字 */ }
  const repaired = repairTruncatedJson(text);
  if (!repaired) return null;
  try { return JSON.parse(repaired); } catch { return null; }
}

// 补上被截断的引号和括号。只在 JSON.parse 失败时用，完整 JSON 走上面的直接解析。
function repairTruncatedJson(text) {
  let out = '';
  let inString = false;
  let escape = false;
  const stack = [];
  for (const ch of String(text)) {
    out += ch;
    if (inString) {
      if (escape) { escape = false; continue; }
      if (ch === '\\') { escape = true; continue; }
      if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') { inString = true; continue; }
    if (ch === '{') stack.push('}');
    else if (ch === '[') stack.push(']');
    else if ((ch === '}' || ch === ']') && stack.at(-1) === ch) stack.pop();
  }
  if (escape) out = out.slice(0, -1);
  if (inString) out += '"';
  out = out.replace(/,\s*$/, '');
  out = out.replace(/,?\s*"[^"\\]*"\s*:\s*$/, '');
  while (stack.length) out += stack.pop();
  return out.trim() ? out : null;
}

// 工具参数是 JSON 编码的字符串。提示词被截断时解开失败，保留已经写下的那段，不要抛错。
export function parseEncodedArg(value) {
  if (typeof value !== 'string') return value;
  try { return JSON.parse(value); } catch { /* 截断的 JSON 字符串，或本来就不是 JSON */ }
  return recoverJsonString(value);
}

function recoverJsonString(value) {
  let body = value.trim();
  if (body.startsWith('"')) body = body.slice(1);
  body = body.replace(/\\u[0-9a-fA-F]{0,3}$/, '');
  if (body.endsWith('\\') && !body.endsWith('\\\\')) body = body.slice(0, -1);
  try { return JSON.parse("\"" + (body) + "\""); } catch { /* 里面还有没转义的引号 */ }
  return body.replace(/\\n/g, '\n').replace(/\\r/g, '\r').replace(/\\t/g, '\t').replace(/\\"/g, '"').replace(/\\\\/g, '\\');
}

export function parseToolArgs(args) {
  return Object.fromEntries(Object.entries(args ?? {}).map(([k, v]) => [k, parseEncodedArg(v)]));
}

export function parseTranscript(text) {
  const steps = [];
  for (const line of String(text).split('\n')) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    const step = parseJsonValue(trimmed);
    if (step && typeof step === 'object') steps.push(step);
    else {
      const salvaged = salvageTruncatedStep(trimmed);
      if (salvaged) steps.push(salvaged);
    }
  }
  return steps;
}

// 整行被截断、修不好时，仍尽量留下出图工具和已保存的图片路径。
function salvageTruncatedStep(line) {
  const saved = line.match(/Generated image is saved at\s+(\S+)/);
  const uri = line.match(/"uri"\s*:\s*"((?:\\.|[^"\\])*)"/);
  if (!saved && !uri && !line.includes('generate_image')) return null;
  const step = { content: line, tool_calls: [], media: [] };
  if (line.includes('generate_image')) {
    const prompt = line.match(/"Prompt"\s*:\s*"((?:\\.|[^"\\])*)/);
    const aspect = line.match(/"AspectRatio"\s*:\s*"((?:\\.|[^"\\])*)/);
    const args = {};
    if (prompt) args.Prompt = "\"" + (prompt[1]) + "\"";
    if (aspect) args.AspectRatio = "\"" + (aspect[1]) + "\"";
    step.tool_calls.push({ name: 'generate_image', args });
  }
  const rawUri = uri ? uri[1].replace(/\\"/g, '"').replace(/\\\\/g, '\\') : null;
  const file = rawUri || (saved ? saved[1].replace(/["},]+$/, '') : null);
  if (file) {
    step.media.push({ mime_type: 'image/png', uri: file.startsWith('file:') ? file : "file://" + (file) });
    if (!/Generated image is saved at/.test(step.content)) step.content += "\nGenerated image is saved at " + (file);
  }
  return step;
}

export function mediaPath(uri) {
  if (typeof uri !== 'string' || !uri) return null;
  try {
    const url = new URL(uri);
    if (url.protocol === 'file:') return decodeURIComponent(url.pathname);
  } catch { /* 不是 URL，下面按绝对路径试 */ }
  return uri.startsWith('/') ? uri : null;
}

// 一次会话里：先记下 generate_image 的参数，后面步骤里「图已保存」的媒体就是产出。
// 参数被截断时 call 可能缺提示词，图片路径仍然算数。
export function extractGenerated(steps) {
  const generated = [];
  let call = null;
  for (const step of steps) {
    const used = (step?.tool_calls ?? []).find(t => t?.name === 'generate_image');
    if (used) call = { ...(call ?? {}), ...parseToolArgs(used.args) };
    const content = String(step?.content ?? '');
    for (const media of step?.media ?? []) {
      if (!media?.mime_type?.startsWith('image/') || !/Generated image is saved at/.test(content)) continue;
      const file = mediaPath(media.uri);
      if (file) generated.push({ file, call: { ...(call ?? {}) } });
    }
  }
  return generated;
}

// agy 的 stdout 是 JSON。提示词很长时这一段也会被截断；能找回会话编号就继续去日志里拿图。
export function parseAgyReply(text) {
  const direct = parseJsonValue(text) ?? {};
  const status = typeof direct.status === 'string' ? direct.status : text.match(/"status"\s*:\s*"([^"]+)"/)?.[1] ?? null;
  const conversation_id = typeof direct.conversation_id === 'string'
    ? direct.conversation_id
    : text.match(/"conversation_id"\s*:\s*"([0-9a-f-]{36})"/)?.[1] ?? null;
  const response = typeof direct.response === 'string' ? direct.response : null;
  return { status, conversation_id, response };
}

async function loadTranscript(conversation) {
  const dir = path.join(BRAIN, conversation, '.system_generated', 'logs');
  const file = transcriptFile(dir);
  if (!existsSync(file)) return [];
  return parseTranscript(await readFile(file, 'utf8'));
}

async function main() {
  const start = Date.now(), o = parse(process.argv.slice(2));
  const prompt = (o.promptFile ? await readFile(o.promptFile, 'utf8') : o.prompt).trim();
  if (!prompt) throw new Error('empty prompt');
  await mkdir(path.dirname(o.out), { recursive: true });
  const work = await mkdtemp(path.join(path.dirname(o.out), ".gemini-image-" + (Date.now()) + "-"));
  await markRunDir(work);
  try {
    // 解码后再散列，防止把参考图换个格式冒充新图
    const img = async (...args) => JSON.parse(await runProcess(PY, [IMGTOOL, ...args], work));
    const fingerprint = async file => (await img('fp', file)).fp[0];
    const refs = [], refHashes = new Set();
    for (const [i, ref] of o.refs.entries()) {
      const copy = path.join(work, "ref-" + (i + 1) + (path.extname(ref)));
      await copyFile(ref, copy);
      refs.push(copy);
      refHashes.add(await fingerprint(copy));
    }
    // agy 主代理没有 generate_image，出图交给内置的 image-generator 子代理；要求它原样转交提示词、只出一次
    const instruction = 'Delegate to your image-generator subagent. Do not use the imagegen-swarm skill or any other image engine. Tell the subagent: call generate_image exactly once, ' +
      "with AspectRatio " + (JSON.stringify(o.aspect)) + ", ImageName \"result\"" +
      (refs.length ? ", ImagePaths " + (JSON.stringify(refs)) : '') +
      ', and Prompt set to the exact text between the markers below, copied character for character with no rewriting, no additions and no retries. ' +
      'If the tool fails, report the error and stop; never copy, convert or reuse any existing image.\n' +
      "<<<PROMPT\n" + (prompt) + "\nPROMPT>>>\n" +
      'Do not use any other tool yourself. When it finishes, reply with only the absolute path of the image.';
    const reply = await runProcess(o.agy, ['-p', instruction, '--model', o.model, '--sandbox', '--disable-slash-commands', '--output-format', 'json',
      '--print-timeout', (Math.ceil(o.timeout / 1000)) + "s", '--log-file', path.join(work, 'agy.log')], work, o.timeout + 30000);
    const result = parseAgyReply(reply);
    if (result.status && result.status !== 'SUCCESS') throw new Error("agy status " + (result.status) + ": " + (reply.slice(-3000)));
    if (!result.conversation_id) throw new Error("agy status " + (result.status ?? 'unknown') + ": " + (reply.slice(-3000)));
    const parent = result.conversation_id, brain = path.join(BRAIN, parent);
    // 主会话记录里登记了它开的子代理；在主会话和子代理的记录里找 generate_image 调用和它保存的图
    const steps = await loadTranscript(parent);
    const children = [...new Set(steps.flatMap(s => [...String(s.content ?? '').matchAll(/"conversationId":\s*"([0-9a-f-]{36})"/g)].map(m => m[1])))];
    const generated = extractGenerated(steps);
    for (const conversation of children) {
      if (conversation !== parent) generated.push(...extractGenerated(await loadTranscript(conversation)));
    }
    // 日志被截断、解析不到媒体时，会话目录里这次新写出的图仍然算数
    if (!generated.length) {
      for (const file of await freshImages(brain, start)) generated.push({ file, call: {} });
    }
    // 子代理出图失败（额度用完会报 429 RESOURCE_EXHAUSTED）时原因在主代理最后的回复里，放在报错最前面
    if (!generated.length) throw new Error("generate_image produced no image: " + ((result.response ?? reply).slice(-1500)) + " (agy conversation " + (parent) + ")");
    const picked = generated.find(g => result.response?.includes(g.file)) ?? generated.at(-1);
    const source = picked.file;
    if (path.dirname(source) !== brain) throw new Error("generated image outside this conversation's artifacts: " + (source));
    if ((await stat(source)).mtimeMs < start) throw new Error("stale output: " + (source) + " predates this run");
    if (refHashes.has(await fingerprint(source))) throw new Error('stale output: matches a reference image');
    const { width, height } = await img('png', source, o.out);
    const data = await readFile(o.out);
    if (!data.subarray(0, 8).equals(Buffer.from('89504e470d0a1a0a', 'hex'))) throw new Error('invalid output PNG signature');
    const toolPrompt = typeof picked.call.Prompt === 'string' ? picked.call.Prompt : null;
    console.log(JSON.stringify({
      status: 'ok', path: o.out, engine: 'gemini', source_path: source, width, height, aspect: picked.call.AspectRatio ?? o.aspect,
      tool_prompt: toolPrompt, prompt_verbatim: toolPrompt == null ? null : toolPrompt.trim() === prompt, attempts: generated.length,
      conversation_id: parent, bytes: data.length, elapsed_seconds: Math.round((Date.now() - start) / 1000),
    }));
  } finally {
    await rm(work, { recursive: true, force: true });
  }
}

async function freshImages(dir, since) {
  let names = [];
  try { names = await readdir(dir); } catch { return []; }
  const found = [];
  for (const name of names) {
    if (!/\.(png|jpe?g|webp)$/i.test(name)) continue;
    const file = path.join(dir, name);
    try {
      const info = await stat(file);
      if (info.isFile() && info.size > 0 && info.mtimeMs >= since) found.push(file);
    } catch { /* 文件在列出之后消失 */ }
  }
  return found;
}

if (isInvokedDirectly(import.meta.url)) {
  main().catch(e => {
    console.log(JSON.stringify({ status: 'error', engine: 'gemini', reason: e.message }));
    process.exitCode = 1;
  });
}
