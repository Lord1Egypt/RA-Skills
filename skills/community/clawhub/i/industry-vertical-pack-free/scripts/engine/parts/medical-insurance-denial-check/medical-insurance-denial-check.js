/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * medical-insurance-denial-check.js —— 医保拒付与申诉核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月医保结算之后**。医保经办机构把拒付明细打回来，
 * 医院/诊所必须在时限内逐笔决定「申诉还是放弃」：拒付明细金额扣掉已放弃金额才是
 * 值得申诉的钱；申诉出去以后还有多少没回款，账上就挂多少应收。
 *
 *   应申诉金额 = 拒付明细金额 − 已放弃金额
 *   未回款金额 = 拒付明细金额 − 已申诉金额
 *
 * 漏申诉就是**白丢收入**：钱追不回来，账上还挂着一笔虚的应收。
 * 这张表的每一格都能手算复现，所以"对不对"是完全可以机械核出来的。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应申诉金额 = 拒付明细金额 − 已放弃金额
 *   未回款金额 = 拒付明细金额 − 已申诉金额
 *   合计行各列 = 本表对应列明细之和
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某一笔拒付该不该申诉、申诉能不能赢（那属于医保政策与病案/临床判断）：
 *    表里的申诉状态、拒付日期、拒付率一律**只当作提示依据**，口径以表里给的为准。
 */

const CHECKS_GIVEN = [
  '应申诉金额复算（拒付明细金额 − 已放弃金额 = 应申诉金额）',
  '未回款金额复算（拒付明细金额 − 已申诉金额 = 未回款金额）',
  '合计行逐列复核',
  '同一拒付单号重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '申诉金额超过拒付明细金额提示',
  '申诉时限已过仍未申诉提示（按拒付日期 + 参考 60 天时限）',
  '同一拒付单号重复申诉提示',
  '申诉状态为已申诉但申诉金额为零提示',
  '拒付率偏离参考区间（0~20%）提示',
];

const OUT_OF_SCOPE = [
  '判断某一笔拒付到底该不该申诉、申诉能不能赢（那属于医保政策与病案/临床判断，请咨询医保办或病案室）',
  '核对结算清单 / DRG-DIP 分组与拒付理由本身的依据（那要以经办机构给的结算明细为准）',
  '读取 HIS 或医保结算系统导出文件（需要你先导出成文本贴进来）',
  '代替医院向医保经办机构提交申诉（本工具只核表，不对外发任何材料）',
];

const SAMPLE_TEXT = [
  '拒付单号\t拒付日期\t结算期间\t拒付明细金额\t已放弃金额\t应申诉金额\t已申诉金额\t未回款金额\t申诉状态\t拒付率',
  'JP2026010001\t2026-01-05\t2026-01\t10000.00\t0.00\t10000.00\t8000.00\t2000.00\t已申诉\t5%',
  'JP2026010002\t2026-01-12\t2026-01\t6000.00\t1000.00\t5000.00\t5000.00\t1000.00\t已申诉\t8%',
  'JP2026020007\t2026-02-03\t2026-02\t4000.00\t4000.00\t0.00\t0.00\t4000.00\t已放弃\t0%',
  '合计\t\t合计\t20000.00\t5000.00\t15000.00\t13000.00\t7000.00\t\t',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;                    // 比例容差：0.05 个百分点
const APPEAL_DAYS = 60;                     // 参考申诉时限：拒付日期 + 60 天
const DENIAL_RATE_MAX = 0.20;               // 参考拒付率区间上限：20%

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「应申诉金额」不能被「申诉金额」抢走、
  //    「拒付明细金额」不能被「拒付额」抢走、「结算期间」不能被「结算金额」抢走）
  denialNo: ['拒付单号', '拒付编号', '结算单号', '拒付文号', '单据号', '单号'],
  denialDate: ['拒付日期', '拒付时间', '扣款日期', '拒付发生日期'],
  status: ['申诉状态', '申诉情况', '处理状态', '状态'],
  denialAmount: ['拒付明细金额', '拒付金额', '扣款金额', '拒付额', '明细金额'],
  waived: ['已放弃金额', '放弃申诉金额', '放弃金额', '已放弃', '放弃'],
  appealDue: ['应申诉金额', '可申诉金额', '应申诉'],
  appealPaid: ['已申诉金额', '已申诉', '申诉金额'],
  unpaid: ['未回款金额', '未回款额', '未回款'],
  settlement: ['医保结算金额', '结算金额', '结算总额'],
  denialRate: ['拒付率', '拒付比例'],
  period: ['结算期间', '费用期间', '所属期', '期间', '月份', '月度'],
};

const LABELS = {
  denialNo: '拒付单号', denialDate: '拒付日期', status: '申诉状态',
  denialAmount: '拒付明细金额', waived: '已放弃金额', appealDue: '应申诉金额',
  appealPaid: '已申诉金额', unpaid: '未回款金额', settlement: '结算金额',
  denialRate: '拒付率', period: '结算期间',
};

const REQUIRED = ['denialNo', 'denialDate', 'denialAmount', 'waived', 'appealDue', 'appealPaid', 'unpaid'];
/** 合计行逐列复核的列（都是各明细行直接相加的口径） */
const SUM_ROLES = ['denialAmount', 'waived', 'appealDue', 'appealPaid', 'unpaid'];
/** 负值检测覆盖的列（denialRate 另按比例解析） */
const NEGATIVE_ROLES = ['denialAmount', 'waived', 'appealDue', 'appealPaid', 'unpaid', 'settlement', 'denialRate'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|本期合计)$/;

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

/** 比率归一化成小数：`20%` ⇒ 0.2；`0.2` ⇒ 0.2；`20` ⇒ 0.2 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

/** 日期归一化成 `YYYY-MM-DD`：`2026-01-05` / `2026/1/5` / `2026年1月5日` / `20260105` 都认 */
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
    roles.forEach((role, c) => {
      if (!role) return;
      row[role] = cells[c] === undefined ? '' : cells[c];
    });
    // 合计行的「合计」可能落在任何一格（从 Excel 复制出来时常常落在单号列或期间列）
    const isTotal = cells.some((v) => TOTAL_WORDS.test(String(v).trim()));
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const no = it && it.denialNo !== undefined && String(it.denialNo).trim() !== ''
    ? String(it.denialNo).trim() : `第 ${it && it.line} 行`;
  const st = it && it.status !== undefined && String(it.status).trim() !== '' ? String(it.status).trim() : '';
  return st ? `${no}（${st}）` : no;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/** 参考日：优先用入参给的 as_of / reference_date（可复算）；没给就用本机当天 */
/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkAppealDueRecompute(it) {
  const out = [];
  const denial = normNumber(it.denialAmount);
  const waived = normNumber(it.waived);
  const stated = normNumber(it.appealDue);
  if (denial === null || waived === null || stated === null) return out;
  const expect = round2(denial - waived);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应申诉金额与复算不符', line: it.line,
    message: `${who(it)}：拒付明细金额 ${denial.toFixed(2)} − 已放弃金额 ${waived.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「应申诉金额」填的是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)} —— `
      + '应申诉金额就是"这笔拒付里还值得申诉的钱"，填小了就是自己少要钱。',
  });
  return out;
}

function checkUnpaidRecompute(it) {
  const out = [];
  const denial = normNumber(it.denialAmount);
  const appeal = normNumber(it.appealPaid);
  const stated = normNumber(it.unpaid);
  if (denial === null || appeal === null || stated === null) return out;
  const expect = round2(denial - appeal);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '未回款金额与复算不符', line: it.line,
    message: `${who(it)}：拒付明细金额 ${denial.toFixed(2)} − 已申诉金额 ${appeal.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「未回款金额」填的是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)} —— `
      + '这一列就是账上还挂着的应收，填错等于账实不符。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
    if (!n) continue;
    const expect = round2(sum);
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，${n} 行明细相加是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const no = it.denialNo !== undefined ? String(it.denialNo).trim() : '';
    if (!no) continue;
    if (seen.has(no)) {
      out.push({
        level: 'P1', category: '同一拒付单号重复出现', line: it.line,
        message: `${who(it)}在第 ${seen.get(no)} 行已经出现过，第 ${it.line} 行又来一行 —— `
          + '同一笔拒付被重复登记，金额会被重复统计、申诉也可能重复提交。',
      });
    } else seen.set(no, it.line);
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

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = role === 'denialRate' ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = role === 'denialRate' ? `${(v * 100).toFixed(3)}%` : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额或比例为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— `
        + '拒付金额、申诉金额与未回款金额都不该为负，冲回或调整要单独列示。',
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
    return insufficient('没有收到核对表正文（text）—— 请把「拒付单号 / 拒付日期 / 拒付明细金额 / 已放弃金额 / 应申诉金额 / 已申诉金额 / 未回款金额」这张医保拒付与申诉核对表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `医保拒付与申诉核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何拒付明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  let asOf = null;

  for (const it of t.items) {
    findings.push(...checkAppealDueRecompute(it));
    findings.push(...checkUnpaidRecompute(it));
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

  let denialTotal = 0;
  let dueTotal = 0;
  let unpaidTotal = 0;
  for (const it of t.items) {
    const v = normNumber(it.denialAmount);
    if (v !== null) denialTotal += v;
    const d = normNumber(it.appealDue);
    if (d !== null) dueTotal += d;
    const u = normNumber(it.unpaid);
    if (u !== null) unpaidTotal += u;
  }

  const result = {
    status: 'success',
    service_type: 'MEDICAL_INSURANCE_DENIAL_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      denial_amount_total: round2(denialTotal),
      appeal_due_total: round2(dueTotal),
      unpaid_total: round2(unpaidTotal),
      as_of: asOf,
      appeal_deadline_days: APPEAL_DAYS,
      denial_rate_max: DENIAL_RATE_MAX,
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
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
    disclaimer: '只核"拒付明细金额 − 已放弃金额 = 应申诉金额"与"拒付明细金额 − 已申诉金额 = 未回款金额"这类**表内勾稽**及档位提示，'
      + '**不判断某一笔拒付该不该申诉**（以医保政策与经办机构口径为准）；参考日与时限口径都写在结论里，结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
