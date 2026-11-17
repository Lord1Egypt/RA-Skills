#!/usr/bin/env node
// Original local media tooling for Hype Shorts Remix. Node.js 22+, FFmpeg/FFprobe.
import { spawn } from 'node:child_process';
import { createReadStream } from 'node:fs';
import { lstat, stat, realpath, readFile, writeFile, mkdir, mkdtemp, link, rm } from 'node:fs/promises';
import { resolve, dirname, extname, join } from 'node:path';
import { createHash } from 'node:crypto';

const FFMPEG = process.env.FFMPEG_PATH || 'ffmpeg';
const FFPROBE = process.env.FFPROBE_PATH || 'ffprobe';
const FORMATS = { '.mp4': 'mov', '.mov': 'mov', '.m4a': 'mov', '.webm': 'matroska', '.mkv': 'matroska', '.avi': 'avi', '.wav': 'wav', '.mp3': 'mp3', '.ogg': 'ogg', '.flac': 'flac', '.aac': 'aac', '.png': 'image2', '.jpg': 'image2', '.jpeg': 'image2', '.webp': 'image2' };
const IMAGES = new Set(['.png', '.jpg', '.jpeg', '.webp']);
const fail = (code, message) => { throw Object.assign(new Error(message), { code }); };
const check = (condition, code, message) => { if (!condition) fail(code, message); };
const numeric = (value, min, max) => typeof value === 'number' && Number.isFinite(value) && value >= min && value <= max;

function localPath(value, base = process.cwd()) {
  check(typeof value === 'string' && value.length > 0 && value.length <= 4096 && !/[\x00-\x1f]/.test(value) && !/^[a-z][a-z0-9+.-]*:/i.test(value) && !value.startsWith('//'), 'UNSAFE_PATH', 'Use a local filesystem path, not a URL or protocol.');
  return resolve(base, value);
}

async function absent(path) {
  try { await lstat(path); } catch (error) { if (error.code === 'ENOENT') return; throw error; }
  fail('OUTPUT_EXISTS', 'The output path already exists; choose a new path.');
}

function processRun(binary, args, cwd, timeout = 120_000) {
  return new Promise((resolveResult, reject) => {
    const child = spawn(binary, args, { cwd, shell: false, stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '', stderr = '', exceeded = false;
    const timer = setTimeout(() => { exceeded = true; child.kill('SIGKILL'); }, timeout);
    for (const [stream, name] of [[child.stdout, 'out'], [child.stderr, 'err']]) {
      stream.on('data', data => {
        if (name === 'out') stdout += data; else stderr += data;
        if (stdout.length + stderr.length > 2 * 1024 * 1024) { exceeded = true; child.kill('SIGKILL'); }
      });
    }
    child.once('error', error => { clearTimeout(timer); reject(Object.assign(new Error(`Cannot start ${binary === FFMPEG ? 'FFmpeg' : 'FFprobe'}; check installation and PATH.`), { code: 'TOOL_UNAVAILABLE', cause: error })); });
    child.once('close', code => {
      clearTimeout(timer);
      if (exceeded) reject(Object.assign(new Error('Media processing exceeded its time or diagnostic limit.'), { code: 'MEDIA_LIMIT' }));
      else if (code !== 0) reject(Object.assign(new Error('Media processing failed. Check supported codecs and FFmpeg capabilities.'), { code: 'MEDIA_PROCESS_FAILED', detail: stderr.slice(-1800) }));
      else resolveResult(stdout);
    });
  });
}

function inputArgs(media, { loop = false, fps = 24 } = {}) {
  const args = ['-protocol_whitelist', 'file', '-format_whitelist', media.format, '-f', media.format];
  if (media.image) args.push('-pattern_type', 'none', ...(loop ? ['-loop', '1', '-framerate', String(fps)] : []));
  if (media.format === 'mov') args.push('-enable_drefs', '0');
  return [...args, '-i', media.file];
}

async function fingerprint(file) {
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(file)) hash.update(chunk);
  return hash.digest('hex');
}

function containFilter(width, height) {
  // Use display aspect ratio (including non-square source pixels), then make square pixels.
  return `scale=w='max(2,trunc(min(${width},${height}*dar)/2)*2)':h='max(2,trunc(min(${height},${width}/dar)/2)*2)',setsar=1,pad=${width}:${height}:(ow-iw)/2:(oh-ih)/2`;
}

async function probe(file, base) {
  const selected = localPath(file, base);
  const extension = extname(selected).toLowerCase();
  check(FORMATS[extension], 'UNSUPPORTED_MEDIA', 'Supported inputs: MP4/MOV/WebM/MKV/AVI, PNG/JPEG/WebP, WAV/MP3/M4A/OGG/FLAC/AAC.');
  const info = await stat(selected);
  check(info.isFile() && info.size > 0 && info.size <= 2 * 1024 ** 3, 'MEDIA_LIMIT', 'Media must be a regular nonempty file no larger than 2 GiB.');
  const media = { file: await realpath(selected), format: FORMATS[extension], image: IMAGES.has(extension), bytes: info.size };
  const raw = JSON.parse(await processRun(FFPROBE, ['-v', 'error', ...inputArgs(media), '-show_streams', '-show_format', '-of', 'json']));
  const video = raw.streams?.find(stream => stream.codec_type === 'video' && !stream.disposition?.attached_pic);
  const audio = raw.streams?.find(stream => stream.codec_type === 'audio');
  check(video || audio, 'UNSUPPORTED_MEDIA', 'The file has no usable video or audio stream.');
  const duration = Number(raw.format?.duration || video?.duration || audio?.duration);
  check(media.image || numeric(duration, 0.001, 3600), 'MEDIA_LIMIT', 'Timed input media must have a finite duration up to one hour.');
  if (video) check(numeric(video.width, 1, 8192) && numeric(video.height, 1, 8192) && video.width * video.height <= 35_000_000, 'MEDIA_LIMIT', 'Input frame dimensions exceed the supported bounds.');
  media.duration = media.image ? null : duration;
  media.video = video ? { streamIndex: video.index, width: video.width, height: video.height, codec: video.codec_name, pixelFormat: video.pix_fmt, frameRate: video.avg_frame_rate, sampleAspectRatio: video.sample_aspect_ratio || '1:1', rotation: video.side_data_list?.find(item => Number.isFinite(item.rotation))?.rotation || 0 } : null;
  media.audio = audio ? { streamIndex: audio.index, codec: audio.codec_name, sampleRate: Number(audio.sample_rate), channels: audio.channels } : null;
  media.sha256 = await fingerprint(media.file);
  return media;
}

async function inspect(input, outputDirectory) {
  const output = localPath(outputDirectory);
  await absent(output);
  const media = await probe(input);
  check(media.video, 'UNSUPPORTED_MEDIA', 'Inspection requires a video or still image.');
  await mkdir(output, { mode: 0o700 }); // Exclusive: existing directories are never reused.
  try {
    const count = media.image ? 1 : 8;
    const frames = [];
    const [frameNumerator, frameDenominator] = (media.video.frameRate || '0/1').split('/').map(Number);
    const frameRate = frameNumerator / frameDenominator;
    const lastSample = media.image ? 0 : Math.max(0, media.duration - (Number.isFinite(frameRate) && frameRate > 0 ? 2 / frameRate : 0.2));
    for (let index = 0; index < count; index++) {
      const time = media.image ? 0 : Math.min(media.duration * index / count, lastSample);
      const file = `frame-${String(index + 1).padStart(2, '0')}.jpg`;
      await processRun(FFMPEG, ['-hide_banner', '-loglevel', 'error', '-nostdin', '-n', ...(time ? ['-ss', String(time)] : []), ...inputArgs(media), '-map', `0:${media.video.streamIndex}`, '-frames:v', '1', '-vf', containFilter(320, 180), '-q:v', '3', '-update', '1', file], output);
      check((await stat(join(output, file))).size > 0, 'MEDIA_PROCESS_FAILED', 'A sampled frame could not be decoded.');
      frames.push({ time, file });
    }
    await processRun(FFMPEG, ['-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-protocol_whitelist', 'file', '-f', 'image2', '-framerate', '1', '-start_number', '1', '-i', 'frame-%02d.jpg', '-vf', `tile=${Math.min(count, 4)}x${Math.ceil(count / 4)}`, '-frames:v', '1', '-update', '1', 'contact-sheet.jpg'], output);
    await writeFile(join(output, 'analysis.json'), JSON.stringify({ version: 1, media, frames, contactSheet: 'contact-sheet.jpg', visualAnalysis: 'Review the sampled frames with the host Agent; metadata alone does not describe the scene.' }, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
  } catch (error) { await rm(output, { recursive: true, force: true }); throw error; }
  return { status: 'completed', analysis: join(output, 'analysis.json'), contactSheet: join(output, 'contact-sheet.jpg') };
}

function strictObject(value, allowed, required) {
  check(value && typeof value === 'object' && !Array.isArray(value) && Object.keys(value).every(key => allowed.includes(key)) && required.every(key => Object.hasOwn(value, key)), 'INVALID_PROJECT', 'The edit project contains missing or unsupported fields.');
}

async function loadProject(path) {
  const file = localPath(path);
  check((await stat(file)).size <= 256 * 1024, 'INVALID_PROJECT', 'The edit project must be at most 256 KiB.');
  let project;
  try { project = JSON.parse(await readFile(file, 'utf8')); } catch { fail('INVALID_PROJECT', 'The edit project must contain valid JSON.'); }
  strictObject(project, ['version', 'width', 'height', 'fps', 'shots', 'captions', 'narration', 'music'], ['version', 'width', 'height', 'fps', 'shots']);
  check(project.version === 1 && [project.width, project.height].every(value => Number.isInteger(value) && value >= 128 && value <= 1920 && value % 2 === 0) && project.width * project.height <= 2_073_600 && Number.isInteger(project.fps) && numeric(project.fps, 1, 60), 'INVALID_PROJECT', 'Use version 1, even dimensions from 128 to 1920 (at most 2073600 pixels), and integer fps from 1 to 60.');
  check(Array.isArray(project.shots) && project.shots.length >= 1 && project.shots.length <= 60, 'INVALID_PROJECT', 'Provide 1 to 60 shots.');
  for (const shot of project.shots) {
    strictObject(shot, ['file', 'start', 'duration'], ['file', 'start', 'duration']);
    check(numeric(shot.start, 0, 3600) && numeric(shot.duration, 1 / project.fps, 180), 'INVALID_PROJECT', 'Shot start/duration is outside its supported range.');
    localPath(shot.file, dirname(file));
  }
  const duration = project.shots.reduce((sum, shot) => sum + shot.duration, 0);
  check(duration <= 180 && duration * project.fps <= 10800, 'INVALID_PROJECT', 'The edit must be at most 180 seconds and 10800 frames.');
  if (project.captions !== undefined) {
    check(Array.isArray(project.captions) && project.captions.length <= 200, 'INVALID_PROJECT', 'Use at most 200 captions.');
    for (const caption of project.captions) {
      strictObject(caption, ['start', 'end', 'text'], ['start', 'end', 'text']);
      check(numeric(caption.start, 0, duration) && numeric(caption.end, 0, duration) && caption.end > caption.start && typeof caption.text === 'string' && caption.text.length > 0 && caption.text.length <= 1000 && !/[\x00-\x08\x0b-\x1f]/.test(caption.text), 'INVALID_PROJECT', 'Caption times/text are invalid. Use seconds within the edit and up to 1000 Unicode characters.');
    }
  }
  for (const key of ['narration', 'music']) if (project[key] !== undefined) {
    strictObject(project[key], ['file', 'volume'], ['file', 'volume']);
    check(numeric(project[key].volume, 0, 2), 'INVALID_PROJECT', 'Audio volume must be a number from 0 to 2.');
    localPath(project[key].file, dirname(file));
  }
  return { project, file, duration };
}

const assTime = seconds => {
  const ticks = Math.round(seconds * 100);
  return `${Math.floor(ticks / 360000)}:${String(Math.floor(ticks / 6000) % 60).padStart(2, '0')}:${String(Math.floor(ticks / 100) % 60).padStart(2, '0')}.${String(ticks % 100).padStart(2, '0')}`;
};
// A word joiner after a literal backslash prevents ASS \N/\h control sequences.
const literalAss = text => text.replace(/\\/g, '\\\u2060').replace(/\{/g, '\\{').replace(/\}/g, '\\}').replace(/\n/g, '\\N');
function captionsAss(project) {
  const size = Math.max(18, Math.round(project.width * 0.055));
  const margin = Math.round(project.height * 0.08);
  return `[Script Info]\nScriptType: v4.00+\nPlayResX: ${project.width}\nPlayResY: ${project.height}\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,Arial,${size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,16,16,${margin},1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n` + (project.captions || []).map(caption => `Dialogue: 0,${assTime(caption.start)},${assTime(caption.end)},Default,,0,0,0,,${literalAss(caption.text)}\n`).join('');
}

async function render(projectPath, outputPath) {
  const output = localPath(outputPath);
  check(extname(output).toLowerCase() === '.mp4', 'INVALID_OUTPUT', 'Render output must end in .mp4.');
  const reportPath = `${output}.render.json`;
  await absent(output); await absent(reportPath);
  const { project, file, duration } = await loadProject(projectPath);
  const sources = [];
  for (const shot of project.shots) {
    const media = await probe(shot.file, dirname(file));
    check(media.video && (media.image ? shot.start === 0 : shot.start + shot.duration <= media.duration + 0.02), 'INVALID_PROJECT', 'Each shot must select an available video segment; still images start at zero.');
    sources.push(media);
  }
  const extras = [];
  for (const key of ['narration', 'music']) if (project[key]) {
    const media = await probe(project[key].file, dirname(file));
    check(media.audio, 'INVALID_PROJECT', `${key} must contain audio.`);
    extras.push({ ...media, role: key, volume: project[key].volume });
  }
  const temporary = await mkdtemp(join(dirname(output), '.hype-render-'));
  let linkedReport = false;
  try {
    const args = ['-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-filter_complex_threads', '2'];
    const filters = [];
    project.shots.forEach((shot, index) => {
      if (!sources[index].image) args.push('-ss', String(shot.start));
      args.push('-t', String(shot.duration), ...inputArgs(sources[index], { loop: true, fps: project.fps }));
      filters.push(`[${index}:${sources[index].video.streamIndex}]setpts=PTS-STARTPTS,fps=${project.fps},${containFilter(project.width, project.height)},format=yuv420p,tpad=stop_mode=clone:stop_duration=1,trim=duration=${shot.duration},setpts=PTS-STARTPTS[v${index}]`);
      const audio = sources[index].audio ? `[${index}:${sources[index].audio.streamIndex}]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS,apad` : 'anullsrc=r=48000:cl=stereo';
      filters.push(`${audio},atrim=duration=${shot.duration},asetpts=PTS-STARTPTS[a${index}]`);
    });
    filters.push(`${project.shots.map((_, index) => `[v${index}][a${index}]`).join('')}concat=n=${sources.length}:v=1:a=1[basev][basea]`);
    for (const [index, audio] of extras.entries()) {
      args.push(...inputArgs(audio));
      filters.push(`[${sources.length + index}:${audio.audio.streamIndex}]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS,volume=${audio.volume},apad,atrim=duration=${duration}[extra${index}]`);
    }
    filters.push(`[basea]${extras.map((_, index) => `[extra${index}]`).join('')}amix=inputs=${1 + extras.length}:duration=first:normalize=0,alimiter=limit=0.95:latency=1,atrim=duration=${duration}[audio]`);
    if (project.captions?.length) {
      await writeFile(join(temporary, 'captions.ass'), captionsAss(project), { flag: 'wx', mode: 0o600 });
      filters.push('[basev]ass=filename=captions.ass[video]');
    } else filters.push('[basev]null[video]');
    args.push('-filter_complex', filters.join(';'), '-map', '[video]', '-map', '[audio]', '-t', String(duration), '-r', String(project.fps), '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-threads', '2', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-map_metadata', '-1', 'render.mp4');
    await processRun(FFMPEG, args, temporary, 20 * 60_000);
    const actual = await probe(join(temporary, 'render.mp4'));
    check(actual.video?.codec === 'h264' && actual.video.pixelFormat === 'yuv420p' && actual.video.width === project.width && actual.video.height === project.height && Math.abs(actual.duration - duration) <= Math.max(0.15, sources.length / project.fps), 'VERIFY_FAILED', 'The rendered media did not match the requested canvas or duration.');
    const report = { version: 1, project: file, fit: 'contain', requestedDuration: duration, canvas: { width: project.width, height: project.height, fps: project.fps }, sources, additionalAudio: extras, captions: project.captions?.length || 0, output: { ...actual, file: output }, note: 'Output dimensions describe the composed canvas. Source dimensions above are the original encoded dimensions; they do not imply upstream portrait generation.' };
    await writeFile(join(temporary, 'report.json'), JSON.stringify(report, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
    // Same-directory hard links publish completed files atomically and fail on EEXIST.
    await link(join(temporary, 'report.json'), reportPath); linkedReport = true;
    await link(join(temporary, 'render.mp4'), output);
    return { status: 'completed', output, report: reportPath, duration: actual.duration, width: actual.video.width, height: actual.video.height };
  } catch (error) {
    if (linkedReport) await rm(reportPath, { force: true });
    if (error.code === 'EEXIST') fail('OUTPUT_EXISTS', 'The output appeared during processing; it was preserved.');
    throw error;
  } finally { await rm(temporary, { recursive: true, force: true }); }
}

try {
  check(Number(process.versions.node.split('.')[0]) >= 22, 'NODE_VERSION', 'Node.js 22 or later is required.');
  const [command, ...argv] = process.argv.slice(2);
  const required = command === 'inspect' ? ['--input', '--out-dir'] : command === 'render' ? ['--project', '--output'] : null;
  check(required && argv.length === 4, 'USAGE', 'Use inspect --input FILE --out-dir NEW_DIR or render --project EDIT.json --output NEW.mp4.');
  const options = new Map();
  for (let index = 0; index < argv.length; index += 2) { check(required.includes(argv[index]) && !options.has(argv[index]) && argv[index + 1], 'USAGE', 'Invalid or repeated command option.'); options.set(argv[index], argv[index + 1]); }
  const result = command === 'inspect' ? await inspect(options.get('--input'), options.get('--out-dir')) : await render(options.get('--project'), options.get('--output'));
  process.stdout.write(JSON.stringify(result) + '\n');
} catch (error) {
  process.stderr.write(JSON.stringify({ error: { code: error.code || 'MEDIA_ERROR', message: error.message, ...(error.detail ? { detail: error.detail } : {}) } }) + '\n');
  process.exitCode = 1;
}
