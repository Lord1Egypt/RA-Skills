/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * clinic-revenue-check.js —— 医疗收费与医保结算核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**诊所 / 民营医院的财务在每月与医保局对账时**，
 * 必须把同一张「医疗收费与医保结算表」的四条线勾稽上 ——
 * **医疗服务收入（应收合计）**、**医保结算款**、**自费收款**、**医保拒付金额**。
 * 四者必须勾稽，差一分都要向医保局查。完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应收合计   = 医保结算款 + 自费收款 + 医保拒付金额
 *   医保结算款 = 医保申报金额 × 结算比例
 *   合计行逐列 = 各结算批次明细行之和
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**医保政策口径（拒付率、自付比例的参考区间只用于"明显超出"时提示），
 *    比例与结算口径**以表里给的为准**，以当地医保协议与结算清单为准。
 */

const CHECKS_GIVEN = [
  '应收合计勾稽复算（应收合计 = 医保结算款 + 自费收款 + 医保拒付金额）',
  '医保结算款复算（医保结算款 = 医保申报金额 × 结算比例）',
  '合计行逐列复核',
  '同一结算批次重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '医保拒付率超过参考上限（5%）提示（参考口径）',
  '自付比例超出参考区间（0%~50%）提示（参考口径）',
  '医保申报金额为零却有结算款检测',
  '医保结算款超过医保申报金额检测',
  '拒付金额与拒付率方向矛盾检测',
];

const OUT_OF_SCOPE = [
  '判断医保结算比例、拒付率与自付比例的政策口径（各地医保协议不同，请以当地医保局与结算清单为准）',
  '核对医保申报清单（病案首页 / 费用明细 / DRG 分组）本身的正确性',
  '处理跨期补付、年度清算、总额预付与结余留用',
  '读取医保局或 HIS 系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考口径：仅供"明显超出"时提示，**不是**判定标准 */
const DENY_RATE_REF = 0.05;            // 医保拒付率参考上限 5%
const SELF_PAY_RATE_REF = [0, 0.5];    // 自付比例参考区间 0%~50%

const SAMPLE_TEXT = [
  '结算期间\t结算批次\t应收合计\t医保申报金额\t结算比例\t医保结算款\t自费收款\t医保拒付金额\t拒付率\t自付比例',
  '2026-01\tJS202601\t100000.00\t80000.00\t90%\t72000.00\t25000.00\t3000.00\t3%\t20%',
  '2026-02\tJS202602\t120000.00\t100000.00\t90%\t90000.00\t26000.00\t4000.00\t3.33%\t25%',
  '2026-03\tJS202603\t90000.00\t70000.00\t90%\t63000.00\t24000.00\t3000.00\t3.33%\t30%',
  '合计\t\t310000.00\t250000.00\t\t225000.00\t75000.00\t10000.00\t\t',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名**必须**排在更宽泛的前面。
  //    否则宽泛别名会把具体列抢走（两列落到同一 role，后一列覆盖前一列）——
  //    表现是"跑起来不报错、只是永远静默算错"，所以这里不许出现裸「结算」「拒付」这类词。
  period: ['结算期间', '所属期间', '结算月份', '期间', '月份'],
  batch: ['结算批次', '批次号', '批次'],
  receivable: ['应收合计', '收费合计', '医疗收入合计', '应收金额'],
  declared: ['医保申报金额', '申报金额', '医保申报'],
  ratio: ['医保结算比例', '结算比例', '结算率'],
  settled: ['医保结算款', '医保结算金额', '结算款', '医保拨付金额'],
  selfPay: ['自费收款', '自费收入', '自费金额', '现金收款'],
  denied: ['医保拒付金额', '拒付金额', '医保拒付'],
  denyRate: ['拒付率', '拒付比例'],
  selfPayRate: ['自付比例', '自付率', '个人自付比例'],
};

const LABELS = {
  period: '结算期间', batch: '结算批次', receivable: '应收合计', declared: '医保申报金额',
  ratio: '结算比例', settled: '医保结算款', selfPay: '自费收款', denied: '医保拒付金额',
  denyRate: '拒付率', selfPayRate: '自付比例',
};

const REQUIRED = ['period', 'batch', 'receivable', 'declared', 'ratio', 'settled', 'selfPay', 'denied'];
const AMOUNT_ROLES = ['receivable', 'declared', 'settled', 'selfPay', 'denied'];
const SUM_ROLES = ['receivable', 'declared', 'settled', 'selfPay', 'denied'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|合计行)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|未结算)$/i.test(s);
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
function rateValue(raw) {
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

const who = (it) => (it && it.period ? `${String(it.period).trim()} 期` : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */
/* 每条 check 都返回「对象或 null」；只有多命中的三项（合计行 / 重复 / 空白）返回数组，
   它们在调用处一律用 for...of 展开 —— 两类混用会把空数组当成一条发现。 */

function checkArticulation(it) {
  const recv = normNumber(it.receivable);
  const settled = normNumber(it.settled);
  const self = normNumber(it.selfPay);
  const denied = normNumber(it.denied);
  if (recv === null || settled === null || self === null || denied === null) return null;
  const sum = round2(settled + self + denied);
  if (Math.abs(sum - recv) <= TOL) return null;
  return {
    level: 'P0', category: '应收合计与三项来源不勾稽', line: it.line,
    message: `${who(it)}：医保结算款 ${settled.toFixed(2)} + 自费收款 ${self.toFixed(2)} + 医保拒付金额 ${denied.toFixed(2)} = ${sum.toFixed(2)}，`
      + `但应收合计填的是 ${recv.toFixed(2)}，相差 ${round2(recv - sum).toFixed(2)} —— 收费收入的三个来源必须与应收合计勾稽。`,
  };
}

function checkSettlement(it) {
  const declared = normNumber(it.declared);
  const rate = rateValue(it.ratio);
  const settled = normNumber(it.settled);
  if (declared === null || rate === null || settled === null) return null;
  const expect = round2(declared * rate);
  if (Math.abs(expect - settled) <= TOL) return null;
  return {
    level: 'P0', category: '医保结算款与申报金额×结算比例不符', line: it.line,
    message: `${who(it)}：医保申报金额 ${declared.toFixed(2)} × 结算比例 ${(rate * 100).toFixed(2)}% 应为 ${expect.toFixed(2)}，`
      + `表里结算款是 ${settled.toFixed(2)}，相差 ${round2(settled - expect).toFixed(2)}。`,
  };
}

function checkAmountNegative(it) {
  for (const role of AMOUNT_ROLES) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      return {
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲销请单独列示，不要与本期正数混在一格里。`,
      };
    }
  }
  return null;
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各结算批次相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.batch || '').trim() || String(it.period || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一结算批次出现多行', line: it.line,
        message: `${who(it)}的结算批次「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 该批次会被重复结算。`,
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
    return insufficient('没有收到医疗收费与医保结算表正文（text）—— 请把「结算期间 / 结算批次 / 应收合计 / 医保申报金额 / 结算比例 / 医保结算款 / 自费收款 / 医保拒付金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `医疗收费与医保结算表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何结算批次明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkArticulation(it); if (a) findings.push(a);
    const b = checkSettlement(it); if (b) findings.push(b);
    const c = checkAmountNegative(it); if (c) findings.push(c);

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

  const periods = new Set();
  let recvTotal = 0; let settledTotal = 0; let selfTotal = 0; let deniedTotal = 0;
  for (const it of t.items) {
    const p = String(it.period === undefined ? '' : it.period).trim();
    if (p) periods.add(p);
    const a = normNumber(it.receivable); if (a !== null) recvTotal += a;
    const b = normNumber(it.settled); if (b !== null) settledTotal += b;
    const c = normNumber(it.selfPay); if (c !== null) selfTotal += c;
    const d = normNumber(it.denied); if (d !== null) deniedTotal += d;
  }

  const result = {
    status: 'success',
    service_type: 'CLINIC_REVENUE_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      receivable_total: round2(recvTotal),
      insurance_settled_total: round2(settledTotal),
      self_pay_total: round2(selfTotal),
      denied_total: round2(deniedTotal),
      deny_rate_ref: DENY_RATE_REF,
      self_pay_rate_ref: SELF_PAY_RATE_REF,
      tolerance: TOL,
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
    disclaimer: '只核"应收合计 = 医保结算款 + 自费收款 + 拒付""医保结算款 = 申报金额 × 结算比例"这类内部勾稽，'
      + '**不判断医保政策口径**（拒付率与自付比例的参考区间仅用于提示，以当地医保协议为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
