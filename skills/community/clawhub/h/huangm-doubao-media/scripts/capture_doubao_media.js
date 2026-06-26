#!/usr/bin/env node
/**
 * Capture Doubao-generated image/video assets from browser network traffic.
 *
 * Usage:
 *   node capture_doubao_media.js monitor
 *   node capture_doubao_media.js monitor --download
 *   node capture_doubao_media.js monitor --output <dir>
 */

const CDP = require('chrome-remote-interface');
const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

const DEFAULT_PORT = 18800;
const DEFAULT_OUTPUT = path.join(process.cwd(), 'captures');

function parseArgs(argv) {
  const args = {
    command: 'monitor',
    download: false,
    output: DEFAULT_OUTPUT,
    port: DEFAULT_PORT,
  };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg) continue;
    if (!arg.startsWith('--') && i === 0) {
      args.command = arg;
      continue;
    }
    if (arg === '--download') args.download = true;
    else if (arg === '--output') args.output = argv[++i];
    else if (arg === '--port') args.port = Number(argv[++i]) || DEFAULT_PORT;
  }
  return args;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function timestamp() {
  return new Date().toISOString().replace(/[:.]/g, '-');
}

function isInterestingUrl(url) {
  return /(doubao|bytedance|byteimg|douyin|douyinvod|snssdk|volces|image|video|img|poster|cover|playlet|tos-cn|tos\-|token|generate|completion)/i.test(url || '');
}

function looksLikeMediaUrl(url) {
  return /^https?:\/\//i.test(url || '') && /\.(png|jpg|jpeg|webp|gif|mp4|mov|webm|m3u8|heic|image)(\?|$)/i.test(url);
}

function guessKind(url, contentType) {
  const s = `${url || ''} ${contentType || ''}`.toLowerCase();
  if (/(video\/mp4|video\/webm|mime_type=video_mp4|\/video\/|video_dsz|video_pre|video_gen|\.mp4|\.mov|\.webm|\.m3u8)/.test(s)) return 'video';
  if (/(image|png|jpg|jpeg|webp|gif|heic|\.image)/.test(s)) return 'image';
  return 'other';
}

function sanitizeFileName(name) {
  return name.replace(/[<>:"/\\|?*\x00-\x1F]/g, '_').slice(0, 180);
}

function inferExt(url, contentType, fallbackKind) {
  const match = (url || '').match(/\.([a-zA-Z0-9]{2,5})(?:\?|$)/);
  if (match) return '.' + match[1].toLowerCase();
  const ct = (contentType || '').toLowerCase();
  if (ct.includes('png')) return '.png';
  if (ct.includes('jpeg') || ct.includes('jpg')) return '.jpg';
  if (ct.includes('webp')) return '.webp';
  if (ct.includes('gif')) return '.gif';
  if (ct.includes('heic')) return '.heic';
  if (ct.includes('mp4')) return '.mp4';
  if (ct.includes('webm')) return '.webm';
  if (ct.includes('quicktime') || ct.includes('mov')) return '.mov';
  if (ct.includes('mpegurl') || ct.includes('m3u8')) return '.m3u8';
  return fallbackKind === 'video' ? '.mp4' : '.bin';
}

function appendJsonl(file, obj) {
  fs.appendFileSync(file, JSON.stringify(obj) + '\n');
}

function appendPretty(file, text) {
  fs.appendFileSync(file, text + '\n');
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
      if (looksLikeMediaUrl(cleaned) || isInterestingUrl(cleaned)) found.add(cleaned);
    }
    return found;
  }
  if (Array.isArray(value)) {
    for (const item of value) collectUrlsDeep(item, found);
    return found;
  }
  if (value && typeof value === 'object') {
    for (const [k, v] of Object.entries(value)) {
      if (typeof v === 'string' && /^https?:\/\//i.test(v) && (looksLikeMediaUrl(v) || /(url|uri|video|image|poster|cover|origin|download|play_addr|src)/i.test(k))) {
        found.add(v);
      }
      collectUrlsDeep(v, found);
    }
  }
  return found;
}

function isLikelyGeneratedVideo(url, parentUrl = '', contentType = '') {
  const s = `${url} ${parentUrl} ${contentType}`.toLowerCase();
  return (
    /douyinvod\.com|douyin\.com\/.*download=true|snssdk\.com\/video\/fplay/.test(s) ||
    /mime_type=video_mp4/.test(s) ||
    /\/samantha\/video\/get_play_info/.test(s) ||
    /video_gen_watermark_dyn/.test(s)
  );
}

function isLikelyGeneratedImage(url, parentUrl = '', contentType = '') {
  const s = `${url} ${parentUrl} ${contentType}`.toLowerCase();
  return (
    /rc_gen_image/.test(s) ||
    /image_raw|image_dld|image_pre|img_pre_mark/.test(s) ||
    /\/chat\/completion|\/samantha\/chat\/completion/.test(s)
  );
}

function classifyAsset(url, parentUrl = '', contentType = '') {
  const kind = guessKind(url, contentType);
  const lowerUrl = (url || '').toLowerCase();
  const lowerParent = (parentUrl || '').toLowerCase();
  const generatedBy = [];

  if (/\/samantha\/chat\/completion/.test(lowerParent)) generatedBy.push('chat_completion');
  if (/\/samantha\/video\/get_play_info/.test(lowerParent)) generatedBy.push('video_get_play_info');
  if (/\/im\/chain\/single/.test(lowerParent)) generatedBy.push('conversation_chain');
  if (/\/samantha\/skill\/pack/.test(lowerParent)) generatedBy.push('skill_pack');

  const generated =
    kind === 'video'
      ? isLikelyGeneratedVideo(lowerUrl, lowerParent, contentType)
      : kind === 'image'
        ? isLikelyGeneratedImage(lowerUrl, lowerParent, contentType)
        : false;

  let variant = 'other';
  if (kind === 'video') {
    if (/video_dsz|video_pre|watermark/.test(lowerUrl) && !/video_mp4|fplay|download=true/.test(lowerUrl)) variant = 'preview';
    else if (/download=true|video_mp4|\/video\/fplay\//.test(lowerUrl)) variant = 'download';
    else if (/douyinvod\.com/.test(lowerUrl)) variant = 'play';
  } else if (kind === 'image') {
    if (/rc_gen_image/.test(lowerUrl)) variant = 'generated';
    else if (/poster|cover|thumb|noop\.image/.test(lowerUrl)) variant = 'thumbnail';
  }

  return {
    kind,
    generated,
    variant,
    generatedBy,
    parentUrl,
  };
}

function stableAssetId(url) {
  const s = url || '';
  const videoId = s.match(/\/video\/tos\/[^/]+\/([^/?]+)/i);
  if (videoId) return videoId[1];
  const fplayId = s.match(/\/video\/fplay\/[^/]+\/([^/?]+)/i);
  if (fplayId) return fplayId[1];
  const imageId = s.match(/rc_gen_image\/([^./?~]+)/i);
  if (imageId) return imageId[1];
  const tok = s.match(/\/([^/?#]+)(?:\?|$)/);
  return tok ? tok[1] : s;
}

function scoreAsset(item) {
  const s = `${item.url || ''} ${item.parentUrl || ''}`.toLowerCase();
  let score = 0;
  if (item.generated) score += 100;
  if (item.kind === 'video') score += 100;
  if (/download=true|video_mp4|\/video\/fplay\//.test(s)) score += 80;
  if (/douyinvod\.com/.test(s)) score += 60;
  if (/\/samantha\/video\/get_play_info/.test(s)) score += 50;
  if (/\/im\/chain\/single/.test(s)) score += 20;
  if (/video_dsz|video_pre|watermark/.test(s) && !/video_mp4|fplay|download=true/.test(s)) score -= 40;
  if (/thumb|poster|cover|noop\.image/.test(s)) score -= 30;
  if (/favicon|banner|creation|smallword|user-avatar|bot_icon/.test(s)) score -= 100;
  return score;
}

async function downloadFile(url, filePath) {
  const client = url.startsWith('https:') ? https : http;
  return new Promise((resolve, reject) => {
    client.get(url, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        return resolve(downloadFile(res.headers.location, filePath));
      }
      if (res.statusCode !== 200 && res.statusCode !== 206) {
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

async function main() {
  const args = parseArgs(process.argv.slice(2));
  ensureDir(args.output);
  const ts = timestamp();
  const manifestPath = path.join(args.output, `doubao-media-${ts}.jsonl`);
  const summaryPath = path.join(args.output, `doubao-media-${ts}-summary.txt`);
  const curatedPath = path.join(args.output, `doubao-media-${ts}-curated.json`);
  const downloaded = new Set();
  const captured = new Set();
  const responseMeta = new Map();
  const recordedItems = [];

  console.log('='.repeat(64));
  console.log('Doubao media capture');
  console.log('='.repeat(64));
  console.log(`CDP port: ${args.port}`);
  console.log(`Output: ${args.output}`);
  console.log(`Download media: ${args.download ? 'yes' : 'no'}`);
  console.log('Open Doubao in your browser and generate an image/video now.');
  console.log('Press Ctrl+C to stop.\n');

  const client = await CDP({ port: args.port });
  const { Network, Page } = client;
  await Network.enable();
  await Page.enable();

  async function recordUrl(url, source, extra = {}) {
    if (!url || captured.has(`${source}:${url}`)) return;
    if (/^data:/i.test(url)) return;
    captured.add(`${source}:${url}`);

    const classification = classifyAsset(url, extra.parentUrl, extra.contentType);
    const item = {
      time: new Date().toISOString(),
      source,
      url,
      assetId: stableAssetId(url),
      score: 0,
      ...classification,
      ...extra,
    };
    item.score = scoreAsset(item);
    recordedItems.push(item);

    appendJsonl(manifestPath, item);
    appendPretty(summaryPath, `[${item.time}] ${source} ${item.kind} generated=${item.generated} variant=${item.variant} score=${item.score} ${url}`);
    console.log(`📎 ${source} ${item.kind}: ${url}`);

    const shouldDownload =
      args.download &&
      (item.kind === 'image' || item.kind === 'video') &&
      item.generated &&
      (item.variant === 'download' || item.variant === 'play' || item.variant === 'generated');

    if (shouldDownload && !downloaded.has(url)) {
      downloaded.add(url);
      try {
        const ext = inferExt(url, extra.contentType, item.kind);
        const name = sanitizeFileName(`${item.kind}-${Date.now()}${ext}`);
        const target = path.join(args.output, name);
        await downloadFile(url, target);
        item.saved = target;
        appendPretty(summaryPath, `  ↳ saved ${target}`);
        console.log(`   ↳ saved ${target}`);
      } catch (err) {
        item.downloadError = err.message;
        appendPretty(summaryPath, `  ↳ download failed: ${err.message}`);
        console.log(`   ↳ download failed: ${err.message}`);
      }
    }
  }

  function writeCuratedManifest() {
    const grouped = new Map();
    for (const item of recordedItems.filter(x => x.generated && (x.kind === 'image' || x.kind === 'video'))) {
      const key = `${item.kind}:${item.assetId}`;
      if (!grouped.has(key)) grouped.set(key, []);
      grouped.get(key).push(item);
    }

    const assets = Array.from(grouped.values()).map(items => {
      items.sort((a, b) => b.score - a.score);
      const best = items[0];
      return {
        assetId: best.assetId,
        kind: best.kind,
        generated: true,
        bestUrl: best.url,
        bestSaved: best.saved || null,
        bestVariant: best.variant,
        generatedBy: Array.from(new Set(items.flatMap(x => x.generatedBy || []).filter(Boolean))),
        variants: items.map(x => ({
          url: x.url,
          variant: x.variant,
          score: x.score,
          source: x.source,
          parentUrl: x.parentUrl,
          saved: x.saved || null,
        })),
      };
    }).sort((a, b) => (a.kind === b.kind ? 0 : a.kind === 'video' ? -1 : 1));

    fs.writeFileSync(curatedPath, JSON.stringify({
      savedAt: new Date().toISOString(),
      output: args.output,
      assets,
    }, null, 2));
  }

  Network.requestWillBeSent(params => {
    const url = params?.request?.url;
    if (!isInterestingUrl(url)) return;
    const method = params?.request?.method;
    console.log(`➡️  ${method} ${url}`);
    if (looksLikeMediaUrl(url)) {
      recordUrl(url, 'request', { method });
    }
    const postData = params?.request?.postData;
    if (postData) {
      try {
        const obj = JSON.parse(postData);
        for (const foundUrl of collectUrlsDeep(obj)) {
          recordUrl(foundUrl, 'request-body', { method, parentUrl: url });
        }
      } catch {}
    }
  });

  Network.responseReceived(params => {
    const url = params?.response?.url;
    const contentType = params?.response?.headers?.['content-type'] || params?.response?.mimeType || '';
    responseMeta.set(params.requestId, { url, contentType, status: params?.response?.status });
    if (!isInterestingUrl(url)) return;
    console.log(`⬅️  ${params?.response?.status} ${url}`);
    if (looksLikeMediaUrl(url) || /^(image|video)\//i.test(contentType)) {
      recordUrl(url, 'response', { contentType, status: params?.response?.status });
    }
  });

  Network.loadingFinished(async params => {
    const meta = responseMeta.get(params.requestId);
    if (!meta || !isInterestingUrl(meta.url)) return;
    const contentType = (meta.contentType || '').toLowerCase();
    if (!contentType.includes('json') && !contentType.includes('javascript') && !contentType.includes('text')) return;
    try {
      const body = await Network.getResponseBody({ requestId: params.requestId });
      let text = body.body || '';
      if (body.base64Encoded) text = Buffer.from(text, 'base64').toString('utf8');
      if (!text) return;

      for (const foundUrl of collectUrlsDeep(text)) {
        await recordUrl(foundUrl, 'response-body', { parentUrl: meta.url, contentType: meta.contentType, status: meta.status });
      }
      writeCuratedManifest();
    } catch {}
  });

  process.on('SIGINT', async () => {
    console.log('\nStopping capture...');
    writeCuratedManifest();
    console.log(`Manifest: ${manifestPath}`);
    console.log(`Summary:  ${summaryPath}`);
    console.log(`Curated:  ${curatedPath}`);
    await client.close();
    process.exit(0);
  });
}

main().catch(err => {
  console.error('Capture failed:', err.message);
  process.exit(1);
});
