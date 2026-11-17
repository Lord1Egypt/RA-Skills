import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { copyFile, mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { markRunDir } from './safety.mjs';
import { STDIO_DISCARD, STDIO_PIPE } from './stdio-modes.mjs';

// 即梦（Dreamina）引擎，参数和其他引擎一致：无 --ref 文生图，有 --ref 改图（image2image，最多 10 张），
// --video 无 --ref 文生视频、有 --ref 图生视频（第一张参考图当首帧）。提交、轮询、下载交给同目录的 jimeng.mjs。
const here = path.dirname(fileURLToPath(import.meta.url));
const PY = process.env.PYTHON ?? (process.platform === 'win32' ? 'python' : 'python3');
const IMAGE_RATIOS = ['21:9', '16:9', '3:2', '4:3', '1:1', '3:4', '2:3', '9:16'];
const VIDEO_RATIOS = ['1:1', '3:4', '16:9', '4:3', '9:16', '21:9'];

function parse(argv) {
  const o = { aspect: '1:1', refs: [], video: false, timeout: 600000 };
  for (let i = 0; i < argv.length; i++) {
    const flag = argv[i];
    if (flag === '--json') continue;
    if (flag === '--video') { o.video = true; continue; }
    if (flag === '--help' || flag === '-h') {
      console.log("jimeng-image.mjs --prompt <text> --out <png|mp4> [--ref <image>]... [--aspect " + (IMAGE_RATIOS.join('|')) + "] [--video] [--model <model_version>] [--timeout ms] [--json]");
      process.exit(0);
    }
    const keys = { '--prompt': 'prompt', '--prompt-file': 'promptFile', '--out': 'out', '--ref': 'ref', '--aspect': 'aspect', '--model': 'model', '--timeout': 'timeout' };
    if (!keys[flag] || !argv[i + 1] || argv[i + 1].startsWith('--')) throw new Error("invalid argument: " + (flag));
    const value = argv[++i];
    if (keys[flag] === 'ref') { o.refs.push(path.resolve(value)); continue; }
    o[keys[flag]] = value;
  }
  if (!o.out || Boolean(o.prompt) === Boolean(o.promptFile)) throw new Error('require --out and exactly one of --prompt / --prompt-file');
  o.out = path.resolve(o.out);
  if (path.extname(o.out).toLowerCase() !== (o.video ? '.mp4' : '.png')) throw new Error('--out extension must be .png, or .mp4 with --video');
  const ratios = o.video ? (o.refs.length ? null : VIDEO_RATIOS) : IMAGE_RATIOS;
  if (ratios && !ratios.includes(o.aspect)) throw new Error("unsupported --aspect " + (o.aspect) + " (" + (ratios.join(', ')) + ")");
  if (o.refs.length > 10) throw new Error('image2image accepts at most 10 --ref images');
  o.timeout = Number(o.timeout);
  return o;
}

function runProcess(bin, args, cwd) {
  return new Promise((resolve, reject) => {
    const child = spawn(bin, args, { cwd, stdio: [STDIO_DISCARD, STDIO_PIPE, STDIO_PIPE] });
    let stdout = '', stderr = '';
    child.stdout.on('data', d => { stdout += d; });
    child.stderr.on('data', d => { stderr += d; });
    child.on('error', reject);
    child.on('close', code => resolve({ code, stdout, stderr }));
  });
}

async function main() {
  const offDirs = process.env.IMAGE_GEN_ENGINE_OFF
    ? [process.env.IMAGE_GEN_ENGINE_OFF]
    : [path.join(homedir(), '.config', 'imagegen-swarm', 'engine-off'), path.join(homedir(), '.config', 'image-gen', 'engine-off')];
  const off = offDirs.map(dir => path.join(dir, 'jimeng')).find(file => existsSync(file));
  if (off) throw new Error("jimeng is turned off (" + (off) + "); delete that file to turn it back on");
  const start = Date.now(), o = parse(process.argv.slice(2));
  const prompt = (o.promptFile ? await readFile(o.promptFile, 'utf8') : o.prompt).trim();
  if (!prompt) throw new Error('empty prompt');
  await mkdir(path.dirname(o.out), { recursive: true });
  const work = await mkdtemp(path.join(path.dirname(o.out), ".jimeng-image-" + (Date.now()) + "-"));
  await markRunDir(work);
  try {
    const sub = o.video ? (o.refs.length ? 'image2video' : 'text2video') : (o.refs.length ? 'image2image' : 'text2image');
    const flags = ["--prompt=" + (prompt)];
    if (sub === 'text2image' || sub === 'image2image') flags.push("--ratio=" + (o.aspect), '--resolution_type=2k', '--generate_num=1');
    if (sub === 'image2image') flags.push("--images=" + (o.refs.join(',')));
    // 视频默认用 seedance2.0fast（旗舰档常常排队），720p、5 秒；图生视频的比例跟首帧走
    if (sub === 'text2video') flags.push("--ratio=" + (o.aspect), '--video_resolution=720p');
    if (sub === 'image2video') flags.push("--image=" + (o.refs[0]), '--video_resolution=720p');
    if (o.video) flags.push("--model_version=" + (o.model ?? 'seedance2.0fast'));
    else if (o.model) flags.push("--model_version=" + (o.model));
    const r = await runProcess(process.execPath, [path.join(here, 'jimeng.mjs'), sub, '--out', work, '--json', '--poll', String(Math.ceil(o.timeout / 1000)), ...flags], work);
    const line = r.stdout.trim().split('\n').at(-1) ?? '';
    const report = line.startsWith('{') ? JSON.parse(line) : { status: 'error', error: (r.stderr || r.stdout).slice(-1500) };
    if (report.status !== 'ok') throw new Error(report.error ?? 'jimeng failed');
    const media = report.files.map(f => f.path).filter(p => (o.video ? /\.(mp4|mov)$/i : /\.(png|jpe?g|webp)$/i).test(p));
    if (!media.length) throw new Error("jimeng task " + (report.submit_id) + " succeeded but downloaded no " + (o.video ? 'video' : 'image'));
    if (o.video) {
      await copyFile(media[0], o.out);
    } else {
      // 解码后不能和任何参考图一样，再转成真正的 PNG
      const fps = JSON.parse((await runProcess(PY, [path.join(here, 'imgtool.py'), 'fp', media[0], ...o.refs], work)).stdout).fp;
      if (fps.slice(1).includes(fps[0])) throw new Error('stale output: matches a reference image');
      const conv = await runProcess(PY, [path.join(here, 'imgtool.py'), 'png', media[0], o.out], work);
      if (conv.code !== 0) throw new Error("could not convert to PNG: " + (conv.stderr.slice(-300)));
    }
    const data = await readFile(o.out);
    console.log(JSON.stringify({ status: 'ok', path: o.out, engine: 'jimeng', subcommand: sub, submit_id: report.submit_id,
      sha256: createHash('sha256').update(data).digest('hex').slice(0, 16), bytes: data.length, elapsed_seconds: Math.round((Date.now() - start) / 1000) }));
  } finally {
    await rm(work, { recursive: true, force: true });
  }
}

main().catch(e => {
  console.log(JSON.stringify({ status: 'error', engine: 'jimeng', reason: e.message }));
  process.exitCode = 1;
});
