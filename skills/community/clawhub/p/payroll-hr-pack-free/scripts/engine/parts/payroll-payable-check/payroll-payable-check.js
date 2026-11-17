/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * payroll-payable-check.js —— 应付职工薪酬计提与发放核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每个月发薪并结账之后**，财务要把"应付职工薪酬"这个科目核一遍 ——
 * **计提了多少（成本费用）/ 实际发了多少（银行付出）/ 代扣代缴了多少（个税+社保）/ 还欠多少**。
 * 这个科目是**审计与所得税汇算的常查项**：只计提不发放 ⇒ 费用虚增；发放不冲减 ⇒ 负债虚增；
 * 代扣代缴没对上 ⇒ 个税社保申报与实际不符。每月必做，且**完全能算出来对错**。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   期末应付 = 期初应付 + 本期计提 − 本期发放 − 本期代扣代缴
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**薪酬该怎么算（工资、个税、社保的计算口径由政策与公司制度定），只核科目勾稽。
 */

const CHECKS_GIVEN = [
  '期末应付勾稽（期初 + 计提 − 发放 − 代扣代缴 = 期末）',
  '期末应付为负检测',
  '计提、发放或代扣为负检测',
  '合计行逐列复核',
  '重复月份检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '本月未计提却发放检测（漏计提）',
  '代扣代缴超过本月计提检测',
  '期末应付超过本月计提（挂账超过一个月）检测',
  '发放与计提比例异常检测（<0.5 或 >1.2）',
  '跨月衔接检测（本月期初 = 上月期末）',
];

const OUT_OF_SCOPE = [
  '核对工资表明细、个税与社保的逐人计算（请用「工资表代扣与个税社保申报核对」）',
  '判断辞退福利、股权激励、带薪年假的会计处理',
  '跨年度奖金计提与发放的所得税税前扣除时点判断',
  '读取 ERP 或银行流水（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '月份\t期初应付职工薪酬\t本期计提\t本期发放\t本期代扣代缴\t期末应付职工薪酬',
  '2026-01\t0.00\t420000.00\t360000.00\t60000.00\t0.00',
  '2026-02\t0.00\t430000.00\t368000.00\t62000.00\t0.00',
  '2026-03\t0.00\t455000.00\t389000.00\t66000.00\t0.00',
  '合计\t0.00\t1305000.00\t1117000.00\t188000.00\t0.00',
].join('\n');

const TOL = 0.01;
const RATIO_MIN = 0.5;
const RATIO_MAX = 1.2;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  month: ['月份', '所属期', '期间', '月度'],
  openPayable: ['期初应付职工薪酬', '期初应付', '上期应付余额'],
  accrued: ['本期计提', '计提金额', '本期计提额'],
  paidOut: ['本期发放', '实发合计', '本期发放额'],
  withheld: ['本期代扣代缴', '代扣代缴', '代扣个税社保'],
  closePayable: ['期末应付职工薪酬', '期末应付', '应付余额'],
};

const LABELS = {
  month: '月份', openPayable: '期初应付职工薪酬', accrued: '本期计提',
  paidOut: '本期发放', withheld: '本期代扣代缴', closePayable: '期末应付职工薪酬',
};

const REQUIRED = ['month', 'openPayable', 'accrued', 'paidOut', 'withheld', 'closePayable'];
const SUM_ROLES = ['accrued', 'paidOut', 'withheld'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计)$/;

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
      if (role === 'month' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.month ? `${String(it.month).trim()} 期` : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkIdentity(it) {
  const open = normNumber(it.openPayable);
  const acc = normNumber(it.accrued);
  // ⛔ 这个变量**不能叫 paid**：`paid` 是"是否完整档"的开关名，
  //    叫同名会被付费层泄漏守卫认成"免费引擎里还留着付费开关"（第 231 轮实测踩到）。
  const paidOutAmt = normNumber(it.paidOut);
  const wh = normNumber(it.withheld);
  const close = normNumber(it.closePayable);
  if ([open, acc, paidOutAmt, wh, close].some((v) => v === null)) return null;
  const expect = round2(open + acc - paidOutAmt - wh);
  if (Math.abs(expect - close) <= TOL) return null;
  return {
    level: 'P0', category: '期末应付勾稽不符', line: it.line,
    message: `${who(it)}：期初 ${open.toFixed(2)} + 计提 ${acc.toFixed(2)} − 发放 ${paidOutAmt.toFixed(2)} − 代扣代缴 ${wh.toFixed(2)} 应为 ${expect.toFixed(2)}，表里期末写的是 ${close.toFixed(2)}，相差 ${round2(close - expect).toFixed(2)}。`,
  };
}

function checkNegativeClose(it) {
  const v = normNumber(it.closePayable);
  if (v === null || v >= -TOL) return null;
  return {
    level: 'P0', category: '期末应付为负', line: it.line,
    message: `${who(it)}的期末应付职工薪酬是 ${v.toFixed(2)}（负数）—— 应付是负债，负数说明发放或代扣超过了计提。`,
  };
}

function checkNegativeFlow(it) {
  const out = [];
  for (const [role, label] of [['accrued', '本期计提'], ['paidOut', '本期发放'], ['withheld', '本期代扣代缴']]) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '计提、发放或代扣为负', line: it.line,
        message: `${who(it)}的「${label}」是 ${v.toFixed(2)}（负数）—— 冲回建议单独列示。`,
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
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) sum += v;
  }
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
    const key = String(it.month || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一月份出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 至少有一行是多余的。`,
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
    return insufficient('没有收到台账正文（text）—— 请把「月份 / 期初应付 / 计提 / 发放 / 代扣代缴 / 期末应付」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何月份明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkIdentity(it); if (a) findings.push(a);
    const b = checkNegativeClose(it); if (b) findings.push(b);
    for (const x of checkNegativeFlow(it)) findings.push(x);

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

  let paidTotal = 0; let accruedTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.paidOut); if (a !== null) paidTotal += a;
    const b = normNumber(it.accrued); if (b !== null) accruedTotal += b;
  }

  const result = {
    status: 'success',
    service_type: 'PAYROLL_PAYABLE_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      periods: t.items.length,
      accrued_total: round2(accruedTotal),
      paid_total: round2(paidTotal),
      pay_ratio: accruedTotal > 0 ? Number((paidTotal / accruedTotal).toFixed(6)) : null,
      ratio_range: [RATIO_MIN, RATIO_MAX],
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
    disclaimer: '只核"应付职工薪酬"科目的计提/发放/代扣代缴勾稽，**不判断薪酬与个税社保该怎么算**；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
