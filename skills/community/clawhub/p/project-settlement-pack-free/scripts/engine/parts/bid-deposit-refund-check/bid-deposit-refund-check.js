/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * bid-deposit-refund-check.js —— 投标保证金收退核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**投标/财务在开标后与合同签订后核对保证金收退台账** ——
 * 保证金是按投标报价的一定比例（工程招投标常见 ≤2%）真金白银交出去的：
 * 收多了占用资金、退晚了供应商投诉、退少了要补款，每个月都要对一遍。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应缴保证金 = 投标报价 × 保证金比例
 *   差额       = 实缴保证金 − 应缴保证金
 *   退还差额   = 退还金额 − 实缴保证金
 *
 * 比例填写口径（**必须写清楚，否则算出来是错的**）：
 *   可写 `2`、`2%`（按 2% 理解），也可写 `0.02`（比例，同样 2%）；
 *   判据：带 `%` 或数值 > 0.1 时按百分数，否则按比例。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 */

const CHECKS_GIVEN = [
  '应缴保证金勾稽（投标报价 × 保证金比例）',
  '实缴与应缴差额检测',
  '退还金额与实缴差额检测',
  '合计行逐列复核',
  '重复投标人检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '保证金比例超出常见区间（0.5% ~ 2%）检测',
  '日期倒挂检测（应退/退还日期早于缴款日期）',
  '逾期未退与逾期天数检测',
  '退还金额为负或超过实缴检测',
  '投标报价非正或保证金为负检测',
];

const OUT_OF_SCOPE = [
  '判断保证金比例是否合法（招标文件约定优先；各地规定不同）',
  '计算逾期退还的利息或资金占用费（需要合同或招标文件约定的利率）',
  '处理银行保函、保险保单形式的保证金（本表只核现金缴纳）',
  '读取 .xlsx 或财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '投标人\t项目名称\t投标报价\t保证金比例\t应缴保证金\t实缴保证金\t缴款日期\t应退日期\t退还日期\t退还金额',
  '豫州第一建筑工程有限公司\t市政道路工程\t1286400.00\t2%\t25728.00\t25728.00\t2026-03-01\t2026-04-10\t2026-04-08\t25728.00',
  '中岳路桥工程股份有限公司\t市政道路工程\t1412900.00\t2%\t28258.00\t28258.00\t2026-03-02\t2026-04-10\t2026-04-09\t28258.00',
  '豫通市政建设集团有限公司\t市政道路工程\t1351250.00\t2%\t27025.00\t27025.00\t2026-03-02\t2026-04-10\t2026-04-09\t27025.00',
].join('\n');

const TOL = 0.01;
const RATE_MIN = 0.005;      // 0.5%
const RATE_MAX = 0.02;       // 2%

const ROLES = {
  // ⚠️ 顺序即优先级，更具体的别名在前 —— 不能让「应缴保证金」被宽泛词抢走
  party: ['投标人', '供应商', '投标单位', '单位名称'],
  project: ['项目名称', '标段名称', '项目'],
  bid: ['投标报价', '中标价', '报价金额', '报价'],
  rate: ['保证金比例', '保证金率', '比例'],
  due: ['应缴保证金', '应缴金额', '应缴'],
  paidIn: ['实缴保证金', '已缴保证金', '实缴', '已缴'],
  payDate: ['缴款日期', '缴纳日期', '付款日期', '缴款日'],
  refundDue: ['应退日期', '应退期限', '应退日'],
  refundDate: ['退还日期', '退款日期', '退还日'],
  refundAmt: ['退还金额', '退款金额', '退还额'],
};

const LABELS = {
  party: '投标人', project: '项目名称', bid: '投标报价', rate: '保证金比例',
  due: '应缴保证金', paidIn: '实缴保证金', payDate: '缴款日期',
  refundDue: '应退日期', refundDate: '退还日期', refundAmt: '退还金额',
};

const REQUIRED = ['party', 'bid', 'rate', 'due', 'paidIn'];
const SUM_ROLES = ['bid', 'due', 'paidIn', 'refundAmt'];
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

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
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;

/** 比例归一化成小数：`2` / `2%` ⇒ 0.02；`0.02` ⇒ 0.02 */
function rateRatio(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return n > 0.1 ? n / 100 : n;
}

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (role === 'party' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.party ? String(it.party) : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkDueCalc(it) {
  const bid = normNumber(it.bid);
  const rate = rateRatio(it.rate);
  const stated = normNumber(it.due);
  if (bid === null || rate === null || stated === null) return null;
  const expect = round2(bid * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应缴保证金与复算不符', line: it.line,
    message: `${who(it)}的应缴保证金是 ${stated.toFixed(2)}，按 投标报价 ${bid.toFixed(2)} × 比例 ${(rate * 100).toFixed(2)}% 应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkPaidInDiff(it) {
  const due = normNumber(it.due);
  const paidIn = normNumber(it.paidIn);
  if (due === null || paidIn === null || Math.abs(paidIn - due) <= TOL) return null;
  return {
    level: 'P0', category: '实缴与应缴之差不为零', line: it.line,
    message: `${who(it)}的实缴保证金是 ${paidIn.toFixed(2)}，应缴是 ${due.toFixed(2)}，相差 ${round2(paidIn - due).toFixed(2)}（正数=多缴，负数=少缴）。`,
  };
}

function checkRefundDiff(it) {
  const paidIn = normNumber(it.paidIn);
  const refund = normNumber(it.refundAmt);
  if (paidIn === null || refund === null) return null;
  if (Math.abs(refund - paidIn) <= TOL) return null;
  return {
    level: 'P1', category: '退还金额与实缴之差不为零', line: it.line,
    message: `${who(it)}的退还金额是 ${refund.toFixed(2)}，实缴是 ${paidIn.toFixed(2)}，相差 ${round2(refund - paidIn).toFixed(2)}；若确有扣款（如违约金），请在台账里写明扣款依据。`,
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) sum += v;
  }
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const name = String(it.party || '').trim();
    if (!name) continue;
    const key = `${name}|${String(it.project || '').trim()}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一投标人同一项目出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现（可能是重复入账或标段未区分）。`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
        });
      }
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到台账正文（text）—— 请把含表头的表格贴进来');
  }
  const t = parseTable(text);
  // ⚠️ 空数组在 JS 里是**真值**：`if ([])` 会成立 —— 必须判长度，否则「没缺列」也会被当成缺列。
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账表头缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何投标人明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkDueCalc(it); if (a) findings.push(a);
    const b = checkPaidInDiff(it); if (b) findings.push(b);
    const c = checkRefundDiff(it); if (c) findings.push(c);

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

  let paidTotal = 0;
  let refundTotal = 0;
  for (const it of t.items) {
    const d = normNumber(it.paidIn); if (d !== null) paidTotal += d;
    const r = normNumber(it.refundAmt); if (r !== null) refundTotal += r;
  }

  const result = {
    status: 'success',
    service_type: 'BID_DEPOSIT_REFUND_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      paid_in_total: round2(paidTotal),
      refunded_total: round2(refundTotal),
      outstanding_total: round2(paidTotal - refundTotal),
      rate_convention: '比例可写 2 / 2% / 0.02，均按 2% 理解',
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
    disclaimer: '只核对台账内部一致性与常见口径，不判断保证金比例是否合法、不计算逾期利息；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateRatio, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
