#!/usr/bin/env node
/**
 * Doubao media helper.
 * - Calls chat/completion
 * - Extracts image/video URLs from SSE payloads
 * - Groups URL variants by asset id
 * - Optionally downloads best assets to disk
 *
 * Usage:
 *   node doubao_media_api.js chat "生成一张猫咪图片"
 *   node doubao_media_api.js chat "生成一张猫咪图片" --download --output ./captures
 */

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const DEFAULT_OUTPUT = path.join(process.cwd(), 'captures');
const {
  DEFAULT_BOT_ID: BOT_ID,
  DEFAULT_REQUEST_PATH: REQUEST_PATH,
  readSession,
  getCookieString,
  ensureSession,
} = require('./doubao_session');

function parseArgs(argv) {
  const args = { command: argv[0], prompt: '', download: false, output: DEFAULT_OUTPUT };
  const parts = [];
  for (let i = 1; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--download') args.download = true;
    else if (arg === '--output') args.output = argv[++i] || DEFAULT_OUTPUT;
    else parts.push(arg);
  }
  args.prompt = parts.join(' ').trim();
  return args;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function timestamp() {
  return new Date().toISOString().replace(/[:.]/g, '-');
}

function sanitizeFileName(name) {
  return name.replace(/[<>:"/\\|?*\x00-\x1F]/g, '_').slice(0, 180);
}

function collectUrlsDeep(value, found = new Set()) {
  if (typeof value === 'string') {
    const trimmed = value.trim();
    if ((trimmed.startsWith('{') && trimmed.endsWith('}')) || (trimmed.startsWith('[') && trimmed.endsWith(']'))) {
      try { collectUrlsDeep(JSON.parse(trimmed), found); } catch {}
    }
    const matches = trimmed.match(/https?:\/\/[^\s"'<>\\]+/g) || [];
    for (const m of matches) {
      const cleaned = m.replace(/[),\]]+$/, '');
      if (/\.(png|jpg|jpeg|webp|gif|mp4|mov|webm|m3u8|heic)(\?|$)/i.test(cleaned) || /(image|video|poster|cover|play_addr|tos-cn|byteimg)/i.test(cleaned)) {
        found.add(cleaned);
      }
    }
    return found;
  }
  if (Array.isArray(value)) {
    for (const item of value) collectUrlsDeep(item, found);
    return found;
  }
  if (value && typeof value === 'object') {
    for (const [k, v] of Object.entries(value)) {
      if (typeof v === 'string' && /^https?:\/\//i.test(v) && (/(url|uri|video|image|poster|cover|play_addr|src|download)/i.test(k) || /\.(png|jpg|jpeg|webp|gif|mp4|mov|webm|m3u8|heic)(\?|$)/i.test(v))) {
        found.add(v);
      }
      collectUrlsDeep(v, found);
    }
  }
  return found;
}

function guessKind(url) {
  const s = (url || '').toLowerCase();
  if (/(video|mp4|mov|webm|m3u8)/.test(s)) return 'video';
  return 'image';
}

function scoreUrl(url) {
  const s = (url || '').toLowerCase();
  if (s.includes('image_raw')) return 100;
  if (s.includes('image_dld')) return 90;
  if (s.includes('image_pre')) return 80;
  if (s.includes('img_pre_mark')) return 70;
  if (s.includes('downsize_watermark')) return 60;
  if (s.includes('hcg_watermark')) return 50;
  if (s.includes('poster') || s.includes('cover')) return 40;
  return 10;
}

function extractAssetId(url) {
  const m = (url || '').match(/rc_gen_image\/([^./?~]+)/i);
  if (m) return m[1];
  const mv = (url || '').match(/\/([^/?#]+)\.(?:png|jpg|jpeg|webp|gif|mp4|mov|webm|m3u8|heic)(?:\?|$)/i);
  return mv ? mv[1] : url;
}

function normalizeMediaUrls(urls) {
  const groups = new Map();
  for (const url of urls) {
    const assetId = extractAssetId(url);
    if (!groups.has(assetId)) groups.set(assetId, []);
    groups.get(assetId).push(url);
  }

  return Array.from(groups.entries()).map(([assetId, variants]) => {
    const uniqueVariants = Array.from(new Set(variants.filter(Boolean)));
    uniqueVariants.sort((a, b) => scoreUrl(b) - scoreUrl(a));
    return {
      assetId,
      kind: guessKind(uniqueVariants[0] || ''),
      bestUrl: uniqueVariants[0],
      variants: uniqueVariants
    };
  });
}

function parseSsePayload(raw) {
  const result = { text: '', mediaUrls: [], assets: [] };
  const media = new Set();
  const events = raw.split('\n\n');
  for (const rawEvent of events) {
    const lines = rawEvent.split('\n').map(line => line.trim()).filter(Boolean);
    const eventLine = lines.find(line => line.startsWith('event:'));
    const dataLine = lines.find(line => line.startsWith('data:'));
    if (!eventLine || !dataLine) continue;
    const eventName = eventLine.replace(/^event:\s*/, '');
    try {
      const json = JSON.parse(dataLine.replace(/^data:\s*/, ''));
      const blocks = json?.content?.content_block || json?.message?.content_block || json?.data?.content?.content_block || [];
      for (const block of blocks) {
        const text = block?.content?.text_block?.text;
        if (eventName === 'STREAM_MSG_NOTIFY' && text) result.text += text;
      }
      for (const url of collectUrlsDeep(json)) media.add(url);
    } catch {}
  }
  result.mediaUrls = Array.from(media);
  result.assets = normalizeMediaUrls(result.mediaUrls);
  return result;
}

async function downloadFile(url, filePath) {
  const client = url.startsWith('https:') ? https : http;
  return new Promise((resolve, reject) => {
    client.get(url, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        return resolve(downloadFile(res.headers.location, filePath));
      }
      if (res.statusCode !== 200) {
        res.resume();
        return reject(new Error(`HTTP ${res.statusCode}`));
      }
      const out = fs.createWriteStream(filePath);
      res.pipe(out);
      out.on('finish', () => out.close(resolve));
      out.on('error', reject);
    }).on('error', reject);
  });
}

function inferExt(url, kind) {
  const match = (url || '').match(/\.([a-zA-Z0-9]{2,5})(?:\?|$)/);
  if (match) return '.' + match[1].toLowerCase();
  return kind === 'video' ? '.mp4' : '.png';
}

async function downloadAssets(assets, outputDir) {
  ensureDir(outputDir);
  const manifestPath = path.join(outputDir, `doubao-api-assets-${timestamp()}.json`);
  const results = [];

  for (let i = 0; i < assets.length; i++) {
    const asset = assets[i];
    if (!asset.bestUrl) continue;
    const ext = inferExt(asset.bestUrl, asset.kind);
    const filename = sanitizeFileName(`${String(i + 1).padStart(2, '0')}-${asset.kind}-${asset.assetId}${ext}`);
    const filePath = path.join(outputDir, filename);
    try {
      await downloadFile(asset.bestUrl, filePath);
      results.push({ ...asset, saved: filePath, ok: true });
    } catch (error) {
      results.push({ ...asset, ok: false, error: error.message });
    }
  }

  fs.writeFileSync(manifestPath, JSON.stringify({ savedAt: new Date().toISOString(), outputDir, assets: results }, null, 2));
  return { outputDir, manifestPath, assets: results };
}

async function chat(prompt, opts = {}) {
  await ensureSession({ message: '你好', requestPath: REQUEST_PATH, botId: BOT_ID });
  const session = readSession();
  const cookieStr = getCookieString(session);
  const localMsgId = 'local_' + Date.now();
  const postData = JSON.stringify({
    client_meta: { local_conversation_id: localMsgId, conversation_id: '', bot_id: BOT_ID },
    messages: [{
      local_message_id: localMsgId,
      content_block: [{ block_type: 10000, content: { text_block: { text: prompt } }, block_id: 'msg_1' }],
      message_status: 0
    }],
    option: { create_time_ms: Date.now(), is_audio: false }
  });

  const options = {
    hostname: 'www.doubao.com',
    port: 443,
    path: REQUEST_PATH,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData),
      'Cookie': cookieStr,
      'Origin': 'https://www.doubao.com',
      'Referer': 'https://www.doubao.com/chat/',
      'Accept': 'text/event-stream'
    }
  };

  return new Promise((resolve, reject) => {
    let data = '';
    const req = https.request(options, res => {
      res.on('data', chunk => { data += chunk; });
      res.on('end', async () => {
        try {
          const parsed = parseSsePayload(data);
          if (opts.download && parsed.assets.length) {
            parsed.download = await downloadAssets(parsed.assets, opts.output || DEFAULT_OUTPUT);
          }
          console.log(JSON.stringify(parsed, null, 2));
          resolve(parsed);
        } catch (error) {
          reject(error);
        }
      });
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

const args = parseArgs(process.argv.slice(2));
if (args.command === 'chat') {
  chat(args.prompt || '生成一张猫咪图片', { download: args.download, output: args.output });
} else {
  console.log('Usage: node doubao_media_api.js chat "prompt" [--download] [--output ./captures]');
}
