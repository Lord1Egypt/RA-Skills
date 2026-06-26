/**
 * inspect-dom.js — Grok 页面 DOM 结构探查工具
 *
 * 当 scrape.js 的 CSS 选择器因推特发版而失效时，用此脚本探查当前页面的
 * 实际 DOM 结构，找到新的选择器，再更新 scrape.js 中的 SELECTORS 常量。
 *
 * 用法:
 *   npm run inspect               # 用默认 prompt
 *   npm run inspect -- "你好"     # 用自定义 prompt
 *
 * 输出:
 *   - 终端打印关键 DOM 信息（testId、aria-label、回复祖先链等）
 *   - output/inspect-reply.html   回复容器的完整 HTML（供离线分析）
 *   - output/inspect-dom.json     结构化 DOM 信息（供脚本比对）
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SESSION_DIR = path.join(__dirname, '..', 'session');
const OUTPUT_DIR = path.join(__dirname, '..', 'output');

const DEFAULT_PROMPT = '用 Markdown 格式（含标题、粗体和列表）介绍 Python 语言的3个优点，简短回答。';
const PROMPT = process.argv[2] || DEFAULT_PROMPT;

(async () => {
  if (!fs.existsSync(SESSION_DIR)) {
    console.error('❌ 请先运行 npm run login');
    process.exit(2);
  }
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  console.log('🔍 Grok DOM Inspector');
  console.log(`📝 Prompt: ${PROMPT.substring(0, 60)}...`);
  console.log('');

  const context = await chromium.launchPersistentContext(SESSION_DIR, {
    headless: false,
    args: ['--disable-blink-features=AutomationControlled', '--no-sandbox'],
    viewport: { width: 1280, height: 900 },
  });

  const page = context.pages()[0] || await context.newPage();
  await page.goto('https://x.com/i/grok', { waitUntil: 'domcontentloaded', timeout: 30000 });

  try {
    await page.waitForSelector('textarea', { timeout: 30000, state: 'visible' });
  } catch {
    console.error('❌ 页面加载失败或需要登录，URL:', page.url());
    await context.close();
    process.exit(1);
  }

  console.log('✅ 页面加载完成');

  const textarea = page.locator('textarea').first();
  await textarea.click();
  await page.waitForTimeout(500);
  await textarea.fill(PROMPT);
  await page.waitForTimeout(500);
  await page.keyboard.press('Enter');

  console.log('⏳ 等待 Grok 回复...');

  // 轮询等待"重新生成"按钮出现（最多 120s）
  for (let i = 0; i < 40; i++) {
    await page.waitForTimeout(3000);
    const hasBtn = await page.evaluate(() =>
      document.querySelectorAll('[aria-label="重新生成"], [aria-label="Regenerate"]').length > 0
    );
    const elapsed = (i + 1) * 3;
    if (hasBtn) {
      console.log(`✅ 回复完成 (${elapsed}s)`);
      break;
    }
    if (i === 39) {
      console.log(`⚠️  120s 未检测到重新生成按钮，继续分析当前页面`);
    }
  }

  await page.waitForTimeout(2000);

  // ========== 探查 DOM 结构 ==========
  const domInfo = await page.evaluate(() => {
    const info = {};

    // 1. 所有 data-testid
    info.testIds = Array.from(new Set(
      Array.from(document.querySelectorAll('[data-testid]'))
        .map(el => el.getAttribute('data-testid'))
    ));

    // 2. 所有 aria-label（去重、只取有意义的）
    info.ariaLabels = Array.from(new Set(
      Array.from(document.querySelectorAll('[aria-label]'))
        .map(el => el.getAttribute('aria-label'))
        .filter(l => l && l.length < 50)
    ));

    // 3. 从"重新生成"按钮向上遍历祖先链
    const regenBtns = document.querySelectorAll('[aria-label="重新生成"], [aria-label="Regenerate"]');
    info.regenerateButtonFound = regenBtns.length > 0;
    info.regenerateAncestors = [];

    if (regenBtns.length > 0) {
      const btn = regenBtns[regenBtns.length - 1];
      let el = btn.parentElement;
      for (let depth = 0; depth < 12 && el && el !== document.body; depth++) {
        info.regenerateAncestors.push({
          depth,
          tag: el.tagName,
          testId: el.getAttribute('data-testid'),
          ariaLabel: el.getAttribute('aria-label'),
          className: el.className.substring(0, 120),
          textLen: (el.innerText || '').length,
          childCount: el.children.length,
        });
        el = el.parentElement;
      }
    }

    // 4. 找回复文字的 DOM 位置（从 text node 向上溯源）
    info.replyTextAncestors = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let textNode;
    let longestMatch = null;
    while ((textNode = walker.nextNode())) {
      const t = textNode.textContent.trim();
      if (t.length > 30 && t.length < 500 && !t.includes('查看键盘') && !t.includes('搜索')) {
        if (!longestMatch || t.length > longestMatch.textContent.trim().length) {
          longestMatch = textNode;
        }
      }
    }
    if (longestMatch) {
      let el = longestMatch.parentElement;
      for (let depth = 0; depth < 15 && el && el !== document.body; depth++) {
        info.replyTextAncestors.push({
          depth,
          tag: el.tagName,
          testId: el.getAttribute('data-testid'),
          ariaLabel: el.getAttribute('aria-label'),
          className: el.className.substring(0, 120),
          textLen: (el.innerText || '').length,
          childCount: el.children.length,
        });
        el = el.parentElement;
      }
    }

    // 5. Markdown 格式元素（标题 span、粗体 span、列表等）
    const primaryColumn = document.querySelector('[data-testid="primaryColumn"]') || document.body;

    const blockSpans = Array.from(primaryColumn.querySelectorAll('span'))
      .filter(s => {
        const style = s.getAttribute('style') || '';
        return style.includes('display: block') && style.includes('margin-bottom');
      });
    info.headingSpans = blockSpans.map(s => ({
      text: s.innerText.substring(0, 80),
      style: s.getAttribute('style'),
      className: s.className.substring(0, 100),
    }));

    const boldClasses = new Set();
    Array.from(primaryColumn.querySelectorAll('span'))
      .filter(s => {
        const style = window.getComputedStyle(s);
        return style.fontWeight === '700' || style.fontWeight === 'bold';
      })
      .forEach(s => {
        (s.className || '').split(/\s+/).forEach(c => {
          if (c.startsWith('r-') && c !== 'r-bcqeeo' && c !== 'r-1ttztb7' && c !== 'r-qvutc0' && c !== 'r-poiln3') {
            boldClasses.add(c);
          }
        });
      });
    info.boldClasses = Array.from(boldClasses);

    info.lists = {
      ul: primaryColumn.querySelectorAll('ul').length,
      ol: primaryColumn.querySelectorAll('ol').length,
      li: primaryColumn.querySelectorAll('li').length,
    };

    // 6. 从重新生成按钮找到回复容器和内容区的 class
    info.contentContainerClasses = [];
    if (regenBtns.length > 0) {
      const btn = regenBtns[regenBtns.length - 1];
      let el = btn.parentElement;
      for (let i = 0; i < 6; i++) {
        if (!el || el === document.body) break;
        el = el.parentElement;
      }
      if (el) {
        Array.from(el.children).forEach((child, idx) => {
          const classes = (child.className || '').split(/\s+/).filter(c => c.startsWith('r-'));
          info.contentContainerClasses.push({
            childIdx: idx,
            tag: child.tagName,
            classes,
            textLen: (child.innerText || '').length,
            textPreview: (child.innerText || '').substring(0, 80),
          });
        });
      }
    }

    // 7. 提取回复容器的完整 HTML（用于离线分析）
    info.replyHTML = null;
    if (regenBtns.length > 0) {
      const btn = regenBtns[regenBtns.length - 1];
      let el = btn.parentElement;
      for (let i = 0; i < 6; i++) {
        if (!el || el === document.body) break;
        el = el.parentElement;
      }
      if (el) {
        // 找内容区（遍历 el 的所有子孙找文字最多的 div）
        const allDivs = Array.from(el.querySelectorAll('div'));
        const contentDiv = allDivs
          .filter(d => {
            const text = d.innerText || '';
            return text.length > 30 && text.length < (el.innerText || '').length * 0.9;
          })
          .sort((a, b) => (b.innerText || '').length - (a.innerText || '').length)[0];

        if (contentDiv) {
          info.replyHTML = contentDiv.innerHTML;
          info.replyContainerClass = contentDiv.className;
          info.replyContainerTextLen = (contentDiv.innerText || '').length;
        }
      }
    }

    return info;
  });

  // ========== 输出结果 ==========
  console.log('');
  console.log('══════════════════════════════════════════════');
  console.log('  data-testid 列表');
  console.log('══════════════════════════════════════════════');
  domInfo.testIds.forEach(id => console.log(`  • ${id}`));

  console.log('');
  console.log('══════════════════════════════════════════════');
  console.log('  aria-label 列表');
  console.log('══════════════════════════════════════════════');
  domInfo.ariaLabels.forEach(l => console.log(`  • ${l}`));

  console.log('');
  console.log('══════════════════════════════════════════════');
  console.log('  "重新生成"按钮 → 祖先链');
  console.log('══════════════════════════════════════════════');
  if (domInfo.regenerateButtonFound) {
    domInfo.regenerateAncestors.forEach(a => {
      console.log(`  [${a.depth}] <${a.tag}> testId="${a.testId}" ariaLabel="${a.ariaLabel}" textLen=${a.textLen} children=${a.childCount}`);
      console.log(`       class: ${a.className}`);
    });
  } else {
    console.log('  ❌ 未找到重新生成按钮');
  }

  console.log('');
  console.log('══════════════════════════════════════════════');
  console.log('  回复正文 → 祖先链');
  console.log('══════════════════════════════════════════════');
  domInfo.replyTextAncestors.forEach(a => {
    console.log(`  [${a.depth}] <${a.tag}> testId="${a.testId}" ariaLabel="${a.ariaLabel}" textLen=${a.textLen} children=${a.childCount}`);
    console.log(`       class: ${a.className}`);
  });

  console.log('');
  console.log('══════════════════════════════════════════════');
  console.log('  Markdown 格式元素');
  console.log('══════════════════════════════════════════════');
  console.log(`  标题 span (display:block + margin-bottom): ${domInfo.headingSpans.length} 个`);
  domInfo.headingSpans.forEach((h, i) => {
    console.log(`    [${i}] "${h.text}"`);
    console.log(`         style: ${h.style}`);
    console.log(`         class: ${h.className}`);
  });
  console.log(`  粗体 class (font-weight:700): [${domInfo.boldClasses.join(', ')}]`);
  console.log(`  列表: ${domInfo.lists.ul} <ul>, ${domInfo.lists.ol} <ol>, ${domInfo.lists.li} <li>`);

  console.log('');
  console.log('══════════════════════════════════════════════');
  console.log('  回复容器子元素');
  console.log('══════════════════════════════════════════════');
  domInfo.contentContainerClasses.forEach(c => {
    console.log(`  [${c.childIdx}] <${c.tag}> classes=[${c.classes.join(', ')}] textLen=${c.textLen}`);
    console.log(`       text: ${c.textPreview}`);
  });

  // 保存文件
  if (domInfo.replyHTML) {
    const htmlFile = path.join(OUTPUT_DIR, 'inspect-reply.html');
    fs.writeFileSync(htmlFile, domInfo.replyHTML, 'utf-8');
    console.log(`\n📄 回复 HTML 已保存: ${htmlFile} (${domInfo.replyHTML.length} bytes)`);
    console.log(`   容器 class: ${domInfo.replyContainerClass}`);
  }

  const jsonFile = path.join(OUTPUT_DIR, 'inspect-dom.json');
  const jsonData = { ...domInfo };
  delete jsonData.replyHTML;
  fs.writeFileSync(jsonFile, JSON.stringify(jsonData, null, 2), 'utf-8');
  console.log(`📄 DOM 信息已保存: ${jsonFile}`);

  // 当前 scrape.js 用到的选择器验证
  console.log('');
  console.log('══════════════════════════════════════════════');
  console.log('  当前 scrape.js 选择器兼容性检查');
  console.log('══════════════════════════════════════════════');

  const checks = await page.evaluate(() => {
    return {
      regenerateBtn: document.querySelectorAll('[aria-label="重新生成"]').length,
      primaryColumn: !!document.querySelector('[data-testid="primaryColumn"]'),
      contentClass: document.querySelectorAll('.r-16lk18l').length,
      boldClass: document.querySelectorAll('.r-b88u0q').length,
      grokAriaLabel: document.querySelectorAll('[aria-label="Grok"]').length,
    };
  });

  const status = (ok) => ok ? '✅' : '❌';
  console.log(`  ${status(checks.regenerateBtn)} [aria-label="重新生成"]  (${checks.regenerateBtn} 个)`);
  console.log(`  ${status(checks.primaryColumn)} [data-testid="primaryColumn"]`);
  console.log(`  ${status(checks.contentClass)} .r-16lk18l  (${checks.contentClass} 个)`);
  console.log(`  ${status(checks.boldClass)} .r-b88u0q  (${checks.boldClass} 个)`);
  console.log(`  ${status(checks.grokAriaLabel)} [aria-label="Grok"]  (${checks.grokAriaLabel} 个)`);

  const allOk = checks.regenerateBtn > 0 && checks.primaryColumn && checks.contentClass > 0;
  console.log('');
  if (allOk) {
    console.log('  ✅ 所有关键选择器均有效，scrape.js 应能正常工作');
  } else {
    console.log('  ⚠️  部分选择器已失效，需要更新 scrape.js 中的 SELECTORS 常量');
    console.log('  请参考上方祖先链和格式元素信息，找到新的 class 后更新代码');
  }

  console.log('');
  await context.close();
})();
