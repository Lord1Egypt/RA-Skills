/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * union-reserve-check.js —— 工会经费与残保金计提核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月（残保金按年）计提与申报前**，财务要按**工资总额**计提两项费用 ——
 * **工会经费**（一般为工资总额的 2%，其中一部分上缴、一部分留本单位工会使用）与
 * **残疾人就业保障金**（按在职职工人数、比例与社平工资计算，各地口径不同）。
 * 这两项都**直接挂在工资总额上**，算错会连锁影响费用与申报。完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   工会经费应计提 = 工资总额 × 计提比例
 *   上缴 + 留用     = 已计提（两项之和必须等于计提额）
 *   残保金应缴     = 应安排人数不足部分 × 计算标准（表里给出标准与人数）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**比例与标准（各地各企业不同）：比例、计算标准以表里给的为准，
 *    只对"明显超出常见区间"做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '工会经费计提勾稽（工资总额 × 计提比例 = 已计提）',
  '上缴与留用之和不符检测（上缴 + 留用 = 已计提）',
  '合计行逐列复核',
  '重复期间检测',
  '空白与占位符检测',
  '工资总额为负或为零检测',
];

const CHECKS_WITHHELD = [
  '工会经费比例超出常见区间（1.5%~2.5%）提示（参考口径）',
  '上缴比例为负或超过计提额检测',
  '残保金勾稽（应安排人数不足 × 计算标准 = 应缴）',
  '残保金计提与应缴不符检测',
  '留用部分超过计提额检测',
];

const OUT_OF_SCOPE = [
  '判断工会经费比例、残保金计算标准与减免政策（各地各企业不同，请以当地规定与主管机关口径为准）',
  '处理残保金按年申报、分档减缴与超比例奖励',
  '核对工资总额本身的组成口径（是否含奖金、津贴）',
  '读取个税/社保申报系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考区间：仅供"明显超出"时提示 */
const UNION_RATE_REF = [0.015, 0.025];

const SAMPLE_TEXT = [
  '期间\t工资总额\t工会经费比例\t工会经费计提\t其中上缴部分\t其中留用部分\t残保金计算标准\t残保金应缴\t残保金已计提',
  '2026-01\t1200000.00\t2%\t24000.00\t14400.00\t9600.00\t0.00\t0.00\t0.00',
  '2026-02\t1180000.00\t2%\t23600.00\t14160.00\t9440.00\t0.00\t0.00\t0.00',
  '2026-03\t1350000.00\t2%\t27000.00\t16200.00\t10800.00\t18000.00\t18000.00\t18000.00',
  '合计\t3730000.00\t\t74600.00\t44760.00\t29840.00\t18000.00\t18000.00\t18000.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「工会经费计提」不能被「工会经费比例」抢走）
  period: ['期间', '月份', '所属期', '年度'],
  wageTotal: ['工资总额', '工资薪金总额', '计税工资总额'],
  unionRate: ['工会经费比例', '工会经费率', '计提比例'],
  unionAccrued: ['工会经费计提', '工会经费', '已计提工会经费'],
  remitted: ['其中上缴部分', '上缴部分', '上缴工会经费', '上缴'],
  retained: ['其中留用部分', '留用部分', '留用工会经费', '留用'],
  disabilityStd: ['残保金计算标准', '残保金标准', '计算标准'],
  disabilityDue: ['残保金应缴', '应缴残保金', '残保金应缴额'],
  disabilityAccrued: ['残保金已计提', '已计提残保金', '残保金计提'],
};

const LABELS = {
  period: '期间', wageTotal: '工资总额', unionRate: '工会经费比例', unionAccrued: '工会经费计提',
  remitted: '其中上缴部分', retained: '其中留用部分', disabilityStd: '残保金计算标准',
  disabilityDue: '残保金应缴', disabilityAccrued: '残保金已计提',
};

const REQUIRED = ['period', 'wageTotal', 'unionRate', 'unionAccrued'];
const SUM_ROLES = ['wageTotal', 'unionAccrued', 'remitted', 'retained', 'disabilityDue', 'disabilityAccrued'];
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

/** 比率归一化成小数：`2%` ⇒ 0.02；`0.02` ⇒ 0.02；`2` ⇒ 0.02 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
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

const who = (it) => (it && it.period ? `${String(it.period).trim()} 期` : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkUnionAccrual(it) {
  const wage = normNumber(it.wageTotal);
  const rate = rateValue(it.unionRate);
  const stated = normNumber(it.unionAccrued);
  if (wage === null || rate === null || stated === null) return null;
  const expect = round2(wage * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '工会经费计提与复算不符', line: it.line,
    message: `${who(it)}：工资总额 ${wage.toFixed(2)} × 比例 ${(rate * 100).toFixed(2)}% 应为 ${expect.toFixed(2)}，表里计提是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkSplit(it) {
  const accrued = normNumber(it.unionAccrued);
  const remit = normNumber(it.remitted);
  const keep = normNumber(it.retained);
  if (accrued === null || remit === null || keep === null) return null;
  const sum = round2(remit + keep);
  if (Math.abs(sum - accrued) <= TOL) return null;
  return {
    level: 'P0', category: '上缴与留用之和不符', line: it.line,
    message: `${who(it)}：上缴 ${remit.toFixed(2)} + 留用 ${keep.toFixed(2)} = ${sum.toFixed(2)}，但计提额是 ${accrued.toFixed(2)}，相差 ${round2(sum - accrued).toFixed(2)} —— 两部分的来源就是计提额，必须相等。`,
  };
}

function checkWageRange(it) {
  const v = normNumber(it.wageTotal);
  if (v === null) return null;
  if (v < -TOL) {
    return {
      level: 'P0', category: '工资总额为负', line: it.line,
      message: `${who(it)}的工资总额是 ${v.toFixed(2)}（负数）—— 冲回建议单独列示。`,
    };
  }
  if (v <= TOL) {
    return {
      level: 'P0', category: '工资总额为零', line: it.line,
      message: `${who(it)}的工资总额是 ${v.toFixed(2)} —— 为零则两项计提都无从算起，请补齐。`,
    };
  }
  return null;
}

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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各期相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.period || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一期间出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 计提会被重复计算。`,
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
    return insufficient('没有收到计提表正文（text）—— 请把「期间 / 工资总额 / 比例 / 计提 / 上缴 / 留用」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `计提表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何期间明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkUnionAccrual(it); if (a) findings.push(a);
    const b = checkSplit(it); if (b) findings.push(b);
    const c = checkWageRange(it); if (c) findings.push(c);

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

  let unionTotal = 0; let disTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.unionAccrued); if (a !== null) unionTotal += a;
    const b = normNumber(it.disabilityAccrued); if (b !== null) disTotal += b;
  }

  const result = {
    status: 'success',
    service_type: 'UNION_RESERVE_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      periods: t.items.length,
      union_accrued_total: round2(unionTotal),
      disability_accrued_total: round2(disTotal),
      union_rate_ref: UNION_RATE_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      periods: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"工资总额 × 比例 = 计提""上缴 + 留用 = 计提"这类内部勾稽，'
      + '**不规定比例与残保金计算标准**（以当地规定为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
