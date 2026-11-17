// lib/data.mjs — stats.mjs 与 dashboard.mjs 共享的数据解析层
// 契约：Machine Summary 的 YAML fence 紧跟 `## Machine Summary` 标题行，
//       schema SoT 是 modes/evaluate.md（键名变更需同步本文件与该文件）。
// 依赖：零依赖。YAML 只做行级解析（`key: value` 标量）。

import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';

// ---------- 共享标量工具 ----------

// 宽松数字解析：可解析（有限）返回数值，否则 null。统计/筛选/CLI 参数共用。
export function num(s) {
  const v = parseFloat(s);
  return Number.isFinite(v) ? v : null;
}

// ---------- Machine Summary（评估报告） ----------

export function parseMachineSummary(text) {
  const start = text.indexOf('## Machine Summary');
  if (start === -1) return null;
  const fence = /```ya?ml\n([\s\S]*?)```/.exec(text.slice(start));
  if (!fence) return null;
  const obj = {};
  for (const line of fence[1].split('\n')) {
    const m = /^(\w+):\s*(.*?)\s*$/.exec(line);
    if (!m) continue;
    let v = m[2];
    if (v === 'null' || v === '') v = null;
    else if (v === 'true') v = true;
    else if (v === 'false') v = false;
    else if (/^-?\d+(\.\d+)?$/.test(v)) v = Number(v);
    else if (v.startsWith('[') && v.endsWith(']')) {
      try {
        v = JSON.parse(v);
      } catch {
        v = v.slice(1, -1).split(',').map(s => Number(s.trim())).filter(n => !isNaN(n));
      }
    }
    else v = v.replace(/^["']|["']$/g, '');
    obj[m[1]] = v;
  }
  return obj;
}

// 只取主报告（001-xxx-日期.md），排除 -deep / -negotiate 附录报告，避免同一编号重复计数。
// 强约束（ADR-0002）：provenance === 'void' 的作废报告默认对所有消费方不可见——
// 新增数据消费入口时不要自行 opt-in；确需审计作废数据时才显式传 includeVoid: true。
export async function collectReports(reportsDir, { includeVoid = false } = {}) {
  const files = (await readdir(reportsDir).catch(() => []))
    .filter(f => /^\d{3}-.+\.md$/.test(f))
    .filter(f => !/-(deep|negotiate)\.md$/.test(f));
  const rows = [];
  for (const f of files) {
    const text = await readFile(join(reportsDir, f), 'utf8');
    const ms = parseMachineSummary(text);
    if (ms) rows.push({ file: f, provenance: 'legacy', ...ms });
  }
  return includeVoid ? rows : rows.filter(r => r.provenance !== 'void');
}

// ---------- Watchlist（markdown 表格） ----------
// 列结构 SoT：modes/watchlist.md。无状态列——交易状态跟踪已移除（ADR-0001）。
// 真实性三态（ADR-0002）：备注首标记 ⛔=作废/虚构、⚠️=存疑未核实、✅=已实采验证；无标记=legacy（幻觉批次前的旧数据，按存疑对待）

export function authenticityFromNote(note = '') {
  const t = String(note ?? '').trim();
  if (t.startsWith('⛔')) return 'void';
  if (t.startsWith('⚠️')) return 'suspect';
  if (t.startsWith('✅')) return 'verified';
  return 'legacy';
}

// 真实性折叠唯一出口（ADR-0002）：watchlist 备注首标记是 SoT；无 watchlist 行时回落报告
// Machine Summary 的 provenance；两者皆无 → legacy（按存疑对待，绝不静默升为 verified）。
// 消费方（map/dashboard/页面）一律经此函数取真实性，不得自行折叠。
export function effectiveProvenance(report, watchRow) {
  if (watchRow) return watchRow.authenticity ?? 'legacy';
  const p = report?.provenance;
  return p === 'verified' || p === 'suspect' || p === 'void' ? p : 'legacy';
}

export async function parseWatchlist(watchlistPath, { includeVoid = false } = {}) {
  if (!(await readFile(watchlistPath, 'utf8').catch(() => null))) return null;
  const lines = (await readFile(watchlistPath, 'utf8')).split('\n');
  const rows = [];
  for (const line of lines) {
    if (!line.startsWith('|') || line.includes('---') || line.includes('编号')) continue;
    // [| 空, 编号, 小区, 城市板块, 类型, 总价, Global, 风险, 首次, 最近, 备注, 空](尾空)
    const c = line.split('|').map(x => x.trim());
    if (!/^\d{3}$/.test(c[1] ?? '')) continue;
    const note = c[10] ?? '';
    rows.push({
      no: c[1], community: c[2] ?? '', district: c[3] ?? '', type: c[4] ?? '',
      price: c[5] ?? '', score: c[6] ?? '', risk: c[7] ?? '',
      note,
      authenticity: authenticityFromNote(note),
    });
  }
  // 强约束（ADR-0002）：⛔作废行默认对所有消费方不可见（历史记录保留在文件里）
  return includeVoid ? rows : rows.filter(r => r.authenticity !== 'void');
}

// 读取单套房源报告详情
export async function readReportDetail(reportsDir, reportNo) {
  const files = (await readdir(reportsDir).catch(() => []))
    .filter(f => f.startsWith(`${reportNo}-`) && f.endsWith('.md') && !f.includes('-deep') && !f.includes('-negotiate'));
  if (!files.length) return null;
  const filePath = join(reportsDir, files[0]);
  const text = await readFile(filePath, 'utf8');
  const urlMatch = /https?:\/\/[^\s)\"'>]+/i.exec(text);
  const url = urlMatch ? urlMatch[0] : null;
  return { file: files[0], filePath, text, url };
}


