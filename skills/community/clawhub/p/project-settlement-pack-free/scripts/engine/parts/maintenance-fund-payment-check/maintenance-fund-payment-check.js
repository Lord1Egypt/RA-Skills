/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * maintenance-fund-payment-check.js —— 维修资金与专项工程付款核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月付款与资金结账时**。物业公司 / 业委会每个月都要把
 * 住宅专项维修资金的「支用申请 → 审价 → 付款 → 余额」逐笔对一遍：审了多少、按合同约定
 * 该付多少、这个月从专户付出去多少、账上还剩多少。这笔钱是**全体业主的钱**、受资金监管：
 * 错一笔就是业主投诉与资金监管问询，付超了还要追回。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   应付工程款 = 审定金额 × 付款比例
 *   期末余额   = 期初余额 + 本期归集 − 本期支出
 *   合计行各列 = 明细行相加（审定金额按工程去重，同一工程的多期明细只算一次）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**该不该动用这笔维修资金、审价金额本身是否公允（那属于业主共同决定程序、
 *    监管政策与审价口径）：表里给的申请金额、审定金额、付款比例、合同付款比例、
 *    余额一律**以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚。
 */

const CHECKS_GIVEN = [
  '应付工程款复算（审定金额 × 付款比例 = 应付工程款）',
  '期末余额滚动复算（期初余额 + 本期归集 − 本期支出 = 期末余额）',
  '合计行逐列复核',
  '同一工程/申请单重复行检测',
  '空白与占位符检测',
  '金额或比例为负检测',
];

const CHECKS_WITHHELD = [
  '累计付款超过审定金额提示',
  '余额为负（超支）提示',
  '付款比例与合同约定不一致提示',
  '审定金额超过申请金额提示',
  '同一工程重复付款提示',
];

const OUT_OF_SCOPE = [
  '判断这笔维修资金该不该动用、支用条件与业主表决程序是否合规（属于资金监管政策与业主共同决定程序，请咨询主管部门与业委会）',
  '判断审价 / 结算审定金额本身是否公允（工程量认定与审价机构口径不在本工具范围）',
  '核对发票、施工合同、竣工验收单、监理签证等原始凭证的真实性与完整性（本工具只核你贴进来的这张表）',
  '处理维修资金的归集标准、专户利息、定期存放收益的会计与税务处理',
  '读取维修资金监管系统 / 银行专户 / 物业 ERP 的导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t工程名称\t施工单位\t申请单号\t申请金额\t审定金额\t付款比例\t合同付款比例\t应付工程款\t本期支出\t累计付款\t期初余额\t本期归集\t期末余额',
  '2026-01\t屋面防水维修\t华建物业\tSQ-2026-001\t120000.00\t100000.00\t30%\t30%\t30000.00\t30000.00\t30000.00\t800000.00\t200000.00\t970000.00',
  '2026-02\t屋面防水维修\t华建物业\tSQ-2026-002\t120000.00\t100000.00\t30%\t30%\t30000.00\t30000.00\t60000.00\t970000.00\t150000.00\t1090000.00',
  '2026-03\t屋面防水维修\t华建物业\tSQ-2026-003\t120000.00\t100000.00\t40%\t40%\t40000.00\t40000.00\t100000.00\t1090000.00\t100000.00\t1150000.00',
  '2026-01\t电梯大修\t中安机电\tSQ-2026-004\t500000.00\t480000.00\t50%\t50%\t240000.00\t240000.00\t240000.00\t1150000.00\t300000.00\t1210000.00',
  '2026-02\t电梯大修\t中安机电\tSQ-2026-005\t500000.00\t480000.00\t30%\t30%\t144000.00\t144000.00\t384000.00\t1210000.00\t250000.00\t1316000.00',
  '2026-03\t电梯大修\t中安机电\tSQ-2026-006\t500000.00\t480000.00\t20%\t20%\t96000.00\t96000.00\t480000.00\t1316000.00\t200000.00\t1420000.00',
  '合计\t\t\t\t1860000.00\t580000.00\t\t\t580000.00\t580000.00\t1294000.00\t\t1200000.00\t',
].join('\n');

const TOL = 0.01;
const RATIO_TOL = 0.0005;     // 付款比例容差：0.05 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  //    （「合同付款比例」不能被「付款比例」抢走 ⇒ contractRatio 必须排在 payRatio 前面；
  //      「累计付款」不能被「本期付款」抢走 ⇒ paidTotal 必须排在 payExpense 前面；
  //      「上期期末余额」不能被「期末余额」抢走 ⇒ balanceBegin 必须排在 balanceEnd 前面）
  period: ['所属期间', '会计期间', '所属月份', '所属期', '期间', '月份', '月度'],
  project: ['工程名称', '项目名称', '维修项目名称', '维修工程名称', '专项工程名称', '工程项目名称', '维修项目', '项目'],
  vendor: ['施工单位', '维修单位', '承建单位', '施工方', '收款单位', '收款方', '供应商', '服务商'],
  application: ['维修资金申请单号', '支用申请单号', '付款申请单号', '申请单编号', '申请单号', '支用单号', '申请编号'],
  applyAmount: ['支用申请金额', '申请支付金额', '申请金额', '申报金额', '报审金额'],
  approvedAmount: ['结算审定金额', '审价金额', '审核金额', '审定金额', '审定工程款', '核定额'],
  payable: ['本期应付工程款', '应付工程款', '应付款金额', '应付金额', '本期应付', '应付未付'],
  contractRatio: ['合同约定付款比例', '合同付款比例', '合同约定比例', '合同比例'],
  payRatio: ['本期付款比例', '付款比例', '支付比例', '付款比率', '付款百分比'],
  paidTotal: ['累计付款金额', '累计实付', '累计已付', '累计支付', '累计付款', '累计支出', '已付款合计'],
  payExpense: ['本期实际付款', '本期实付', '本期付款', '本期支出', '付款金额', '实付金额', '支出金额', '本期支用'],
  balanceBegin: ['上期期末余额', '期初可用余额', '期初账面余额', '期初余额', '期初结余'],
  collect: ['本期归集金额', '本期归集额', '本期交存', '归集金额', '本期归集'],
  balanceEnd: ['本期期末余额', '期末可用余额', '期末账面余额', '期末余额', '期末结余'],
};

const LABELS = {
  period: '所属期间', project: '工程名称', vendor: '施工单位', application: '申请单号',
  applyAmount: '申请金额', approvedAmount: '审定金额', payable: '应付工程款',
  contractRatio: '合同付款比例', payRatio: '付款比例', paidTotal: '累计付款',
  payExpense: '本期支出', balanceBegin: '期初余额', collect: '本期归集', balanceEnd: '期末余额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'project', 'application', 'applyAmount', 'approvedAmount',
  'payRatio', 'payable', 'payExpense', 'balanceBegin', 'collect', 'balanceEnd'];
/** 合计行逐列复核的列（余额是"时点数"，不参与加总） */
const SUM_ROLES = ['applyAmount', 'approvedAmount', 'payable', 'payExpense', 'paidTotal', 'collect'];
/** 这几列是**按工程**的口径（同一工程的多期明细里，审定金额只算一次，否则会被重复加总） */
const PER_PROJECT_ROLES = ['approvedAmount'];
/**
 * 免费档负值检测覆盖的列：申请侧 / 审定侧 / 付款侧 / 比例。
 * ⚠️ 刻意**不含**期初余额与期末余额 —— "余额为负（超支）"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出余额为负就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['applyAmount', 'approvedAmount', 'payable', 'payExpense', 'paidTotal',
  'collect', 'payRatio', 'contractRatio'];
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

/** 比例归一化成小数：`30%` ⇒ 0.3；`0.3` ⇒ 0.3；`30` ⇒ 0.3 */
function ratioValue(raw) {
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

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.project, it && it.application]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

/** 重复行判据：同一期间 + 同一申请单号（申请单号空时退回同一期间 + 同一工程） */
const pairKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  const a = it && it.application !== undefined ? String(it.application).trim() : '';
  const j = it && it.project !== undefined ? String(it.project).trim() : '';
  const base = p || `第 ${it && it.line} 行`;
  if (a) return `${base}|单号 ${a}`;
  if (j) return `${base}|工程 ${j}`;
  return `${base}|第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkPayableRecompute(it) {
  const out = [];
  const approved = normNumber(it.approvedAmount);
  const ratio = ratioValue(it.payRatio);
  const stated = normNumber(it.payable);
  if (approved === null || ratio === null || stated === null) return out;
  const expect = round2(approved * ratio);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应付工程款复算不符', line: it.line,
    message: `${who(it)}：审定金额 ${approved.toFixed(2)} × 付款比例 ${(ratio * 100).toFixed(2)}% = ${expect.toFixed(2)}，`
      + `表里「应付工程款」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '本期应付就是"审定金额 × 付款比例"：这里错了要么多付给施工单位、要么少付，两种都会被业主问到。',
  });
  return out;
}

function checkBalanceRolling(it) {
  const out = [];
  const begin = normNumber(it.balanceBegin);
  const collect = normNumber(it.collect);
  const pay = normNumber(it.payExpense);
  const stated = normNumber(it.balanceEnd);
  if (begin === null || collect === null || pay === null || stated === null) return out;
  const expect = round2(begin + collect - pay);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '期末余额滚动复算不符', line: it.line,
    message: `${who(it)}：期初余额 ${begin.toFixed(2)} + 本期归集 ${collect.toFixed(2)} − 本期支出 ${pay.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「期末余额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '余额滚不动，下个月的期初余额就跟着错，整本资金账会一直错下去（专户余额与监管系统也会对不上）。',
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
    if (PER_PROJECT_ROLES.indexOf(role) >= 0) {
      const first = new Map();
      for (const it of items) {
        const v = normNumber(it[role]);
        const k = String(it.project === undefined ? '' : it.project).trim();
        if (v !== null && !first.has(k)) first.set(k, v);
      }
      if (!first.size) continue;
      expect = round2(Array.from(first.values()).reduce((a, b) => a + b, 0));
      how = `按工程去重后 ${first.size} 个工程的「${LABELS[role]}」相加`;
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
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是对业主公示与报监管的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicateRows(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = pairKeyOf(it);
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一工程/申请单重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一申请单再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一笔付款被拆成两行（比如分次付款各建一行），'
          + '多出来的那一行会把支出与累计付款重复计一遍，专户余额永远对不平。',
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
    const isRatio = role === 'payRatio' || role === 'contractRatio';
    const v = isRatio ? ratioValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = isRatio ? `${(v * 100).toFixed(2)}%` : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额或比例为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 申请金额、审定金额、应付工程款、`
        + '本期支出、累计付款、归集额与付款比例都不该为负，冲回 / 红字应单独列示并在备注里说明。',
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
    return insufficient('没有收到维修资金与专项工程付款核对表正文（text）—— 请把「所属期间 / 工程名称 / 施工单位 / 申请单号 / 申请金额 / 审定金额 / 付款比例 / 合同付款比例 / 应付工程款 / 本期支出 / 累计付款 / 期初余额 / 本期归集 / 期末余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `维修资金与专项工程付款核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何工程付款明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = String(it.period === undefined ? '' : it.period).trim() || `第 ${it.line} 行`;
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkPayableRecompute(it));
    findings.push(...checkBalanceRolling(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicateRows(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  // 审定金额是**按工程**的口径：同一工程分几期付款时这一列每行都会重复写一遍，
  // 逐行相加会按付款期数把它重复计 —— 所以这里与「合计行逐列复核」用同一口径（按工程去重）。
  const approvedByProject = new Map();
  let paidInTotal = 0;
  let outstanding = 0;
  for (const it of t.items) {
    const a = normNumber(it.approvedAmount);
    const k = String(it.project === undefined ? '' : it.project).trim();
    if (a !== null && !approvedByProject.has(k)) approvedByProject.set(k, a);
    const c = normNumber(it.collect);
    if (c !== null) paidInTotal += c;
    const p = normNumber(it.payable);
    if (p !== null) outstanding += p;
  }
  const approvedTotal = Array.from(approvedByProject.values()).reduce((a, b) => a + b, 0);

  const result = {
    status: 'success',
    service_type: 'MAINTENANCE_FUND_PAYMENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      approved_total: round2(approvedTotal),
      paid_in_total: round2(paidInTotal),
      outstanding_total: round2(outstanding),
      tolerance: TOL,
      ratio_tolerance: RATIO_TOL,
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
    disclaimer: '只核"审定金额 × 付款比例 = 应付工程款"与"期初余额 + 本期归集 − 本期支出 = 期末余额"这类**表内勾稽**与档位提示，'
      + '**不判断这笔维修资金该不该动用、审价金额是否公允**（以业主共同决定、监管政策与审价结论为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
