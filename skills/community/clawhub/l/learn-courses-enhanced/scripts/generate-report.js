// ==================== MOOC 学习报告生成器 ====================
// 数据来源：
//   - learning-progress.json（实时逐章进度，主数据源）
//   - learning-report.json（脚本完整结束时的统计，补充）
//   - run.log（解析平台"总章节数/已完成"用于计算整体完成度）
// 输出: learning-report.html
// 用法: node scripts/generate-report.js

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const REPORT_FILE = path.join(ROOT, 'learning-report.json');
const PROGRESS_FILE = path.join(ROOT, 'learning-progress.json');
const LOG_FILE = path.join(ROOT, 'run.log');
const OUT_FILE = path.join(ROOT, 'learning-report.html');

function readText(p) { try { return fs.readFileSync(p, 'utf8'); } catch (e) { return ''; } }
function readJSON(p) { try { return JSON.parse(readText(p)); } catch (e) { return null; } }

function formatTime(seconds) {
  seconds = Math.max(0, Math.floor(seconds || 0));
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  if (h > 0) return `${h} 小时 ${m} 分 ${s} 秒`;
  if (m > 0) return `${m} 分 ${s} 秒`;
  return `${s} 秒`;
}

function fmtTs(iso) {
  if (!iso) return '—';
  const d = new Date(iso);
  if (isNaN(d.getTime())) return String(iso);
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function statusMeta(status) {
  if (status === 'completed') return { label: '已完成', cls: 'ok' };
  if (status === 'failed') return { label: '失败', cls: 'bad' };
  if (status === 'learning') return { label: '学习中', cls: 'run' };
  return { label: '待学习', cls: 'idle' };
}

// 从 run.log 解析平台总章节数与完成情况
function parseLog(logText) {
  const out = { total: 0, completed: 0, baseCompleted: 0, toolCompletedAfter: 0 };
  if (!logText) return out;
  const re = /总章节数:\s*(\d+),\s*需要学习:\s*(\d+)\s*章,\s*已完成:\s*(\d+)\s*章/g;
  let m, last = null, lastIndex = -1;
  while ((m = re.exec(logText)) !== null) { last = m; lastIndex = re.lastIndex; }
  if (last) {
    out.total = parseInt(last[1], 10) || 0;
    out.baseCompleted = parseInt(last[3], 10) || 0;
    const tail = logText.slice(lastIndex);
    const doneAfter = (tail.match(/第\s*\d+\s*章学习完成/g) || []).length;
    out.toolCompletedAfter = doneAfter;
    out.completed = Math.min(out.baseCompleted + doneAfter, out.total);
  }
  return out;
}

function main() {
  const progress = readJSON(PROGRESS_FILE) || {};
  const report = readJSON(REPORT_FILE) || {};
  const logText = readText(LOG_FILE);
  const logInfo = parseLog(logText);

  const courses = (progress.courses && Object.keys(progress.courses).length)
    ? progress.courses
    : (report.courses || {});

  // 工具逐章记录
  let toolCompleted = 0, toolFailed = 0, toolTimeSec = 0;
  for (const c of Object.values(courses)) {
    const chs = c.chapters || {};
    for (const i of Object.keys(chs)) {
      const st = chs[i].status;
      toolTimeSec += chs[i].timeSpent || 0;
      if (st === 'completed') toolCompleted++;
      else if (st === 'failed') toolFailed++;
    }
  }
  if (!toolTimeSec) toolTimeSec = ((progress.stats || {}).totalTime) || ((report.summary || {}).totalTimeSeconds) || 0;

  const sessions = (progress.stats || {}).sessions || report.sessions || [];

  // 找"当前课程"：最近有章节更新的课程
  let currentCid = null, currentTs = 0;
  for (const [cid, c] of Object.entries(courses)) {
    for (const k of Object.keys(c.chapters || {})) {
      const t = Date.parse((c.chapters[k] || {}).timestamp || '') || 0;
      if (t > currentTs) { currentTs = t; currentCid = cid; }
    }
  }
  let curCompleted = 0, curFailed = 0, curTimeSec = 0;
  if (currentCid) {
    const chs = courses[currentCid].chapters || {};
    for (const k of Object.keys(chs)) {
      curTimeSec += chs[k].timeSpent || 0;
      if (chs[k].status === 'completed') curCompleted++;
      else if (chs[k].status === 'failed') curFailed++;
    }
  }

  // 每门课程的章节明细（当前课程排在最前）
  const orderedCids = currentCid
    ? [currentCid, ...Object.keys(courses).filter((x) => x !== currentCid)]
    : Object.keys(courses);
  let coursesHtml = '';
  for (const cid of orderedCids) {
    const cdata = courses[cid];
    const isCur = cid === currentCid;
    const chapters = cdata.chapters || {};
    const idxs = Object.keys(chapters).map(Number).sort((a, b) => a - b);
    let rows = '', totalSec = 0, done = 0;
    for (const i of idxs) {
      const c = chapters[i];
      const meta = statusMeta(c.status);
      totalSec += c.timeSpent || 0;
      if (c.status === 'completed') done++;
      rows += `<tr>
        <td class="num">第 ${i} 章</td>
        <td><span class="pill ${meta.cls}">${meta.label}</span></td>
        <td class="num">${c.timeSpent ? formatTime(c.timeSpent) : '—'}</td>
        <td class="ts">${fmtTs(c.timestamp)}</td>
      </tr>`;
    }
    if (!rows) rows = `<tr><td colspan="4" class="empty">暂无逐章明细</td></tr>`;

    coursesHtml += `
    <section class="course">
      <h2>${esc(cdata.name || cid)}${isCur ? '<span class="tag-cur">当前课程</span>' : '<span class="tag-his">历史</span>'}<span class="badge">完成 ${done} 章</span></h2>
      <table>
        <thead><tr><th>章节</th><th>状态</th><th>用时</th><th>完成时间</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
      <p class="subtotal">累计用时：<b>${formatTime(totalSec)}</b>　·　课程ID：${esc(cid)}</p>
    </section>`;
  }
  if (!coursesHtml) coursesHtml = `<p class="empty">暂无课程章节数据。</p>`;

  // 整体完成度
  const totalChapters = logInfo.total || toolCompleted;
  const platformCompleted = logInfo.completed || toolCompleted;
  const rate = totalChapters ? Math.round((platformCompleted / totalChapters) * 100) : 0;
  const remaining = Math.max(0, totalChapters - platformCompleted);

  const sessionRows = sessions.map((s) => `<tr>
      <td class="num">${esc(s.id)}</td>
      <td>${esc(s.course || '—')}</td>
      <td class="ts">${fmtTs(s.startTime)}</td>
    </tr>`).join('');

  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MOOC 自动学习报告</title>
<style>
  :root{
    --bg:#f5f7fb; --card:#ffffff; --border:#e6e9f0; --text:#1f2430; --muted:#6b7280;
    --ok:#16a34a; --ok-bg:#e9f7ef; --bad:#dc2626; --bad-bg:#fdecec;
    --run:#2563eb; --run-bg:#e8f0fe; --idle:#6b7280; --idle-bg:#eef1f6;
    --accent:#2f6fed;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:var(--bg);color:var(--text);
    font-family:-apple-system,"Segoe UI","Microsoft YaHei",Roboto,Helvetica,Arial,sans-serif;
    line-height:1.6;padding:40px 20px;}
  .wrap{max-width:920px;margin:0 auto;}
  header{text-align:center;margin-bottom:28px;}
  header h1{margin:0 0 6px;font-size:28px;letter-spacing:.5px;}
  header .meta{color:var(--muted);font-size:14px;}
  .cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:28px;}
  .card{background:var(--card);border:1px solid var(--border);border-radius:14px;
    padding:18px 16px;text-align:center;box-shadow:0 1px 3px rgba(16,24,40,.04);}
  .card .v{font-size:22px;font-weight:700;color:var(--accent);}
  .card .k{font-size:13px;color:var(--muted);margin-top:4px;}
  section.course{background:var(--card);border:1px solid var(--border);border-radius:14px;
    padding:20px 22px;margin-bottom:20px;box-shadow:0 1px 3px rgba(16,24,40,.04);}
  section.course h2{margin:0 0 14px;font-size:18px;display:flex;align-items:center;gap:10px;}
  .badge{font-size:12px;font-weight:600;color:var(--ok);background:var(--ok-bg);
    border-radius:20px;padding:3px 10px;}
  .tag-cur{font-size:11px;font-weight:700;color:#fff;background:var(--accent);border-radius:6px;padding:2px 8px;}
  .tag-his{font-size:11px;font-weight:600;color:var(--muted);background:var(--idle-bg);border-radius:6px;padding:2px 8px;}
  table{width:100%;border-collapse:collapse;font-size:14px;}
  th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--border);}
  th{color:var(--muted);font-weight:600;font-size:13px;background:#fafbfe;}
  tbody tr:last-child td{border-bottom:none;}
  td.num{font-variant-numeric:tabular-nums;}
  td.ts{color:var(--muted);font-size:13px;}
  .pill{display:inline-block;font-size:12px;font-weight:600;border-radius:20px;padding:2px 10px;}
  .pill.ok{color:var(--ok);background:var(--ok-bg);}
  .pill.bad{color:var(--bad);background:var(--bad-bg);}
  .pill.run{color:var(--run);background:var(--run-bg);}
  .pill.idle{color:var(--idle);background:var(--idle-bg);}
  .subtotal{margin:12px 2px 0;color:var(--muted);font-size:13px;}
  .empty{color:var(--muted);text-align:center;padding:18px;}
  footer{color:var(--muted);font-size:12px;text-align:center;margin-top:24px;}
  .bar{height:10px;background:var(--idle-bg);border-radius:99px;overflow:hidden;margin-top:10px;}
  .bar>i{display:block;height:100%;background:linear-gradient(90deg,#34d399,#16a34a);}
  .note{background:#fffbeb;border:1px solid #fde68a;color:#92400e;border-radius:12px;
    padding:12px 16px;font-size:13px;margin-bottom:20px;}
  .kpis{display:flex;gap:22px;flex-wrap:wrap;font-size:14px;color:var(--muted);margin-top:10px;}
  .kpis b{color:var(--text);}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>MOOC 自动学习报告</h1>
    <div class="meta">生成时间：${fmtTs(new Date().toISOString())}　·　数据源：learning-progress.json + run.log</div>
  </header>

  <div class="note">以下为截至「暂停学习」时的真实进度。剩余章节可稍后「继续学习」自动接着完成。</div>

  <div class="cards">
    <div class="card"><div class="v">${curCompleted}</div><div class="k">本次课程完成章节</div></div>
    <div class="card"><div class="v">${curFailed}</div><div class="k">失败章节</div></div>
    <div class="card"><div class="v">${esc(formatTime(curTimeSec))}</div><div class="k">本次课程累计时长</div></div>
    <div class="card"><div class="v">${sessions.length}</div><div class="k">学习会话次数</div></div>
  </div>

  <section class="course">
    <h2>本次课程完成度<span class="badge">${rate}%</span></h2>
    <div class="bar"><i style="width:${rate}%"></i></div>
    <div class="kpis">
      <span>课程总章节：<b>${totalChapters || '—'}</b></span>
      <span>平台已完成：<b>${platformCompleted}</b></span>
      <span>剩余待学：<b>${remaining}</b></span>
    </div>
  </section>

  ${coursesHtml}

  <section class="course">
    <h2>学习会话记录</h2>
    <table>
      <thead><tr><th>会话 ID</th><th>课程</th><th>开始时间</th></tr></thead>
      <tbody>${sessionRows || '<tr><td colspan="3" class="empty">暂无会话记录</td></tr>'}</tbody>
    </table>
  </section>

  <footer>由 mooc-learner 自动生成 · 仅用于个人学习进度统计</footer>
</div>
</body>
</html>`;

  fs.writeFileSync(OUT_FILE, html, 'utf8');
  console.log('✓ 学习报告已生成: ' + OUT_FILE);
  console.log(`  工具完成章节: ${toolCompleted} | 平台完成: ${platformCompleted}/${totalChapters} (${rate}%) | 累计时长: ${formatTime(toolTimeSec)}`);
}

main();
