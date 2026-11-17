/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * advance-receipt-check.js —— 预收账款与收入确认核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**月末结账前**，财务要把预收账款（合同负债）核一遍 ——
 * 客户先付钱、我们后交付，付的钱记在预收里，**交付一部分就确认一部分收入**。
 * 这条链算错会同时错三处：预收余额错、收入错、利润与所得税错；
 * 而且**预收账款是最容易被拿来"调节收入"的科目**，审计必查。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   期末预收 = 期初预收 + 本期预收 − 本期确认收入
 *   本期确认收入不得超过"期初预收 + 本期预收"（没收到钱不能确认成预收转出的收入）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**收入确认时点（履约义务何时完成由合同与准则决定），只核台账勾稽。
 */

const CHECKS_GIVEN = [
  '期末预收勾稽（期初 + 本期预收 − 本期确认收入 = 期末）',
  '期末预收余额为负检测',
  '确认收入或预收为负检测',
  '合计行逐列复核',
  '重复客户检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '确认收入超过可用预收（期初 + 本期预收）检测',
  '合同总额为零或为负检测',
  '预收余额超过合同总额检测',
  '本期已确认收入超过合同总额检测',
  '本期预收为 0 却确认收入检测',
];

const OUT_OF_SCOPE = [
  '判断收入确认时点与履约进度（那属于会计准则判断，请咨询会计师）',
  '处理含税/不含税口径转换、跨期分摊与合同变更',
  '核对增值税纳税义务发生时间与开票时点',
  '读取 ERP 或合同系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '客户名称\t合同总额\t期初预收余额\t本期预收\t本期确认收入\t期末预收余额',
  '豫州建设集团有限公司\t3000000.00\t1200000.00\t500000.00\t700000.00\t1000000.00',
  '中岳科技股份有限公司\t800000.00\t300000.00\t200000.00\t250000.00\t250000.00',
  '豫通物流有限公司\t500000.00\t150000.00\t0.00\t100000.00\t50000.00',
  '合计\t4300000.00\t1650000.00\t700000.00\t1050000.00\t1300000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  customer: ['客户名称', '客户', '单位名称', '往来单位'],
  contractTotal: ['合同总额', '合同金额', '合同总价'],
  openBalance: ['期初预收余额', '期初预收', '上期预收余额'],
  received: ['本期预收', '本期收款', '预收增加'],
  recognized: ['本期确认收入', '确认收入', '本期结转收入'],
  closeBalance: ['期末预收余额', '期末预收', '预收余额'],
};

const LABELS = {
  customer: '客户名称', contractTotal: '合同总额', openBalance: '期初预收余额',
  received: '本期预收', recognized: '本期确认收入', closeBalance: '期末预收余额',
};

const REQUIRED = ['customer', 'openBalance', 'received', 'recognized', 'closeBalance'];
const SUM_ROLES = ['openBalance', 'received', 'recognized', 'closeBalance'];
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
      if (role === 'customer' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.customer ? String(it.customer) : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkIdentity(it) {
  const open = normNumber(it.openBalance);
  const recv = normNumber(it.received);
  const recog = normNumber(it.recognized);
  const close = normNumber(it.closeBalance);
  if ([open, recv, recog, close].some((v) => v === null)) return null;
  const expect = round2(open + recv - recog);
  if (Math.abs(expect - close) <= TOL) return null;
  return {
    level: 'P0', category: '期末预收勾稽不符', line: it.line,
    message: `${who(it)}：期初预收 ${open.toFixed(2)} + 本期预收 ${recv.toFixed(2)} − 确认收入 ${recog.toFixed(2)} 应为 ${expect.toFixed(2)}，表里期末写的是 ${close.toFixed(2)}，相差 ${round2(close - expect).toFixed(2)}。`,
  };
}

function checkNegativeClose(it) {
  const v = normNumber(it.closeBalance);
  if (v === null || v >= -TOL) return null;
  return {
    level: 'P0', category: '期末预收余额为负', line: it.line,
    message: `${who(it)}的期末预收余额是 ${v.toFixed(2)}（负数）—— 预收是负债，负数说明确认收入超过了收到的钱（或应收挂错了科目）。`,
  };
}

function checkNegativeFlow(it) {
  const out = [];
  for (const [role, label] of [['received', '本期预收'], ['recognized', '本期确认收入']]) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '预收或确认收入为负', line: it.line,
        message: `${who(it)}的「${label}」是 ${v.toFixed(2)}（负数）—— 退款或冲回建议单独列示。`,
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.customer || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一客户出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 请合并，否则余额会被重复计算。`,
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
    return insufficient('没有收到台账正文（text）—— 请把「客户 / 期初预收 / 本期预收 / 确认收入 / 期末预收」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何客户明细行');
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

  let closeTotal = 0; let recognizedTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.closeBalance); if (a !== null) closeTotal += a;
    const b = normNumber(it.recognized); if (b !== null) recognizedTotal += b;
  }

  const result = {
    status: 'success',
    service_type: 'ADVANCE_RECEIPT_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      customers: t.items.length,
      closing_balance_total: round2(closeTotal),
      recognized_total: round2(recognizedTotal),
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      customers: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核预收账款台账的内部勾稽与合同口径，**不判断收入确认时点**；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
