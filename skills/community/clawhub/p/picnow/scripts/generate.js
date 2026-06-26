#!/usr/bin/env node
/**
 * Picnow image generation script — standalone, zero npm dependencies.
 * Requires Node 18+ (native fetch + FormData).
 *
 * Uses async API (/v1/async/images/...) to avoid Cloudflare 100s timeouts
 * on 2K/4K renders. POST returns a task id immediately, then polls until
 * the task is completed/failed/cancelled.
 *
 * Usage:
 *   node generate.js --prompt "..." [--quality 1k|2k|4k] [--aspect square|landscape|portrait] [--n 1] [--ref /path]
 *
 * Output (stdout): single JSON line  { "urls": ["https://..."] }
 * Errors:          stderr + exit 1
 */

const API_BASE = 'https://api.letmego.top';

const MODEL_BY_QUALITY = {
  '1k': 'gpt-image-2',
  '2k': 'gpt-image-2-2k',
  '4k': 'gpt-image-2-4k',
};

const SIZE_MATRIX = {
  '1k': { square: '1024x1024', landscape: '1536x1024', portrait: '1024x1536' },
  '2k': { square: '2048x2048', landscape: '2048x1152', portrait: '1152x2048' },
  '4k': { landscape: '3840x2160', portrait: '2160x3840' },
};

const POLL_INITIAL_DELAY_MS = 1500;
const POLL_INTERVAL_MS = 3000;
const POLL_TIMEOUT_MS = 10 * 60 * 1000;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--') && i + 1 < argv.length) {
      args[argv[i].slice(2)] = argv[i + 1];
      i++;
    }
  }
  return args;
}

function fail(msg) {
  process.stderr.write(msg + '\n');
  process.exit(1);
}

function pickSize(quality, aspect) {
  const tier = SIZE_MATRIX[quality];
  if (!tier) fail(`Unknown quality "${quality}". Use: 1k, 2k, 4k`);
  const size = tier[aspect];
  if (!size) {
    const fallback = tier.landscape ?? tier.portrait ?? tier.square;
    process.stderr.write(`Note: ${quality} ${aspect} is not supported, using ${fallback}\n`);
    return fallback;
  }
  return size;
}

function detectMime(b64) {
  const head = b64.slice(0, 16);
  if (head.startsWith('iVBOR')) return 'image/png';
  if (head.startsWith('/9j/') || head.startsWith('/9J/')) return 'image/jpeg';
  if (head.startsWith('UklGR')) return 'image/webp';
  if (head.startsWith('R0lGOD')) return 'image/gif';
  return 'image/png';
}

async function readFileAsBase64(filePath) {
  const { readFile } = await import('fs/promises');
  const buf = await readFile(filePath);
  return buf.toString('base64');
}

function base64ToUint8Array(b64) {
  const bin = Buffer.from(b64, 'base64');
  return new Uint8Array(bin.buffer, bin.byteOffset, bin.byteLength);
}

function extractErrorMessage(text, fallbackStatus) {
  try {
    const parsed = JSON.parse(text);
    const upstream =
      parsed?.detail?.error?.message ??
      parsed?.error?.message ??
      parsed?.message ??
      parsed?.detail?.error?.code ??
      parsed?.error?.code ??
      null;
    if (typeof upstream === 'string' && upstream.length > 0) return upstream;
  } catch {
    // body not JSON
  }
  return `HTTP ${fallbackStatus}`;
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

// ---------------------------------------------------------------------------
// API calls
// ---------------------------------------------------------------------------

async function submitTextToImage(token, { model, prompt, size, n }) {
  const res = await fetch(`${API_BASE}/v1/async/images/generations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ model, prompt, size, n, response_format: 'url' }),
  });
  const text = await res.text();
  if (res.status < 200 || res.status >= 300) {
    fail(`API error: ${extractErrorMessage(text, res.status)}`);
  }
  return { task: JSON.parse(text), kind: 'generations' };
}

async function submitImageToImage(token, { model, prompt, size, n, refB64 }) {
  const mime = detectMime(refB64);
  const ext = mime.split('/')[1] ?? 'png';
  const blob = new Blob([base64ToUint8Array(refB64)], { type: mime });

  const form = new FormData();
  form.append('model', model);
  form.append('prompt', prompt);
  form.append('size', size);
  form.append('n', String(n));
  form.append('response_format', 'url');
  form.append('image', blob, `reference.${ext}`);

  const res = await fetch(`${API_BASE}/v1/async/images/edits`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  const text = await res.text();
  if (res.status < 200 || res.status >= 300) {
    fail(`API error: ${extractErrorMessage(text, res.status)}`);
  }
  return { task: JSON.parse(text), kind: 'edits' };
}

async function pollTask(token, kind, id) {
  const deadline = Date.now() + POLL_TIMEOUT_MS;
  await sleep(POLL_INITIAL_DELAY_MS);

  while (Date.now() < deadline) {
    const res = await fetch(`${API_BASE}/v1/async/images/${kind}/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const text = await res.text();
    if (res.status < 200 || res.status >= 300) {
      fail(`API error while polling: ${extractErrorMessage(text, res.status)}`);
    }
    const task = JSON.parse(text);
    const status = task.status;

    if (status === 'completed') return task;
    if (status === 'failed') {
      const msg = task?.error?.message ?? 'task failed';
      fail(`Task failed: ${msg}`);
    }
    if (status === 'cancelled') fail('Task was cancelled');

    await sleep(POLL_INTERVAL_MS);
  }
  fail(`Task ${id} did not complete within ${POLL_TIMEOUT_MS / 1000}s`);
}

function toAbsoluteUrl(u) {
  if (!u) return null;
  if (u.startsWith('http://') || u.startsWith('https://')) return u;
  return API_BASE + (u.startsWith('/') ? u : '/' + u);
}

function extractUrls(task) {
  return (task.data ?? [])
    .map((d) => {
      if (d.url) return toAbsoluteUrl(d.url);
      if (d.b64_json) return `data:image/png;base64,${d.b64_json}`;
      return null;
    })
    .filter(Boolean);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const token = process.env.LETMEGO_API_KEY;
  if (!token) {
    fail(
      '❌ LETMEGO_API_KEY is not set.\n' +
        'Get your 令牌 at https://api.letmego.top, then:\n' +
        '  export LETMEGO_API_KEY=your_令牌'
    );
  }

  const args = parseArgs(process.argv.slice(2));

  const prompt = args.prompt;
  if (!prompt) fail('--prompt is required');

  const quality = args.quality ?? '1k';
  if (!MODEL_BY_QUALITY[quality]) fail(`Unknown quality "${quality}". Use: 1k, 2k, 4k`);

  const aspect = args.aspect ?? 'square';
  if (!['square', 'landscape', 'portrait'].includes(aspect))
    fail(`Unknown aspect "${aspect}". Use: square, landscape, portrait`);

  const n = Math.min(10, Math.max(1, parseInt(args.n ?? '1', 10)));
  const model = MODEL_BY_QUALITY[quality];
  const size = pickSize(quality, aspect);
  const refPath = args.ref ?? null;

  let submitted;
  if (refPath) {
    const refB64 = await readFileAsBase64(refPath);
    submitted = await submitImageToImage(token, { model, prompt, size, n, refB64 });
  } else {
    submitted = await submitTextToImage(token, { model, prompt, size, n });
  }

  const { task: initial, kind } = submitted;
  const id = initial.id;
  if (!id) fail('Submission did not return a task id');

  const finalTask = await pollTask(token, kind, id);
  const urls = extractUrls(finalTask);
  if (urls.length === 0) fail('Task completed but no image URLs were returned');

  process.stdout.write(JSON.stringify({ urls }) + '\n');
}

main().catch((err) => fail(String(err)));
