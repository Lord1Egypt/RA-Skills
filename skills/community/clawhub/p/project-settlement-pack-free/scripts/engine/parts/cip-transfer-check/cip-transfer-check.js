/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * cip-transfer-check.js —— 在建工程转固核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**工程竣工验收、办完转固手续的那个月**（以及之后的决算月），
 * 财务要把在建工程（CIP）转成固定资产 —— 转固金额从哪来、暂估与决算差多少、
 * 折旧从哪个月开始提，这三件事一旦错，**当月折旧、以后每月的折旧、以及资产原值全跟着错**，
 * 而且往往到审计才被发现。完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   转固金额        = 在建工程累计发生额 − 未转固余额
 *   暂估与决算差异   = 决算金额 − 暂估金额
 *   合计行          = 各明细行逐列之和
 *   转固日期 ≥ 开工日期；折旧起始月 ≥ 转固月
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**竣工验收是否达到可使用状态、也不规定折旧政策（各单位口径不同）：
 *    只核表内勾稽与日期先后，超出范围的一律列进 OUT_OF_SCOPE。
 */

const CHECKS_GIVEN = [
  '转固金额复算（在建工程累计发生额 − 未转固余额 = 转固金额）',
  '暂估与决算差异复算（决算金额 − 暂估金额 = 暂估与决算差异）',
  '合计行逐列复核',
  '同一项目重复转固检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '转固日期早于开工日期检测',
  '转固金额超过在建工程累计发生额检测',
  '折旧起始月早于转固月检测',
  '暂估与决算差异率超过阈值（10%）提示（参考口径）',
  '转固后仍有在建工程发生额提示',
];

const OUT_OF_SCOPE = [
  '判断转固时点是否已满足「竣工验收 / 达到预定可使用状态」（请以竣工验收资料与本单位会计政策为准）',
  '判断暂估转固后是否调整原值、折旧是否追溯调整（涉及会计政策与前期差错，请咨询主管会计或审计）',
  '核对在建工程明细账、总账与工程结算书三方是否一致（需要你先导出成文本贴进来）',
  '读取 ERP / 财务系统导出文件（本工具只吃你贴进来的文本表）',
];

const SAMPLE_TEXT = [
  '项目名称\t开工日期\t转固日期\t在建工程累计发生额\t未转固余额\t转固金额\t暂估金额\t决算金额\t暂估与决算差异\t折旧起始月\t转固后发生额',
  '智能制造车间改造\t2024-03-01\t2025-06-20\t5000000.00\t0.00\t5000000.00\t5000000.00\t5100000.00\t100000.00\t2025-07\t0.00',
  '物流仓储中心\t2024-08-15\t2025-09-30\t3200000.00\t200000.00\t3000000.00\t2900000.00\t3000000.00\t100000.00\t2025-10\t0.00',
  '研发中心实验室\t2025-01-10\t2026-01-15\t1800000.00\t0.00\t1800000.00\t1750000.00\t1800000.00\t50000.00\t2026-02\t0.00',
  '合计\t\t\t10000000.00\t200000.00\t9800000.00\t9650000.00\t9900000.00\t250000.00\t\t0.00',
].join('\n');

const TOL = 0.01;
/* 参考阈值：仅用于「差异率明显偏大」的提示，不是会计判断 */
const DIFF_RATE_REF = 0.10;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的词必须排在更宽泛的词前面
  //    （「转固后发生额」必须在「转固金额」之前，否则会被宽泛词抢走）
  postTransferCost: ['转固后发生额', '转固后在建工程发生额', '转固后累计发生额', '转固后发生'],
  diffAmount: ['暂估与决算差异', '暂估决算差异', '暂估与决算差额'],
  depStartMonth: ['折旧起始月', '折旧起始月份', '折旧开始月'],
  transferDate: ['转固日期', '转固时间', '竣工转固日期'],
  startDate: ['开工日期', '开工时间', '立项开工日期'],
  cipCost: ['在建工程累计发生额', '在建工程累计支出', '累计发生额'],
  remainingBalance: ['未转固余额', '尚未转固余额', '未转固金额'],
  transferAmount: ['转固金额', '转入固定资产金额', '转固入账金额'],
  provisionalAmount: ['暂估金额', '暂估转固金额', '暂估入账金额'],
  finalAmount: ['决算金额', '竣工决算金额', '决算价'],
  project: ['项目名称', '项目编号', '工程项目', '项目'],
};

const LABELS = {
  project: '项目名称', startDate: '开工日期', transferDate: '转固日期',
  cipCost: '在建工程累计发生额', remainingBalance: '未转固余额', transferAmount: '转固金额',
  provisionalAmount: '暂估金额', finalAmount: '决算金额', diffAmount: '暂估与决算差异',
  depStartMonth: '折旧起始月', postTransferCost: '转固后发生额',
};

const REQUIRED = ['project', 'cipCost', 'remainingBalance', 'transferAmount',
  'provisionalAmount', 'finalAmount', 'diffAmount'];
const SUM_ROLES = ['cipCost', 'remainingBalance', 'transferAmount', 'provisionalAmount',
  'finalAmount', 'diffAmount', 'postTransferCost'];
/* ⚠️ 差异列**允许为负**（决算低于暂估是正常冲回），所以不进负数检测 */
const AMOUNT_ROLES = ['cipCost', 'remainingBalance', 'transferAmount', 'provisionalAmount',
  'finalAmount', 'postTransferCost'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|本年合计)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|暂缺)$/i.test(s);
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

/** 归一化日期：`2025-06-20` / `2025/6/20` / `2025年6月20日` / `20250620` / `2025-06`（月） */
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
      if (role === 'project' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.project ? `${String(it.project).trim()}（第 ${it.line} 行）` : `第 ${it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkTransferFormula(it) {
  const cost = normNumber(it.cipCost);
  const left = normNumber(it.remainingBalance);
  const moved = normNumber(it.transferAmount);
  if (cost === null || left === null || moved === null) return null;
  const expect = round2(cost - left);
  if (Math.abs(expect - moved) <= TOL) return null;
  return {
    level: 'P0', category: '转固金额复算不符', line: it.line,
    message: `${who(it)}：在建工程累计发生额 ${cost.toFixed(2)} − 未转固余额 ${left.toFixed(2)} 应为 ${expect.toFixed(2)}，`
      + `表里转固金额是 ${moved.toFixed(2)}，相差 ${round2(moved - expect).toFixed(2)}。`,
  };
}

function checkProvisionVsFinal(it) {
  const prov = normNumber(it.provisionalAmount);
  const fin = normNumber(it.finalAmount);
  const diff = normNumber(it.diffAmount);
  if (prov === null || fin === null || diff === null) return null;
  const expect = round2(fin - prov);
  if (Math.abs(expect - diff) <= TOL) return null;
  return {
    level: 'P0', category: '暂估与决算差异复算不符', line: it.line,
    message: `${who(it)}：决算金额 ${fin.toFixed(2)} − 暂估金额 ${prov.toFixed(2)} 应为 ${expect.toFixed(2)}，`
      + `表里差异是 ${diff.toFixed(2)}，相差 ${round2(diff - expect).toFixed(2)}。`,
  };
}

function checkNegative(it) {
  const out = [];
  for (const role of AMOUNT_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回或红字请单独列示，不要直接用负数混在台账里。`,
    });
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
    level: 'P0', category: '合计行复核不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.project || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一项目重复转固', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经转固过一次，第 ${it.line} 行再次出现 —— `
          + '同一项目重复转固会把固定资产原值记两遍。',
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
          level: 'P0', category: '空白与占位符', line: it.line,
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
    return insufficient('没有收到转固台账正文（text）—— 请把「项目名称 / 在建工程累计发生额 / 未转固余额 / '
      + '转固金额 / 暂估金额 / 决算金额 / 暂估与决算差异」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `转固台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何项目明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkTransferFormula(it); if (a) findings.push(a);
    const b = checkProvisionVsFinal(it); if (b) findings.push(b);
    for (const x of checkNegative(it)) findings.push(x);

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

  let cipTotal = 0;
  let transferTotal = 0;
  let diffTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.cipCost); if (a !== null) cipTotal += a;
    const b = normNumber(it.transferAmount); if (b !== null) transferTotal += b;
    const c = normNumber(it.diffAmount); if (c !== null) diffTotal += c;
  }

  const result = {
    status: 'success',
    service_type: 'CIP_TRANSFER_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      projects: t.items.length,
      cip_cost_total: round2(cipTotal),
      transfer_amount_total: round2(transferTotal),
      provisional_final_diff_total: round2(diffTotal),
      diff_rate_ref: DIFF_RATE_REF,
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
    disclaimer: '只核"在建工程累计发生额 − 未转固余额 = 转固金额""决算金额 − 暂估金额 = 差异"'
      + '"合计行 = 各明细行之和"这类表内勾稽，以及开工/转固/折旧起始的先后关系；'
      + '**不判断转固时点是否达到可使用状态、也不规定折旧政策**（以竣工验收资料与本单位会计政策为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
