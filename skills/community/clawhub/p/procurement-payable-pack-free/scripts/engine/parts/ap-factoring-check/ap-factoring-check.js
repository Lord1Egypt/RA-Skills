/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * ap-factoring-check.js —— 应付账款保理与贴现核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月结账前**，做了保理 / 供应链金融（应收账款保理、应付账款反向保理、
 * 票据或账款贴现）的企业要把这张「应付账款保理与贴现表」核一遍 ——
 * 保理融资金额、利息与手续费、到期扣款、账面应付核销**必须互相对得上**；
 * 漏记一笔利息或手续费、核销额与扣款错位，就是**账实不符**，关账前必须查出来。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   保理融资额 = 应付金额 × 融资比例
 *   到期扣款   = 应付金额 − 保理融资额 + 利息 + 手续费
 *   合计行     = 各明细行逐列相加
 *   （利息与手续费是融资方收的钱，到期要连同未融部分一起从应付账款里扣）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**融资比例与费率（各机构各笔业务不同）：比例以表里给的为准，
 *    只对"明显偏离 0~100%"做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '保理融资额复算（应付金额 × 融资比例 = 保理融资额）',
  '到期扣款复算（应付金额 − 保理融资额 + 利息 + 手续费 = 到期扣款）',
  '合计行逐列复核',
  '同一供应商同一笔重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '保理融资额超过应付金额检测',
  '利息或手续费为负检测',
  '融资比例偏离参考区间（0~100%）提示（参考口径）',
  '到期扣款与应付金额差异超过容差提示',
  '已核销金额超过应付金额检测',
];

const OUT_OF_SCOPE = [
  '判断融资比例、保理费率与贴现利率是否公允（各机构各笔不同，请以保理合同与机构报价为准）',
  '处理有追索 / 无追索保理、票据贴现与反向保理的会计科目归属',
  '核对保理合同条款、保证金与回购安排',
  '读取银行流水、保理商对账单或 ERP 导出文件（需要你先导出成文本贴进来）',
];

/* 参考区间：仅供"明显偏离"时提示 */
const RATIO_REF = [0, 1];

const SAMPLE_TEXT = [
  '期间\t供应商\t保理单号\t应付金额\t融资比例\t保理融资额\t利息（贴现息）\t手续费\t到期扣款\t已核销应付',
  '2026-01\t华东钢材有限公司\tBL-2026-001\t500000.00\t90%\t450000.00\t10000.00\t5000.00\t65000.00\t500000.00',
  '2026-01\t南方物流股份有限公司\tBL-2026-002\t200000.00\t85%\t170000.00\t4000.00\t2000.00\t36000.00\t200000.00',
  '2026-02\t华东钢材有限公司\tBL-2026-003\t300000.00\t90%\t270000.00\t6000.00\t3000.00\t39000.00\t300000.00',
  '2026-02\t北方机电设备有限公司\tBL-2026-004\t180000.00\t80%\t144000.00\t3600.00\t1800.00\t41400.00\t180000.00',
  '合计\t\t\t1180000.00\t\t1034000.00\t23600.00\t11800.00\t181400.00\t1180000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  //    （「融资比例」不能被「保理融资额」抢走，「应付金额」不能被「已核销应付」抢走）
  period: ['期间', '账期', '所属期', '月份'],
  supplier: ['供应商', '往来单位', '单位名称'],
  document: ['保理单号', '保理编号', '单号', '编号'],
  payable: ['应付金额', '应付账款金额', '应付余额'],
  financingRatio: ['融资比例', '保理比例', '融资成数'],
  financing: ['保理融资额', '保理融资金额', '融资额', '保理金额'],
  interest: ['利息', '贴现息', '贴息'],
  fee: ['手续费', '服务费', '保理费'],
  deduction: ['到期扣款', '到期扣款额', '扣款金额'],
  writtenOff: ['已核销应付', '已核销金额', '核销金额', '账面核销额'],
};

const LABELS = {
  period: '期间', supplier: '供应商', document: '保理单号', payable: '应付金额',
  financingRatio: '融资比例', financing: '保理融资额', interest: '利息（贴现息）',
  fee: '手续费', deduction: '到期扣款', writtenOff: '已核销应付',
};

const REQUIRED = ['period', 'supplier', 'document', 'payable', 'financingRatio', 'financing', 'interest', 'fee', 'deduction', 'writtenOff'];
const SUM_ROLES = ['payable', 'financing', 'interest', 'fee', 'deduction', 'writtenOff'];
const AMOUNT_ROLES = ['payable', 'financing', 'interest', 'fee', 'deduction', 'writtenOff'];
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

/** 比率归一化成小数：`90%` ⇒ 0.9；`0.9` ⇒ 0.9；`90` ⇒ 0.9 */
function ratioOf(raw) {
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
  if (!it) return '该行';
  const sup = it.supplier ? String(it.supplier).trim() : '';
  const doc = it.document ? String(it.document).trim() : '';
  if (sup || doc) return `${[sup, doc].filter(Boolean).join(' / ')}（第 ${it.line} 行）`;
  if (it.period) return `${String(it.period).trim()} 期（第 ${it.line} 行）`;
  return `第 ${it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

function checkFactoringRecalc(it) {
  const payable = normNumber(it.payable);
  const ratio = ratioOf(it.financingRatio);
  const stated = normNumber(it.financing);
  if (payable === null || ratio === null || stated === null) return null;
  const expect = round2(payable * ratio);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '保理融资额与复算不符', line: it.line,
    message: `${who(it)}：应付金额 ${payable.toFixed(2)} × 融资比例 ${(ratio * 100).toFixed(2)}% 应为 ${expect.toFixed(2)}，表里保理融资额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkDeductionRecalc(it) {
  const payable = normNumber(it.payable);
  const financing = normNumber(it.financing);
  const interest = normNumber(it.interest);
  const fee = normNumber(it.fee);
  const stated = normNumber(it.deduction);
  if (payable === null || financing === null || interest === null || fee === null || stated === null) return null;
  const expect = round2(payable - financing + interest + fee);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '到期扣款与复算不符', line: it.line,
    message: `${who(it)}：应付金额 ${payable.toFixed(2)} − 保理融资额 ${financing.toFixed(2)} + 利息 ${interest.toFixed(2)} + 手续费 ${fee.toFixed(2)} 应为 ${expect.toFixed(2)}，表里到期扣款是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkAmountNegative(it) {
  const out = [];
  for (const role of AMOUNT_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回或红字请单独列示，别混进这张表。`,
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const sup = String(it.supplier || '').trim();
    const doc = String(it.document || '').trim();
    if (!sup && !doc) continue;
    const key = `${sup}||${doc}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一供应商同一笔出现多行', line: it.line,
        message: `${who(it)}与第 ${seen.get(key)} 行是同一供应商的同一笔（${[sup, doc].filter(Boolean).join(' / ')}）—— 融资额与扣款会被重复计算。`,
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

/**
 * ⚠️ 这两列**本来就不相等**（到期扣款 = 应付金额 − 保理融资额 + 利息 + 手续费），
 * 所以不能拿"扣款 ≠ 应付金额"当异常 —— 那样干净样例会全表误报（第一版就是这么错的）。
 * 这里改成**重大差异提示**：按容差算出的应扣数与实际扣款差得离谱时，才提示复核。
 * 阈值取"应付金额的 1%"，只兜住"整行数错位/漏录一位数"这种大偏差，不参与勾稽判断。
 */
const DEDUCTION_GAP_RATIO = 0.01;

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到核对表正文（text）—— 请把「期间 / 供应商 / 保理单号 / 应付金额 / 融资比例 / 保理融资额 / 利息 / 手续费 / 到期扣款 / 已核销应付」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkFactoringRecalc(it); if (a) findings.push(a);
    const b = checkDeductionRecalc(it); if (b) findings.push(b);
    for (const c of checkAmountNegative(it)) findings.push(c);

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

  let payableTotal = 0; let financingTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.payable); if (a !== null) payableTotal += a;
    const b = normNumber(it.financing); if (b !== null) financingTotal += b;
  }

  const result = {
    status: 'success',
    service_type: 'AP_FACTORING_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: t.items.length,
      payable_total: round2(payableTotal),
      financing_total: round2(financingTotal),
      ratio_ref: RATIO_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"应付金额 × 融资比例 = 保理融资额""应付金额 − 保理融资额 + 利息 + 手续费 = 到期扣款"'
      + '这类内部勾稽，**不规定融资比例与费率**（以保理合同与机构报价为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
