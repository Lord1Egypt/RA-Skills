/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * payroll-withholding-reconcile.js —— 工资表代扣与个税社保申报核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月发薪并申报之后**，财务/HR 必须把三份数据对平 ——
 * **工资表的代扣数 / 个税申报明细 / 社保申报明细**。
 * 这三处的口径是**法律要求相等**的（代扣多少就要申报多少），对不上就是"三表不一致"：
 * 轻则申报要更正，重则被税务或人社比对出异常。这是每个月都要做的活，且**完全能算出来对错**。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   个税差 = 工资表代扣个税 − 个税申报税额   （应当逐人相等）
 *   社保差 = 工资表代扣社保个人部分 − 社保申报个人额（应当逐人相等）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断个税/社保该怎么算**：表里给什么就核什么，只做一致性核对。
 */

const CHECKS_GIVEN = [
  '代扣个税与个税申报税额一致性核对（逐人）',
  '代扣社保与社保申报个人额一致性核对（逐人）',
  '合计行逐列复核',
  '重复人员检测',
  '空白与占位符检测',
  '申报侧人员缺失检测（工资表有人、申报栏为空）',
];

const CHECKS_WITHHELD = [
  '个税差异金额超阈值（1 元）检测',
  '社保差异金额超阈值（1 元）检测',
  '个税申报税额为负或大于应发工资检测',
  '社保个人部分超过应发工资 20% 检测',
  '单侧多出人员检测（申报侧有人但工资表没有）',
];

const OUT_OF_SCOPE = [
  '判断个税、社保、公积金该怎么算（税率表、专项附加扣除、社保基数上下限）',
  '核对申报表本身的填报口径（本工具只核三份数据的数字是否对得上）',
  '处理外籍人员、离职补发、年终奖单独计税等特殊口径',
  '读取 Excel 工资表或申报系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '姓名\t工资表应发\t代扣个税\t代扣社保个人部分\t个税申报税额\t社保申报个人额',
  '王建国\t18000.00\t890.00\t1980.00\t890.00\t1980.00',
  '李海涛\t12500.00\t340.00\t1375.00\t340.00\t1375.00',
  '赵春燕\t9800.00\t96.00\t1078.00\t96.00\t1078.00',
  '合计\t40300.00\t1326.00\t4433.00\t1326.00\t4433.00',
].join('\n');

const TOL = 0.01;
const DIFF_CAP = 1.00;          // 个税/社保差异超过 1 元才算要处理的差异
const SI_RATIO_CAP = 0.20;       // 社保个人部分超过应发的 20% 属异常

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  person: ['姓名', '员工姓名', '人员', '员工'],
  gross: ['工资表应发', '应发工资', '应发合计', '应发'],
  withheldTax: ['代扣个税', '代扣个人所得税', '工资表个税', '个税代扣'],
  withheldSi: ['代扣社保个人部分', '代扣社保', '社保个人部分', '个人社保'],
  filedTax: ['个税申报税额', '申报个税', '个税申报'],
  filedSi: ['社保申报个人额', '社保申报个人部分', '申报社保', '社保申报'],
};

const LABELS = {
  person: '姓名', gross: '工资表应发', withheldTax: '代扣个税', withheldSi: '代扣社保个人部分',
  filedTax: '个税申报税额', filedSi: '社保申报个人额',
};

const REQUIRED = ['person', 'gross', 'withheldTax', 'filedTax', 'withheldSi', 'filedSi'];
const SUM_ROLES = ['gross', 'withheldTax', 'withheldSi', 'filedTax', 'filedSi'];
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

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
      if (role === 'person' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.person ? String(it.person) : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkTaxMatch(it) {
  const a = normNumber(it.withheldTax);
  const b = normNumber(it.filedTax);
  if (a === null || b === null || Math.abs(a - b) <= TOL) return null;
  return {
    level: 'P0', category: '代扣个税与申报税额不符', line: it.line,
    message: `${who(it)}：工资表代扣个税 ${a.toFixed(2)}，个税申报税额 ${b.toFixed(2)}，相差 ${round2(a - b).toFixed(2)} —— 代扣数与申报数必须逐人相等。`,
  };
}

function checkSiMatch(it) {
  const a = normNumber(it.withheldSi);
  const b = normNumber(it.filedSi);
  if (a === null || b === null || Math.abs(a - b) <= TOL) return null;
  return {
    level: 'P0', category: '代扣社保与申报个人额不符', line: it.line,
    message: `${who(it)}：工资表代扣社保个人部分 ${a.toFixed(2)}，社保申报个人额 ${b.toFixed(2)}，相差 ${round2(a - b).toFixed(2)}。`,
  };
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各人相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.person || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一人员出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 可能是离职补发或重复计入，请注明。`,
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

function checkFiledMissing(items) {
  const out = [];
  for (const it of items) {
    if (!String(it.person || '').trim()) continue;
    const noTax = isBlank(it.filedTax);
    const noSi = isBlank(it.filedSi);
    if (noTax || noSi) {
      out.push({
        level: 'P0', category: '申报侧栏位为空', line: it.line,
        message: `${who(it)}的${noTax ? '「个税申报税额」' : ''}${noTax && noSi ? '与' : ''}${noSi ? '「社保申报个人额」' : ''}为空 —— 工资表上有代扣，申报侧却查不到对应数字，可能是漏申报。`,
      });
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
    return insufficient('没有收到对照表正文（text）—— 请把「姓名 / 应发 / 代扣个税社保 / 申报税额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `对照表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何人员明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkTaxMatch(it); if (a) findings.push(a);
    const b = checkSiMatch(it); if (b) findings.push(b);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  for (const f of checkFiledMissing(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let taxDiffTotal = 0; let siDiffTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.withheldTax); const b = normNumber(it.filedTax);
    if (a !== null && b !== null) taxDiffTotal += (a - b);
    const c = normNumber(it.withheldSi); const d = normNumber(it.filedSi);
    if (c !== null && d !== null) siDiffTotal += (c - d);
  }

  const result = {
    status: 'success',
    service_type: 'PAYROLL_WITHHOLDING_RECONCILE',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      persons: t.items.length,
      tax_diff_total: round2(taxDiffTotal),
      si_diff_total: round2(siDiffTotal),
      diff_cap: DIFF_CAP,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      persons: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'MISMATCH_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'RECONCILED'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"工资表代扣 / 个税申报 / 社保申报"三处的数字是否逐人相等，'
      + '**不判断个税与社保该如何计算**；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
