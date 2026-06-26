/**
 * OKKI 背调数据提取脚本（批量版）
 * 用法：node okki-background.js <目标询盘号>
 * 示例：node okki-background.js 20482071681
 *
 * 以目标询盘号为终止点，对列表页从顶部到目标询盘（含）的所有询盘逐条提取背调数据，
 * 每条保存独立 Markdown 文件，并生成汇总报告。
 *
 * 时间窗口：前一天 15:00 ~ 当前日期 15:00
 */
const { chromium } = require('playwright-core');
const fs = require('fs');

const RELAY_TOKEN = '856baea1afbe169e5eec0f6ecb5b90c77ddeb06b2abe1154';

// 动态计算时间窗口：前一天 15:00 ~ 当前日期 15:00
function getTimeWindow() {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  const start = new Date(yesterday);
  start.setHours(15, 0, 0, 0);

  const end = new Date(today);
  end.setHours(15, 0, 0, 0);

  return { start, end };
}

const TIME_WINDOW = getTimeWindow();

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function isInTimeWindow(chatText) {
  const times = chatText.match(/\d{4}-\d{2}-\d{2} \d{2}:\d{2}/g);
  if (!times || times.length === 0) return { pass: true, earliest: null };
  const earliestStr = times[times.length - 1];
  const inquiryTime = new Date(earliestStr.replace(' ', 'T'));
  return { pass: inquiryTime >= TIME_WINDOW.start && inquiryTime <= TIME_WINDOW.end, earliest: earliestStr };
}

// ── 导航到询盘列表页（带排序+每页100条） ──────────────────────────────────
async function navigateToInquiryPage(page) {
  const INQUIRY_URL = 'https://message.alibaba.com/message/default.htm#feedback/all?order={"order":"desc","orderBy":"gmt_create"}&pageSize=100';
  console.log('导航到询盘列表页...');
  await page.goto(INQUIRY_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await sleep(5000);

  // 点击日期排序
  try {
    const dateBtn = page.locator('a.aui-menu-button[data-role="date-selector"]').first();
    await dateBtn.waitFor({ timeout: 8000 });
    await dateBtn.click();
    await sleep(1500);
    const sortItem = page.locator('span[data-widget-point="menuLabel"]', { hasText: '按创建时间从新到旧' }).first();
    await sortItem.waitFor({ timeout: 8000 });
    await sortItem.click();
    await sleep(3000);
  } catch (e) {
    console.log('  [排序] 跳过排序设置:', e.message);
  }

  // 设置每页100条
  try {
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await sleep(1500);
    const pageSizeBtn = page.locator('a[data-page-size="100"]').first();
    await pageSizeBtn.waitFor({ timeout: 8000 });
    await pageSizeBtn.click();
    await sleep(5000);
  } catch (e) {
    console.log('  [分页] 跳过分页设置:', e.message);
  }

  console.log('询盘页面已加载');
}

// ── 收集询盘列表（目标盘及以上所有询盘，支持多页） ─────────────────────────
async function collectInquiries(page, targetNo) {
  await navigateToInquiryPage(page);

  const maxPages = 5;
  let allItems = [];

  for (let pageNum = 1; pageNum <= maxPages; pageNum++) {
    console.log(`  [分页查找] 正在第 ${pageNum} 页查找询盘 ${targetNo}...`);

    // 等待内容稳定加载
    let lastCount = 0, stableRounds = 0;
    for (let i = 0; i < 30; i++) {
      await page.evaluate(() => window.scrollBy(0, 800));
      await sleep(500);
      const count = await page.evaluate(() => document.querySelectorAll('a[href*="maDetail"]').length);
      if (count === lastCount) { stableRounds++; if (stableRounds >= 3) break; }
      else { stableRounds = 0; lastCount = count; }
    }
    const finalCount = await page.evaluate(() => document.querySelectorAll('a[href*="maDetail"]').length);
    console.log(`  [加载检测] 获取到 ${finalCount} 条询盘`);

    // 提取当前页询盘
    const pageItems = await page.evaluate((targetNo) => {
      const cards = Array.from(document.querySelectorAll('a[href*="maDetail"]'));
      const result = [];
      let foundTarget = false;
      cards.forEach((a) => {
        const m = a.href.match(/imInquiryId=(\d+)/);
        if (!m) return;
        const no = m[1];
        let card = a.closest('[class*="item"]') || a.closest('li') || a.parentElement;
        for (let i = 0; i < 5 && card; i++) {
          if (card.querySelectorAll('a[href*="maDetail"]').length === 1) break;
          card = card.parentElement;
        }
        let customerName = '';
        const chatText = card ? (card.innerText || '') : '';
        if (card) {
          const lines = chatText.split('\n').map(l => l.trim()).filter(Boolean);
          for (const line of lines) {
            if (!/^[A-Za-z]/.test(line) || line.length < 2 || line.length > 60) continue;
            if (/[\u4e00-\u9fa5]/.test(line) || /[：:\d]{3,}/.test(line)) continue;
            if (/Inquiry from|TM|询盘|\?|,/.test(line)) continue;
            if (/\b(you|your|it|let me|wait|welcome|thank|please|checking|update|ok|yes|no|hi|hello)\b/i.test(line)) continue;
            customerName = line; break;
          }
        }
        result.push({ no, href: a.href, customerName, chatText });
        if (no === targetNo) foundTarget = true;
      });
      return { items: result, foundTarget };
    }, targetNo);

    allItems = allItems.concat(pageItems.items);

    if (pageItems.foundTarget) {
      console.log(`  [分页查找] 在第 ${pageNum} 页找到目标询盘`);
      console.log(`  [分页查找] 共收集 ${allItems.length} 个询盘（包含前 ${pageNum} 页）`);
      const targetIdx = allItems.findIndex(item => item.no === targetNo);
      const sliced = targetIdx !== -1 ? allItems.slice(0, targetIdx + 1) : allItems;

      // 时间窗口过滤
      return sliced.filter(item => {
        const check = isInTimeWindow(item.chatText);
        if (!check.pass) console.log(`  [跳过] 询盘 ${item.no}（${item.customerName}）超出时间窗口`);
        return check.pass;
      });
    }

    // 翻下一页
    if (pageNum < maxPages) {
      console.log(`  [分页查找] 跳转到第 ${pageNum + 1} 页...`);
      const nextClicked = await page.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('button, a, [class*="next"], [class*="pagination"]'));
        for (const btn of btns) {
          const text = btn.innerText?.trim();
          if (text === '>' || text === '下一页' || btn.getAttribute('aria-label') === '下一页') { btn.click(); return true; }
        }
        const nextBtn = document.querySelector('[class*="next-btn"]:not([disabled]), [class*="pagination-next"]:not([disabled])');
        if (nextBtn) { nextBtn.click(); return true; }
        return false;
      });
      if (!nextClicked) { console.log('  [分页查找] 无法找到下一页按钮，停止翻页'); break; }
      await sleep(5000);
    }
  }

  throw new Error('未找到目标询盘 ' + targetNo + '（已查找 ' + maxPages + ' 页）');
}

// ── 从当前详情页提取所有背调数据 ──────────────────────────────────────────
async function extractBackground(page) {
  // 先点击「OKKI销售助手」标签，触发面板加载
  const tabClicked = await page.evaluate(() => {
    for (const el of document.querySelectorAll('li.tab-item, [class*="tab-item"]')) {
      if (el.innerText && el.innerText.includes('OKKI')) { el.click(); return true; }
    }
    return false;
  });
  if (tabClicked) await sleep(5000);

  // 若有「发起背调」按钮，点击触发背调生成
  const initTriggered = await page.evaluate(() => {
    for (const el of document.querySelectorAll('*')) {
      if (el.children.length === 0 && el.textContent.trim() === '发起背调') {
        el.click(); return true;
      }
    }
    return false;
  });
  if (initTriggered) { console.log('    点击发起背调，等待生成...'); await sleep(8000); }

  // 客户基础信息
  const customerInfo = await page.evaluate(() => {
    const ext = document.querySelector('.okki-extension');
    if (!ext) return { name: '', country: '', email: '', company: '' };
    let name = '';
    const nameSelectors = [
      '[class*="contact-name"]', '[class*="contactName"]',
      '[class*="buyer-name"]', '[class*="buyerName"]',
      '[class*="customer-name"]', '[class*="customerName"]',
    ];
    for (const sel of nameSelectors) {
      const el = ext.querySelector(sel);
      if (el) { name = el.innerText.trim(); break; }
    }
    if (!name || name === '陌生人') {
      const lines = ext.innerText.split('\n').map(l => l.trim()).filter(Boolean);
      for (const line of lines.slice(0, 10)) {
        if (/^[A-Za-z]/.test(line) && line.length >= 2 && line.length <= 60 &&
            !/[：:\d@]/.test(line) && !/[\u4e00-\u9fa5]/.test(line) &&
            !['OKKI', 'AI', 'UTC'].some(w => line.includes(w))) {
          name = line; break;
        }
      }
    }
    let country = '';
    const flagParent = ext.querySelector('[class*="country"]') ||
                       ext.querySelector('img[src*="flag"]')?.parentElement;
    if (flagParent) country = flagParent.innerText.trim().split('\n')[0];
    let email = '';
    const emailMatch = ext.innerText.match(/[\w.+-]+@[\w.-]+\.\w+/);
    if (emailMatch) email = emailMatch[0];
    let company = '';
    const companyMatch = ext.innerText.match(/公司名称[：:]\s*([^\n]+)/);
    if (companyMatch) company = companyMatch[1].trim();
    return { name, country, email, company };
  });

  // 等待背调分析（最多 60 秒）
  let bgData = { tags: [], analysis: '', summary: '' };
  for (let i = 0; i < 60; i++) {
    const data = await page.evaluate(() => {
      const mdEl = document.querySelector('.background-check-analysis-my-markdown');
      const analysis = mdEl ? mdEl.innerText.trim() : '';
      const tagEls = document.querySelectorAll('.okki-tag');
      const tagSet = new Set();
      const tags = Array.from(tagEls).map(el => el.innerText.trim()).filter(t => {
        if (!t || tagSet.has(t)) return false;
        tagSet.add(t); return true;
      });
      let summary = '';
      for (const el of Array.from(document.querySelectorAll('*'))) {
        if (el.children.length === 0 && el.textContent.trim() === '背调概要') {
          let p = el.parentElement;
          for (let j = 0; j < 5 && p; j++) {
            const sib = p.nextElementSibling;
            if (sib && sib.innerText && sib.innerText.length > 20) { summary = sib.innerText.trim(); break; }
            p = p.parentElement;
          }
          break;
        }
      }
      return { tags, analysis, summary };
    });
    if (data.analysis.length > 30) { bgData = data; break; }
    // 检测无效提示，立即跳出等待
    const invalid = await page.evaluate(() => {
      const t = document.body.innerText || '';
      return t.includes('没有挖掘到联系人或公司信息') ||
             t.includes('背调来源信息无效') ||
             t.includes('背调信息无效');
    });
    if (invalid) { console.log('    检测到背调无效提示，立即跳过'); break; }
    if (i === 59) console.log('    等待背调超时，使用已获取数据');
    await sleep(1000);
  }

  // 点击「查看背调详情」，展开并提取挖掘内容
  // 对新触发的背调，按钮可能延迟出现，最多等待 15 秒
  let emailDigData = '';
  let companyDigData = '';

  // 先检测是否存在"背调信息无效"或"没有挖掘到"的提示
  const hasInvalidMsg = await page.evaluate(() => {
    const pageText = document.body.innerText || '';
    return pageText.includes('没有挖掘到联系人或公司信息') ||
           pageText.includes('背调来源信息无效') ||
           pageText.includes('背调信息无效');
  });

  if (hasInvalidMsg) {
    console.log('    背调信息无效，跳过挖掘详情提取');
    const invalidMsg = '没有挖掘到联系人或公司信息。你可尝试检查背调来源信息（公司名称、邮箱、官网）后重试或者背调信息无效。';
    emailDigData = invalidMsg;
    companyDigData = invalidMsg;
  } else try {
    let clicked = false;
    for (let w = 0; w < 15 && !clicked; w++) {
      clicked = await page.evaluate(() => {
        for (const el of Array.from(document.querySelectorAll('*'))) {
          if (el.children.length === 0 && el.textContent.trim() === '查看背调详情') {
            el.click(); return true;
          }
        }
        return false;
      });
      if (!clicked) await sleep(1000);
    }
    if (!clicked) console.log('    未找到「查看背调详情」按钮');
    if (clicked) {
      await sleep(3000);
      // 展开所有"展开挖掘详情"按钮
      const expandCount = await page.evaluate(() => {
        let count = 0;
        for (const el of Array.from(document.querySelectorAll('*'))) {
          if (el.children.length === 0 && el.textContent.trim() === '展开挖掘详情') {
            el.click(); count++;
          }
        }
        return count;
      });
      if (expandCount > 0) await sleep(2000);

      // 等待展开完成并提取
      for (let i = 0; i < 20; i++) {
        const result = await page.evaluate(() => {
          function slice(txt, startKey, endKey) {
            const s = txt.indexOf(startKey);
            const e = endKey ? txt.indexOf(endKey, s + 1) : -1;
            if (s === -1) return '';
            return (e !== -1 ? txt.slice(s, e) : txt.slice(s)).trim();
          }
          for (const el of Array.from(document.querySelectorAll('*'))) {
            const txt = el.innerText || '';
            if (txt.includes('挖掘邮箱相关信息') && txt.includes('挖掘公司相关信息') &&
                txt.includes('收起挖掘详情') && txt.length > 200) {
              return {
                email: slice(txt, '挖掘邮箱相关信息', '整理联系人画像'),
                company: slice(txt, '挖掘公司相关信息', '整理公司画像'),
              };
            }
          }
          return { email: '', company: '' };
        });
        if (result.company.length > 50 || result.email.length > 20) {
          emailDigData = result.email;
          companyDigData = result.company;
          break;
        }
        await sleep(1000);
      }
    }
  } catch (e) {
    console.log('    获取背调详情失败:', e.message);
  }

  return { customerInfo, bgData, emailDigData, companyDigData };
}

// ── 主流程 ────────────────────────────────────────────────────────────────
async function main() {
  const targetNo = process.argv[2];
  if (!targetNo) {
    console.error('用法: node okki-background.js <目标询盘号>');
    console.error('示例: node okki-background.js 20482071681');
    process.exit(1);
  }

  const browser = await chromium.connectOverCDP('http://127.0.0.1:18800', {
    headers: { 'x-openclaw-relay-token': RELAY_TOKEN }, timeout: 10000,
  });
  console.log('Browser Relay 连接成功');

  const context = browser.contexts()[0];
  let aliPage = context.pages().find(p => p.url().includes('message.alibaba.com'));
  if (!aliPage) aliPage = context.pages()[0];

  const now = new Date();
  const dateStr = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

  // 收集询盘列表
  console.log(`\n收集目标盘 ${targetNo} 及以上所有询盘...`);
  const items = await collectInquiries(aliPage, targetNo);
  if (items.length === 0) {
    console.error('未能收集到询盘列表，请检查目标询盘号或列表页状态');
    await browser.close().catch(() => {});
    process.exit(1);
  }
  console.log(`共找到 ${items.length} 条询盘，开始逐条提取背调...\n`);

  const results = [];

  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    console.log(`[${i + 1}/${items.length}] 询盘 ${item.no}（${item.customerName || '未知客户'}）`);

    try {
      // 跳转到询盘详情
      await aliPage.goto(item.href, { waitUntil: 'domcontentloaded', timeout: 20000 });
      await sleep(3000);

      // 提取背调数据
      const data = await extractBackground(aliPage);
      const name = data.customerInfo.name || item.customerName || '未知';
      console.log(`  客户：${name}  ${data.customerInfo.country}`);
      console.log(`  标签：${data.bgData.tags.join(' | ') || '（无）'}`);
      console.log(`  背调分析：${data.bgData.analysis ? data.bgData.analysis.slice(0, 60) + '...' : '（无）'}`);
      console.log(`  挖掘邮箱：${data.emailDigData ? '已获取' : '无'}  挖掘公司：${data.companyDigData ? '已获取' : '无'}\n`);

      results.push({ no: item.no, name, data });
    } catch (e) {
      console.log(`  [错误] 跳过该询盘：${e.message}\n`);
      results.push({
        no: item.no,
        name: item.customerName || '未知',
        data: { customerInfo: { name: item.customerName || '', country: '', email: '', company: '' },
                bgData: { tags: [], analysis: '', summary: '' },
                emailDigData: '', companyDigData: '' }
      });
    }
  }

  // 生成汇总报告（表格格式 + CSV 导出）
  const summaryFile = `okki-reports/okki-report-${targetNo}-${dateStr.replace(/-/g, '-')}.md`;
  const csvFile = `okki-reports/okki-report-${targetNo}-${dateStr.replace(/-/g, '-')}.csv`;

  // 确保 okki-reports 目录存在
  if (!fs.existsSync('okki-reports')) {
    fs.mkdirSync('okki-reports', { recursive: true });
  }

  // 统计有效背调数量
  const validCount = results.filter(r => r.data.bgData.tags.length > 0 || r.data.bgData.analysis).length;

  let summary = `# OKKI 批量背调报告\n\n`;
  summary += `- **目标询盘**：${targetNo}\n`;
  summary += `- **生成日期**：${dateStr}\n`;
  summary += `- **共处理**：${results.length} 条\n`;
  summary += `- **有效背调**：${validCount} 条\n\n`;
  summary += `---\n\n`;

  // 汇总表格
  summary += `## 背调汇总表\n\n`;
  summary += `| 询盘单号 | 客户名称 | 国家 | 公司 | 标签 | 背调分析 |\n`;
  summary += `|----------|----------|------|------|------|----------|\n`;

  for (const r of results) {
    const { customerInfo, bgData } = r.data;
    const tags = bgData.tags.join(' · ') || '--';
    const analysisPreview = bgData.analysis ? bgData.analysis.slice(0, 50) + '...' : '--';
    // 转义表格中的特殊字符
    const escapeTable = (str) => (str || '--').replace(/\|/g, '\\|').replace(/\n/g, ' ');
    summary += `| ${r.no} | ${escapeTable(r.name)} | ${escapeTable(customerInfo.country)} | ${escapeTable(customerInfo.company)} | ${escapeTable(tags)} | ${escapeTable(analysisPreview)} |\n`;
  }

  summary += `\n---\n\n`;
  summary += `## 详细背调内容\n\n`;

  // 详细内容
  for (const r of results) {
    const { customerInfo, bgData, emailDigData, companyDigData } = r.data;
    // 只输出有效背调的详细内容
    if (bgData.tags.length === 0 && !bgData.analysis && !emailDigData && !companyDigData) continue;

    summary += `### ${r.name}（${r.no}）\n\n`;
    summary += `- **国家**：${customerInfo.country || '--'}\n`;
    if (customerInfo.company) summary += `- **公司**：${customerInfo.company}\n`;
    if (customerInfo.email) summary += `- **邮箱**：${customerInfo.email}\n`;
    summary += `- **标签**：${bgData.tags.join(' · ') || '无'}\n\n`;
    if (bgData.analysis) {
      summary += `**背调分析**：${bgData.analysis}\n\n`;
    }
    if (emailDigData && emailDigData.length > 50) {
      summary += `**挖掘邮箱信息**：\n${emailDigData.slice(0, 500)}\n\n`;
    }
    if (companyDigData && companyDigData.length > 50) {
      summary += `**挖掘公司信息**：\n${companyDigData.slice(0, 500)}\n\n`;
    }
    summary += `---\n\n`;
  }

  fs.writeFileSync(summaryFile, summary);

  // 生成 CSV
  let csv = '询盘单号,客户名称,国家,公司,邮箱,标签,背调分析\n';
  const escapeCsv = (str) => {
    if (!str) return '';
    str = String(str);
    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
      return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
  };

  for (const r of results) {
    const { customerInfo, bgData } = r.data;
    csv += `${r.no},${escapeCsv(r.name)},${escapeCsv(customerInfo.country)},${escapeCsv(customerInfo.company)},${escapeCsv(customerInfo.email)},${escapeCsv(bgData.tags.join(' | '))},${escapeCsv(bgData.analysis)}\n`;
  }
  fs.writeFileSync(csvFile, csv);

  console.log(`\n========== 批量背调完成 ==========`);
  console.log(`处理询盘：${results.length} 条`);
  console.log(`有效背调：${validCount} 条`);
  console.log(`报告文件：${summaryFile}`);
  console.log(`CSV 文件：${csvFile}`);

  await browser.close().catch(() => {});
}

main().catch(e => console.error('Fatal:', e.message));
