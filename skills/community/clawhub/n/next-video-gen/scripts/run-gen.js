#!/usr/bin/env node
// Next Video Gen - Pure Node.js implementation
// Usage: node run-gen.js "prompt" [options]
//   --mode txt2img|txt2video|img2video|vid2video
//   --image <url> --video <url> --audio <url>
//   --duration <4-12> --quality <480p|720p|1080p|2K|1K|HD>
//   --aspect-ratio <16:9|9:16|1:1> --watermark <true|false>
//   --model <model-id> --audio (enable audio)

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ── Config ─────────────────────────────────────────────────────────────────────
const IMAGE_API_BASE = 'https://ark.cn-beijing.volces.com/api/v3/images';
const VIDEO_API_BASE = 'https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks';
const IMAGE_MODEL = 'doubao-seedream-5-0-260128';
const VIDEO_MODEL = 'doubao-seedance-1-5-pro-251215';
const MAX_POLL_SECONDS = 600;
const POLL_INTERVAL = 5;
const PROGRESS_INTERVAL = 30;
const OUTPUT_DIR = process.env.NEXT_VIDEO_GEN_OUTPUT_DIR || path.join(os.homedir(), 'Videos', 'next-video-gen');

// ── Args ───────────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
let MODE = 'txt2video';
let MODEL = '';
let DURATION = 5;
let QUALITY = '';
let ASPECT_RATIO = '';
let WATERMARK = 'true';
let GENERATE_AUDIO = 'false';
let VIDEO_URL = '';
let AUDIO_URL = '';
let REF_IMAGES = [];
let PROMPT = '';

let i = 0;
while (i < args.length) {
  switch (args[i]) {
    case '--mode': MODE = args[++i]; break;
    case '--prompt': PROMPT = args[++i]; break;
    case '--image': REF_IMAGES.push(args[++i]); break;
    case '--video': VIDEO_URL = args[++i]; break;
    case '--audio': AUDIO_URL = args[++i]; break;
    case '--duration': DURATION = parseInt(args[++i]); break;
    case '--quality': QUALITY = args[++i]; break;
    case '--aspect-ratio': ASPECT_RATIO = args[++i]; break;
    case '--watermark': WATERMARK = args[++i]; break;
    case '--model': MODEL = args[++i]; break;
    case '--no-audio': GENERATE_AUDIO = 'false'; break;
    case '--enable-audio': GENERATE_AUDIO = 'true'; break;
    default:
      if (!PROMPT) PROMPT = args[i];
      break;
  }
  i++;
}

// ── Validation ─────────────────────────────────────────────────────────────────
if (!process.env.DOUBAO_API_KEY) {
  console.error('ERROR: DOUBAO_API_KEY environment variable is required.');
  console.error('Get your API key from: https://console.volcengine.com/ark');
  console.error('Set it with: export DOUBAO_API_KEY=your_key_here');
  process.exit(1);
}
if (!PROMPT) {
  console.error('ERROR: Prompt required.');
  process.exit(1);
}

// Detect output mode
let OUTPUT_MODE = 'video';
if (MODE === 'txt2img') OUTPUT_MODE = 'image';

// Validate based on mode
if (OUTPUT_MODE === 'image') {
  QUALITY = QUALITY || '2K';
  ASPECT_RATIO = ASPECT_RATIO || '1:1';
  if (!['2K','1K','HD'].includes(QUALITY)) { console.error('Image quality: 2K/1K/HD'); process.exit(1); }
  if (!['1:1','16:9','9:16'].includes(ASPECT_RATIO)) { console.error('Image ratio: 1:1/16:9/9:16'); process.exit(1); }
} else {
  QUALITY = QUALITY || '720p';
  ASPECT_RATIO = ASPECT_RATIO || '16:9';
  if (!['480p','720p','1080p'].includes(QUALITY)) { console.error('Video quality: 480p/720p/1080p'); process.exit(1); }
  if (!['16:9','9:16','1:1'].includes(ASPECT_RATIO)) { console.error('Video ratio: 16:9/9:16/1:1'); process.exit(1); }
  if (VIDEO_URL && MODE === 'txt2video') MODE = 'vid2video';
}

// ── HTTP helper ────────────────────────────────────────────────────────────────
const agent = new https.Agent({ keepAlive: false });

function doRequest(method, url, payload) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const transport = parsedUrl.protocol === 'https:' ? https : http;

    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      method: method,
      agent: transport === https ? agent : undefined,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + process.env.DOUBAO_API_KEY,
      }
    };

    if (payload) {
      options.headers['Content-Length'] = Buffer.byteLength(payload);
    }

    const req = transport.request(options, function(res) {
      let body = '';
      res.on('data', function(chunk) { body += chunk; });
      res.on('end', function() {
        resolve({ body, statusCode: res.statusCode });
      });
    });

    req.on('error', function(e) {
      reject(new Error('HTTP_ERROR:' + e.message));
    });

    req.setTimeout(60000, function() {
      req.destroy();
      reject(new Error('TIMEOUT'));
    });

    if (payload) req.write(payload);
    req.end();
  });
}

// ── JSON helpers ──────────────────────────────────────────────────────────────
function jsonGet(obj, path) {
  const parts = path.split('.').filter(Boolean);
  for (const p of parts) {
    if (obj == null) return '';
    const m = p.match(/^([^\[]+)\[(\d+)\]$/);
    if (m) obj = obj[m[1]][parseInt(m[2])];
    else obj = obj[p];
  }
  return obj == null ? '' : (typeof obj === 'string' ? obj : JSON.stringify(obj));
}

// ── Download helper ────────────────────────────────────────────────────────────
function downloadFile(url, filepath) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const transport = parsedUrl.protocol === 'https:' ? https : http;

    const req = transport.get(parsedUrl, function(res) {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        const redirectUrl = new URL(res.headers.location, parsedUrl);
        const redirectTransport = redirectUrl.protocol === 'https:' ? https : http;
        redirectTransport.get(redirectUrl, function(res2) {
          const stream = fs.createWriteStream(filepath);
          res2.pipe(stream);
          stream.on('finish', () => resolve());
        }).on('error', reject);
        return;
      }
      if (res.statusCode !== 200) {
        reject(new Error('HTTP_ERROR: status=' + res.statusCode));
        return;
      }
      const stream = fs.createWriteStream(filepath);
      res.pipe(stream);
      stream.on('finish', () => resolve());
    });

    req.on('error', reject);
    req.setTimeout(300000, () => { req.destroy(); reject(new Error('TIMEOUT')); });
  });
}

// ── Build payloads ─────────────────────────────────────────────────────────────
function buildImagePayload() {
  return JSON.stringify({
    model: IMAGE_MODEL,
    prompt: PROMPT,
    sequential_image_generation: 'disabled',
    response_format: 'url',
    size: QUALITY,
    aspect_ratio: ASPECT_RATIO,
    watermark: WATERMARK === 'true',
    stream: false
  });
}

function buildVideoPayload() {
  const content = [{ type: 'text', text: PROMPT }];

  REF_IMAGES.forEach(img => {
    content.push({ type: 'image_url', image_url: { url: img }, role: 'reference_image' });
  });

  if (VIDEO_URL) {
    content.push({ type: 'video_url', video_url: { url: VIDEO_URL }, role: 'reference_video' });
  }
  if (AUDIO_URL) {
    content.push({ type: 'audio_url', audio_url: { url: AUDIO_URL }, role: 'reference_audio' });
  }

  return JSON.stringify({
    model: MODEL || VIDEO_MODEL,
    content: content,
    generate_audio: GENERATE_AUDIO === 'true',
    ratio: ASPECT_RATIO,
    duration: DURATION,
    watermark: WATERMARK === 'true'
  });
}

// ── Error handler ─────────────────────────────────────────────────────────────
function handleError(statusCode, body) {
  switch (statusCode) {
    case 401: console.error('ERROR: Invalid API key. https://console.volcengine.com/ark'); break;
    case 403: console.error('ERROR: Access forbidden. Check API key permissions.'); break;
    case 429: console.error('ERROR: Rate limit exceeded. Wait and retry.'); break;
    case 500: case 502: case 503: console.error('ERROR: Service error. Try again later.'); break;
    default: console.error('ERROR: API error (' + statusCode + '): ' + body); break;
  }
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  if (OUTPUT_MODE === 'image') {
    // Submit image (sync)
    const payload = buildImagePayload();
    console.log('INFO: Submitting image generation...');

    const { body, statusCode } = await doRequest('POST', IMAGE_API_BASE + '/generations', payload);
    if (statusCode !== 200) { handleError(statusCode, body); process.exit(1); }

    const obj = JSON.parse(body);
    const imageUrl = jsonGet(obj, 'data[0].url');
    if (!imageUrl) { console.error('ERROR: Failed to get image URL:', body); process.exit(1); }

    console.log('TASK_SUBMITTED: task_id=sync mode=文生图');
    console.log('IMAGE_URL=' + imageUrl);
    console.log('RESOLUTION=' + QUALITY);
    console.log('ASPECT_RATIO=' + ASPECT_RATIO);
    console.log('ELAPSED=0s');

    const ext = 'png';
    const filename = 'img_' + Date.now() + '.' + ext;
    const filepath = path.join(OUTPUT_DIR, filename);

    try {
      await downloadFile(imageUrl, filepath);
      console.log('INFO: Image saved to ' + filepath);
      console.log('LOCAL_FILE=' + filepath);
    } catch(e) {
      console.warn('WARNING: Image download failed, use online URL: ' + imageUrl);
    }

  } else {
    // Submit video (async)
    const payload = buildVideoPayload();
    const modeInfo = { txt2video: GENERATE_AUDIO === 'true' ? '文生音画' : '文生视频',
                       img2video: GENERATE_AUDIO === 'true' ? '图生音画' : '图生视频',
                       vid2video: '素材生视频' }[MODE] || MODE;

    console.log('INFO: Submitting video generation (' + modeInfo + ')...');

    const { body, statusCode } = await doRequest('POST', VIDEO_API_BASE, payload);
    if (statusCode !== 200) { handleError(statusCode, body); process.exit(1); }

    const obj = JSON.parse(body);
    const taskId = jsonGet(obj, 'id');
    if (!taskId) { console.error('ERROR: Failed to get task_id:', body); process.exit(1); }

    console.log('TASK_SUBMITTED: task_id=' + taskId + ' mode=' + modeInfo);

    // Poll
    const startTime = Date.now();
    let lastReport = -1;

    while (true) {
      const elapsed = Math.floor((Date.now() - startTime) / 1000);

      if (elapsed > MAX_POLL_SECONDS) {
        console.warn('WARNING: Poll timeout. Check: https://console.volcengine.com/ark');
        process.exit(1);
      }

      const bucket = Math.floor(elapsed / PROGRESS_INTERVAL);
      if (bucket > lastReport && elapsed >= PROGRESS_INTERVAL) {
        lastReport = bucket;
        console.log('STATUS_UPDATE: 视频生成中... (已等待 ' + elapsed + ' 秒)');
      }

      await new Promise(r => setTimeout(r, POLL_INTERVAL * 1000));

      const pollResp = await doRequest('GET', VIDEO_API_BASE + '/' + taskId, null);
      if (pollResp.statusCode !== 200) { handleError(pollResp.statusCode, pollResp.body); process.exit(1); }

      const pollObj = JSON.parse(pollResp.body);
      const status = pollObj.status;

      if (status === 'succeeded') {
        const videoUrl = jsonGet(pollObj, 'content.video_url');
        const duration = jsonGet(pollObj, 'duration');
        const ratio = jsonGet(pollObj, 'ratio');
        const resolution = jsonGet(pollObj, 'resolution');
        const hasAudio = jsonGet(pollObj, 'generate_audio');

        console.log('ELAPSED=' + elapsed + 's');
        if (duration) console.log('DURATION=' + duration + 's');
        if (ratio) console.log('ASPECT_RATIO=' + ratio);
        if (resolution) console.log('RESOLUTION=' + resolution);
        console.log('HAS_AUDIO=' + hasAudio);
        console.log('VIDEO_URL=' + videoUrl);

        const ext = 'mp4';
        const filename = 'video_' + Date.now() + '.' + ext;
        const filepath = path.join(OUTPUT_DIR, filename);

        try {
          await downloadFile(videoUrl, filepath);
          console.log('INFO: Video saved to ' + filepath);
          console.log('LOCAL_FILE=' + filepath);
        } catch(e) {
          console.warn('WARNING: Video download failed, use online URL: ' + videoUrl);
        }
        break;

      } else if (status === 'failed') {
        const err = jsonGet(pollObj, 'error') || jsonGet(pollObj, 'message') || 'Unknown';
        console.error('ERROR: Generation failed: ' + err);
        process.exit(1);
      }
      // running or pending - continue polling
    }
  }
}

main().catch(e => {
  console.error('ERROR:', e.message);
  process.exit(1);
});