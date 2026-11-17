/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * input-vat-deduction-check.js —— 增值税进项税额认证与抵扣核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月申报前**，财务要把进项这一侧对平 ——
 * **认证（勾选）了多少税额 / 转出多少不得抵扣 / 实际申报抵扣多少**。
 * 进项是"钱"：认证了没抵扣等于白白占资金，没认证就抵扣会被系统拦下甚至要更正申报；
 * 转出算错直接影响应纳税额。这是每个月都要做的活，且**完全能算出来对错**。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   申报抵扣进项税额 = 认证税额 − 不得抵扣转出税额
 *   进项税率         = 认证税额 ÷ 认证金额
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**哪些进项能抵扣：表里给什么就核什么，只做勾稽与档位提示。
 */

const CHECKS_GIVEN = [
  '抵扣勾稽（认证税额 − 转出税额 = 申报抵扣）',
  '转出税额超过认证税额检测',
  '抵扣税额为负检测',
  '合计行逐列复核',
  '重复月份检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '进项税率不在常见档位（1%/3%/5%/6%/9%/13%）检测',
  '认证金额或认证税额为负检测',
  '抵扣税额大于认证税额检测',
  '已认证却未抵扣检测（认证税额 > 0 而抵扣为 0）',
  '期末留抵税额为负检测',
];

const OUT_OF_SCOPE = [
  '判断某项进项能否抵扣、该不该转出（那属于税务判断，请咨询税务师）',
  '核对发票真伪、比对发票明细与申报表附表二逐行数据',
  '处理加计抵减、增量留抵退税等优惠政策计算',
  '读取勾选平台或财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '月份\t认证金额\t认证税额\t申报抵扣进项税额\t不得抵扣转出税额\t期末留抵税额',
  '2026-01\t800000.00\t104000.00\t104000.00\t0.00\t0.00',
  '2026-02\t650000.00\t84500.00\t82000.00\t2500.00\t0.00',
  '2026-03\t920000.00\t119600.00\t119600.00\t0.00\t0.00',
  '合计\t2370000.00\t308100.00\t305600.00\t2500.00\t',
].join('\n');

const TOL = 0.01;
const COMMON_RATES = [0.01, 0.03, 0.05, 0.06, 0.09, 0.13];
const RATE_TOL = 0.0005;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  month: ['月份', '所属期', '期间', '月度'],
  certAmount: ['认证金额', '勾选金额', '认证的不含税金额', '进项金额'],
  certTax: ['认证税额', '勾选税额', '认证进项税额'],
  deducted: ['申报抵扣进项税额', '申报抵扣', '抵扣税额', '实际抵扣'],
  transferred: ['不得抵扣转出税额', '进项税额转出', '转出税额', '转出'],
  creditCarry: ['期末留抵税额', '留抵税额', '期末留抵'],
};

const LABELS = {
  month: '月份', certAmount: '认证金额', certTax: '认证税额',
  deducted: '申报抵扣进项税额', transferred: '不得抵扣转出税额', creditCarry: '期末留抵税额',
};

const REQUIRED = ['month', 'certAmount', 'certTax', 'deducted', 'transferred'];
const SUM_ROLES = ['certAmount', 'certTax', 'deducted', 'transferred'];
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

function checkDeductionIdentity(it) {
  const cert = normNumber(it.certTax);
  const trans = normNumber(it.transferred);
  const stated = normNumber(it.deducted);
  if (cert === null || trans === null || stated === null) return null;
  const expect = round2(cert - trans);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '抵扣额与复算不符', line: it.line,
    message: `${who(it)}：认证税额 ${cert.toFixed(2)} − 转出 ${trans.toFixed(2)} 应为 ${expect.toFixed(2)}，表里申报抵扣写的是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkTransferOverCert(it) {
  const cert = normNumber(it.certTax);
  const trans = normNumber(it.transferred);
  if (cert === null || trans === null || trans <= cert + TOL) return null;
  return {
    level: 'P0', category: '转出税额超过认证税额', line: it.line,
    message: `${who(it)}的转出税额 ${trans.toFixed(2)} 超过认证税额 ${cert.toFixed(2)} —— 转出的前提是先认证，超出部分没有来源。`,
  };
}

function checkNegativeDeducted(it) {
  const v = normNumber(it.deducted);
  if (v === null || v >= -TOL) return null;
  return {
    level: 'P0', category: '抵扣税额为负', line: it.line,
    message: `${who(it)}的申报抵扣进项税额是 ${v.toFixed(2)}（负数）—— 负数通常来自更正或冲回，请单独列示。`,
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
    return insufficient('没有收到对照表正文（text）—— 请把「月份 / 认证金额 / 认证税额 / 抵扣 / 转出」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `对照表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何期间明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkDeductionIdentity(it); if (a) findings.push(a);
    const b = checkTransferOverCert(it); if (b) findings.push(b);
    const c = checkNegativeDeducted(it); if (c) findings.push(c);

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

  let certTaxTotal = 0; let deductedTotal = 0; let transTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.certTax); if (a !== null) certTaxTotal += a;
    const b = normNumber(it.deducted); if (b !== null) deductedTotal += b;
    const c = normNumber(it.transferred); if (c !== null) transTotal += c;
  }

  const result = {
    status: 'success',
    service_type: 'INPUT_VAT_DEDUCTION_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      periods: t.items.length,
      certified_tax_total: round2(certTaxTotal),
      deducted_total: round2(deductedTotal),
      transferred_total: round2(transTotal),
      undeducted_total: round2(certTaxTotal - deductedTotal),
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      periods: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'MISMATCH_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'RECONCILED'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"认证 / 转出 / 抵扣"三者的勾稽与税率档位，**不判断某项进项能否抵扣**；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
