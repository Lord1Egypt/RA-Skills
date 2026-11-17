/**
 * late-fee-check.js —— 税款滞纳金计算核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**补缴税款时**（自查补报、稽查补税、申报后发现少缴），
 * 财务要按"滞纳税额 × 万分之五 × 滞纳天数"算滞纳金并一次性缴清；
 * 计错天数或比例就是**真金白银**的差错，而且完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   滞纳金   = 滞纳税额 × 日加收率 × 滞纳天数
 *   滞纳天数 = 实际缴纳日期 − 税款限缴日期（按日差）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**日加收率（法定为万分之五即 0.05%/日，表里给的为准，只在明显偏离时提示）。
 */

const CHECKS_GIVEN = [
  '滞纳金复算（滞纳税额 × 日加收率 × 滞纳天数）',
  '滞纳天数与日期差一致（实际缴纳日期 − 税款限缴日期）',
  '合计行逐列复核',
  '同一税种同一所属期重复检测',
  '空白与占位符检测',
  '滞纳税额为负或为零检测',
];

const CHECKS_WITHHELD = [
  '日加收率偏离法定万分之五（0.05%/日）提示（参考口径）',
  '限缴日期晚于或等于实际缴纳日期却仍计滞纳金检测',
  '滞纳金为负检测',
  '滞纳天数超过 3650 天（约 10 年）异常提示',
  '滞纳金与滞纳税额之比超过 100% 提示（长期滞纳的常见信号）',
];

const OUT_OF_SCOPE = [
  '判断滞纳义务的起算日（是否批准延期、是否属于税务机关责任、能否免除）',
  '处理税收征管法与我省口径下的减免、退还、行政复议与诉讼',
  '计算税款本身的应纳税额（那是申报环节的事）',
  '读取电子税务局导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '税种\t税款所属期\t滞纳税额\t税款限缴日期\t实际缴纳日期\t滞纳天数\t日加收率\t滞纳金',
  '增值税\t2026-03\t48200.00\t2026-04-20\t2026-05-10\t20\t0.05%\t482.00',
  '企业所得税\t2025年度\t120000.00\t2026-05-31\t2026-06-15\t15\t0.05%\t900.00',
  '合计\t\t168200.00\t\t\t\t\t1382.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.00002;
const STATUTORY_RATE = 0.0005;
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

const ROLES = {
  taxType: ['税种', '税目', '税费种类'],
  period: ['税款所属期', '所属期', '所属期间'],
  taxDue: ['滞纳税额', '欠缴税额', '滞纳本金'],
  deadline: ['税款限缴日期', '限缴日期', '缴款期限', '限缴日'],
  paidDate: ['实际缴纳日期', '缴纳日期', '实际缴款日期', '缴款日期'],
  days: ['滞纳天数', '逾期天数', '滞纳日数'],
  rate: ['日加收率', '滞纳金比例', '加收率'],
  penalty: ['滞纳金', '滞纳金金额', '加收滞纳金'],
};

const LABELS = {
  taxType: '税种', period: '税款所属期', taxDue: '滞纳税额', deadline: '税款限缴日期',
  paidDate: '实际缴纳日期', days: '滞纳天数', rate: '日加收率', penalty: '滞纳金',
};

const REQUIRED = ['taxDue', 'deadline', 'paidDate', 'days', 'penalty'];
const SUM_ROLES = ['taxDue', 'days', 'penalty'];

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  if (s.endsWith('%')) s = s.slice(0, -1);
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

function rateValue(raw) {
  const n = normNumber(raw);
  if (n === null) return null;
  return String(raw).indexOf('%') >= 0 ? n / 100 : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const who = (it) => `${String(it.taxType || '').trim()}${it.period ? ' ' + String(it.period).trim() : ''}`.trim() || `第 ${it.line} 行`;

function daysBetween(a, b) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(a) || !/^\d{4}-\d{2}-\d{2}$/.test(b)) return null;
  const d1 = Date.UTC(+a.slice(0, 4), +a.slice(5, 7) - 1, +a.slice(8, 10));
  const d2 = Date.UTC(+b.slice(0, 4), +b.slice(5, 7) - 1, +b.slice(8, 10));
  return Math.round((d2 - d1) / 86400000);
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [] };
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const missingColumns = REQUIRED.filter((r) => !cols.some((c) => c.role === r));
  const items = [];
  const totals = {};
  for (let li = 1; li < lines.length; li += 1) {
    const cells = splitRow(lines[li]);
    const row = { line: li + 1 };
    cols.forEach((c) => { if (c.role) row[c.role] = cells[c.i] === undefined ? '' : cells[c.i]; });
    const label = (cells[0] || '').replace(/\s/g, '');
    if (TOTAL_WORDS.test(label)) { totals.line = li + 1; totals.row = row; continue; }
    items.push(row);
  }
  return { items, totals, missingColumns, header };
}

/* ================================ 免费档检查项 ================================ */

function checkPenalty(it) {
  const due = normNumber(it.taxDue); const days = normNumber(it.days);
  const rate = rateValue(it.rate); const pen = normNumber(it.penalty);
  if (due === null || days === null || pen === null) return null;
  if (rate === null) return null;
  const want = round2(due * rate * days);
  if (Math.abs(want - pen) > Math.max(TOL, Math.abs(want) * 0.000001)) {
    return {
      line: it.line, level: 'P0', category: '滞纳金复算',
      message: `${who(it)} 滞纳金 ${pen} ≠ 滞纳税额 ${due} × 日加收率 ${(rate * 100).toFixed(3)}% × ${days} 天 = ${want}`,
      evidence: `滞纳税额=${due}；日加收率=${rate}；滞纳天数=${days}；滞纳金=${pen}；应为 ${want}`,
    };
  }
  return null;
}

function checkDaysVsDates(it) {
  const d = daysBetween(String(it.deadline || '').trim(), String(it.paidDate || '').trim());
  const days = normNumber(it.days);
  if (d === null || days === null) return null;
  if (d !== days) {
    return {
      line: it.line, level: 'P0', category: '滞纳天数与日期不符',
      message: `${who(it)} 填的滞纳天数 ${days} 天，但按日期算应为 ${d} 天（限缴 ${it.deadline} → 实缴 ${it.paidDate}）`,
      evidence: `限缴日期=${it.deadline}；实际缴纳日期=${it.paidDate}；填报天数=${days}；应为 ${d}`,
    };
  }
  return null;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const declared = normNumber(totals.row[role]);
  if (declared === null) return out;
  let sum = 0; let n = 0;
  for (const it of items) { const v = normNumber(it[role]); if (v !== null) { sum += v; n += 1; } }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(sum - declared) > TOL) {
    out.push({
      line: totals.line, level: 'P1', category: '合计复核',
      message: `合计行「${LABELS[role]}」填 ${declared}，但明细逐行相加是 ${sum}`,
      evidence: `合计=${declared}；明细合计=${sum}（${n} 行）`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = []; const seen = new Map();
  for (const it of items) {
    const k = `${String(it.taxType || '').trim()}|${String(it.period || '').trim()}`;
    if (k === '|') continue;
    if (seen.has(k)) {
      out.push({
        line: it.line, level: 'P1', category: '重复税种期间',
        message: `${who(it)} 重复出现（第 ${seen.get(k)} 行与第 ${it.line} 行）`,
        evidence: `键=${k}；首次出现在第 ${seen.get(k)} 行`,
      });
    } else seen.set(k, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  const watch = ['taxDue', 'deadline', 'paidDate', 'days', 'penalty'];
  for (const it of items) {
    const miss = watch.filter((r) => isBlank(it[r]));
    if (miss.length) {
      out.push({
        line: it.line, level: 'P1', category: '空白字段',
        message: `${who(it)} 有 ${miss.length} 个关键字段没填：${miss.map((r) => LABELS[r]).join('、')}`,
        evidence: `缺失列=${miss.map((r) => LABELS[r]).join('、')}`,
      });
    }
  }
  return out;
}

function checkTaxDueValue(it) {
  const due = normNumber(it.taxDue);
  if (due === null) return null;
  if (due < 0) {
    return {
      line: it.line, level: 'P0', category: '滞纳税额异常',
      message: `${who(it)} 滞纳税额为负数 ${due}`,
      evidence: `滞纳税额=${due}`,
    };
  }
  if (due === 0) {
    return {
      line: it.line, level: 'P1', category: '滞纳税额异常',
      message: `${who(it)} 滞纳税额为 0 —— 没有滞纳税额就不应产生滞纳金`,
      evidence: '滞纳税额=0',
    };
  }
  return null;
}

/* ====================== 完整档（付费）检查项（不进免费包） ====================== */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到滞纳金计算表正文（text）—— 请把「税种 / 所属期 / 滞纳税额 / 限缴日期 / 实缴日期 / 滞纳天数 / 日加收率 / 滞纳金」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `滞纳金计算表缺少必需列：${t.missingColumns.map((r) => LABELS[r]).join('、')}`,
      `已识别的表头：${splitRow(String(text).split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) return insufficient('表里只有表头，没有任何税种明细行');

  const findings = [];
  for (const it of t.items) {
    const a = checkPenalty(it); if (a) findings.push(a);
    const b = checkDaysVsDates(it); if (b) findings.push(b);
    const c = checkTaxDueValue(it); if (c) findings.push(c);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let dueTotal = 0; let penTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.taxDue); if (a !== null) dueTotal += a;
    const b = normNumber(it.penalty); if (b !== null) penTotal += b;
  }

  return {
    status: 'success',
    result: {
      status: 'success',
      service_type: 'LATE_FEE_CHECK',
      scope: {
        checks: CHECKS_GIVEN.slice(),
        checks_not_run: notRun,
        rows: t.items.length,
        tax_due_total: round2(dueTotal),
        penalty_total: round2(penTotal),
        statutory_rate_ref: STATUTORY_RATE,
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
      findings,
      summary: {
        rows: t.items.length,
        total: findings.length,
        p0, p1, p2,
        verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
        omitted: 0,
      },
      checks_out_of_scope: OUT_OF_SCOPE,
      note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
      disclaimer: '只核"滞纳税额 × 日加收率 × 滞纳天数 = 滞纳金""天数与日期差一致"这类内部勾稽；'
        + '**不判断滞纳义务起算与减免**（以主管税务机关口径为准）；结论可由第三方用同一份输入复算。',
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, daysBetween, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
