/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * payroll-payment-bank-check.js —— 工资代发与银行回单核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月发薪、银行代发落地之后、工资表封账之前**，
 * 出纳/财务必须把「代发指令」和「银行回单」核一遍：代发总额、银行回单金额、
 * 成功笔数与失败退回必须对得上。**退票没追回来就是重复发薪或漏发**：
 * 钱退回账上却没人重发 ⇒ 员工少发；退票又按原批次再发一次 ⇒ 公司多发。
 * 这两件事都能从表里直接算出来，不靠感觉。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应发合计         = 代发金额 + 失败退回金额            （一行一条代发记录）
 *   合计行「代发金额」= 状态为「成功」的明细行代发金额之和 （代发合计 = 成功笔数金额之和）
 *   合计行每一列      = 全部明细行该列之和
 *   回单金额          = 代发金额（成功笔；差额超过容差即提示）
 *   合计行「成功笔数」= 状态为「成功」的明细行数
 *   失败退回          → 必须在**更晚的期间**（次月）重新出现该员工，否则就是漏发
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**退票原因、银行责任、跨行到账时点 —— 那些要拿银行回单与柜面凭证说话。
 *
 * 约定（写进 SKILL.md「常见错法」，内置样例就是按这个约定写的干净稿）：
 *   · 「代发金额」= 这笔**实际成功发出**的金额；失败退回的笔这一列填 0，
 *     指令金额体现在「应发合计」上，退回的那部分填「失败退回金额」；
 *   · 「发放状态」只写「成功」或「失败退回」这类词，不把备注写进这一列。
 *
 * 检查函数返回形状（**不许混用**）：一条结论的函数返回 `object | null`；
 * 可能有多条结论的函数返回 `array`（可能为空数组）。调用方按各自形状取用。
 */

const CHECKS_GIVEN = [
  '代发合计与成功笔数金额之和的复算（合计行代发金额 = 成功行代发金额之和）',
  '应发合计与代发加退回之和不符检测（应发合计 = 代发金额 + 失败退回金额）',
  '合计行逐列复核',
  '同一员工同一期重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '银行回单金额与代发金额不符提示（差额超过容差）',
  '成功笔数与明细行数不一致检测',
  '失败退回未在次月重发提示',
  '同一银行账号同一期出现多笔（疑似重复发薪）提示',
  '实发为负检测',
];

const OUT_OF_SCOPE = [
  '判断退票/退回的真实原因与银行责任（以银行回单与柜面凭证为准）',
  '核对工资表本身的应发口径（考勤、绩效、个税与社保代扣是否正确）',
  '处理跨行到账时点差异、节假日顺延与在途资金',
  '读取银行网银/代发系统的导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t员工编号\t员工姓名\t银行账号\t应发合计\t代发金额\t银行回单金额\t发放状态\t失败退回金额\t实发合计\t成功笔数',
  '2026-01\tE001\t张三\t6222020200000001\t10000.00\t10000.00\t10000.00\t成功\t0.00\t10000.00\t',
  '2026-01\tE002\t李四\t6222020200000002\t8000.00\t0.00\t0.00\t失败退回\t8000.00\t0.00\t',
  '2026-02\tE001\t张三\t6222020200000001\t10000.00\t10000.00\t10000.00\t成功\t0.00\t10000.00\t',
  '2026-02\tE002\t李四\t6222020200000002\t8000.00\t8000.00\t8000.00\t成功\t0.00\t8000.00\t',
  '合计\t\t\t\t36000.00\t28000.00\t28000.00\t\t8000.00\t28000.00\t3',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「员工姓名」不能被「员工」抢走，「失败退回金额」不能被「退回」抢走）
  period: ['发薪期间', '发放期间', '期间', '月份', '所属期'],
  empId: ['员工编号', '员工工号', '工号', '员工号', '人员编号'],
  empName: ['员工姓名', '姓名', '员工'],
  bankAccount: ['银行账号', '银行卡号', '收款账号', '卡号', '账号'],
  grossPay: ['应发合计', '应发工资', '应发金额'],
  payAmount: ['代发指令金额', '代发金额', '代发额', '指令金额', '代发合计'],
  receiptAmount: ['银行回单金额', '回单金额', '银行回单', '回单'],
  status: ['发放状态', '发放结果', '发放情况', '状态', '结果'],
  returnedAmount: ['失败退回金额', '退票金额', '退回金额', '失败退回', '退回'],
  netPay: ['实发合计', '实发工资', '实发金额', '实发'],
  successCount: ['成功笔数合计', '成功笔数', '成功人数'],
};

const LABELS = {
  period: '期间', empId: '员工编号', empName: '员工姓名', bankAccount: '银行账号',
  grossPay: '应发合计', payAmount: '代发金额', receiptAmount: '银行回单金额', status: '发放状态',
  returnedAmount: '失败退回金额', netPay: '实发合计', successCount: '成功笔数',
};

const REQUIRED = ['period', 'payAmount', 'status'];
const SUM_ROLES = ['grossPay', 'payAmount', 'receiptAmount', 'returnedAmount', 'netPay'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|本期合计|累计)$/;
const FAIL_WORDS = /失败|退回|退票|未到账|未成功|冲正|不成功/;
const SUCCESS_WORDS = /成功|已发|已代发|已到账|已完成/;

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

const who = (it) => (it && it.empName ? `${String(it.empName).trim()}（第 ${it.line} 行）` : `第 ${it && it.line} 行`);
const ft = (n) => (Number.isFinite(n) ? n.toFixed(2) : '');

/** 发放状态：失败/退回类（退票、未到账…） */
function isFailed(it) {
  const s = String(it && it.status === undefined ? '' : it.status).trim();
  return s !== '' && FAIL_WORDS.test(s);
}

/** 发放状态：成功类。状态没填的不算成功 —— 空白由「空白与占位符检测」单独报。 */
function isSuccess(it) {
  if (isFailed(it)) return false;
  const s = String(it && it.status === undefined ? '' : it.status).trim();
  return s !== '' && SUCCESS_WORDS.test(s);
}

/** 同一员工的稳定标识：优先员工编号，没有编号时退回姓名 */
function empKey(it) {
  const id = String(it && it.empId === undefined ? '' : it.empId).trim();
  if (id) return `id:${id}`;
  const nm = String(it && it.empName === undefined ? '' : it.empName).trim();
  return nm ? `name:${nm}` : '';
}

/* ================================ 免费档检查项 ================================ */

/** 免费 1｜应发合计 = 代发金额 + 失败退回金额（单行单结论 → object | null） */
function checkGrossPaySplit(it) {
  const gross = normNumber(it.grossPay);
  const pay = normNumber(it.payAmount);
  const back = normNumber(it.returnedAmount);
  if (gross === null || pay === null || back === null) return null;
  const sum = round2(pay + back);
  if (Math.abs(sum - gross) <= TOL) return null;
  return {
    level: 'P0', category: '应发合计与代发加退回之和不符', line: it.line,
    message: `${who(it)}：代发金额 ${ft(pay)} + 失败退回金额 ${ft(back)} = ${ft(sum)}，但应发合计是 ${ft(gross)}，相差 ${ft(round2(gross - sum))} —— 一笔工资要么发出去、要么退回来，两部分之和就是应发额。`,
  };
}

/** 免费 6｜金额为负（单行多结论 → array） */
function checkNegativeAmount(it) {
  const out = [];
  for (const role of ['grossPay', 'payAmount', 'receiptAmount', 'returnedAmount']) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${ft(v)}（负数）—— 红冲/冲回请单独列示，不要用负数混在发放明细里。`,
      });
    }
  }
  return out;
}

/** 免费 3｜合计行逐列复核（汇总多结论 → array） */
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
    message: `合计行的「${LABELS[role]}」是 ${ft(stated)}，各明细行相加是 ${ft(sum)}，相差 ${ft(round2(stated - sum))}。`,
  });
  return out;
}

/** 免费 1｜代发合计 = 成功笔数金额之和（汇总多结论 → array，空数组即通过） */
function checkSuccessSum(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row.payAmount);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    if (!isSuccess(it)) continue;
    const v = normNumber(it.payAmount);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '代发合计与成功笔数金额之和不符', line: totals.line,
    message: `合计行的「代发金额」是 ${ft(stated)}，但状态为成功的 ${n} 行代发金额之和只有 ${ft(sum)}，相差 ${ft(round2(stated - sum))} —— 代发合计只算**真正发成功**的笔数，失败退回的金额不能算进去。`,
  });
  return out;
}

/** 免费 4｜同一员工同一期重复行（汇总多结论 → array） */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = empKey(it);
    const period = String(it && it.period === undefined ? '' : it.period).trim();
    if (!key || !period) continue;
    const k = `${period}|${key}`;
    if (seen.has(k)) {
      out.push({
        level: 'P1', category: '同一员工同一期出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(k)} 行已出现过（期间 ${period}）—— 同一个人同一期的工资列了两行，很容易被重复代发。`,
      });
    } else seen.set(k, it.line);
  }
  return out;
}

/** 免费 5｜空白与占位符（汇总多结论 → array） */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 这一列是核对的必需项，缺了就没法判断这笔到底发出去没有。`,
        });
      }
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 完整 1｜银行回单金额与代发金额不符（单行单结论 → object | null） */
/** 完整 2｜成功笔数与明细行数不一致（汇总多结论 → array） */
/** 完整 3｜失败退回未在次月重发（汇总多结论 → array） */
/** 完整 4｜同一银行账号同一期出现多笔（疑似重复发薪）（汇总多结论 → array） */
/** 完整 5｜实发为负（单行单结论 → object | null） */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到核对表正文（text）—— 请把「期间 / 员工 / 银行账号 / 应发合计 / 代发金额 / 银行回单金额 / 发放状态 / 失败退回金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何员工代发明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkGrossPaySplit(it); if (a) findings.push(a);
    for (const x of checkNegativeAmount(it)) findings.push(x);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkSuccessSum(t.totals, t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);


  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const periods = new Set();
  for (const it of t.items) {
    const p = String(it.period === undefined ? '' : it.period).trim();
    if (p) periods.add(p);
  }

  const result = {
    status: 'success',
    service_type: 'PAYROLL_PAYMENT_BANK_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"应发 = 代发 + 退回""代发合计 = 成功行之和""回单 = 代发"这类**表内勾稽**，'
      + '**不判断**退票原因与银行责任（以银行回单与柜面凭证为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
