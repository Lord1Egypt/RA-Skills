/* NPC 觉醒 · 真机冒烟测试
 *
 * 为什么需要它：Node 的 mock DOM 环境与浏览器不一致——
 * 例如 `function top(){}` 在 Node 里合法，在浏览器里因 window.top 是
 * 不可配置内置属性而抛 SyntaxError（解析期错误，整个 script 不执行，
 * 页面全黑）。mock 测试给了假绿灯。本脚本用真实 Chromium 内核验证。
 *
 *   node scripts/smoke.js [html 路径]
 *   退出码 0 = 通过；非 0 = 失败
 */
const fs = require('fs');
const path = require('path');

// ---------- 定位 playwright 与浏览器 ----------
function loadPlaywright() {
  const cands = [
    process.env.PW_MODULES,
    'C:/Users/yangduo/.workbuddy/binaries/node/workspace/node_modules',
    path.join(process.env.APPDATA || '', 'npm/node_modules'),
  ].filter(Boolean);
  for (const c of cands) {
    const p = path.join(c, 'playwright');
    if (fs.existsSync(p)) return require(p);
  }
  try { return require('playwright'); } catch (e) { return null; }
}
function findChrome() {
  const cands = [
    process.env.CHROME_PATH,
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    '/usr/bin/google-chrome', '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ].filter(Boolean);
  return cands.find(p => fs.existsSync(p)) || null;
}

const HTML = process.argv[2] || path.join(__dirname, '..', 'npc-demo.html');
const TITLE = 'NPC 觉醒 · 真机冒烟';

(async () => {
  if (!fs.existsSync(HTML)) {
    console.log('[FAIL] HTML 不存在:', HTML);
    process.exit(2);
  }
  const pw = loadPlaywright();
  const chrome = findChrome();
  if (!pw || !chrome) {
    console.log('[SKIP] 缺少 playwright 或浏览器，真机冒烟未执行');
    console.log('       playwright:', pw ? '有' : '无', '| 浏览器:', chrome || '无');
    process.exit(0);   // 环境缺失不算失败，但要显式告知
  }

  const { chromium } = pw;
  const browser = await chromium.launch({ executablePath: chrome, headless: true });
  const fails = [];
  const notes = [];

  for (const scheme of ['light', 'dark']) {
    const ctx = await browser.newContext({
      viewport: { width: 720, height: 1000 }, colorScheme: scheme,
    });
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });

    await page.goto('file:///' + HTML.replace(/\\/g, '/'), { waitUntil: 'load' });
    await page.waitForTimeout(300);

    // 断言 1：零脚本错误（SyntaxError 会在这里被抓住）
    if (errs.length) fails.push(`[${scheme}] 脚本错误：` + errs.slice(0, 2).join(' | '));

    // 断言 2：#app 非空
    const len = await page.evaluate(() => {
      const e = document.getElementById('app');
      return e ? e.innerHTML.length : -1;
    });
    if (len <= 0) fails.push(`[${scheme}] #app 为空（长度 ${len}）——页面会全黑`);
    else notes.push(`[${scheme}] 首屏渲染 ${len} 字符`);

    // 断言 3：背景色确实是主题色（浅色不该是深色底）
    const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    const rgb = (bg.match(/\d+/g) || []).map(Number);
    const lum = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
    if (scheme === 'light' && lum < 128) fails.push(`[light] 背景仍是深色 ${bg}（亮度 ${lum.toFixed(0)}）——浅色主题未生效`);
    if (scheme === 'dark' && lum > 128) fails.push(`[dark] 背景是浅色 ${bg}`);
    notes.push(`[${scheme}] 背景 ${bg}`);

    // 断言 4：能完整答完 12 题并出卡
    if (len > 0) {
      await page.click('#go');
      for (let i = 0; i < 12; i++) {
        const opts = await page.$$('.opt');
        if (!opts.length) { fails.push(`[${scheme}] 第 ${i + 1} 题没有选项`); break; }
        await opts[i % opts.length].click();
        await page.waitForTimeout(230);
      }
      const sub = await page.$('#sub');
      if (!sub) fails.push(`[${scheme}] 未到达最后一题，找不到提交按钮`);
      else {
        await sub.click();
        await page.waitForTimeout(450);
      }
      const card = await page.evaluate(() => {
        const t = document.querySelector('.type');
        const c = document.querySelector('.card');
        return {
          type: t ? t.textContent.trim() : null,
          cardLen: c ? c.innerHTML.length : 0,
          quests: document.querySelectorAll('.quest').length,
          axes: document.querySelectorAll('.ax').length,
          coord: (document.querySelector('.coord') || {}).textContent || '',
        };
      });
      if (!card.type) fails.push(`[${scheme}] 出卡失败：无类型`);
      if (card.quests !== 3) fails.push(`[${scheme}] 破局支线应为 3 条，实为 ${card.quests}`);
      if (card.axes !== 7) fails.push(`[${scheme}] 参数面板应为 7 轴，实为 ${card.axes}`);
      if (!/第 \d{4} 号刷新点/.test(card.coord)) fails.push(`[${scheme}] 坐标格式异常：${card.coord}`);
      notes.push(`[${scheme}] 出卡「${card.type}」| 支线 ${card.quests} | 七轴 ${card.axes} | ${card.coord}`);
    }

    // 断言 5：主题切换按钮真的切换
    const before = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    await page.click('#theme');
    await page.waitForTimeout(200);
    const after = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    if (before === after) fails.push(`[${scheme}] 点击主题按钮后背景未变（${before}）`);
    else notes.push(`[${scheme}] 主题切换生效 ${before} → ${after}`);

    await ctx.close();
  }

  await browser.close();

  console.log('=== ' + TITLE + ' ===');
  notes.forEach(n => console.log('  · ' + n));
  if (fails.length) {
    console.log('\n[FAIL] 真机冒烟未通过：');
    fails.forEach(f => console.log('  ✗ ' + f));
    process.exit(1);
  }
  console.log('\n[ok] 真机冒烟通过（浅色/深色双主题 · 零脚本错误 · 出卡完整 · 切换生效）');
  process.exit(0);
})().catch(e => {
  console.log('[FAIL] 冒烟脚本异常：' + e.message);
  process.exit(1);
});
