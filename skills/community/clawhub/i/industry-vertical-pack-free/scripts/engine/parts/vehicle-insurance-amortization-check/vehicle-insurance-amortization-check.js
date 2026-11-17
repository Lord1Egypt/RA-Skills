/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * vehicle-insurance-amortization-check.js —— 车辆保险与保费摊销核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月结账前**。有车队的公司（物流 / 工程 / 租赁）一次性交一年期车险，
 * 保费必须按月摊进费用，剩下的挂在预付账款（待摊费用）上；中途退保 / 批改还要把未摊销的余额冲回。
 * 这张表算错，方向只有两个 —— **摊销额错了**（费用错）或 **未摊销余额错了**（预付账款错），
 * 而这两笔在年审时是必查项：保费摊销错就是**费用与预付账款双错**。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   本期摊销额       = 保费总额 ÷ 保险月数
 *   期末未摊销余额   = 期初未摊销余额 + 本期新增保费 − 本期摊销额
 *   合计行各列       = 明细行相加（保费总额按保单去重，同一保单的多期明细只算一次）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**这笔保费该按什么口径摊销、退保该冲回多少（那属于合同与会计判断）：
 *    表里给的保费总额、保险月数、起止日期、期初未摊销余额一律**以你填的为准**，
 *    本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚。
 */

const CHECKS_GIVEN = [
  '本期摊销额复算（保费总额 ÷ 保险月数 = 本期摊销额）',
  '期末未摊销余额滚动复算（期初未摊销余额 + 本期新增保费 − 本期摊销额 = 期末未摊销余额）',
  '合计行逐列复核',
  '同一车牌同一保单同一期间重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '摊销月数与保险起止日期不一致提示',
  '未摊销余额为负检测',
  '已过保险期仍有未摊销余额提示',
  '退保/批改未冲回未摊销余额提示',
  '同一车牌重复投保同一险种提示',
];

const OUT_OF_SCOPE = [
  '判断这笔保费该按什么口径摊销（直线法 / 按天摊销 / 是否含车船税与代收代付，属于会计判断，请咨询会计师）',
  '核对保险单条款本身（退保手续费、短期费率、批改加保减保的应收应付）对摊销额的影响',
  '判断退保 / 批改应当冲回多少未摊销余额（按未到期天数还是按月，属于合同与会计口径判断）',
  '处理车船税、增值税、代收代付保费、理赔款与保险返利的会计与税务处理',
  '读取保险公司的保单 / 批单 / 理赔系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t车牌号\t保单号\t保险公司\t险种\t保险起期\t保险止期\t保险月数\t保费总额\t期初未摊销余额\t本期新增保费\t本期摊销额\t期末未摊销余额\t备注',
  '2026-01\t京A12345\tBX2026-001\t平安财险\t交强险\t2026-01-01\t2026-12-31\t12\t12000.00\t0.00\t12000.00\t1000.00\t11000.00\t',
  '2026-02\t京A12345\tBX2026-001\t平安财险\t交强险\t2026-01-01\t2026-12-31\t12\t12000.00\t11000.00\t0.00\t1000.00\t10000.00\t',
  '2026-03\t京A12345\tBX2026-001\t平安财险\t交强险\t2026-01-01\t2026-12-31\t12\t12000.00\t10000.00\t0.00\t1000.00\t9000.00\t',
  '2026-01\t京B67890\tBX2026-002\t人保财险\t商业三者险\t2026-01-01\t2026-06-30\t6\t6000.00\t0.00\t6000.00\t1000.00\t5000.00\t',
  '2026-02\t京B67890\tBX2026-002\t人保财险\t商业三者险\t2026-01-01\t2026-06-30\t6\t6000.00\t5000.00\t0.00\t1000.00\t4000.00\t',
  '2026-03\t京B67890\tBX2026-002\t人保财险\t商业三者险\t2026-01-01\t2026-06-30\t6\t6000.00\t4000.00\t0.00\t1000.00\t3000.00\t',
  '合计\t\t\t\t\t\t\t\t18000.00\t30000.00\t18000.00\t6000.00\t42000.00\t',
].join('\n');

const TOL = 0.01;
const MONTH_TOL = 1;          // 保险月数容差：起止日期不足整月（如 1/15 起保）时宽放 1 个月

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前。
  //    「期末未摊销余额」不能被「期初未摊销余额」抢走、「本期新增保费」不能被「保费总额」抢走、
  //    「本期摊销额」不能被「本期新增保费」或「摊销月数」抢走。
  period: ['所属期间', '会计期间', '摊销期间', '所属期', '期间', '月份', '月度'],
  plate: ['车牌号码', '车牌号', '车辆牌照', '车牌', '车号', '车辆编号'],
  policy: ['保单号码', '保单编号', '保险单编号', '保险单号', '投保单号', '保单号'],
  insurer: ['保险公司', '承保公司', '保险机构', '承保机构', '保险人'],
  coverage: ['险种名称', '投保险种', '保险险种', '投保险别', '险种', '险别'],
  startDate: ['保险起期', '保险起始日期', '保险开始日期', '起保日期', '保险生效日期', '生效日期', '起期'],
  endDate: ['保险止期', '保险终止日期', '保险结束日期', '保险到期日', '终止日期', '到期日期', '到期日', '止期'],
  months: ['保险月数', '保险期间月数', '承保月数', '摊销月数', '保险期限月', '月数'],
  premiumAdd: ['本期新增保费', '本期增加保费', '新增保费', '本期增加额', '本期保费'],
  premiumTotal: ['保费总额', '保单保费', '全年保费', '保费合计', '总保费', '保费'],
  unamortizedBegin: ['期初未摊销余额', '期初未摊销保费', '上期期末未摊销余额', '期初待摊余额', '期初未摊', '期初余额'],
  amortization: ['本期摊销额', '本期摊销保费', '本期摊销金额', '本期摊销', '月摊销额', '摊销额'],
  unamortizedEnd: ['期末未摊销余额', '期末未摊销保费', '期末待摊余额', '期末未摊', '期末余额'],
  remark: ['处理情况', '处理说明', '备注', '说明', '摘要', '状态'],
};

const LABELS = {
  period: '所属期间', plate: '车牌号', policy: '保单号', insurer: '保险公司', coverage: '险种',
  startDate: '保险起期', endDate: '保险止期', months: '保险月数', premiumTotal: '保费总额',
  unamortizedBegin: '期初未摊销余额', premiumAdd: '本期新增保费', amortization: '本期摊销额',
  unamortizedEnd: '期末未摊销余额', remark: '备注',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'plate', 'policy', 'premiumTotal', 'months',
  'unamortizedBegin', 'premiumAdd', 'amortization', 'unamortizedEnd'];
/** 合计行逐列复核的列 */
const SUM_ROLES = ['premiumTotal', 'unamortizedBegin', 'premiumAdd', 'amortization', 'unamortizedEnd'];
/** 这几列是**按保单**的口径（同一保单的多期明细里，保费总额只算一次，否则会被重复加总） */
const PER_POLICY_ROLES = ['premiumTotal'];
/**
 * 免费档负值检测覆盖的列：**收付与摊销侧**的金额。
 * ⚠️ 刻意**不含**期初 / 期末未摊销余额 —— "未摊销余额为负"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出余额为负就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['premiumTotal', 'premiumAdd', 'amortization'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
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

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.plate, it && it.policy, it && it.coverage]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const policyKeyOf = (it) => {
  const c = it && it.policy !== undefined ? String(it.policy).trim() : '';
  if (c) return c;
  const p = it && it.plate !== undefined ? String(it.plate).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const plateKeyOf = (it) => {
  const p = it && it.plate !== undefined ? String(it.plate).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkAmortizationRecompute(it) {
  const out = [];
  const premium = normNumber(it.premiumTotal);
  const months = normNumber(it.months);
  const stated = normNumber(it.amortization);
  if (premium === null || months === null || stated === null) return out;
  if (months <= 0) return out;                 // 保险月数填 0 或负：除不出月摊销额（负值由负值检测报）
  const expect = round2(premium / months);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '本期摊销额复算不符', line: it.line,
    message: `${who(it)}：保费总额 ${premium.toFixed(2)} ÷ 保险月数 ${months} = ${expect.toFixed(2)}，`
      + `表里「本期摊销额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '一年期保费就是"保费总额 ÷ 保险月数"按月摊，摊少了费用少计、预付账款多挂，摊多了反过来，两边同时错。',
  });
  return out;
}

function checkUnamortizedRolling(it) {
  const out = [];
  const begin = normNumber(it.unamortizedBegin);
  const add = normNumber(it.premiumAdd);
  const amort = normNumber(it.amortization);
  const stated = normNumber(it.unamortizedEnd);
  if (begin === null || add === null || amort === null || stated === null) return out;
  const expect = round2(begin + add - amort);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '期末未摊销余额滚动复算不符', line: it.line,
    message: `${who(it)}：期初未摊销余额 ${begin.toFixed(2)} + 本期新增保费 ${add.toFixed(2)} − 本期摊销额 ${amort.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「期末未摊销余额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '余额滚不动，后面每一期的摊销与预付款余额都会跟着错（下期的期初就是本期的期末）。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let expect = null;
    let how = '';
    if (PER_POLICY_ROLES.indexOf(role) >= 0) {
      const first = new Map();
      for (const it of items) {
        const v = normNumber(it[role]);
        if (v !== null && !first.has(policyKeyOf(it))) first.set(policyKeyOf(it), v);
      }
      if (!first.size) continue;
      expect = round2(Array.from(first.values()).reduce((a, b) => a + b, 0));
      how = `按保单去重后 ${first.size} 张保单的「${LABELS[role]}」相加`;
    } else {
      let sum = 0;
      let n = 0;
      for (const it of items) {
        const v = normNumber(it[role]);
        if (v !== null) { sum += v; n += 1; }
      }
      if (!n) continue;
      expect = round2(sum);
      how = `本表 ${n} 行明细的「${LABELS[role]}」相加`;
    }
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，${how}是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是月报与预付账款台账的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const plate = it.plate !== undefined ? String(it.plate).trim() : '';
    const pol = it.policy !== undefined ? String(it.policy).trim() : '';
    if (!p || !plate || !pol) continue;
    const key = `${p}|${plate}|${pol}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一车牌同一保单重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一车牌、同一保单再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一张保单被拆成两行（比如交强险与商业险各建一行却填了同一个保单号），'
          + '多出来的那一行会把保费、摊销额与未摊销余额都重复计一遍。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 保费总额、本期新增保费与本期摊销额都不该为负，`
        + '退保 / 批改的冲回应当单独列示成负数的「本期新增保费」并在备注里说明，而不是把摊销额填成负数。',
    });
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
    return insufficient('没有收到车辆保险与保费摊销核对表正文（text）—— 请把「所属期间 / 车牌号 / 保单号 / 保险公司 / 险种 / 保险起期 / 保险止期 / 保险月数 / 保费总额 / 期初未摊销余额 / 本期新增保费 / 本期摊销额 / 期末未摊销余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `车辆保险与保费摊销核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何保费摊销明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkAmortizationRecompute(it));
    findings.push(...checkUnamortizedRolling(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let premiumTotal = 0;
  let amortizationTotal = 0;
  const perPolicy = new Map();
  for (const it of t.items) {
    const p = normNumber(it.premiumTotal);
    if (p !== null && !perPolicy.has(policyKeyOf(it))) perPolicy.set(policyKeyOf(it), p);
    const a = normNumber(it.amortization);
    if (a !== null) amortizationTotal += a;
  }
  for (const v of perPolicy.values()) premiumTotal += v;

  const result = {
    status: 'success',
    service_type: 'VEHICLE_INSURANCE_AMORTIZATION_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      premium_total: round2(premiumTotal),
      amortization_total: round2(amortizationTotal),
      tolerance: TOL,
      month_tolerance: MONTH_TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: groups.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"保费总额 ÷ 保险月数 = 本期摊销额"与"期初未摊销余额 + 本期新增保费 − 本期摊销额 = 期末未摊销余额"这类**表内勾稽**与档位提示，'
      + '**不判断这笔保费该按什么口径摊销、退保该冲回多少**（以保险合同与会计师口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
