#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import https from 'https';
import http from 'http';
import PptxGenJS from 'pptxgenjs';

const input = process.argv[2];
const output = process.argv[3];
if (!input || !output) {
  console.error('Usage: manus_slides_json_to_pptx.mjs <slides.json> <output.pptx>');
  process.exit(1);
}

const raw = fs.readFileSync(input, 'utf8');
const obj = JSON.parse(raw);
const outDir = path.join(path.dirname(output), '.manus-slide-assets');
fs.mkdirSync(outDir, { recursive: true });

function download(url, dest) {
  const client = url.startsWith('https:') ? https : http;
  return new Promise((resolve, reject) => {
    const req = client.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        return resolve(download(res.headers.location, dest));
      }
      if (res.statusCode !== 200) {
        res.resume();
        return reject(new Error(`HTTP ${res.statusCode} for ${url}`));
      }
      const file = fs.createWriteStream(dest);
      res.pipe(file);
      file.on('finish', () => file.close(() => resolve(dest)));
      file.on('error', reject);
    });
    req.on('error', reject);
    req.setTimeout(120000, () => req.destroy(new Error('timeout')));
  });
}

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'OpenClaw';
pptx.company = 'OpenClaw';
pptx.subject = obj.title || 'Manus Slides';
pptx.title = obj.title || 'Manus Slides';
pptx.lang = 'zh-CN';
pptx.theme = {
  headFontFace: 'Arial',
  bodyFontFace: 'Arial',
  lang: 'zh-CN'
};

const slides = Array.isArray(obj.slide_ids) ? obj.slide_ids : [];
for (let i = 0; i < slides.length; i++) {
  const slideId = slides[i];
  const slide = pptx.addSlide();
  const imgUrl = obj.images?.[slideId];
  const outline = Array.isArray(obj.outline) ? obj.outline.find((x) => x.id === slideId) : undefined;
  if (imgUrl) {
    const imgPath = path.join(outDir, `${String(i + 1).padStart(2, '0')}_${slideId}.png`);
    if (!fs.existsSync(imgPath)) {
      await download(imgUrl, imgPath);
    }
    slide.addImage({ path: imgPath, x: 0, y: 0, w: 13.333, h: 7.5 });
  } else {
    slide.background = { color: 'F5F5F7' };
    slide.addText(outline?.title || slideId, {
      x: 0.5, y: 0.4, w: 12.3, h: 0.8,
      fontSize: 24, bold: true, color: '222222'
    });
    slide.addText(outline?.summary || 'No preview image available for this slide.', {
      x: 0.7, y: 1.4, w: 12, h: 4,
      fontSize: 16, color: '444444', breakLine: false
    });
  }
}

await pptx.writeFile({ fileName: output });
console.log(output);
