'use strict';
/**
 * labor-cost-allocation-check.js —— 工时与人工成本分摊核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月结账与成本核算时**，制造 / 软件 / 服务企业要把本期
 * **人工成本**按**工时**分摊到产品 / 项目 / 工序上。小时费率（分摊率）一错，
 * 产品成本、项目毛利、存货计价全部跟着错；而"分摊出去多少 + 还留多少没分摊"
 * 又必须与本期**人工成本总额勾稽得上**。全是算术，完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（所有引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *   CHECKS_GIVEN / CHECKS_WITHHELD / OUT_OF_SCOPE / SAMPLE_TEXT
 *
 * 核心可算关系（都能手算复现）：
 *   分摊金额 = 工时 × 小时费率
 *   分摊合计 = 人工成本总额 − 未分摊金额
 *   合计行   = 各明细行相加（期间级口径列按期间去重后相加）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**小时费率：费率以表里给的为准，只对"明显超出常见区间"做**提示**
 *    并明确标注那是**参考**口径（不是判定）。工时口径、成本归集口径同样不判断。
 */

const CHECKS_GIVEN = [
  '分摊金额复算（工时 × 小时费率 = 分摊金额）',
  '分摊合计勾稽（人工成本总额 − 未分摊金额 = 分摊合计）',
  '合计行逐列复核',
  '同一员工同一项目重复行检测',
  '空白与占位符检测',
  '工时或费率为负检测',
];

const CHECKS_WITHHELD = [
  '分摊合计超过人工成本总额检测',
  '工时合计与考勤工时不一致检测',
  '小时费率偏离参考区间（20~500 元/小时）提示（参考口径）',
  '未分摊金额为负检测',
  '工时为零却有分摊金额检测',
];

const OUT_OF_SCOPE = [
  '判断小时费率该定多少（工资水平、技能等级、地区差异，以本单位薪酬制度与劳动合同为准）',
  '判断工时本身是否真实（加班审批、考勤机原始记录、工时填报口径）',
  '核对人工成本总额的归集口径（是否含社保公积金、奖金、福利、辞退福利）',
  '处理制造费用 / 期间费用的分摊与在产品完工进度的约当产量',
  '读取考勤系统或 ERP 导出文件（需要你先导出成文本贴进来）',
];

/* 参考区间：仅供"明显超出"时提示，不是判定标准 */
const RATE_REF = [20, 500];

const SAMPLE_TEXT = [
  '期间\t员工\t项目\t工时\t小时费率\t分摊金额\t人工成本总额\t未分摊金额\t分摊合计\t考勤工时',
  '2026-01\t张伟\t产品A\t80.00\t200.00\t16000.00\t48000.00\t6000.00\t42000.00\t240.00',
  '2026-01\t张伟\t产品B\t40.00\t200.00\t8000.00\t48000.00\t6000.00\t42000.00\t240.00',
  '2026-01\t李娜\t产品A\t60.00\t150.00\t9000.00\t48000.00\t6000.00\t42000.00\t240.00',
  '2026-01\t李娜\t产品C\t60.00\t150.00\t9000.00\t48000.00\t6000.00\t42000.00\t240.00',
  '2026-02\t张伟\t产品A\t100.00\t200.00\t20000.00\t52000.00\t4000.00\t48000.00\t260.00',
  '2026-02\t李娜\t产品B\t80.00\t150.00\t12000.00\t52000.00\t4000.00\t48000.00\t260.00',
  '2026-02\t王强\t产品A\t80.00\t200.00\t16000.00\t52000.00\t4000.00\t48000.00\t260.00',
  '合计\t\t\t500.00\t\t90000.00\t100000.00\t10000.00\t90000.00\t500.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的前面（第 232 轮 header_map_check 的由来）
  period: ['期间', '月份', '所属期', '年度'],
  // 「考勤工时」必须排在「工时」之前，否则会被 hours 抢走 ⇒ 工时列整列算错（且不报缺列）
  attendanceHours: ['考勤工时', '出勤工时', '应出勤工时', '考勤小时'],
  // 「未分摊金额」里含「分摊」字样，必须排在 allocated 之前，否则被分摊金额抢走
  unallocated: ['未分摊金额', '未分摊额', '未分摊人工成本', '未分摊'],
  allocated: ['分摊金额', '分摊额', '已分摊金额', '分摊人工成本'],
  allocTotal: ['分摊合计', '已分摊合计', '分摊总额'],
  laborTotal: ['人工成本总额', '人工成本合计', '人工成本'],
  hours: ['实际工时', '投入工时', '工时', '小时数'],
  rate: ['小时费率', '分摊率', '费率', '时薪'],
  employee: ['员工', '工号', '姓名', '人员'],
  project: ['项目', '产品', '工序', '订单'],
};

const LABELS = {
  period: '期间', attendanceHours: '考勤工时', unallocated: '未分摊金额', allocated: '分摊金额',
  allocTotal: '分摊合计', laborTotal: '人工成本总额', hours: '工时', rate: '小时费率',
  employee: '员工', project: '项目',
};

const REQUIRED = ['period', 'employee', 'project', 'hours', 'rate', 'allocated',
                  'laborTotal', 'unallocated', 'allocTotal'];
const SUM_ROLES = ['hours', 'allocated', 'laborTotal', 'unallocated', 'allocTotal', 'attendanceHours'];
/* 期间级口径列：同一期间内各行重复填写，合计时必须**按期间去重**再相加，不能按行相加 */
const PERIOD_ROLES = ['laborTotal', 'unallocated', 'allocTotal', 'attendanceHours'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|本期合计)$/;

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
const lineOf = (it) => `第 ${it && it.line} 行`;

/* ================================ 免费档检查项 ================================ */

function checkAllocation(it) {
  const h = normNumber(it.hours);
  const r = normNumber(it.rate);
  const stated = normNumber(it.allocated);
  if (h === null || r === null || stated === null) return null;
  const expect = round2(h * r);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '分摊金额复算不符', line: it.line,
    message: `${who(it)}${lineOf(it)}（${String(it.employee || '').trim()} / ${String(it.project || '').trim()}）：`
      + `工时 ${h.toFixed(2)} × 小时费率 ${r.toFixed(2)} 应为 ${expect.toFixed(2)}，`
      + `表里分摊金额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkPoolSplit(it) {
  const pool = normNumber(it.laborTotal);
  const un = normNumber(it.unallocated);
  const alloc = normNumber(it.allocTotal);
  if (pool === null || un === null || alloc === null) return null;
  const expect = round2(pool - un);
  if (Math.abs(expect - alloc) <= TOL) return null;
  return {
    level: 'P0', category: '分摊合计勾稽不符', line: it.line,
    message: `${who(it)}：人工成本总额 ${pool.toFixed(2)} − 未分摊金额 ${un.toFixed(2)} = ${expect.toFixed(2)}，`
      + `但表里分摊合计是 ${alloc.toFixed(2)}，相差 ${round2(alloc - expect).toFixed(2)} —— `
      + `已分摊 + 未分摊 必须正好等于本期人工成本总额。`,
  };
}

function checkNegative(it) {
  const out = [];
  const h = normNumber(it.hours);
  const r = normNumber(it.rate);
  if (h !== null && h < -TOL) {
    out.push({
      level: 'P0', category: '工时或费率为负', line: it.line,
      message: `${who(it)}${lineOf(it)}的工时是 ${h.toFixed(2)}（负数）—— 冲回或红字请单独列示，`
        + `混在明细里会把分摊金额算反。`,
    });
  }
  if (r !== null && r < -TOL) {
    out.push({
      level: 'P0', category: '工时或费率为负', line: it.line,
      message: `${who(it)}${lineOf(it)}的小时费率是 ${r.toFixed(2)}（负数）—— 费率不该为负。`,
    });
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
  if (PERIOD_ROLES.indexOf(role) >= 0) {
    // 期间级口径列：同一期间在多行重复填写 ⇒ 每期只取一次（首行），否则会被重复累加
    const seen = new Set();
    for (const it of items) {
      const key = String(it.period === undefined ? '' : it.period).trim();
      if (seen.has(key)) continue;
      seen.add(key);
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
  } else {
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  const how = PERIOD_ROLES.indexOf(role) >= 0 ? '各期相加' : '各明细行相加';
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，${how}是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = [String(it.period || '').trim(), String(it.employee || '').trim(),
                 String(it.project || '').trim()].join('|');
    if (key === '||') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一员工同一项目重复行', line: it.line,
        message: `${who(it)}的「${String(it.employee || '').trim()} / ${String(it.project || '').trim()}」`
          + `在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 工时与分摊金额会被重复计入。`,
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
          message: `${who(it)}${lineOf(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
        });
      }
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 按期间汇总：工时合计、分摊金额合计，以及期间级口径列（取该期首次出现的值） */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到分摊表正文（text）—— 请把「期间 / 员工 / 项目 / 工时 / 小时费率 / '
      + '分摊金额 / 人工成本总额 / 未分摊金额 / 分摊合计」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `分摊表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何分摊明细行');
  }

  const periodKeys = [];
  const seenPeriod = new Set();
  for (const it of t.items) {
    const k = String(it.period === undefined ? '' : it.period).trim();
    if (k && !seenPeriod.has(k)) { seenPeriod.add(k); periodKeys.push(k); }
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkAllocation(it); if (a) findings.push(a);
    const b = checkPoolSplit(it); if (b) findings.push(b);
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
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let hoursTotal = 0;
  let allocatedTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.hours); if (a !== null) hoursTotal += a;
    const b = normNumber(it.allocated); if (b !== null) allocatedTotal += b;
  }
  const firstOfPeriod = (role) => {
    for (const it of t.items) { const v = normNumber(it[role]); if (v !== null) return v; }
    return null;
  };

  const result = {
    status: 'success',
    service_type: 'LABOR_COST_ALLOCATION_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periodKeys.length,
      period_keys: periodKeys,
      hours_total: round2(hoursTotal),
      allocated_total: round2(allocatedTotal),
      labor_total: firstOfPeriod('laborTotal'),
      unallocated_total: firstOfPeriod('unallocated'),
      rate_ref: RATE_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periodKeys.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"工时 × 小时费率 = 分摊金额""人工成本总额 − 未分摊 = 分摊合计""合计行 = 明细之和"'
      + '这类内部勾稽，**不规定小时费率与工时口径**（以本单位薪酬制度、分摊办法与考勤记录为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
