/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * sales-commission-tier-check.js —— 阶梯提成与销售业绩核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月发提成之前**。销售的提成要按一条链逐人算出来 ——
 *   业绩额 → 扣掉退货与未回款 → 提成基数 → 命中阶梯档位的适用比例 → 提成金额 → 扣减项 → 实发。
 * 这条链上任何一环抄错，直接变成销售的收入和公司的销售费用；发错一次就影响士气，多发一次就是成本。
 * 全程只有算术与字符串比对，**完全能算出对错**，不需要任何主观判断。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   提成基数 = 业绩额 − 退货金额 − 未回款部分
 *   提成金额 = 提成基数 × 适用比例
 *   合计行   = 各明细行逐列相加
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**各家的阶梯表：档位与比例按内置**参考阶梯**（见 TIER_LADDER）核对，
 *    只用来发现「比例与档位明显对不上」；与实际制度不同时**以本单位制度为准**。
 */

const CHECKS_GIVEN = [
  '提成基数勾稽（业绩额 − 退货金额 − 未回款部分 = 提成基数）',
  '提成金额勾稽（提成基数 × 适用比例 = 提成金额）',
  '合计行逐列复核',
  '同一销售同一期重复行检测',
  '空白与占位符检测',
  '业绩或金额为负检测',
];

const CHECKS_WITHHELD = [
  '比例与阶梯档位不匹配（落错档）检测',
  '提成超过业绩额（比例超过 100%）提示',
  '未回款部分仍计提成提示',
  '同一人跨期业绩重复提示',
  '实发为负（扣减项超过提成金额）提示',
];

const OUT_OF_SCOPE = [
  '判断各家的阶梯档位划分与提成比例是否合理（各公司制度不同，请以本单位提成制度与审批口径为准）',
  '核对业绩额本身的确认口径（是否含税、按发货还是按验收、跨月退货怎么冲）',
  '处理提成预支、跨期调整与离职人员提成结算的账务处理',
  '读取 ERP / 工资 / 提成系统导出的文件（需要你先导出成文本贴进来）',
];

/* 参考阶梯：仅供「比例与档位对不上」时提示；本单位制度不同时一律以制度为准 */
const TIER_LADDER = [
  { index: 1, label: '第一档', min: 0, max: 100000, rate: 0.03 },
  { index: 2, label: '第二档', min: 100000, max: 300000, rate: 0.05 },
  { index: 3, label: '第三档', min: 300000, max: Infinity, rate: 0.08 },
];

const SAMPLE_TEXT = [
  '期间\t销售姓名\t业绩额\t退货金额\t未回款部分\t提成基数\t提成比例\t阶梯档位\t提成金额\t扣减项\t实发提成',
  '2026-01\t张伟\t80000.00\t0.00\t10000.00\t70000.00\t3%\t第一档\t2100.00\t0.00\t2100.00',
  '2026-02\t李娜\t180000.00\t5000.00\t25000.00\t150000.00\t5%\t第二档\t7500.00\t500.00\t7000.00',
  '2026-03\t王强\t360000.00\t0.00\t60000.00\t300000.00\t8%\t第三档\t24000.00\t0.00\t24000.00',
  '合计\t\t620000.00\t5000.00\t95000.00\t520000.00\t\t\t33600.00\t500.00\t33100.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名排在更宽泛的前面。
  //    「销售」这个宽泛别名必须让「销售业绩 / 销售额」先被 performance 认走；
  //    「提成」这个宽泛别名必须让「提成基数 / 提成比例 / 提成金额 / 实发提成」先被各自认走。
  period: ['期间', '所属期', '结算期', '月份'],
  performance: ['业绩额', '业绩金额', '销售业绩', '销售额', '业绩'],
  sales: ['销售姓名', '销售人员', '销售员', '业务员', '姓名', '销售'],
  returns: ['退货金额', '退货额', '退货'],
  unpaid: ['未回款部分', '未回款金额', '未回款'],
  base: ['提成基数', '计提基数', '基数'],
  rate: ['提成比例', '适用比例', '提成率', '比例'],
  tier: ['阶梯档位', '档位', '阶梯'],
  net: ['实发提成', '实发金额', '实发'],
  commission: ['提成金额', '应发提成', '提成'],
  deduction: ['扣减项', '扣减金额', '扣款', '扣减'],
};

const LABELS = {
  period: '期间', sales: '销售姓名', performance: '业绩额', returns: '退货金额',
  unpaid: '未回款部分', base: '提成基数', rate: '提成比例', tier: '阶梯档位',
  commission: '提成金额', deduction: '扣减项', net: '实发提成',
};

const REQUIRED = ['period', 'sales', 'performance', 'returns', 'unpaid', 'base', 'rate', 'commission'];
const SUM_ROLES = ['performance', 'returns', 'unpaid', 'base', 'commission', 'deduction', 'net'];
const NEG_ROLES = ['performance', 'returns', 'unpaid', 'base', 'commission'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|全年合计|季度合计)$/;

const CN_DIGITS = { 一: 1, 二: 2, 三: 3, 四: 4, 五: 5, 六: 6, 七: 7, 八: 8, 九: 9, 十: 10 };

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|--)$/i.test(s);
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

/** 比例归一化成小数：`5%` ⇒ 0.05；`0.05` ⇒ 0.05；`5` ⇒ 0.05 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

/** 把「第一档 / 1档 / 档2」这类写法归一成档位序号；认不出返回 null（认不出就不下结论） */
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

const who = (it) => (it && it.sales
  ? `${String(it.sales).trim()}（第 ${it.line} 行）`
  : `第 ${it.line} 行`);

function uniqPeriods(items) {
  const seen = new Set();
  for (const it of items) {
    const p = String(it.period === undefined || it.period === null ? '' : it.period).trim();
    if (p) seen.add(p);
  }
  return seen.size;
}

/* ================================ 免费档检查项 ================================ */

function checkBase(it) {
  const perf = normNumber(it.performance);
  const ret = normNumber(it.returns);
  const unpaid = normNumber(it.unpaid);
  const stated = normNumber(it.base);
  if (perf === null || ret === null || unpaid === null || stated === null) return null;
  const expect = round2(perf - ret - unpaid);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '提成基数与业绩勾稽不符', line: it.line,
    message: `${who(it)}：业绩额 ${perf.toFixed(2)} − 退货 ${ret.toFixed(2)} − 未回款 ${unpaid.toFixed(2)} = ${expect.toFixed(2)}，`
      + `但表里的提成基数是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkCommission(it) {
  const base = normNumber(it.base);
  const rate = rateValue(it.rate);
  const stated = normNumber(it.commission);
  if (base === null || rate === null || stated === null) return null;
  const expect = round2(base * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '提成金额与基数比例不符', line: it.line,
    message: `${who(it)}：提成基数 ${base.toFixed(2)} × 适用比例 ${(rate * 100).toFixed(3)}% = ${expect.toFixed(2)}，`
      + `但表里的提成金额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkNegative(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '业绩或金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回或调整建议单独列示并注明原因，`
          + '混进正常行会让整条提成链跟着错。',
      });
    }
  }
  return out;
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const name = String(it.sales === undefined || it.sales === null ? '' : it.sales).trim();
    const period = String(it.period === undefined || it.period === null ? '' : it.period).trim();
    if (!name || !period) continue;
    const key = period + '::' + name;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一销售同一期重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过（${period} 期）—— 提成会被重复计算，请先合并或删除重复行。`,
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
    return insufficient('没有收到提成表正文（text）—— 请把「期间 / 销售姓名 / 业绩额 / 退货金额 / 未回款部分 / 提成基数 / 提成比例 / 提成金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `提成表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何销售提成明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkBase(it); if (a) findings.push(a);
    const b = checkCommission(it); if (b) findings.push(b);
    for (const x of checkNegative(it)) findings.push(x);

  }

  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const rows = t.items.length;
  const periods = uniqPeriods(t.items);
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const result = {
    status: 'success',
    service_type: 'SALES_COMMISSION_TIER_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows,
      periods,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows,
      periods,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核「业绩额 − 退货 − 未回款 = 提成基数」「提成基数 × 适用比例 = 提成金额」这类表内勾稽，'
      + '**不规定**各家的阶梯档位与比例（参考阶梯仅供自查，以本单位提成制度为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
