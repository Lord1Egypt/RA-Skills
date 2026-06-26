/**
 * 猎聘全流程 v3 - 含翻页/去重/自动沟通/进度恢复
 * 
 * 根据 Excel 画像配置搜索 -> 匹配评分 -> 截图 -> 写入候选人库
 * 匹配 >= 55%: 自动点击"立即沟通" -> 选职位 -> 确定 -> 发送消息
 * 滚动加载下一页 -> 继续处理直到达到目标数量
 * 记录断点，支持断点续跑
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'url';
import XLSX from 'xlsx';
import iconv from 'iconv-lite';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = path.resolve(__dirname, '..');
const sleep = ms => new Promise(r => setTimeout(r, ms));

// 急停信号
const KILL_SIGNAL = path.join('C:\\Users', process.env.USERNAME || '10362974', 'Desktop', '.kill-signal');
function checkKill() { return fs.existsSync(KILL_SIGNAL); }
function clearKill() { try { fs.rmSync(KILL_SIGNAL, { recursive: true, force: true }); } catch {} }

// 起始页码（支持续跑：从进度文件中读取上次进度）
const PROGRESS_FILE = path.join(WORKSPACE, 'liepin-progress.json');
let START_PAGE = 1;
let EXISTING_RECORDS = [];
let EXISTING_NAMES = new Set();
try {
  const prev = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8'));
  if (prev.lastPage && prev.lastPage > 1) {
    START_PAGE = prev.lastPage;
    console.log('[续跑] 从第', START_PAGE, '页继续');
  }
  if (prev.seenNames && prev.seenNames.length > 0) {
    EXISTING_NAMES = new Set(prev.seenNames);
    console.log('[续跑] 已有', EXISTING_NAMES.size, '条去重指纹');
  }
  if (prev.records && prev.records.length > 0) {
    EXISTING_RECORDS = prev.records;
    console.log('[续跑] 已有', EXISTING_RECORDS.length, '条记录');
  }
} catch {}

// Excel 配置读取
const TARGET_COUNT = 50;
const EXCEL_PATH = 'C:\\Users\\10362974\\Desktop\\简历AI搜寻功能设计模板_V1.0.xlsx';

function readConfig() {
  if (!fs.existsSync(EXCEL_PATH)) throw new Error('Excel not found');
  const wb = XLSX.readFile(EXCEL_PATH);
  const ws = wb.Sheets['候选人画像配置'];
  const data = XLSX.utils.sheet_to_json(ws, { header: 1, defval: '' });
  const config = { skills: [], schools: [], companies: [], filters: {} };
  let section = '';
  for (const row of data) {
    const cell = (row[1] || '').trim();
    if (!cell) continue;
    if (cell.includes('画像配置') || cell.includes('说明')) continue;
    if (cell.includes('关键技能配置')) { section = 'skills'; continue; }
    if (cell.includes('目标院校配置')) { section = 'schools'; continue; }
    if (cell.includes('目标公司配置')) { section = 'companies'; continue; }
    if (cell.includes('其他筛选条件')) { section = 'filters'; continue; }
    if (['技能名称','院校名称','公司名称','条件名称','条件值'].includes(cell)) continue;
    if (section === 'skills') config.skills.push({ name: row[1], category: row[2]||'', weight: parseInt(row[3])||5, required: row[4]||'可选', proficiency: row[5]||'' });
    else if (section === 'schools') config.schools.push({ name: row[1], level: row[2], priority: row[3], major: row[4], edu: row[5] });
    else if (section === 'companies') config.companies.push({ name: row[1], type: row[2], priority: row[3], position: row[4], experience: row[5] });
    else if (section === 'filters') config.filters[row[1]] = row[2];
  }
  return config;
}

// 匹配度评分（支持逗号分隔的多技能）
function calcMatchScore(text, config) {
  let score = 0, maxScore = 0, details = [];
  const tl = text.toLowerCase();
  for (const sk of config.skills) {
    maxScore += sk.weight;
    const subs = sk.name.split(',').map(s => s.trim().toLowerCase()).filter(s => s);
    const matched = subs.some(sub => tl.includes(sub));
    if (matched) { score += sk.weight; details.push('[OK] ' + sk.name); }
    else if (sk.required === '必选') return { score: 0, maxScore, ratio: 0, passed: false, reason: 'Missing: ' + sk.name };
    else details.push('[-] ' + sk.name);
  }
  for (const sc of config.schools) { if (text.includes(sc.name)) { score += 5; maxScore += 5; } }
  const ratio = maxScore > 0 ? score / maxScore : 0;
  return { score, maxScore, ratio: Math.round(ratio * 100), passed: ratio >= 0.3 };
}

const STEALTH = () => {
  Object.defineProperty(navigator, 'webdriver', { get: () => false });
  Object.defineProperty(navigator, 'plugins', { get: () => [{ name: 'Chrome PDF Plugin' }, { name: 'Chrome PDF Viewer' }] });
  Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] });
};

async function detectCaptcha(page) {
  const t = await page.evaluate(() => document.body?.innerText || '').catch(() => '');
  return ['安全验证','验证码','captcha','账号行为异常'].some(k => t.includes(k));
}

async function waitCaptcha(page) {
  console.log('\n[!] CAPTCHA!');
  let n = 0;
  while (n < 600) {
    await sleep(5000); n += 5;
    if (!(await detectCaptcha(page))) { console.log('[OK]\n'); await sleep(2000); return; }
    if (n % 30 === 0) console.log(' wait ' + n + 's');
  }
  throw new Error('Timeout');
}

// 截图简历
async function captureResume(page, shotPath, txtPath) {
  const info = await page.evaluate(() => {
    for (const sel of ['.resume-detail-content-body', '[class*="resume-detail-content-body"]']) {
      const el = document.querySelector(sel);
      if (el) {
        const r = el.getBoundingClientRect();
        if (r.width > 400) return { sel, text: el.innerText||'', x: r.x, y: r.y, w: r.width, h: r.height, scrollH: el.scrollHeight, clientH: el.clientHeight };
      }
    }
    return null;
  });
  if (!info) return { text: '', shot: false };
  fs.writeFileSync(txtPath, info.text, 'utf8');
  if (info.scrollH > info.clientH) {
    for (let s = 1; s <= Math.ceil(info.scrollH / info.clientH) + 2; s++) {
      await page.evaluate((o) => { const el = document.querySelector(o.sel); if (el) el.scrollTop = o.p; }, { sel: info.sel, p: Math.min(s * info.clientH * 0.8, info.scrollH) });
      await sleep(300);
    }
    await page.evaluate((sel) => { const el = document.querySelector(sel); if (el) el.scrollTop = el.scrollHeight; }, info.sel);
    await sleep(500);
  }
  const final = await page.evaluate((sel) => { const el = document.querySelector(sel); return el ? { scrollH: el.scrollHeight } : null; }, info.sel);
  await page.setViewportSize({ width: 1400, height: Math.max(info.y + (final?.scrollH||0) + 100, 900) });
  await sleep(300);
  // 重置滚动到顶部，确保头部信息在截图可见区域内
  await page.evaluate((sel) => { const el = document.querySelector(sel); if (el) el.scrollTop = 0; }, info.sel);
  await sleep(200);
  const pos = await page.evaluate((sel) => { const el = document.querySelector(sel); if (!el) return null; const r = el.getBoundingClientRect(); return r; }, info.sel);
  await page.screenshot({ path: shotPath, clip: { x: pos?.x||0, y: pos?.y||0, width: pos?.w||1008, height: Math.min(final?.scrollH||5000, 5000) } });
  await page.setViewportSize({ width: 1400, height: 900 });
  return { text: info.text, shot: true };
}

// ===== 立即沟通流程（鼠标模拟版）=====
async function contactCandidate(page) {
  const status = await page.evaluate(() => {
    const b = document.querySelector('[class*="xpath-open-im-btn"]');
    if (b) return (b.innerText||'').trim();
    return '';
  });
  if (status === "继续沟通") { console.log("   [沟通] 已是继续沟通，跳过"); return true; }
  if (status !== "立即沟通") { console.log("   [沟通] 找不到按钮"); return false; }
  console.log("   [沟通] 鼠标点击立即沟通...");
  const btnPos = await page.evaluate(() => {
    const b = document.querySelector('[class*="xpath-open-im-btn"]');
    if (!b) return null;
    const r = b.getBoundingClientRect();
    return { x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2) };
  });
  if (!btnPos) { console.log("   [沟通] 找不到按钮位置"); return false; }
  await page.mouse.click(btnPos.x, btnPos.y);
  console.log("   [沟通] 已点击("+btnPos.x+","+btnPos.y+")");
  await sleep(2000);
  console.log("   [沟通] 鼠标选中UI设计卡片...");
  let cardPos = null;
  for (let c = 0; c < 15; c++) {
    cardPos = await page.evaluate(() => {
      const modals = document.querySelectorAll('[class*="ant-lpt-modal"]');
      for (const m of modals) {
        const t = (m.innerText||'').trim();
        const mr = m.getBoundingClientRect();
        if (!t.includes('请选择开聊职位') || mr.width < 100 || mr.height < 50) continue;
        const liCards = m.querySelectorAll('li');
        for (const li of liCards) {
          const lt = (li.innerText||'').trim();
          const lr = li.getBoundingClientRect();
          if (lt.includes('UI设计') && lr.width > 100 && lr.x > 400) {
            return { x: Math.round(lr.x + lr.width/2), y: Math.round(lr.y + lr.height/2) };
          }
        }
        const allEls = m.querySelectorAll('*');
        for (const el of allEls) {
          const et = (el.innerText||'').trim();
          const er = el.getBoundingClientRect();
          if (et.includes('UI设计') && er.width > 50 && er.x > 400 && el.offsetParent) {
            return { x: Math.round(er.x + er.width/2), y: Math.round(er.y + er.height/2) };
          }
        }
      }
      return null;
    });
    if (cardPos) { console.log("   [沟通] 卡片位置("+cardPos.x+","+cardPos.y+")"); break; }
    await sleep(500);
  }
  if (cardPos) { await page.mouse.click(cardPos.x, cardPos.y); console.log("   [沟通] 已点击UI设计卡片"); await sleep(1000); }
  else { console.log("   [沟通] 找不到卡片（弹窗可能已自动选中）"); }
  console.log("   [沟通] 鼠标点击确认...");
  let confirmed = false;
  for (let attempt = 0; attempt < 20; attempt++) {
    const confirmPos = await page.evaluate(() => {
      const btns = document.querySelectorAll('button');
      for (const b of btns) {
        if (!b.offsetParent) continue;
        const t = (b.innerText||'').trim();
        if (t !== '确认') continue;
        const r = b.getBoundingClientRect();
        if (r.x > 300 && r.height > 20) {
          const parent = b.parentElement;
          if (parent && parent.innerText && parent.innerText.includes("取消")) {
            return { x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2) };
          }
        }
      }
      return null;
    });
    if (confirmPos) { console.log("   [沟通] 确认按钮位置("+confirmPos.x+","+confirmPos.y+")"); await page.mouse.click(confirmPos.x, confirmPos.y); console.log("   [沟通] 已点击确认"); confirmed = true; await sleep(2000); break; }
    await sleep(500);
  }
  if (confirmed) {
    await sleep(3000);
    const ns = await page.evaluate(() => {
      const b = document.querySelector('[class*="xpath-open-im-btn"]');
      if (b) return (b.innerText||'').trim();
      return '';
    });
    console.log("   [沟通] 状态:", ns);
  } else { console.log("   [沟通] 未找到确认按钮"); }
  return confirmed;
}

// ===== IM 面板检查回复（同一浏览器，开沟通面板检查刚沟通的候选人）=====
const PHONE_RE = /1[3-9]\d{9}/;

async function checkIMReplies(page, records, newlyCommunicated) {
  if (!newlyCommunicated.length) { console.log('\n[检查回复] 没有新沟通的候选人需要检查'); return; }
  console.log(`\n[检查回复] 检查 ${newlyCommunicated.length} 个新沟通候选人...`);

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  // 打开沟通面板
  console.log('[检查回复] 打开沟通面板...');
  await page.evaluate(() => {
    for (const a of document.querySelectorAll('a')) {
      if ((a.innerText||'').includes('沟通') && a.offsetParent) { a.click(); return; }
    }
  });
  await sleep(8000);
  try { await page.addStyleTag({content:'[class*="guideMask"]{display:none!important;'}); } catch {}

  // 读取联系人列表
  console.log('[检查回复] 读取联系人列表...');
  const contacts = await page.evaluate(() => {
    const results = [];
    const items = document.querySelectorAll('[class*="im-ui-contact-list-item"]');
    for (const item of items) {
      const text = (item.innerText||'').trim();
      if (!text || text.length < 5) continue;
      const nameSpan = item.querySelector('.im-ui-contact-title-main, [class*="im-ui-contact-title-main"]');
      const name = nameSpan ? nameSpan.innerText.trim() : '';
      const msgEl = item.querySelector('.im-ui-contact-item-message, [class*="im-ui-contact-item-message"]');
      const lastMsg = msgEl ? msgEl.innerText.trim() : '';
      const r = item.getBoundingClientRect();
      if (name && r.width > 50) results.push({ name, lastMsg, x: Math.round(r.x+r.width/2), y: Math.round(r.y+r.height/2) });
    }
    return results;
  });
  console.log(`[检查回复] 共 ${contacts.length} 个联系人`);

  // 遍历新沟通候选人，匹配联系人
  const myImId = await page.evaluate(() => {
    try { return document.querySelector('[class*="im-id"], [class*="myImId"]')?.innerText||''; } catch { return ''; }
  });

  let updated = [];
  for (const rec of newlyCommunicated) {
    const name = (rec.name||'').replace(/\*\*/g, '');
    const company = rec.company||'';
    if (!name && !company) continue;

    // 找匹配的联系人
    let match = null;
    for (const c of contacts) {
      const cleanName = c.name.replace(/\s+/g, '');
      if (name && (cleanName.includes(name) || cleanName === name)) { match = c; break; }
      if (company && c.name.includes(company)) { match = c; break; }
    }

    if (!match) {
      console.log(`  [检查回复] ${rec.name||'?'}: 未在联系人列表中找到`);
      rec.contact = rec.contact || '已发起沟通';
      rec.notes = (rec.notes ? rec.notes+' | ' : '') + '对方未回复';
      updated.push(rec.name||'?');
      continue;
    }

    // 点击该联系人查看对话
    await page.mouse.click(match.x, match.y);
    await sleep(3000);

    // 读取对话区域的最新消息
    const msgInfo = await page.evaluate(() => {
      // 找消息气泡
      const msgs = document.querySelectorAll('[class*="im-ui-message-content"], [class*="im-chat-message"]');
      const lastMsgEl = msgs[msgs.length - 1];
      if (!lastMsgEl) return { text: '', isSelf: false };
      const text = (lastMsgEl.innerText||'').trim();
      // 判断是不是自己发的（通常在 class 上有 self/right 标记）
      const cls = (lastMsgEl.className||'') + ' ' + (lastMsgEl.parentElement?.className||'');
      const isSelf = cls.includes('self') || cls.includes('right') || cls.includes('mine') || cls.includes('sent');
      return { text, isSelf };
    });

    const phoneMatch = msgInfo.text.match(PHONE_RE);

    if (msgInfo.isSelf) {
      // 最后一条是自己发的 -> 对方未回复
      console.log(`  [检查回复] ${rec.name||'?'}: 对方未回复`);
      rec.contact = rec.contact || '已发起沟通';
      rec.notes = (rec.notes ? rec.notes+' | ' : '') + '对方未回复';
    } else if (phoneMatch) {
      // 对方回复了，且含手机号
      console.log(`  [检查回复] ${rec.name||'?'}: ✅ 已回复，手机号 ${phoneMatch[0]}`);
      rec.contact = phoneMatch[0];
      rec.notes = (rec.notes ? rec.notes+' | ' : '') + '已收到回复';
    } else {
      // 对方回复了，但无手机号（或手机号被猎聘隐藏）
      const preview = msgInfo.text.substring(0, 60);
      console.log(`  [检查回复] ${rec.name||'?'}: 💬 已回复 "${preview}"`);
      rec.contact = '候选人有回复';
      rec.notes = (rec.notes ? rec.notes+' | ' : '') + `已收到回复 | ${preview}`;
    }
    updated.push(rec.name||'?');
    await sleep(500);
  }

  console.log(`[检查回复] 已更新 ${updated.length} 人`);
  for (const u of updated) console.log(`  [检查回复] ${u}`);

  // 切回搜索页
  await page.evaluate(() => {
    for (const a of document.querySelectorAll('a')) {
      if ((a.innerText||'').includes('搜职位') && a.offsetParent) { a.click(); return; }
    }
  });
  await sleep(3000);
}

// ===== 保存结果 =====
function saveResults(records, dir) {
  if (!records.length) return;
  const csvPath = path.join(dir, 'candidates.csv');
  const esc = v => '"' + (v||'').replace(/"/g, '""') + '"';
  const h = '编号,姓名,公司,职位,学校,学历,工作年限,技能,匹配度,来源,联系方式,日期,状态,备注';
  const rows = records.map(r => [r.id,r.name,r.company,r.position,r.school,r.edu,r.workYears,r.skills,r.matchScore,r.source,r.contact,r.date,r.status,r.notes].map(esc).join(','));
  fs.writeFileSync(csvPath, '\ufeff' + h + '\n' + rows.join('\n'), 'utf8');
  console.log('CSV:', csvPath);
}

function saveProgress(records, pageNum, nameSet) {
  // 保存时附带最近 50 条记录的姓名+公司，方便后续补全
  const recentRecs = records.slice(-50).map(r => ({ id: r.id, name: r.name, company: r.company, phone: r.contact }));
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify({
    processedCount: records.length,
    lastPage: pageNum,
    seenNames: [...nameSet],
    records: recentRecs,
    timestamp: new Date().toISOString(),
  }, null, 2));
}

// ===== 主流程 =====
async function main() {
  const config = readConfig();
  const position = config.filters['岗位名称'] || 'ui设计';
  const location = config.filters['工作地点'] || '上海';
  const searchTerm = position;
  const targetCount = TARGET_COUNT;

  console.log('=== Liepin v4 ===');
  console.log('Job:', position, '| Loc:', location);
  console.log('Skills:', config.skills.map(s => s.name + '(' + s.required + ')').join(', '));
  console.log('Target:', targetCount, '| Kill: Desktop/.kill-signal');
  console.log('Mode: page-by-page (ant-lpt-pagination)');
  console.log('Auto-communicate: >= 55% match');
  console.log('================');

  const OUT = path.join('C:\\Users', process.env.USERNAME||'10362974', 'Desktop', 'candidates', 'liepin-' + searchTerm);
  fs.mkdirSync(OUT, { recursive: true });

  const { chromium } = await import('playwright');
  const browser = await chromium.launch({ channel: 'chrome', headless: false, args: ['--disable-blink-features=AutomationControlled'] });
  const ctx = await browser.newContext({ viewport: { width: 1400, height: 900 }, locale: 'zh-CN', timezoneId: 'Asia/Shanghai' });
  await ctx.addInitScript(STEALTH);

  let cfg = { cookies: [] };
  try { cfg = JSON.parse(fs.readFileSync(path.join(WORKSPACE, 'liepin-config.json'), 'utf8')); } catch {}
  if (cfg.cookies?.length) {
    await ctx.addCookies(cfg.cookies.map(c => ({ name: c.name, value: c.value, domain: '.liepin.com', path: '/', httpOnly: false, secure: false, sameSite: 'Lax' })));
  }

  const page = await ctx.newPage();
  await page.setExtraHTTPHeaders({ 'Accept-Language': 'zh-CN,zh;q=0.9' });

  const records = EXISTING_RECORDS.map(r => ({...r}));  // 恢复已有记录
  const newlyCommunicated = [];  // 追踪新沟通的候选人，用于后续检查回复
  const seenNames = new Set(EXISTING_NAMES);  // 恢复已有去重指纹
  let totalProcessed = records.length;
  let currentPage = START_PAGE;
  let noNewCandidatesCount = 0;

  const gracefulExit = async (msg) => {
    console.log('\n[STOP] ' + msg);
    clearKill();
    saveResults(records, OUT);
    saveProgress(records, currentPage, seenNames);
    try { await browser.close(); } catch {}
    console.log('[DONE] Saved');
    process.exit(0);
  };

  try {
    if (checkKill()) await gracefulExit('Initial kill');

    console.log('\n[1] Open liepin...');
    await page.goto('https://lpt.liepin.com/search', { timeout: 60000, waitUntil: 'networkidle' });
    await sleep(5000);
    if (await detectCaptcha(page)) await waitCaptcha(page);
    try { await page.addStyleTag({ content: '[class*="guideMask"]{display:none!important;}' }); } catch {}
    await sleep(1000);

    if (checkKill()) await gracefulExit('Before search');

    // Search
    console.log('[2] Search:', searchTerm);
    const input = await page.$('input[placeholder*="搜职位"], input[placeholder*="搜索"]');
    if (input) {
      await input.click({ force: true }); await sleep(300);
      await input.fill('');
      for (const ch of searchTerm) await page.keyboard.type(ch, { delay: 50 });
      await sleep(500);
      await page.keyboard.press('Enter');
      await sleep(20000);
    }
    try { await page.addStyleTag({ content: '[class*="guideMask"]{display:none!important;}' }); } catch {}
    await sleep(2000);
    if (await detectCaptcha(page)) await waitCaptcha(page);

    // Set city filter
    console.log('[3] Set city:', location);
    try {
      const cityBtn = await page.$('text=期望城市');
      if (cityBtn) { await cityBtn.click(); await sleep(1500); }
      const locBtn = await page.$('text=' + location);
      if (locBtn) { await locBtn.click(); console.log('    OK'); await sleep(5000); }
    } catch (e) { console.log('    city:', e.message); }

    try { await page.addStyleTag({ content: '[class*="guideMask"]{display:none!important;}' }); } catch {}
    await sleep(2000);
    if (await detectCaptcha(page)) await waitCaptcha(page);
    if (checkKill()) await gracefulExit('After city');

    console.log('\n[3] Target:', targetCount, 'candidates');

    // Main loop: process page by page
    while (totalProcessed < targetCount) {
      if (checkKill()) await gracefulExit('Kill at page ' + currentPage);

      // Get current visible candidates
      const currentCount = await page.evaluate(() => document.querySelectorAll('[class*="resumeCardContent"]').length);
      console.log('\nPage', currentPage, '- candidates:', currentCount, 'processed:', totalProcessed, '/', targetCount);

      if (currentCount === 0) {
        console.log('[WARN] No candidates found');
        break;
      }

      // Process candidates on this page（从0开始索引）
      
      for (let i = 0; i < Math.min(currentCount, 20); i++) {
        if (totalProcessed >= targetCount) break;

        if (checkKill()) await gracefulExit('Kill before ' + (i+1));

        console.log('\n--- [' + (i+1) + '/' + targetCount + '] ---');

        // Dedup check: get candidate name
        const cardFingerprint = await page.evaluate((idx) => {
          const cards = document.querySelectorAll('[class*="resumeCardContent"]');
          if (!cards[idx]) return '';
          const text = (cards[idx].innerText || '').trim();
          // 取姓名+公司+年限作为唯一指纹
          let name = (text.match(/([\u4e00-\u9fa5]{1,4})\s*\*\*/) || [,''])[1];
          if (!name) name = (text.match(/([\u4e00-\u9fa5]{2,4})[\s\n]+\d+年/) || [,''])[1];
          if (!name) name = (text.match(/([\u4e00-\u9fa5]{2,4})[\s\n]+学历/) || [,''])[1];
          const company = text.match(/(有限公司|责任公司|集团|股份)/);
          const years = text.match(/(\d+)\s*年/);
          return (name||'') + '|' + (company?.[0]||'') + '|' + (years?.[0]||'');
        }, i);

        if (!cardFingerprint) { console.log('   [skip] no fingerprint'); continue; }
        if (seenNames.has(cardFingerprint)) { console.log('   [skip] dup:', cardFingerprint); continue; }
        seenNames.add(cardFingerprint);

        // Click candidate
        try {
          await page.evaluate((idx) => {
            const cards = document.querySelectorAll('[class*="resumeCardContent"]');
            const t = cards[idx]?.querySelector('[class*="cardLeft"]') || cards[idx];
            if (t) t.click();
          }, i);
          await sleep(5000);
          if (await detectCaptcha(page)) await waitCaptcha(page);
          try { await page.addStyleTag({ content: '[class*="guideMask"]{display:none!important;}' }); } catch {}
          await sleep(2000);

          // Extract data
          const fn = 'candidate_' + String(i+1).padStart(3,'0');
          const { text } = await captureResume(page, path.join(OUT, fn+'.png'), path.join(OUT, fn+'.txt'));
          const match = calcMatchScore(text, config);

                    // ===== 取名字（精准提取）=====
          let n = '';
          const headTxt = text.substring(0, 250);
          // 方式A: 查看大图后的名字行
          const afterPic = headTxt.match(/查看大图[\s\n]+([\u4e00-\u9fa5]{2,4})/);
          if (afterPic) n = afterPic[1];
          // 方式B: 汉字**格式（带**标记的可靠，允许1-4字符姓名）
          if (!n) {
            const nameMatch = headTxt.match(/([\u4e00-\u9fa5]{1,4})\s*\*\*/);
            if (nameMatch) n = nameMatch[1];
          }
          // 方式C: 汉字后跟年龄
          if (!n) {
            const ageMatch = headTxt.match(/([\u4e00-\u9fa5]{2,4})[\s\n]+\d+岁/);
            if (ageMatch) n = ageMatch[1];
          }
          // 方式D: 汉字后跟在职/离职等状态
          if (!n) {
            const statusMatch = headTxt.match(/([\u4e00-\u9fa5]{2,4})[\s\n]+(?:在职|离职|毕业|在|项目|没找到|应届|目前)/);
            if (statusMatch) n = statusMatch[1];
          }

          // 取公司
          const companyName = (text.match(/([\u4e00-\u9fa5（）()]{3,20}(?:有限公司|责任公司|集团))/))?.[1];

          // 取学历
          const edu = (text.match(/(博士|硕士|本科|大专)/))?.[1];

          // 取工作年限
          const workYears = [...text.matchAll(/(\d+)\s*年/g)].filter(x => {const nv=parseInt(x[1]);return nv>=1&&nv<=40;});

          // 取职位：多种格式
          let pos = text.match(/(?:期望[职岗]位|目前职位|职位)[：:]\s*([\u4e00-\u9fa5A-Za-z/（）()]+)/)?.[1];
          if (!pos) {
            const xy = text.match(/求职意向[\s\S]{1,200}/);
            if (xy) {
              const lines = xy[0].split('\n').filter(l => l.trim()).map(l => l.trim());
              const firstLine = lines.find(l => !l.includes('查看全部') && !l.includes('求职意向') && !l.includes('k×') && !l.includes('上海') && l.length >= 2 && l.length <= 20);
              if (firstLine) pos = firstLine;
            }
          }

          // 取学校
          const matchSchool = text.match(/([\u4e00-\u9fa5（）()]{2,})(?:大学|学院)/);
          const matchS2 = text.match(/(?:毕业[于院校]|学校|院校)[：:]\s*([\u4e00-\u9fa5（）()]+)/);
          const schoolName = matchSchool ? matchSchool[1] + (matchSchool[0].slice(matchSchool[1].length) || '') : (matchS2?.[1] || '');
          const phoneNum = (text.match(/1[3-9]\d{9}/))?.[0] || '';
const rec = {
            id: 'LP-' + new Date().toISOString().slice(0,10).replace(/-/g,'') + '-' + String(i+1).padStart(3,'0'),
            name: n ? n+'**' : (cardFingerprint||'').split('|')[0],
            company: companyName||'', position: pos||'', school: schoolName, edu: edu||'',
            workYears: workYears.length ? workYears[0][1]+'年' : '',
            skills: config.skills.map(s => s.name.split(',').map(t => t.trim().toLowerCase()).filter(t => text.toLowerCase().includes(t)).filter(Boolean).join(',')).filter(s => s).join('、'),
            matchScore: match.ratio + '%', source: 'liepin', contact: phoneNum || '',
            date: new Date().toISOString().slice(0,10),
            status: match.passed ? (match.ratio >= 55 ? '沟通中' : '已通过') : '淘汰',
            notes: match.passed ? '' : (match.reason?.replace('Missing:','缺少') || '低匹配度'),
          };

          console.log('   ' + (match.passed?'[OK] ':'[X] ') + 'Match:' + match.ratio + '% | ' + (rec.name||'?') + ' | ' + (rec.company||'?'));

          // Auto-communicate if >= 55%
          if (match.passed && match.ratio >= 55) {
            const success = await contactCandidate(page);
            rec.status = success ? '已沟通' : '沟通失败';
            if (success) {
              // 沟通成功后，简历的隐藏联系方式会暴露，重新读一遍提取手机号
              await sleep(2000);
              const freshText = await page.evaluate(() => {
                const el = document.querySelector('[class*="resume-detail-content-body"]');
                return el ? el.innerText : '';
              });
              const freshPhone = (freshText.match(/1[3-9]\d{9}/))?.[0] || '';
              rec.contact = freshPhone ? (freshPhone + ' | 已发起沟通') : '已发起沟通';
              if (freshPhone) console.log('   [电话] ' + freshPhone);
            } else {
              rec.contact = phoneNum || '';
            }
          }

          // 记录新沟通的候选人用于后续 IM 检查
          if (rec.status === '已沟通') {
            newlyCommunicated.push(rec);
          }

          records.push(rec);
          totalProcessed++;

          // Close modal
          await page.keyboard.press('Escape');
          await sleep(1500);
        } catch (err) {
          console.log('   [ERR] ' + err.message);
          try { await page.keyboard.press('Escape'); await sleep(1000); } catch {}
          records.push({ id:'ERR-'+String(i+1).padStart(3,'0'), name: (cardFingerprint||'').split('|')[0], company:'', position:'', school:'', edu:'', workYears:'', skills:'', matchScore:'', source:'liepin', contact:'', date:'', status:'错误', notes: '异常: ' + (err.message || '未知') });
          totalProcessed++;
        }

        // Save progress every 5 candidates
        if (records.length % 5 === 0) {
          saveProgress(records, currentPage, seenNames);
        }
      }

      // 翻到下一页
      if (totalProcessed < targetCount) {
        console.log('[PAGE] Go to page', (currentPage + 1), '...');
        // 滚动到底部显示分页
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        await sleep(1500);
        
        await sleep(1000);
        const clicked = await page.evaluate(() => {
          // 滚动到底部确保分页可见
          window.scrollTo(0, document.body.scrollHeight);
          
          // 猎聘使用的是 ant-lpt-pagination（Ant Design 定制版）
          // 方法1: 直接找 ant-lpt-pagination-next 里的 a 标签
          const nextBtn = document.querySelector('li[class*="pagination-next"] a');
          if (nextBtn) { nextBtn.click(); return 'next-btn'; }
          
          // 方法2: 从 ant-lpt-pagination 容器里找
          const pagination = document.querySelector('[class*="ant-lpt-pagination"]');
          if (pagination) {
            const nextLi = pagination.querySelector('li[class*="next"]');
            if (nextLi) {
              const link = nextLi.querySelector('a') || nextLi.querySelector('button');
              if (link) { link.click(); return 'pagination-next'; }
            }
          }
          
          // 方法3: 找当前页下一个页码 li
          const activeLi = document.querySelector('li[class*="pagination-item-active"]');
          if (activeLi) {
            const p = activeLi.parentElement;
            const liList = p ? [...p.querySelectorAll('li')] : [];
            const currentIdx = liList.indexOf(activeLi);
            for (let j = currentIdx + 1; j < liList.length; j++) {
              const link = liList[j].querySelector('a');
              if (link && link.innerText.trim()) {
                link.click();
                return 'sibling-page-' + link.innerText.trim();
              }
            }
          }
          
          // 方法4: 文本查找
          const allLinks = document.querySelectorAll('a');
          for (const a of allLinks) {
            const t = a.innerText.trim();
            if (t === '下一页' || t === '>' || a.getAttribute('aria-label') === 'Next' || a.getAttribute('aria-label') === 'next') {
              a.click(); return 'text-' + t;
            }
          }
          return null;
        });
        
        if (clicked) {
          console.log('   [OK] Clicked:', clicked);
          currentPage++;
          await sleep(5000);
        } else {
          console.log('   [WARN] No next page button found, stopping');
          break;
        }
      } else {
        currentPage++;
      }
      await sleep(2000);
    }

    console.log('\n[DONE] Processed:', totalProcessed);

    // 先保存结果（确保数据不丢失）
    saveResults(records, OUT);
    saveProgress(records, currentPage, seenNames);

    // 再检查新沟通候选人的回复
    try { await checkIMReplies(page, records, newlyCommunicated); } catch(e) {
      console.log('[检查回复] 出错:', e.message);
    }
    // 回复检查后再次保存（可能会更新联系方式/备注）
    try { saveResults(records, OUT); } catch(e) {
      console.log('[保存] 出错:', e.message);
    }
    saveProgress(records, currentPage, seenNames);

    const passed = records.filter(r => r.status === '已沟通' || r.status === '已通过');
    const communicated = records.filter(r => r.status === '已沟通');
    const replied = records.filter(r => r.notes && r.notes.includes('已收到回复'));
    console.log('Passed:', passed.length, '| Communicated:', communicated.length, '| Replied:', replied.length);
    for (const r of communicated) {
      const hasReply = r.notes && r.notes.includes('已收到回复');
      const hasPhone = /1[3-9]\d{9}/.test(r.contact);
      console.log('  [沟通] ' + r.name + ' - ' + (r.company || '?') + (hasReply ? ' ✅' : ' ❌') + (hasPhone ? ' 📞' : ''));
    }

  } catch (err) {
    console.error('[FATAL]', err.message);
    saveResults(records, OUT);
    saveProgress(records, currentPage, seenNames);
  }
  console.log('\n[DONE] Browser stays open');
}

main().catch(err => { console.error(err.message); process.exit(1); });
