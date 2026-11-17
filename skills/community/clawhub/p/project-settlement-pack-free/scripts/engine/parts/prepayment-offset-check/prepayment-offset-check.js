/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * prepayment-offset-check.js —— 预付款与预付账款核销核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**月末结账前**，财务要把预付账款台账核一遍 ——
 * 预付出去的钱有没有到票、到票有没有及时冲销、还剩多少挂账。
 * 预付账款是**最容易被长期挂账藏问题**的科目：到票不冲销 → 资产虚高、成本少计；
 * 冲销超过到票 → 成本多计；长期挂账不清理 → 审计与所得税汇算都要调。
 * 这是每个月都要做、且**完全能算出来对错**的活。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   期末余额     = 预付金额 − 已冲销金额
 *   应冲未冲     = 已到票金额 − 已冲销金额（>0 表示票到了还没冲）
 *   挂账天数     = 表内最晚日期 − 首次预付日期
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 */

const CHECKS_GIVEN = [
  '期末余额勾稽（预付金额 − 已冲销金额）',
  '未到票不得冲销检测（已冲销 ≤ 已到票）',
  '余额为负检测（冲销超过预付）',
  '合计行逐列复核',
  '重复供应商合同检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '长期挂账检测（首次预付至今超过 365 天仍有余額）',
  '冲销金额超过预付金额检测',
  '到票金额超过预付金额检测',
  '已到票未冲销检测（应冲未冲 = 已到票 − 已冲销）',
  '金额为负检测（预付 / 到票 / 冲销 / 余额）',
];

const OUT_OF_SCOPE = [
  '判断预付款的商业合理性、是否构成资金占用或关联方往来',
  '计提坏账准备、判断是否需要重分类到其他应收款',
  '处理外币预付款的汇率折算（请先把折算后的本位币金额填进表里）',
  '读取 ERP 或银行流水（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '供应商\t合同编号\t预付金额\t已到票金额\t已冲销金额\t期末余额\t首次预付日期\t最后到票日期',
  '豫州建材有限公司\tCG-2026-011\t300000.00\t300000.00\t300000.00\t0.00\t2026-01-10\t2026-02-20',
  '中岳设备租赁有限公司\tCG-2026-014\t150000.00\t150000.00\t150000.00\t0.00\t2026-02-01\t2026-03-05',
  '豫通物流有限公司\tCG-2026-019\t80000.00\t80000.00\t80000.00\t0.00\t2026-02-15\t2026-03-18',
  '合计\t\t530000.00\t530000.00\t530000.00\t0.00\t\t',
].join('\n');

const TOL = 0.01;
const STALE_DAYS = 365;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  supplier: ['供应商', '往来单位', '收款单位', '单位名称'],
  contract: ['合同编号', '合同号', '采购单号', '订单号'],
  prepaid: ['预付金额', '预付款金额', '预付款', '已付金额'],
  invoiced: ['已到票金额', '到票金额', '已开票金额', '已入库金额'],
  offset: ['已冲销金额', '冲销金额', '已核销金额', '核销金额'],
  balance: ['期末余额', '余额', '未核销余额'],
  firstDate: ['首次预付日期', '预付日期', '首次付款日期'],
  lastDate: ['最后到票日期', '到票日期', '最后开票日期'],
};

const LABELS = {
  supplier: '供应商', contract: '合同编号', prepaid: '预付金额', invoiced: '已到票金额',
  offset: '已冲销金额', balance: '期末余额', firstDate: '首次预付日期', lastDate: '最后到票日期',
};

const REQUIRED = ['supplier', 'prepaid', 'invoiced', 'offset', 'balance'];
const SUM_ROLES = ['prepaid', 'invoiced', 'offset', 'balance'];
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

function parseDay(s) {
  const m = String(s === undefined || s === null ? '' : s).trim().match(/(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})/);
  if (!m) return null;
  const y = +m[1]; const mo = +m[2]; const d = +m[3];
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  return Date.UTC(y, mo - 1, d) / 86400000;
}

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, lastDay: null };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  let lastDay = null;
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (role === 'supplier' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else {
      items.push(row);
      for (const role of ['firstDate', 'lastDate']) {
        const d = parseDay(row[role]);
        if (d !== null && (lastDay === null || d > lastDay)) lastDay = d;
      }
    }
  }
  return { items, totals, missingColumns, lastDay };
}

const who = (it) => (it && it.supplier ? String(it.supplier) : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkBalance(it) {
  const prepaid = normNumber(it.prepaid);
  const offset = normNumber(it.offset);
  const stated = normNumber(it.balance);
  if (prepaid === null || offset === null || stated === null) return null;
  const expect = round2(prepaid - offset);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '期末余额与复算不符', line: it.line,
    message: `${who(it)}的期末余额是 ${stated.toFixed(2)}，按 预付 ${prepaid.toFixed(2)} − 已冲销 ${offset.toFixed(2)} 应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkOffsetVsInvoiced(it) {
  const inv = normNumber(it.invoiced);
  const off = normNumber(it.offset);
  if (inv === null || off === null || off <= inv + TOL) return null;
  return {
    level: 'P0', category: '未到票却已冲销', line: it.line,
    message: `${who(it)}的已冲销金额 ${off.toFixed(2)} 超过已到票金额 ${inv.toFixed(2)}，超出 ${round2(off - inv).toFixed(2)} —— 没有票就冲销，成本会被提前计入。`,
  };
}

function checkNegativeBalance(it) {
  const bal = normNumber(it.balance);
  if (bal === null || bal >= -TOL) return null;
  return {
    level: 'P0', category: '期末余额为负', line: it.line,
    message: `${who(it)}的期末余额是 ${bal.toFixed(2)}（负数）—— 说明冲销超过了预付，账上会出现"负资产"。`,
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const name = String(it.supplier || '').trim();
    if (!name) continue;
    const key = `${name}|${String(it.contract || '').trim()}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一供应商同一合同出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 可能是重复挂账，也可能是同一合同的多次预付（请合并或注明）。`,
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
    return insufficient('没有收到台账正文（text）—— 请把含表头的预付账款台账贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账表头缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何供应商明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkBalance(it); if (a) findings.push(a);
    const b = checkOffsetVsInvoiced(it); if (b) findings.push(b);
    const c = checkNegativeBalance(it); if (c) findings.push(c);

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

  let prepaidTotal = 0; let balTotal = 0; let pendingTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.prepaid); if (a !== null) prepaidTotal += a;
    const b = normNumber(it.balance); if (b !== null) balTotal += b;
    const inv = normNumber(it.invoiced); const off = normNumber(it.offset);
    if (inv !== null && off !== null) pendingTotal += (inv - off);
  }

  const result = {
    status: 'success',
    service_type: 'PREPAYMENT_OFFSET_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      prepaid_total: round2(prepaidTotal),
      balance_total: round2(balTotal),
      invoiced_not_offset_total: round2(pendingTotal),
      stale_days: STALE_DAYS,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核台账内部勾稽与常见口径（是否到票、是否冲销、挂账多久），'
      + '不判断预付款的商业合理性、不计提坏账；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, parseDay, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
