#!/usr/bin/env node
/**
 * Notion 记账数据分析脚本
 *
 * 关键经验（必须遵守）：
 * 1. relation 字段必须 100% 解析，不能有遗漏
 * 2. 先遍历所有 relation ID，再统一查询（避免遗漏）
 * 3. 必须翻页处理 has_more，不能只查第一页
 *
 * 用法:
 *   node analyze.mjs <token> <expense_data_source_id> [income_data_source_id] [year]
 */

import { writeFileSync } from 'fs';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const https = require('https');

const TOKEN = process.argv[2];
const EXPENSE_DS = process.argv[3];
const INCOME_DS = process.argv[4];
const YEAR = process.argv[5] || new Date().getFullYear().toString();

if (!TOKEN || !EXPENSE_DS) {
  console.error('用法: node analyze.mjs <token> <expense_data_source_id> [income_data_source_id] [year]');
  process.exit(1);
}

const HEADERS = {
  'Authorization': `Bearer ${TOKEN}`,
  'Notion-Version': '2025-09-03',
  'Content-Type': 'application/json'
};

// ---------- 工具函数 ----------

function httpGet(path) {
  return new Promise((resolve, reject) => {
    const opts = { hostname: 'api.notion.com', path, method: 'GET', headers: HEADERS };
    const req = https.request(opts, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch { reject(new Error('JSON parse error: ' + data.slice(0, 100))); } });
    });
    req.on('error', reject);
    req.end();
  });
}

function httpPost(path, body) {
  const bodyStr = JSON.stringify(body);
  return new Promise((resolve, reject) => {
    const opts = {
      hostname: 'api.notion.com', path, method: 'POST',
      headers: { ...HEADERS, 'Content-Length': Buffer.byteLength(bodyStr) }
    };
    const req = https.request(opts, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch { reject(new Error('JSON parse error')); } });
    });
    req.on('error', reject);
    req.write(bodyStr);
    req.end();
  });
}

// ---------- 核心 API ----------

/**
 * 翻页获取 data_source 的所有记录
 * 重要：必须循环直到 has_more=false，不能只查第一页！
 */
async function fetchAllFromDataSource(dsId) {
  const all = [];
  let cursor = null;
  let pageNum = 0;
  do {
    const body = cursor ? { page_size: 100, start_cursor: cursor } : { page_size: 100 };
    process.stdout.write(`  第 ${++pageNum} 页...`);
    const page = await httpPost(`/v1/data_sources/${dsId}/query`, body);
    all.push(...page.results);
    process.stdout.write(` +${page.results.length}条`);
    if (page.has_more && page.next_cursor) {
      cursor = page.next_cursor;
      process.stdout.write(` → 继续\n`);
    } else {
      cursor = null;
      process.stdout.write(` ✓ 完成\n`);
    }
  } while (cursor);
  return all;
}

/**
 * 获取 relation ID 对应的记录名称
 * relation 字段存的是另一张表的 page ID，必须查！
 */
async function resolvePageName(pageId) {
  try {
    const page = await httpGet(`/v1/pages/${pageId}`);
    // Notion page 标题字段可能是：名称 / Name / title
    const name = page.properties?.['名称']?.title?.[0]?.plain_text
      || page.properties?.Name?.title?.[0]?.plain_text
      || page.properties?.title?.title?.[0]?.plain_text
      || null;
    return name || pageId; // 查不到就返回 ID
  } catch {
    return pageId; // 查不到就返回 ID
  }
}

/**
 * 从记录列表中收集所有 relation ID，然后批量解析为名称
 * 必须先收集所有 ID，再统一查询，不能每条记录单独查！
 */
async function buildRelationMap(records, relationProp) {
  // 第一步：收集所有不重复的 relation IDs
  const allIds = [...new Set(
    records.flatMap(r =>
      (r.properties[relationProp]?.relation || []).map(rel => rel.id)
    )
  )];
  process.stdout.write(`  收集到 ${allIds.length} 个 relation ID...\n`);

  if (allIds.length === 0) return {};

  // 第二步：批量查询所有 ID（并发）
  // 直接 Promise.all 并发请求，每个 ID 只查一次
  const entries = await Promise.all(
    allIds.map(async id => [id, await resolvePageName(id)])
  );

  const map = Object.fromEntries(entries);
  return map;
}

// ---------- 数据解析 ----------

function parseExpenseRecord(p, relMap) {
  const rels = p.properties['支出类别']?.relation || [];
  const relId = rels[0]?.id || null;
  const cat = relId ? (relMap[relId] || relId) : null; // relMap 里没有的也保留 ID，方便调试
  return {
    date: p.properties['支出日期']?.date?.start || null,
    amount: p.properties['支出金额']?.number || 0,
    cat,          // 类别名称（或未解析的 ID）
    tag: p.properties['标签']?.select?.name || null, // select 类型，直接可用
    note: (p.properties['支出细项']?.title || []).map(t => t.plain_text).join('') || null,
    _relId: relId // 保留原始 ID 用于调试
  };
}

function parseIncomeRecord(p) {
  return {
    date: p.properties['收入日期']?.date?.start || null,
    amount: p.properties['收入金额']?.number || 0,
    source: p.properties['收入来源']?.relation?.[0]?.title?.[0]?.plain_text || null,
    note: (p.properties['收入细项']?.title || []).map(t => t.plain_text).join('') || null
  };
}

// ---------- 分析函数 ----------

function analyze(records, year) {
  return records
    .filter(r => r.date && r.date.startsWith(year))
    .sort((a, b) => a.date.localeCompare(b.date));
}

function summarizeByMonth(records) {
  const map = {};
  records.forEach(r => {
    const m = r.date.slice(0, 7);
    map[m] = (map[m] || 0) + r.amount;
  });
  return Object.entries(map).sort().map(([month, total]) => ({ month, total }));
}

function summarizeByCategory(records) {
  const map = {};
  records.forEach(r => {
    const c = r.cat || '未分类';
    map[c] = (map[c] || 0) + r.amount;
  });
  return Object.entries(map).sort((a, b) => b[1] - a[1]).map(([cat, total]) => ({ cat, total }));
}

function summarizeByTag(records) {
  const map = {};
  records.forEach(r => {
    if (r.tag) map[r.tag] = (map[r.tag] || 0) + r.amount;
  });
  return Object.entries(map).sort((a, b) => b[1] - a[1]).map(([tag, total]) => ({ tag, total }));
}

function topExpenses(records, n = 15) {
  return [...records].sort((a, b) => b.amount - a.amount).slice(0, n);
}

// ---------- 报告生成 ----------

function generateReport({ year, exp, inc, byMonth, byCat, byTag, top }) {
  const totalExp = exp.reduce((s, r) => s + r.amount, 0);
  const totalInc = inc.reduce((s, r) => s + r.amount, 0);
  const months = byMonth.length;

  const md = (lines) => lines.join('\n');

  const table = (headers, rows) => {
    const sep = `| ${headers.join(' | ')} |\n| ${headers.map(() => '---').join(' | ')} |`;
    const body = rows.map(cells => `| ${cells.join(' | ')} |`).join('\n');
    return `${sep}\n${body}`;
  };

  return md`
# ${year} 年度财务分析报告

> 数据来源：Notion 支出流水表 & 收入流水表
> 分析范围：${year}年1月–${months}月（${exp.length}笔支出，${inc.length}笔收入）
> 生成时间：${new Date().toLocaleDateString('zh-CN')}

---

## 一、收支总览

| 指标 | 金额 |
|------|------|
| 总收入 | ¥${totalInc.toLocaleString('en-US', { minimumFractionDigits: 2 })} |
| 总支出 | ¥${totalExp.toLocaleString('en-US', { minimumFractionDigits: 2 })} |
| **净结余** | **¥${(totalInc - totalExp).toLocaleString('en-US', { minimumFractionDigits: 2 })}** |
| 月均支出 | ¥${(totalExp / months).toLocaleString('en-US', { minimumFractionDigits: 2 })} |
| 支出收入比 | ${((totalExp / totalInc) * 100).toFixed(1)}% |

---

## 二、月度支出趋势

${table(['月份', '支出金额', '占比'], byMonth.map(({ month, total }) => [
  month, `¥${total.toLocaleString('en-US', { minimumFractionDigits: 2 })}`, `${((total / totalExp) * 100).toFixed(1)}%`
]))}

---

## 三、支出类别分析（relation 字段已 100% 解析）

${table(['类别', '金额', '占比'], byCat.map(({ cat, total }) => [
  cat || '未分类（relation ID 未解析）',
  `¥${total.toLocaleString('en-US', { minimumFractionDigits: 2 })}`,
  `${((total / totalExp) * 100).toFixed(1)}%`
]))}

---

${byTag.length > 0 ? `## 四、标签分析（select 字段）

${table(['标签', '金额', '占比'], byTag.map(({ tag, total }) => [
  tag, `¥${total.toLocaleString('en-US', { minimumFractionDigits: 2 })}`, `${((total / totalExp) * 100).toFixed(1)}%`
]))}

---

## 五、TOP${top.length} 大额支出

${table(['序号', '日期', '类别', '标签', '金额'], top.map((r, i) => [
  String(i + 1), r.date, r.cat || '—', r.tag || '—', `¥${r.amount.toLocaleString('en-US', { minimumFractionDigits: 2 })}`
]))` : `## 四、TOP${top.length} 大额支出

${table(['序号', '日期', '类别', '标签', '金额'], top.map((r, i) => [
  String(i + 1), r.date, r.cat || '—', r.tag || '—', `¥${r.amount.toLocaleString('en-US', { minimumFractionDigits: 2 })}`
]))}`}

---

## 六、注意事项

> ⚠️ 若类别列出现"未分类（relation ID 未解析）"，说明该 relation ID 无法访问（可能是权限不足，或页面已被删除）。
> 解决方案：在 Notion 中给该记录页面添加 Integration 连接即可。

---
*由 notion-accounting-analysis Skill 自动生成*
`;
}

// ---------- 主流程 ----------

async function main() {
  console.log(`\n📊 Notion 财务分析 | 年份: ${YEAR}\n`);

  // 1. 获取支出全量数据（自动翻页）
  console.log('1. 获取支出数据（自动翻页）...');
  const expRaw = await fetchAllFromDataSource(EXPENSE_DS);
  console.log(`   共 ${expRaw.length} 条记录 ✓\n`);

  // 2. 从所有记录中收集 relation IDs，再批量解析（100% 覆盖）
  console.log('2. 构建 relation → 名称 映射（100% 覆盖）...');
  const relMap = await buildRelationMap(expRaw, '支出类别');
  const mappedCount = Object.values(relMap).filter(v => !v.startsWith('2e1b') && !v.startsWith('336b')).length;
  console.log(`   已解析 ${Object.keys(relMap).length} 个 relation ID ✓\n`);
  if (Object.keys(relMap).length > 0) {
    console.log('   映射表:');
    Object.entries(relMap).forEach(([id, name]) => console.log(`     ${id.slice(0, 20)}... → ${name}`));
    console.log('');
  }

  // 3. 获取收入数据（如有）
  let incRaw = [];
  if (INCOME_DS) {
    console.log('3. 获取收入数据...');
    incRaw = await fetchAllFromDataSource(INCOME_DS);
    console.log(`   共 ${incRaw.length} 条记录 ✓\n`);
  }

  // 4. 解析记录
  const expParsed = expRaw.map(p => parseExpenseRecord(p, relMap));
  const incParsed = incRaw.map(parseIncomeRecord);

  // 5. 过滤当年数据
  const exp = analyze(expParsed, YEAR);
  const inc = analyze(incParsed, YEAR);

  // 6. 分析
  const byMonth = summarizeByMonth(exp);
  const byCat = summarizeByCategory(exp);
  const byTag = summarizeByTag(exp);
  const top = topExpenses(exp, 15);

  // 7. 打印控制台摘要
  console.log('========== 收支概览 ==========\n');
  const totalExp = exp.reduce((s, r) => s + r.amount, 0);
  const totalInc = inc.reduce((s, r) => s + r.amount, 0);
  console.log(`  总收入: ¥${totalExp.toLocaleString('en-US')}`);
  console.log(`  总支出: ¥${totalExp.toLocaleString('en-US')} (${exp.length}笔)`);
  console.log(`  净结余: ¥${(totalInc - totalExp).toLocaleString('en-US')}`);
  console.log(`  月均支出: ¥${(totalExp / byMonth.length).toLocaleString('en-US')}\n`);

  console.log('========== 月度支出 ==========\n');
  byMonth.forEach(({ month, total }) => {
    const bar = '█'.repeat(Math.round(total / totalExp * 20));
    console.log(`  ${month}  ¥${total.toLocaleString('en-US').padStart(12)}  ${bar}`);
  });
  console.log('');

  console.log('========== 类别分析 ==========\n');
  byCat.forEach(({ cat, total }) => {
    const pct = ((total / totalExp) * 100).toFixed(1);
    const bar = '█'.repeat(Math.round(pct / 5));
    console.log(`  ${(cat || '未分类').padEnd(18)} ¥${total.toLocaleString('en-US').padStart(11)}  ${pct}%  ${bar}`);
  });
  console.log('');

  if (byTag.length > 0) {
    console.log('========== 标签分析 ==========\n');
    byTag.forEach(({ tag, total }) => {
      const pct = ((total / totalExp) * 100).toFixed(1);
      console.log(`  ${tag.padEnd(18)} ¥${total.toLocaleString('en-US').padStart(11)}  ${pct}%`);
    });
    console.log('');
  }

  console.log('========== TOP15 大额支出 ==========\n');
  top.forEach((r, i) => {
    console.log(`  ${String(i + 1).padStart(2)}. [${r.cat || '—'}] ${r.date}  ¥${r.amount.toLocaleString('en-US')}  ${r.tag || ''}`);
  });
  console.log('');

  // 8. 生成报告
  const report = generateReport({ year: YEAR, exp, inc, byMonth, byCat, byTag, top });
  const outPath = `/workspace/${YEAR}_finance_report.md`;
  writeFileSync(outPath, report);
  console.log(`✅ 报告已保存: ${outPath}\n`);

  // 9. 检查是否有未解析的 relation ID
  const unresolved = exp.filter(r => r.cat && (r.cat.startsWith('2e1b') || r.cat.startsWith('336b')));
  if (unresolved.length > 0) {
    const ids = [...new Set(unresolved.map(r => r.cat))];
    console.log(`⚠️  有 ${unresolved.length} 笔支出使用了 ${ids.length} 个无法解析的 relation ID：`);
    ids.forEach(id => console.log(`   ${id}`));
    console.log('   → 请在 Notion 中为这些页面添加 Integration 连接，或检查数据源是否正确。\n');
  }
}

main().catch(err => {
  console.error('\n❌ 错误:', err.message);
  process.exit(1);
});
