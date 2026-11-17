/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * welfare-limit-check-full.js —— 职工福利费与教育经费限额核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月计提及每年汇算清缴前**，财务要把「职工福利费 / 职工教育经费 /
 * 工会经费」三项与**工资总额**的税前扣除上限对一遍 —— 福利费 14%、教育经费 8%、工会经费 2%。
 * 超支的部分要做**纳税调整**（调增应纳税所得额），算错会直接把税报错。完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   职工福利费限额   = 工资总额 × 14%
 *   职工教育经费限额 = 工资总额 × 8%
 *   工会经费限额     = 工资总额 × 2%
 *   实际发生额 > 税前扣除限额 ⇒ 超支部分需做纳税调整（本工具只提示，不判断调整年度）
 *   职工教育经费结转下年 ≤ 限额余额（限额 − 实际发生额）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 法定比例（14% / 8% / 2%）是**参考口径**：以现行税收法规与主管税务机关口径为准，
 *    本工具只做复算与提示，不替谁认定税务处理。
 */

const CHECKS_GIVEN = [
  '职工福利费限额复算（工资总额 × 14% = 税前扣除限额）',
  '职工教育经费限额复算（工资总额 × 8% = 税前扣除限额）',
  '合计行逐列复核',
  '同一费用类型重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '实际发生额超过税前扣除限额提示（含超支金额与纳税调整方向）',
  '工会经费超过工资总额 2% 提示',
  '工资总额为零却有计提检测',
  '职工教育经费结转下年金额超过限额余额提示',
  '计提比例偏离法定参考口径提示',
];

const OUT_OF_SCOPE = [
  '判断超支部分在哪一年度做纳税调整、如何填报 A105050 等明细表（以主管税务机关口径为准）',
  '核对工资总额本身的组成口径（是否含奖金、津贴、劳务派遣、离职补偿）',
  '处理教育经费结转扣除的年限条件与专项用途认定',
  '读取财务软件或申报系统导出文件（需要你先导出成文本贴进来）',
];

/* 法定参考比例：14% / 8% / 2%（参考口径，以现行税收法规为准） */
const STATUTORY_RATES = { welfare: 0.14, education: 0.08, union: 0.02 };

const KIND_LABELS = { welfare: '职工福利费', education: '职工教育经费', union: '工会经费' };

const SAMPLE_TEXT = [
  '期间\t费用类型\t工资总额\t计提比例\t计提金额\t实际发生额\t税前扣除限额\t结转下年金额',
  '2026-01\t职工福利费\t1200000.00\t14%\t168000.00\t150000.00\t168000.00\t0.00',
  '2026-01\t职工教育经费\t1200000.00\t8%\t96000.00\t70000.00\t96000.00\t26000.00',
  '2026-01\t工会经费\t1200000.00\t2%\t24000.00\t24000.00\t24000.00\t0.00',
  '2026-02\t职工福利费\t1180000.00\t14%\t165200.00\t160000.00\t165200.00\t0.00',
  '2026-02\t职工教育经费\t1180000.00\t8%\t94400.00\t90000.00\t94400.00\t4400.00',
  '2026-02\t工会经费\t1180000.00\t2%\t23600.00\t23600.00\t23600.00\t0.00',
  '2026-03\t职工福利费\t1350000.00\t14%\t189000.00\t170000.00\t189000.00\t0.00',
  '2026-03\t职工教育经费\t1350000.00\t8%\t108000.00\t95000.00\t108000.00\t13000.00',
  '2026-03\t工会经费\t1350000.00\t2%\t27000.00\t27000.00\t27000.00\t0.00',
  '合计\t\t\t\t895200.00\t809600.00\t895200.00\t43400.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  //    （「税前扣除限额」不能被「比例」抢走；「计提金额」不能被「计提比例」抢走）
  period: ['会计期间', '所属期间', '期间', '月份', '所属期', '年度'],
  feeType: ['费用类型', '费用类别', '费用项目', '支出类型', '费用种类', '类型'],
  wageTotal: ['工资总额', '工资薪金总额', '计税工资总额', '薪金总额'],
  accrualRate: ['计提比例', '计提比率', '扣除比例', '计提率', '比例'],
  accrued: ['计提金额', '已计提金额', '计提额', '本期计提'],
  actual: ['实际发生额', '实际发生金额', '实际支出', '实际发生', '发生额'],
  limit: ['税前扣除限额', '扣除限额', '税前限额', '限额'],
  carryover: ['结转下年金额', '结转下年', '结转以后年度', '结转金额', '结转'],
};

const LABELS = {
  period: '期间', feeType: '费用类型', wageTotal: '工资总额', accrualRate: '计提比例',
  accrued: '计提金额', actual: '实际发生额', limit: '税前扣除限额', carryover: '结转下年金额',
};

const REQUIRED = ['period', 'feeType', 'wageTotal', 'accrued', 'actual', 'limit'];
/* 合计行只复核**可加**的列：工资总额在「一期多种费用」的行结构里会重复出现，相加无意义 */
const SUM_ROLES = ['accrued', 'actual', 'limit', 'carryover'];
const NEG_ROLES = ['accrued', 'actual', 'limit', 'carryover'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|全年合计)$/;

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

/** 比率归一化成小数：`14%` ⇒ 0.14；`0.14` ⇒ 0.14；`14` ⇒ 0.14 */
/** 费用类型归一化：`职工福利费` / `福利费` ⇒ welfare；教育 ⇒ education；工会 ⇒ union */
function feeKind(raw) {
  const s = String(raw === undefined || raw === null ? '' : raw).replace(/[\s（）()]/g, '');
  if (!s) return null;
  if (s.indexOf('福利') >= 0) return 'welfare';
  if (s.indexOf('教育') >= 0) return 'education';
  if (s.indexOf('工会') >= 0) return 'union';
  return null;
}

const round2 = (n) => Math.round(n * 100) / 100;

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
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.period
  ? `${String(it.period).trim()}「${String(it.feeType === undefined ? '' : it.feeType).trim() || '未注费用类型'}」`
  : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

/** 免费 1：职工福利费限额 = 工资总额 × 14% */
function checkWelfareLimit(it) {
  const out = [];
  if (feeKind(it.feeType) !== 'welfare') return out;
  const wage = normNumber(it.wageTotal);
  const limit = normNumber(it.limit);
  if (wage === null || limit === null) return out;
  const expect = round2(wage * STATUTORY_RATES.welfare);
  if (Math.abs(expect - limit) <= TOL) return out;
  out.push({
    level: 'P0', category: '职工福利费限额与工资总额 14% 复算不符', line: it.line,
    message: `${who(it)}：工资总额 ${wage.toFixed(2)} × 14% 应为 ${expect.toFixed(2)}，表里的税前扣除限额是 ${limit.toFixed(2)}，相差 ${round2(limit - expect).toFixed(2)}。`,
  });
  return out;
}

/** 免费 2：职工教育经费限额 = 工资总额 × 8% */
function checkEducationLimit(it) {
  const out = [];
  if (feeKind(it.feeType) !== 'education') return out;
  const wage = normNumber(it.wageTotal);
  const limit = normNumber(it.limit);
  if (wage === null || limit === null) return out;
  const expect = round2(wage * STATUTORY_RATES.education);
  if (Math.abs(expect - limit) <= TOL) return out;
  out.push({
    level: 'P0', category: '职工教育经费限额与工资总额 8% 复算不符', line: it.line,
    message: `${who(it)}：工资总额 ${wage.toFixed(2)} × 8% 应为 ${expect.toFixed(2)}，表里的税前扣除限额是 ${limit.toFixed(2)}，相差 ${round2(limit - expect).toFixed(2)}。`,
  });
  return out;
}

/** 免费 3：合计行逐列复核（可加列逐列与明细之和比对） */
function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

/** 免费 4：同一费用类型重复行检测（同一期间 + 同一费用类型出现两次 ⇒ 计提会被重复计算） */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = String(it.period === undefined || it.period === null ? '' : it.period).trim();
    const k = String(it.feeType === undefined || it.feeType === null ? '' : it.feeType).trim();
    if (!p && !k) continue;
    const key = `${p}|${k}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一费用类型重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 同一期间的同一项费用被计了两次，限额与超支都会算错。`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 免费 5：空白与占位符检测（必需列） */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 缺了它这一项的限额就核不了。`,
        });
      }
    }
  }
  return out;
}

/** 免费 6：金额为负检测 */
function checkNegatives(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回或红字请单独列示，别混在计提里。`,
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 完整档 1：实际发生额超过税前扣除限额（含超支金额与纳税调整方向） */
/** 完整档 2：工会经费超过工资总额 2% */
/** 完整档 3：工资总额为零却有计提 */
/** 完整档 4：职工教育经费结转下年金额超过限额余额（限额 − 实际发生额） */
/** 完整档 5：计提比例偏离法定参考口径（14% / 8% / 2%） */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到台账正文（text）—— 请把「期间 / 费用类型 / 工资总额 / 计提比例 / 计提金额 / 实际发生额 / 税前扣除限额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何费用明细行');
  }

  const findings = [];
  for (const it of t.items) {
    for (const f of checkWelfareLimit(it)) findings.push(f);
    for (const f of checkEducationLimit(it)) findings.push(f);
    for (const f of checkNegatives(it)) findings.push(f);

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

  const periodSet = new Set();
  for (const it of t.items) {
    const p = String(it.period === undefined || it.period === null ? '' : it.period).trim();
    if (p) periodSet.add(p);
  }

  const result = {
    status: 'success',
    service_type: 'WELFARE_LIMIT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periodSet.size,
      tolerance: TOL,
      statutory_rates: STATUTORY_RATES,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periodSet.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: '本版本只执行免费检查项；未执行的检查项见 scope.checks_not_run。',
    disclaimer: '只核「限额 = 工资总额 × 法定参考比例」「实际发生额 vs 限额」「合计 = 明细之和」这类可复算关系；'
      + '**不规定**超支部分的调整年度与申报表填法（以主管税务机关口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
