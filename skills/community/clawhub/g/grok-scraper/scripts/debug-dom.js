/**
 * debug-dom.js — 发一条简单消息，等回复出来后 dump DOM 结构
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SESSION_DIR = path.join(__dirname, '..', 'session');
const OUTPUT_DIR = path.join(__dirname, '..', 'output');

(async () => {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const context = await chromium.launchPersistentContext(SESSION_DIR, {
    headless: true,
    args: ['--disable-blink-features=AutomationControlled', '--no-sandbox'],
    viewport: { width: 1280, height: 900 },
  });

  const page = context.pages()[0] || await context.newPage();

  console.log('🌐 Opening Grok...');
  await page.goto('https://x.com/i/grok', {
    waitUntil: 'domcontentloaded',
    timeout: 30000,
  });

  await page.waitForSelector('textarea', { timeout: 30000, state: 'visible' });
  console.log('✅ Page loaded');

  // 发一条简单消息
  const textarea = page.locator('textarea').first();
  await textarea.click();
  await page.waitForTimeout(500);
  await textarea.fill('What is 2+2? Answer in one sentence.');
  await page.waitForTimeout(500);
  await page.keyboard.press('Enter');
  console.log('📤 Test message sent');

  // 等待回复（简单问题应该很快）
  console.log('⏳ Waiting for reply...');
  await page.waitForTimeout(15000);

  await page.screenshot({ path: path.join(OUTPUT_DIR, 'debug-reply.png') });

  // Dump DOM 结构（只要带文本的元素）
  const domInfo = await page.evaluate(() => {
    function getSelector(el) {
      const tag = el.tagName.toLowerCase();
      const id = el.id ? `#${el.id}` : '';
      const cls = el.className && typeof el.className === 'string'
        ? '.' + el.className.split(/\s+/).filter(c => c).slice(0, 3).join('.')
        : '';
      const testId = el.getAttribute('data-testid') ? `[data-testid="${el.getAttribute('data-testid')}"]` : '';
      const role = el.getAttribute('role') ? `[role="${el.getAttribute('role')}"]` : '';
      return `${tag}${id}${cls}${testId}${role}`;
    }

    // 找到所有包含文本的 div，按文本长度排序
    const results = [];
    const allDivs = document.querySelectorAll('div, article, section, p, span, li');
    for (const el of allDivs) {
      // 只看直接文本内容较多的元素
      const directText = Array.from(el.childNodes)
        .filter(n => n.nodeType === 3)
        .map(n => n.textContent.trim())
        .join('');
      const innerText = el.innerText || '';

      if (innerText.length > 20 && innerText.length < 5000) {
        results.push({
          selector: getSelector(el),
          parentSelector: el.parentElement ? getSelector(el.parentElement) : null,
          textLength: innerText.length,
          directTextLength: directText.length,
          preview: innerText.substring(0, 150),
          childCount: el.children.length,
          depth: (() => {
            let d = 0; let p = el;
            while (p.parentElement) { d++; p = p.parentElement; }
            return d;
          })(),
        });
      }
    }

    // 按 textLength 降序，取前 30
    results.sort((a, b) => b.textLength - a.textLength);
    return results.slice(0, 30);
  });

  console.log('\n📊 DOM elements (sorted by text length):\n');
  for (const item of domInfo) {
    console.log(`[${item.textLength} chars] ${item.selector}`);
    console.log(`  parent: ${item.parentSelector}`);
    console.log(`  depth: ${item.depth}, children: ${item.childCount}`);
    console.log(`  preview: ${item.preview.substring(0, 100)}`);
    console.log('');
  }

  // 额外：dump 聊天区域的 HTML 结构
  const chatHTML = await page.evaluate(() => {
    // 找包含 "2+2" 和回复的区域
    const body = document.body.innerText;
    const has2plus2 = body.includes('2+2');
    
    // 找主内容区域
    const main = document.querySelector('main') || document.querySelector('[role="main"]');
    if (main) {
      // 简化 HTML：只保留结构
      function simplify(el, depth = 0) {
        if (depth > 8) return '';
        const tag = el.tagName?.toLowerCase();
        if (!tag) return '';
        const cls = el.className && typeof el.className === 'string'
          ? ` class="${el.className.split(/\s+/).slice(0, 2).join(' ')}"` : '';
        const testId = el.getAttribute?.('data-testid') ? ` data-testid="${el.getAttribute('data-testid')}"` : '';
        const text = el.childNodes.length === 1 && el.childNodes[0].nodeType === 3
          ? el.textContent.substring(0, 50) : '';
        const indent = '  '.repeat(depth);
        let result = `${indent}<${tag}${cls}${testId}>${text ? text : ''}\n`;
        for (const child of el.children) {
          result += simplify(child, depth + 1);
        }
        return result;
      }
      return simplify(main).substring(0, 10000);
    }
    return 'NO MAIN FOUND. Body text includes 2+2: ' + has2plus2;
  });

  fs.writeFileSync(path.join(OUTPUT_DIR, 'debug-dom.txt'), chatHTML, 'utf-8');
  console.log('\n📁 Full DOM structure saved to output/debug-dom.txt');

  await context.close();
  console.log('🔒 Done');
})();
