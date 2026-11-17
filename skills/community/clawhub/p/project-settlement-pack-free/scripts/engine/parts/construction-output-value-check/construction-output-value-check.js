/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * construction-output-value-check.js —— 工程产值与进度确认核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月末报产值时**（工程月度产值与进度确认，甲方/监理确认后作为
 * 结算与收入确认依据），商务/财务要把「工程产值与进度确认表」核一遍：形象进度报了多少、
 * 本期已完产值、累计已完产值、本期计量金额、累计计量金额、本期扣款与应付，**必须与合同额勾稽**。
 * 这张表里的几个数**完全能算出来对错**（手算即可复现）：
 *
 *   本期计量金额        = 本期已完产值 − 本期扣款              （本期计量口径）
 *   累计计量 + 剩余产值  = 合同额                              （合同总额闭合）
 *
 * 而"形象进度该报多少"属于现场与监理的业务判断，本工具**只做提示**（偏差超 10 个百分点时提醒），
 * 不替你做结论，也不规定合同口径与扣款是否应当扣 —— 那些见 checks_out_of_scope。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**，也不套用默认值。
 */

const CHECKS_GIVEN = [
  '计量金额复算（本期计量金额 = 本期已完产值 − 本期扣款）',
  '累计计量与剩余产值勾稽（累计计量 + 剩余产值 = 合同额）',
  '合计行逐列复核',
  '同一项目同一期重复行检测',
  '空白与占位符检测',
  '金额或产值为负检测',
];

const CHECKS_WITHHELD = [
  '已完产值超过合同额检测',
  '形象进度与产值偏差超 10 个百分点提示（参考口径）',
  '计量金额超过已完产值检测',
  '扣款比例偏离参考区间（0%~10%）提示（参考口径）',
  '累计计量与累计产值不一致提示（偏差超 10%，参考口径）',
];

const OUT_OF_SCOPE = [
  '判断形象进度是否真实（进度由现场与监理确认，本工具只核它与已完产值对不对得上）',
  '判断合同额、变更签证、暂列金额的口径（以合同与补充协议为准）',
  '处理质保金、预付款抵扣、违约金等扣款是否应当扣（属于合同与商务判断）',
  '读取造价软件/ERP/甲方确认系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '项目名称\t期次\t形象进度\t合同额\t本期已完产值\t累计已完产值\t本期计量金额\t累计计量金额\t本期扣款\t本期应付金额\t剩余产值',
  '滨江路改造工程\t2026-01\t10%\t10000000.00\t1000000.00\t1000000.00\t980000.00\t980000.00\t20000.00\t980000.00\t9020000.00',
  '滨江路改造工程\t2026-02\t20%\t10000000.00\t1000000.00\t2000000.00\t980000.00\t1960000.00\t20000.00\t980000.00\t8040000.00',
  '滨江路改造工程\t2026-03\t30%\t10000000.00\t1000000.00\t3000000.00\t980000.00\t2940000.00\t20000.00\t980000.00\t7060000.00',
  '合计\t\t\t\t3000000.00\t\t2940000.00\t\t60000.00\t2940000.00\t',
].join('\n');

const TOL = 0.01;
/** 形象进度与产值推算进度的允许偏差（**百分点**） */
const PROGRESS_TOL = 10;
/** 本期扣款占本期已完产值的参考区间（参考口径，供"明显偏离"时提示） */
const DEDUCT_RATE_REF = [0, 0.10];
/** 累计计量与累计已完产值的允许偏差（相对值，参考口径） */
const CUM_DEV_REF = 0.10;
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的前面，否则会被抢走列（第 232 轮的坑）。
  //   例如「累计已完产值」必须由 cumCompleted 先认领，否则会被 completed 的「已完产值」抢走；
  //   同理「累计计量金额」要先于 measured 的「计量金额」。
  project: ['项目名称', '工程名称', '项目名', '项目'],
  period: ['期次', '所属期', '期间', '计量期', '月份', '所属月份'],
  progress: ['形象进度', '完工进度', '完成比例', '进度'],
  cumCompleted: ['累计已完产值', '累计完成产值', '累计产值'],
  cumMeasured: ['累计计量金额', '累计计量产值', '累计计量'],
  contractAmount: ['合同额', '合同金额', '合同总价', '合同价'],
  completed: ['本期已完产值', '本期完成产值', '已完产值', '本期产值', '完成产值'],
  measured: ['本期计量金额', '本期计量产值', '计量金额', '本期计量'],
  deduction: ['本期扣款', '扣款金额', '本期扣减', '扣款'],
  payable: ['本期应付金额', '本期应付', '应付金额', '应付'],
  remaining: ['剩余产值', '剩余金额', '剩余产值额'],
};

const LABELS = {
  project: '项目名称', period: '期次', progress: '形象进度', contractAmount: '合同额',
  completed: '本期已完产值', cumCompleted: '累计已完产值', measured: '本期计量金额',
  cumMeasured: '累计计量金额', deduction: '本期扣款', payable: '本期应付金额',
  remaining: '剩余产值',
};

// 少一列就核不动：这 9 列缺任何一列都直接判"材料不足"，绝不猜
const REQUIRED = ['project', 'period', 'contractAmount', 'completed', 'cumCompleted',
  'measured', 'cumMeasured', 'deduction', 'remaining'];
// 只有"本期流量"列可以合计；合同额、累计列、剩余产值是余额概念，相加没有意义
const SUM_ROLES = ['completed', 'measured', 'deduction', 'payable'];
const NEG_ROLES = ['contractAmount', 'completed', 'cumCompleted', 'measured', 'cumMeasured',
  'deduction', 'payable', 'remaining'];

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|待确认|—)$/i.test(s);
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
      if ((role === 'period' || role === 'project') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && it.project !== undefined && String(it.project).trim() ? String(it.project).trim() : '';
  const q = it && it.period !== undefined && String(it.period).trim() ? String(it.period).trim() : '';
  if (p && q) return `${p} ${q}`;
  if (p) return p;
  return `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

function checkMeasured(it) {
  const completed = normNumber(it.completed);
  const deduction = normNumber(it.deduction);
  const stated = normNumber(it.measured);
  if (completed === null || deduction === null || stated === null) return null;
  const expect = round2(completed - deduction);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '计量金额复算不符', line: it.line,
    message: `${who(it)}：本期已完产值 ${completed.toFixed(2)} − 本期扣款 ${deduction.toFixed(2)} 应为 ${expect.toFixed(2)}，`
      + `表里的本期计量金额却是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkCumulative(it) {
  const contract = normNumber(it.contractAmount);
  const cumMeasured = normNumber(it.cumMeasured);
  const remaining = normNumber(it.remaining);
  if (contract === null || cumMeasured === null || remaining === null) return null;
  const sum = round2(cumMeasured + remaining);
  if (Math.abs(sum - contract) <= TOL) return null;
  return {
    level: 'P0', category: '累计计量与剩余产值勾稽不符', line: it.line,
    message: `${who(it)}：累计计量 ${cumMeasured.toFixed(2)} + 剩余产值 ${remaining.toFixed(2)} = ${sum.toFixed(2)}，`
      + `与合同额 ${contract.toFixed(2)} 相差 ${round2(sum - contract).toFixed(2)} —— 合同总额必须闭合。`,
  };
}

function checkNegatives(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v < -TOL) {
      out.push({
        level: 'P0', category: '金额或产值为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回或红字请单独列示并说明来源。`,
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
    const p = String(it.project === undefined ? '' : it.project).trim();
    const q = String(it.period === undefined ? '' : it.period).trim();
    if (!p && !q) continue;
    const key = `${p}|${q}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一项目同一期重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行又出现一次 —— `
          + '产值与计量会被重复汇总（累计列尤其危险）。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    const miss = REQUIRED.filter((r) => isBlank(it[r]));
    if (!miss.length) continue;
    out.push({
      level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
      message: `${who(it)}有 ${miss.length} 个关键字段是空的或占位符：`
        + `${miss.map((r) => `${LABELS[r]}（${String(it[r] === undefined ? '' : it[r]).trim() || '空'}）`).join('、')}。`,
    });
  }
  return out;
}

/* ------------------------ 完整档（付费）追加的检查项 ------------------------ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到确认表正文（text）—— 请把「项目名称 / 期次 / 形象进度 / 合同额 / 本期已完产值 / '
      + '累计已完产值 / 本期计量金额 / 累计计量金额 / 本期扣款 / 剩余产值」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `确认表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(String(text).split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何项目明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkMeasured(it); if (a) findings.push(a);
    const b = checkCumulative(it); if (b) findings.push(b);
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
    const q = String(it.period === undefined ? '' : it.period).trim();
    if (q) periodSet.add(q);
  }
  const rows = t.items.length;
  const periods = periodSet.size;

  const result = {
    status: 'success',
    service_type: 'CONSTRUCTION_OUTPUT_VALUE_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
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
    note: '本版本只执行 6 项免费检查项；未执行的检查项见 scope.checks_not_run。',
    disclaimer: '只核"本期计量 = 本期已完产值 − 本期扣款""累计计量 + 剩余产值 = 合同额"这类**表内勾稽**；'
      + '形象进度、扣款比例、累计口径偏差只按参考区间**提示**，不替代合同与现场判断；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
