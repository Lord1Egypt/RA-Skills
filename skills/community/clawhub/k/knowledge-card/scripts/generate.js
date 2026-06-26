#!/usr/bin/env node
/**
 * knowledge-card/scripts/generate.js
 *
 * Usage:
 *   node generate.js --title "书名" --subtitle "副标题" --badge "标签" \
 *     --concepts '[{"icon":"💡","color":"#3B82F6","bg":"#DBEAFE","title":"概念名","tag":"标签","quote":"金句","desc":"解读"}]' \
 *     --quote "底部金句" --quote-author "作者" \
 *     --theme "blue|green|orange|red|purple" \
 *     --brand "心光年觉醒读书会" \
 *     --vol "Vol.01 · 系列名" \
 *     --output "/path/to/output.png"
 *
 * Prints the output PNG path on success.
 */

const { chromium } = require('/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright');
const path = require('path');
const fs = require('fs');
const os = require('os');

// ── CLI 参数解析 ────────────────────────────────────────────────────────────
function arg(name, def) {
  const idx = process.argv.indexOf('--' + name);
  if (idx !== -1 && process.argv[idx + 1]) return process.argv[idx + 1];
  return def;
}

const THEMES = {
  blue:   { grad: '#3B82F6, #6366F1', accent: '#2563EB', light: '#EFF6FF', border: '#BFDBFE', tag_bg: '#DBEAFE', tag_color: '#1D4ED8' },
  green:  { grad: '#10B981, #059669', accent: '#059669', light: '#F0FDF4', border: '#BBF7D0', tag_bg: '#D1FAE5', tag_color: '#065F46' },
  orange: { grad: '#F59E0B, #EF4444', accent: '#D97706', light: '#FFFBEB', border: '#FDE68A', tag_bg: '#FEF3C7', tag_color: '#92400E' },
  red:    { grad: '#F43F5E, #EC4899', accent: '#E11D48', light: '#FFF1F2', border: '#FECDD3', tag_bg: '#FFE4E6', tag_color: '#9F1239' },
  purple: { grad: '#8B5CF6, #6366F1', accent: '#7C3AED', light: '#F5F3FF', border: '#DDD6FE', tag_bg: '#EDE9FE', tag_color: '#5B21B6' },
  teal:   { grad: '#0EA5E9, #06B6D4', accent: '#0284C7', light: '#F0F9FF', border: '#BAE6FD', tag_bg: '#E0F2FE', tag_color: '#0C4A6E' },
};

const themeName = arg('theme', 'blue');
const t = THEMES[themeName] || THEMES.blue;
const title = arg('title', '知识卡片');
const subtitle = arg('subtitle', '');
const badge = arg('badge', '核心概念');
const quote = arg('quote', '');
const quoteAuthor = arg('quote-author', '');
const brand = arg('brand', '心光年觉醒读书会');
const vol = arg('vol', '知识图解系列');
const outputPath = arg('output', path.join(os.tmpdir(), `knowledge-card-${Date.now()}.png`));
const concepts = JSON.parse(arg('concepts', '[]'));

// ── HTML 模版 ───────────────────────────────────────────────────────────────
function makeHtml() {
  const conceptsHtml = concepts.map((item, i) => `
    <div class="concept-item" style="border-left-color:${item.color || t.accent}">
      <div class="concept-num">${String(i + 1).padStart(2, '0')}</div>
      <div class="concept-icon" style="background:${item.bg || t.tag_bg};color:${item.color || t.accent};font-family:'Noto Serif SC',serif;font-size:18px;font-weight:900;">${String(i + 1).padStart(2, '0')}</div>
      <div class="concept-body">
        <div class="concept-title">
          ${item.title}
          ${item.tag ? `<span class="concept-tag" style="background:${item.bg||t.tag_bg};color:${item.color||t.accent}">${item.tag}</span>` : ''}
        </div>
        ${item.quote ? `<div class="concept-quote">"${item.quote}"</div>` : ''}
        <div class="concept-desc">${item.desc || ''}</div>
      </div>
    </div>
  `).join('');

  return `<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{width:800px;background:#fff;font-family:'Noto Sans SC',sans-serif}
.card{width:800px;padding:52px 48px 44px;background:#fff;position:relative;overflow:hidden}
.top-bar{position:absolute;top:0;left:0;right:0;height:6px;background:linear-gradient(90deg,${t.grad})}
.header{text-align:center;margin-bottom:36px}
.book-label{display:inline-flex;align-items:center;gap:6px;background:${t.light};color:${t.accent};font-size:12px;font-weight:700;padding:5px 16px;border-radius:20px;letter-spacing:3px;margin-bottom:14px;border:1px solid ${t.border}}
.main-title{font-family:'Noto Serif SC',serif;font-size:34px;font-weight:900;color:#1E293B;line-height:1.35;margin-bottom:8px;letter-spacing:2px}
.main-title span{color:${t.accent}}
.sub-ttl{font-size:14px;color:#94A3B8;letter-spacing:3px;font-weight:300}
.hline{width:52px;height:3px;background:linear-gradient(90deg,${t.grad});border-radius:2px;margin:14px auto 0}
.intro{background:${t.light};border:1px solid ${t.border};border-radius:14px;padding:24px 28px;margin-bottom:32px;text-align:center}
.intro-text{font-family:'Noto Serif SC',serif;font-size:16px;color:#334155;line-height:1.85;white-space:pre-line}
.intro-text strong{color:${t.accent}}
.sec-label{display:flex;align-items:center;gap:10px;margin-bottom:18px}
.sec-label-text{font-size:12px;font-weight:700;color:#94A3B8;letter-spacing:4px;white-space:nowrap}
.sec-line{flex:1;height:1px;background:linear-gradient(90deg,#E2E8F0,transparent)}
.concept-list{display:flex;flex-direction:column;gap:16px;margin-bottom:32px}
.concept-item{display:flex;align-items:flex-start;gap:18px;padding:20px 22px 20px 26px;background:#FAFBFF;border:1px solid #EEF2FF;border-radius:14px;position:relative;overflow:hidden;border-left-width:4px;border-left-style:solid}
.concept-num{position:absolute;right:16px;top:12px;font-size:38px;font-weight:900;color:rgba(100,100,200,0.05);font-family:'Noto Serif SC',serif;line-height:1}
.concept-icon{width:50px;height:50px;min-width:50px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px}
.concept-body{flex:1}
.concept-title{font-family:'Noto Serif SC',serif;font-size:18px;font-weight:700;color:#1E293B;margin-bottom:5px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.concept-tag{font-family:'Noto Sans SC',sans-serif;font-size:11px;font-weight:600;padding:2px 9px;border-radius:7px}
.concept-quote{font-size:12.5px;color:#94A3B8;font-style:italic;margin-bottom:7px;line-height:1.6}
.concept-desc{font-size:14.5px;color:#475569;line-height:1.8}
.concept-desc b,.concept-desc strong{font-weight:700;color:${t.accent}}
.bottom-quote{background:linear-gradient(135deg,#1E1B4B,#312E81);border-radius:14px;padding:28px 32px;text-align:center;margin-bottom:28px;position:relative;overflow:hidden}
.bottom-quote::before{content:'❝';position:absolute;top:-10px;left:16px;font-size:90px;color:rgba(255,255,255,0.05);font-family:serif;line-height:1}
.bq-text{font-family:'Noto Serif SC',serif;font-size:18px;color:#F8FAFC;line-height:1.85;letter-spacing:1px;margin-bottom:10px;position:relative}
.bq-author{font-size:12px;color:rgba(255,255,255,0.35);letter-spacing:3px}
.footer{display:flex;align-items:center;justify-content:space-between;padding-top:20px;border-top:1px solid #F1F5F9}
.footer-brand{display:flex;align-items:center;gap:8px}
.footer-dot{width:7px;height:7px;border-radius:50%;background:linear-gradient(135deg,${t.grad})}
.footer-name{font-family:'Noto Serif SC',serif;font-size:15px;font-weight:700;color:#334155;letter-spacing:2px}
.footer-right{text-align:right}
.footer-book{font-size:12px;color:#94A3B8;letter-spacing:1px;margin-bottom:2px}
.footer-series{font-size:10px;color:#CBD5E1;letter-spacing:2px}
</style></head>
<body><div class="card">
<div class="top-bar"></div>
<div class="header">
  <div class="book-label">📖 ${badge}</div>
  <div class="main-title">${title}${subtitle ? `<br><span>${subtitle}</span>` : ''}</div>
  <div class="hline"></div>
</div>
<div class="sec-label"><div class="sec-label-text">核 心 要 素</div><div class="sec-line"></div></div>
<div class="concept-list">${conceptsHtml}</div>
${quote ? `<div class="bottom-quote">
  <div class="bq-text">${quote}</div>
  <div class="bq-author">${quoteAuthor}</div>
</div>` : ''}
<div class="footer">
  <div class="footer-brand"><div class="footer-dot"></div><div class="footer-name">${brand}</div></div>
  <div class="footer-right">
    <div class="footer-book">${title} 知识概念卡片</div>
    <div class="footer-series">${vol}</div>
  </div>
</div>
</div></body></html>`;
}

// ── 截图 ────────────────────────────────────────────────────────────────────
(async () => {
  const html = makeHtml();
  const tmpHtml = path.join(os.tmpdir(), `kc-${Date.now()}.html`);
  fs.writeFileSync(tmpHtml, html, 'utf8');

  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 800, height: 1400 }, deviceScaleFactor: 3 });
  const page = await ctx.newPage();
  await page.goto(`file://${tmpHtml}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1800);
  const el = await page.$('.card');
  await el.screenshot({ path: outputPath, type: 'png' });
  await browser.close();
  fs.unlinkSync(tmpHtml);

  console.log(outputPath);
})().catch(e => { console.error(e); process.exit(1); });
