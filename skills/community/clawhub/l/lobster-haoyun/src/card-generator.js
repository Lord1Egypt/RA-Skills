/**
 * card-generator.js — 运势卡片本地合成引擎
 *
 * sharp 加载节气背景图 → SVG 文字叠加 → composite → 输出 PNG。
 * 本地运行，不经 OB，不调外部 API。秒级出图。
 *
 * Font: Noto Sans SC (SIL OFL). Downloaded once on first use, cached at
 * ~/.lucky-lobster/NotoSansSC-Regular.ttf, embedded as base64 in SVG @font-face.
 */
import sharp from "sharp";
import path from "node:path";
import fs from "node:fs";
import os from "node:os";
import https from "node:https";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUTPUT_SIZE = 768;
const DATA_DIR = path.join(os.homedir(), ".lucky-lobster");
const FONT_CACHE = path.join(DATA_DIR, "NotoSansSC-Regular.ttf");

// GitHub Releases permanent asset URL for the font
const FONT_URL = "https://github.com/ryanbihai/lobster-haoyun/releases/download/font-v1/NotoSansSC.ttf";

// Load 24节气 background images from base64 JSON
const CARDS_BASE64 = JSON.parse(
  fs.readFileSync(path.join(__dirname, "assets", "cards-base64.json"), "utf-8")
);

let _fontBase64 = null;

// ── Font Loading ──

async function loadFontBase64() {
  if (_fontBase64) return _fontBase64;

  if (fs.existsSync(FONT_CACHE)) {
    _fontBase64 = fs.readFileSync(FONT_CACHE).toString("base64");
    return _fontBase64;
  }

  // First use — download from GitHub Releases (one-time ~10MB, cached forever)
  console.error("[card-generator] Downloading font (first use, ~10MB)...");
  try {
    const buf = await download(FONT_URL);
    fs.mkdirSync(DATA_DIR, { recursive: true });
    fs.writeFileSync(FONT_CACHE, buf);
    _fontBase64 = buf.toString("base64");
    console.error("[card-generator] Font cached:", FONT_CACHE);
    return _fontBase64;
  } catch (e) {
    console.error("[card-generator] Font download failed:", e.message);
    // Try fallback URL (jsDelivr CDN mirror)
    try {
      const fallbackUrl = "https://cdn.jsdelivr.net/gh/ryanbihai/lobster-haoyun@font-v1/NotoSansSC-Regular.ttf";
      console.error("[card-generator] Trying fallback URL...");
      const buf = await download(fallbackUrl);
      fs.writeFileSync(FONT_CACHE, buf);
      _fontBase64 = buf.toString("base64");
      console.error("[card-generator] Font cached via fallback");
      return _fontBase64;
    } catch (e2) {
      console.error("[card-generator] Fallback also failed:", e2.message);
      console.error("[card-generator] Chinese text may not render correctly.");
      return null;
    }
  }
}

function download(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { timeout: 60000 }, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        https.get(res.headers.location, { timeout: 60000 }, (res2) => {
          if (res2.statusCode !== 200) return reject(new Error(`HTTP ${res2.statusCode}`));
          collect(res2, resolve, reject);
        }).on("error", reject);
        return;
      }
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode}`));
      collect(res, resolve, reject);
    }).on("error", reject);
  });
}

function collect(res, resolve, reject) {
  const chunks = [];
  res.on("data", c => chunks.push(c));
  res.on("end", () => resolve(Buffer.concat(chunks)));
  res.on("error", reject);
}

// ── Public API ──

export async function generateCard({ type_name, one_liner, story_title, solar_term, date }) {
  const bgBase64 = CARDS_BASE64[solar_term];
  if (!bgBase64) throw new Error(`no background for solar term: ${solar_term}`);

  const fontBase64 = await loadFontBase64();
  const overlaySvg = buildOverlaySvg({ type_name, one_liner, story_title, solar_term, date, fontBase64 });
  const overlayBuf = await sharp(Buffer.from(overlaySvg, "utf-8"))
    .resize(OUTPUT_SIZE, OUTPUT_SIZE).png().toBuffer();

  const card = await sharp(Buffer.from(bgBase64, "base64"))
    .resize(OUTPUT_SIZE, OUTPUT_SIZE, { fit: "cover" })
    .composite([{ input: overlayBuf, top: 0, left: 0 }])
    .flatten({ background: "#f0f0f0" })
    .png({ compressionLevel: 9, palette: true })
    .toBuffer();

  return {
    card_base64: card.toString("base64"),
    card_id: `card_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`,
  };
}

// ── SVG Layout ──

function buildOverlaySvg({ type_name, one_liner, story_title, solar_term, date, fontBase64 }) {
  const W = OUTPUT_SIZE, H = OUTPUT_SIZE, centerX = W / 2;
  const displayDate = date || new Date().toISOString().slice(0, 10);

  const fontFace = fontBase64
    ? `@font-face { font-family: 'CardFont'; src: url(data:font/truetype;base64,${fontBase64}) format('truetype'); }`
    : '';
  const fontFamily = fontBase64
    ? "'CardFont', sans-serif"
    : "'Noto Sans SC', 'Microsoft YaHei', 'PingFang SC', sans-serif";

  const lines = wrapText(one_liner, 14);
  const tspans = lines.map((l, i) =>
    `<tspan x="${centerX}" dy="${i === 0 ? 0 : 52}">${esc(l)}</tspan>`
  ).join("\n");

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <style>${fontFace} text { font-family: ${fontFamily}; }</style>
    <filter id="s" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.5"/>
    </filter>
    <linearGradient id="tf" x1="0" y1="0" x2="0" y2="0.3">
      <stop offset="0%" stop-color="#000" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="bf" x1="0" y1="1" x2="0" y2="0.75">
      <stop offset="0%" stop-color="#000" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="${W}" height="${H}" fill="url(#tf)"/>
  <rect x="0" y="0" width="${W}" height="${H}" fill="url(#bf)"/>
  <text x="48" y="72" font-size="24" fill="#fff" opacity="0.85" filter="url(#s)">${esc(displayDate)} · ${esc(solar_term)}</text>
  <rect x="${W-160}" y="36" width="112" height="40" rx="20" fill="#fff" opacity="0.25"/>
  <text x="${W-104}" y="63" font-size="22" fill="#fff" text-anchor="middle" filter="url(#s)">${esc(type_name)}</text>
  <text x="${centerX}" y="${H*0.42}" font-size="40" fill="#fff" text-anchor="middle" filter="url(#s)" font-weight="bold">${tspans}</text>
  <text x="${centerX}" y="${H-110}" font-size="22" fill="#fff" text-anchor="middle" opacity="0.8" filter="url(#s)">「${esc(story_title)}」</text>
  <text x="${centerX}" y="${H-45}" font-size="16" fill="#fff" text-anchor="middle" opacity="0.45">龙虾好运势</text>
</svg>`;
}

function wrapText(text, max) {
  const lines = []; let r = text;
  while (r.length > 0) {
    if (r.length <= max) { lines.push(r); break; }
    let cut = max;
    for (let i = max; i >= max - 5 && i > 0; i--) {
      if (/[，。、；：？！\s,.]/.test(r[i])) { cut = i + 1; break; }
    }
    lines.push(r.slice(0, cut)); r = r.slice(cut);
  }
  return lines;
}

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/[\n\r\t]/g, "");   // strip control chars that break SVG text
}
