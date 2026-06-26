/**
 * scrape.js — Playwright 全程浏览器操作 (v7)
 *
 * v7 改进：
 *   - 用 innerHTML + turndown 替代 innerText + 字符串比对，解决内容截断和格式丢失
 *   - 直接定位 Grok 回复 DOM 节点（[aria-label="Grok"] .r-16lk18l），不依赖文本对比
 *   - 自定义 turndown 规则处理 Grok 特有的"block span 标题"和"r-b88u0q 粗体"
 *   - 等待逻辑保留 innerText 长度监控（稳定性检测），内容提取改用 innerHTML
 *   - 如果 DOM 选择器失效，回退到 innerText 方式
 *
 * 用法:
 *   npm run scrape                    # 默认 prompt
 *   npm run scrape -- "自定义 prompt"  # 自定义
 *
 * 退出码: 0=成功, 1=失败, 2=登录失效
 */

const { chromium } = require('playwright');
const TurndownService = require('turndown');
const path = require('path');
const fs = require('fs');

const SESSION_DIR = path.join(__dirname, '..', 'session');
const OUTPUT_DIR = path.join(__dirname, '..', 'output');

// ========== 可变选择器（推特发版后可能需要更新） ==========
// 运行 `npm run inspect` 探查当前 DOM 结构，然后更新此处
const SELECTORS = {
  // 回复内容区的 class（从"重新生成"按钮向上 6 层后，在其中搜索此 class）
  contentClass: 'r-16lk18l',
  // 粗体 span 的 class
  boldClass: 'r-b88u0q',
  // 以下为较稳定的属性选择器（aria-label / data-testid），一般不需修改
  regenerateBtn: '[aria-label="重新生成"]',
  primaryColumn: '[data-testid="primaryColumn"]',
  grokContainer: '[aria-label="Grok"]',
};

const DEFAULT_PROMPT = `What are the top AI hot topics and trending discussions on Twitter/X in the past 24 hours? Search in English. For each topic, provide:
1. A brief summary
2. Why it's trending
3. Source links (tweet URLs or relevant links)

Format the response in Markdown.`;

const args = process.argv.slice(2);

// 解析 --record [可选路径] 和 --size WxH，其余参数作为 prompt
let recordTarget = null;  // null = 不录制；'' = 录制用默认时间戳命名；string = 录制到该路径
let recordSize = { width: 1280, height: 800 };
const cleanArgs = [];
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--record') {
    const next = args[i + 1];
    recordTarget = (next && !next.startsWith('--')) ? (i++, next) : '';
  } else if (args[i] === '--size') {
    const next = args[i + 1];
    if (next && /^\d+x\d+$/i.test(next)) {
      const [w, h] = next.split('x').map(Number);
      recordSize = { width: w, height: h };
      i++;
    } else {
      console.warn(`⚠️  Invalid --size value: ${next}, using default 1280x800`);
    }
  } else {
    cleanArgs.push(args[i]);
  }
}
const PROMPT = cleanArgs[0] || DEFAULT_PROMPT;

/**
 * 创建 Turndown 实例，带自定义规则处理 Grok 特有的 HTML 结构
 *
 * Grok 的 Markdown 渲染特征：
 *   - 标题：<span style="display: block; ... margin-bottom: 0.5em;"> 内嵌套 <span>
 *   - 粗体：包含 class r-b88u0q 的 <span>
 *   - 列表：标准 <ul><li>，但 li 内用 <br> 分隔标题和描述
 *   - 列表中的粗体标题（"标题\n描述"格式）：用 <br> 分隔
 */
function createTurndown() {
  const td = new TurndownService({
    headingStyle: 'atx',
    bulletListMarker: '-',
    codeBlockStyle: 'fenced',
  });

  // 规则1：识别 Grok 的"block span 标题"（display:block + margin-bottom）
  // Grok 有两种标题级别：
  //   一级（整体标题）：只有 margin-bottom: 0.5em，用 ## 渲染
  //   二级（子标题）：margin-top: 1.5em + margin-bottom: 0.5em，用 ### 渲染
  td.addRule('grok-heading', {
    filter: (node) => {
      if (node.nodeName !== 'SPAN') return false;
      const style = node.getAttribute('style') || '';
      return style.includes('display: block') && style.includes('margin-bottom');
    },
    replacement: (content) => {
      const text = content.trim();
      if (!text) return '';
      // 二级标题用 ###（有 margin-top）
      return `\n\n## ${text}\n\n`;
    },
  });

  // 规则2：识别 Grok 的粗体（class 含 r-b88u0q 的 span）
  // 注意：只处理不是标题的粗体 span（标题 span 由 grok-heading 处理）
  td.addRule('grok-bold', {
    filter: (node) => {
      if (node.nodeName !== 'SPAN') return false;
      const cls = node.className || '';
      const style = node.getAttribute('style') || '';
      // 排除标题 span（由 grok-heading 处理）
      if (style.includes('display: block') && style.includes('margin-bottom')) return false;
      // 有 r-b88u0q 且父节点没有 r-b88u0q（避免重复加粗）
      const parentCls = node.parentElement?.className || '';
      return cls.includes(SELECTORS.boldClass) && !parentCls.includes(SELECTORS.boldClass);
    },
    replacement: (content) => {
      const text = content.trim();
      if (!text) return '';
      return `**${text}**`;
    },
  });

  // 规则3：处理 Grok 列表项中的 <br>（粗体标题 + 描述的分隔符）
  // Grok 的列表格式：<li><span class="bold">标题</span><br><span>描述</span></li>
  // turndown 默认会把 <br> 转成两个换行，我们保持一个换行（列表项内换行）
  td.addRule('grok-li-br', {
    filter: 'br',
    replacement: () => '\n  ',
  });

  // 规则4：去掉 emoji 图片（Grok 会把 emoji 渲染成 <img alt="😀">）
  td.addRule('emoji-img', {
    filter: (node) => {
      return node.nodeName === 'IMG' && !!node.getAttribute('alt') &&
        node.src && node.src.includes('twimg.com/emoji');
    },
    replacement: (content, node) => node.getAttribute('alt') || '',
  });

  return td;
}

/**
 * 从页面中提取最后一条 Grok 回复的 innerHTML
 * 选择器策略：
 *   主路径：找到最后一个 [aria-label="Grok"] 容器内的 .r-16lk18l 回复内容 div
 *   备用路径：直接从 primaryColumn 中找包含最多内容的 .r-16lk18l
 */
async function extractReplyHTML(page) {
  return await page.evaluate((sel) => {
    const contentSelector = '.' + sel.contentClass;

    // 主路径：通过重新生成按钮定位最后一条回复
    // 重新生成按钮的祖先第6层是回复大容器，其内含内容区
    const regenerateBtns = document.querySelectorAll(sel.regenerateBtn);
    if (regenerateBtns.length > 0) {
      const lastBtn = regenerateBtns[regenerateBtns.length - 1];
      let el = lastBtn.parentElement;
      for (let i = 0; i < 6; i++) {
        if (!el || el === document.body) break;
        el = el.parentElement;
      }
      if (el) {
        const contentDivs = el.querySelectorAll(contentSelector);
        if (contentDivs.length > 0) {
          const replyContainer = contentDivs[0];
          const firstChild = replyContainer.children[0];
          if (firstChild && (firstChild.innerText || '').length > 10) {
            return { html: firstChild.innerHTML, method: 'regenerate-button' };
          }
          return { html: replyContainer.innerHTML, method: 'regenerate-button-full' };
        }
      }
    }

    // 备用路径1：找 [aria-label="Grok"] div 内的内容区
    const grokDivs = Array.from(document.querySelectorAll(sel.grokContainer))
      .filter(el => el.tagName === 'DIV');
    for (const grokDiv of grokDivs.reverse()) {
      const contentDivs = grokDiv.querySelectorAll(contentSelector);
      if (contentDivs.length > 0) {
        const firstChild = contentDivs[0].children[0];
        if (firstChild && (firstChild.innerText || '').length > 10) {
          return { html: firstChild.innerHTML, method: 'grok-aria-label' };
        }
        return { html: contentDivs[0].innerHTML, method: 'grok-aria-label-full' };
      }
    }

    // 备用路径2：在 primaryColumn 中找内容区，取文字最多的
    const primaryColumn = document.querySelector(sel.primaryColumn);
    if (primaryColumn) {
      const contentDivs = Array.from(primaryColumn.querySelectorAll(contentSelector));
      if (contentDivs.length > 0) {
        const best = contentDivs.reduce((a, b) =>
          (a.innerText || '').length > (b.innerText || '').length ? a : b
        );
        if ((best.innerText || '').length > 50) {
          const firstChild = best.children[0];
          if (firstChild && (firstChild.innerText || '').length > 10) {
            return { html: firstChild.innerHTML, method: 'primaryColumn-best' };
          }
          return { html: best.innerHTML, method: 'primaryColumn-best-full' };
        }
      }
    }

    return { html: null, method: 'none' };
  }, SELECTORS);
}

/**
 * 将 Grok 回复的 HTML 转换为 Markdown
 */
function htmlToMarkdown(html) {
  const td = createTurndown();
  let md = td.turndown(html);

  // 清理多余空行
  md = md.replace(/\n{3,}/g, '\n\n').trim();

  return md;
}

/**
 * 两阶段等待：
 *   Phase 1: 等待新增内容出现（包含搜索/思考阶段，容忍短暂稳定）
 *   Phase 2: 检测到回复内容后，等待页面文字长度稳定
 *
 * v7: 只监控 innerText 长度变化，不再做字符串比对提取内容
 *     内容提取由 extractReplyHTML 在稳定后完成
 */
async function waitForReply(page, beforeLen, {
  pollMs = 3000,
  stableRounds = 5,
  timeoutMs = 240000,
  thinkingTimeoutMs = 90000,
} = {}) {
  const start = Date.now();
  let lastLen = beforeLen;
  let stableCount = 0;
  let phase = 'waiting';
  let thinkingLastGrowth = null;

  const ERROR_SIGNALS = [
    '出错了，请刷新',
    'Something went wrong',
    'Try again',
    'Reconnect',
  ];

  while (Date.now() - start < timeoutMs) {
    try {
      await page.waitForTimeout(pollMs);
    } catch (e) {
      console.log(`📊 ⚠️ Page closed: ${e.message}`);
      return { ok: false, forced: false, error: 'Page closed' };
    }

    let currentText = '';
    try {
      currentText = await page.evaluate(() => document.body.innerText);
    } catch (e) {
      console.log(`📊 ⚠️ Unable to read page content: ${e.message}`);
      return { ok: false, forced: false, error: 'Page closed' };
    }

    const len = currentText.length;
    const elapsed = Math.floor((Date.now() - start) / 1000);

    const errorSignal = ERROR_SIGNALS.find(s => currentText.includes(s));
    if (errorSignal) {
      console.log(`📊 ${elapsed}s — ❌ Error detected: "${errorSignal}", exiting early`);
      return { ok: false, forced: false, error: errorSignal };
    }

    let hasRegenerateBtn = false;
    try {
      hasRegenerateBtn = await page.evaluate(
        (sel) => document.querySelectorAll(sel).length > 0,
        SELECTORS.regenerateBtn
      );
    } catch {}

    if (len > lastLen) {
      stableCount = 0;
      const growth = len - lastLen;

      if (phase === 'waiting') {
        phase = 'thinking';
        thinkingLastGrowth = Date.now();
        console.log(`📊 ${elapsed}s — [thinking] Content started growing (+${growth}, total ${len})`);
      } else if (phase === 'thinking' || phase === 'replying') {
        thinkingLastGrowth = Date.now();
        if (len > beforeLen + 500 || hasRegenerateBtn) {
          if (phase !== 'replying') {
            phase = 'replying';
            console.log(`📊 ${elapsed}s — [replying] ✨ Reply content detected (+${growth}, total ${len})`);
          } else {
            console.log(`📊 ${elapsed}s — [replying] Reply still growing (+${growth}, total ${len})`);
          }
        } else {
          console.log(`📊 ${elapsed}s — [thinking] Content growing (+${growth}, total ${len})`);
        }
      }
    } else {
      stableCount++;

      if (phase === 'thinking' && thinkingLastGrowth && (Date.now() - thinkingLastGrowth) > thinkingTimeoutMs) {
        const stuckSec = Math.floor((Date.now() - thinkingLastGrowth) / 1000);
        console.log(`📊 ${elapsed}s — ❌ thinking phase no growth for ${stuckSec}s, Grok might be stuck`);
        return { ok: false, forced: false, error: 'Thinking timeout' };
      }

      if (phase === 'waiting') {
        console.log(`📊 ${elapsed}s — [waiting] Waiting for reply... (${len})`);
      } else if (phase === 'thinking') {
        // 出现重新生成按钮 → 回复完成
        if (hasRegenerateBtn) {
          phase = 'replying';
          console.log(`📊 ${elapsed}s — [replying] ✨ Regenerate button appeared, reply complete`);
          return { ok: true, forced: false };
        } else if (stableCount >= stableRounds + 3) {
          console.log(`📊 ${elapsed}s — [thinking] Thinking phase stable for ${stableCount} rounds, no substantive content, keep waiting...`);
          if (stableCount >= stableRounds + 8) {
            console.log(`📊 ${elapsed}s — [thinking] Waited too long, forcing content check...`);
            return { ok: true, forced: true };
          }
        } else {
          console.log(`📊 ${elapsed}s — [thinking] Thinking phase stable ${stableCount}/${stableRounds + 3}`);
        }
      } else if (phase === 'replying') {
        console.log(`📊 ${elapsed}s — [replying] Stable ${stableCount}/${stableRounds}`);
        if (stableCount >= stableRounds || hasRegenerateBtn) {
          return { ok: true, forced: false };
        }
      }
    }

    lastLen = len;
  }

  return { ok: false, forced: false, error: 'Timeout' };
}

/**
 * 清理 HTML→Markdown 转换后的文本残留
 * v7: 不再需要复杂的字符串比对清理，只去掉少量已知 Grok UI 残留
 */
function cleanMarkdown(text) {
  // 去掉"已经思考 N 秒"残留
  text = text.replace(/已经思考\s*\d+\s*秒\n?/g, '');
  // 去掉"努力思考\n自动"残留
  text = text.replace(/努力思考\n?自动\n?/g, '');
  // 清理多余空行
  text = text.replace(/\n{3,}/g, '\n\n').trim();
  return text;
}

/**
 * 解析视频输出路径：
 *   - 空字符串 → output/grok-<时间戳>.webm
 *   - 相对路径或纯文件名 → output/<target>
 *   - 绝对路径 → 直接使用
 */
function resolveVideoPath(target) {
  const ts = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
  const filename = target || `grok-${ts}.webm`;
  if (path.isAbsolute(filename)) return filename;
  return path.join(OUTPUT_DIR, filename);
}

// ========== MAIN ==========
(async () => {
  if (!fs.existsSync(SESSION_DIR)) {
    console.error('❌ Session does not exist, please run: npm run login first');
    process.exit(2);
  }
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  console.log('');
  console.log('╔══════════════════════════════════════════╗');
  console.log('║      🐾 Grok Scraper v7 — Starting      ║');
  console.log('╚══════════════════════════════════════════╝');
  console.log('');

  console.log('🐾 Starting browser...');
  if (recordTarget !== null) {
    console.log(`🎬 Record mode enabled — size: ${recordSize.width}x${recordSize.height}, output: ${resolveVideoPath(recordTarget)}`);
  }
  const context = await chromium.launchPersistentContext(SESSION_DIR, {
    headless: recordTarget === null,
    slowMo: recordTarget !== null ? 50 : 0,
    args: ['--disable-blink-features=AutomationControlled', '--no-sandbox'],
    viewport: recordTarget !== null ? recordSize : { width: 1280, height: 900 },
    ...(recordTarget !== null && {
      recordVideo: { dir: OUTPUT_DIR, size: recordSize },
    }),
  });

  const page = context.pages()[0] || await context.newPage();

  console.log('🌐 Opening Grok...');
  await page.goto('https://x.com/i/grok', { waitUntil: 'domcontentloaded', timeout: 30000 });

  try {
    await page.waitForSelector('textarea', { timeout: 30000, state: 'visible' });
  } catch {
    if (page.url().includes('/login') || page.url().includes('/i/flow/login')) {
      console.error('');
      console.error('╔══════════════════════════════════════════╗');
      console.error('║  ❌ FAILED — Login expired               ║');
      console.error('║  Run: npm run login                      ║');
      console.error('╚══════════════════════════════════════════╝');
      await context.close();
      process.exit(2);
    }
    console.error('❌ Page load error, URL:', page.url());
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'error-screenshot.png') });
    await context.close();
    process.exit(1);
  }

  console.log('✅ Page loaded, textarea is ready');

  // 记录发送前的页面文本长度（用于监控增长）
  const beforeLen = await page.evaluate(() => document.body.innerText.length);
  console.log(`📏 Page text before sending: ${beforeLen} chars`);

  // 输入 prompt 并发送
  console.log('📝 Entering prompt...');
  const textarea = page.locator('textarea').first();
  await textarea.click();
  await page.waitForTimeout(500);
  await textarea.fill(PROMPT);
  await page.waitForTimeout(500);

  console.log('📤 Prompt sent, waiting for Grok reply...');
  const startTime = Date.now();
  await page.keyboard.press('Enter');

  // 两阶段等待（只监控长度稳定）
  const result = await waitForReply(page, beforeLen, {
    pollMs: 3000,
    stableRounds: 5,
    timeoutMs: 240000,
  });

  const elapsed = Math.floor((Date.now() - startTime) / 1000);

  // 截图留档
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'final-screenshot.png') });

  // 提取回复 HTML（必须在 context.close() 之前）
  let replyHTML = null;
  let extractMethod = 'none';
  if (result.ok) {
    const extracted = await extractReplyHTML(page);
    replyHTML = extracted.html;
    extractMethod = extracted.method;
    console.log(`🔍 HTML extracted via: ${extractMethod} (${replyHTML ? replyHTML.length : 0} bytes)`);

    // 选择器失效时自动输出调试信息（不中断流程，但保存线索）
    if (!replyHTML || extractMethod === 'none') {
      console.warn('⚠️  DOM 选择器可能已失效，正在收集调试信息...');
      try {
        const debugInfo = await page.evaluate((sel) => {
          return {
            timestamp: new Date().toISOString(),
            url: location.href,
            bodyTextLen: document.body.innerText.length,
            regenerateBtn: document.querySelectorAll(sel.regenerateBtn).length,
            contentClass: document.querySelectorAll('.' + sel.contentClass).length,
            boldClass: document.querySelectorAll('.' + sel.boldClass).length,
            primaryColumn: !!document.querySelector(sel.primaryColumn),
            grokContainer: document.querySelectorAll(sel.grokContainer).length,
            allTestIds: Array.from(new Set(
              Array.from(document.querySelectorAll('[data-testid]'))
                .map(el => el.getAttribute('data-testid'))
            )),
            hint: '请运行 npm run inspect 进行详细探查，然后更新 scrape.js 中的 SELECTORS',
          };
        }, SELECTORS);
        const debugFile = path.join(OUTPUT_DIR, 'debug-dom.json');
        fs.writeFileSync(debugFile, JSON.stringify(debugInfo, null, 2), 'utf-8');
        console.warn(`📄 调试信息已保存: ${debugFile}`);
        console.warn('💡 请运行 npm run inspect 进行详细 DOM 探查');
      } catch (e) {
        console.warn(`⚠️  无法收集调试信息: ${e.message}`);
      }
    }
  }

  // 必须在 context.close() 之前获取视频临时路径，关闭后 page.video() 不可用
  const videoPendingPath = recordTarget !== null ? await page.video()?.path() : null;

  await context.close();

  if (recordTarget !== null) {
    if (videoPendingPath) {
      const destPath = resolveVideoPath(recordTarget);
      fs.mkdirSync(path.dirname(destPath), { recursive: true });
      fs.renameSync(videoPendingPath, destPath);
      console.log(`🎬 Video saved: ${destPath}`);
    } else {
      console.warn('⚠️  Record mode was on but no video file was produced');
    }
  }
  console.log(`🔒 Browser closed (${elapsed}s)`);

  if (!result.ok) {
    const reason = result.error ? `Grok error: ${result.error}` : 'Timeout waiting for reply';
    console.error('');
    console.error('╔══════════════════════════════════════════╗');
    console.error('║  ❌ FAILED                               ║');
    console.error(`║  ${reason.substring(0, 40).padEnd(40)}║`);
    console.error(`║  Elapsed: ${elapsed}s                          ║`);
    console.error('╚══════════════════════════════════════════╝');
    process.exit(result.error && result.error !== 'Page closed' ? 3 : 1);
  }

  // 将 HTML 转换为 Markdown
  let reply = '';
  if (replyHTML) {
    const rawMd = htmlToMarkdown(replyHTML);
    reply = cleanMarkdown(rawMd);
    console.log(`✅ HTML→Markdown conversion done (${reply.length} chars)`);
  }

  if (!reply || reply.length < 50) {
    console.error('');
    console.error('╔══════════════════════════════════════════╗');
    console.error('║  ❌ FAILED — Reply too short              ║');
    console.error(`║  Length: ${reply ? reply.length : 0} chars (min: 50)         ║`);
    console.error(`║  Method: ${extractMethod.padEnd(30)}║`);
    console.error('╚══════════════════════════════════════════╝');
    if (extractMethod === 'none') {
      console.error('');
      console.error('💡 DOM 选择器可能已失效，请执行以下步骤：');
      console.error('   1. npm run inspect          # 探查当前 DOM 结构');
      console.error('   2. 对照输出更新 scrape.js 中的 SELECTORS 常量');
      console.error('   3. 参考 learn/dom-selector-fragility.md 文档');
    }
    fs.writeFileSync(path.join(OUTPUT_DIR, 'debug-reply.html'), replyHTML || 'empty');
    process.exit(1);
  }

  // 保存结果
  const ts = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
  const outFile = path.join(OUTPUT_DIR, `grok-${ts}.md`);
  const output = `# Grok AI Report\n\n_Generated: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}_\n\n---\n\n${reply}`;
  fs.writeFileSync(outFile, output, 'utf-8');
  fs.writeFileSync(path.join(OUTPUT_DIR, 'latest.md'), output, 'utf-8');

  // ========== SUCCESS OUTPUT ==========
  console.log('');
  console.log('╔══════════════════════════════════════════╗');
  console.log('║  ✅ SUCCESS — Grok reply captured!       ║');
  console.log('╠══════════════════════════════════════════╣');
  console.log(`║  📄 File: ${path.basename(outFile).padEnd(29)}║`);
  console.log(`║  📏 Length: ${String(reply.length).padEnd(28)}║`);
  console.log(`║  ⏱️  Time: ${String(elapsed + 's').padEnd(28)}║`);
  console.log(`║  🔍 Method: ${extractMethod.padEnd(27)}║`);
  console.log('╚══════════════════════════════════════════╝');
  console.log('');
  console.log('--- Grok Reply Preview (first 500 chars) ---');
  console.log('');
  console.log(reply.substring(0, 500));
  if (reply.length > 500) console.log('\n... (truncated)');
  console.log('');
  console.log('🐾 Done!');

  process.exit(0);
})();
