/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * inventory-provision-check.js —— 存货跌价准备核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每季 / 每年计提存货跌价准备时**（以及月末结账复核时），
 * 财务要按**成本与可变现净值孰低**逐项算出应计提的跌价准备，再把
 * **期初余额 + 本期计提 − 本期转回/结转 = 期末余额** 这条余额链勾稽上。
 * 这两个数直接影响**当期利润**（资产减值损失）与**税会差异**（计提不得税前扣除），
 * 算错一定会被审计与汇算清缴追出来。完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应计提跌价准备 = 存货成本 − 可变现净值（**小于 0 时取 0** —— 孰低，不确认升值）
 *   期末准备余额   = 期初准备余额 + 本期计提 − 本期转回或结转
 *   合计行         = 各明细行**逐列**之和（应计提列是各行"孰低"结果之和，
 *                    不是"成本合计 − 可变现净值合计"—— 有 0 下限时两者不相等）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**可变现净值的估计是否恰当、也不判断税会差异怎么调整：
 *    估计售价、至完工时估计将发生的成本、估计销售费用与相关税费一律**以表里给的为准**；
 *    只对"跌价率明显偏离常见区间"做**提示**，并明确标注是参考口径。
 */

const CHECKS_GIVEN = [
  '应计提跌价准备复算（存货成本 − 可变现净值，小于 0 取 0）',
  '准备余额勾稽（期初 + 本期计提 − 本期转回或结转 = 期末）',
  '合计行逐列复核',
  '同一存货（同期间）重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '可变现净值高于成本却仍计提/保留跌价准备检测',
  '本期计提额超过应计提额检测',
  '准备余额为负检测',
  '本期转回超过期初余额提示',
  '跌价率偏离参考区间（0%~50%）提示（参考口径）',
];

const OUT_OF_SCOPE = [
  '判断可变现净值的估计是否恰当（估计售价、至完工时估计将发生的成本、估计销售费用与相关税费的取值依据）',
  '复核存货成本本身的归集与结转口径（是否含运费、加工费、分摊差异）',
  '处理存货跌价准备的税务口径与税会差异调整（资产减值损失税前扣除与纳税调整）',
  '判断计提是否经过审批、是否需要在报表附注中单独披露',
  '读取 ERP / 进销存系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考区间：仅供"明显偏离"时提示 */
const DECLINE_RATE_REF = [0, 0.5];

const SAMPLE_TEXT = [
  '期间\t存货名称\t存货成本\t可变现净值\t应计提跌价准备\t期初准备余额\t本期计提\t本期转回或结转\t期末准备余额',
  '2026-12-31\tA原材料\t100000.00\t92000.00\t8000.00\t5000.00\t3000.00\t0.00\t8000.00',
  '2026-12-31\tB库存商品\t250000.00\t200000.00\t50000.00\t30000.00\t20000.00\t0.00\t50000.00',
  '2026-12-31\tC在产品\t80000.00\t80000.00\t0.00\t6000.00\t0.00\t6000.00\t0.00',
  '2026-12-31\tD包装物\t40000.00\t39000.00\t1000.00\t0.00\t1000.00\t0.00\t1000.00',
  '合计\t\t470000.00\t411000.00\t59000.00\t41000.00\t24000.00\t6000.00\t59000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的词在前。
  //    「存货成本」里的「成本」不能被兜底的「存货」抢走，所以 item 必须排在最后。
  period: ['期间', '所属期', '会计期间', '报告期', '月份', '年度'],
  cost: ['存货成本', '期末存货成本', '账面成本', '成本'],
  nrv: ['可变现净值', '预计可变现净值', '净值'],
  shouldAccrue: ['应计提跌价准备', '应计提准备', '应计提额', '应计提'],
  beginBal: ['期初准备余额', '期初跌价准备', '期初余额', '年初余额'],
  accrued: ['本期计提额', '本期计提', '计提跌价准备', '计提额'],
  reversed: ['本期转回或结转', '转回或结转', '本期转回', '转回', '结转'],
  endBal: ['期末准备余额', '期末跌价准备', '期末余额', '年末余额'],
  item: ['存货名称', '存货类别', '存货项目', '存货编码', '品名', '存货'],
};

const LABELS = {
  period: '期间', cost: '存货成本', nrv: '可变现净值', shouldAccrue: '应计提跌价准备',
  beginBal: '期初准备余额', accrued: '本期计提', reversed: '本期转回或结转',
  endBal: '期末准备余额', item: '存货名称',
};

const REQUIRED = ['item', 'cost', 'nrv', 'shouldAccrue', 'beginBal', 'accrued', 'endBal'];
const NEG_ROLES = ['cost', 'nrv', 'shouldAccrue', 'accrued', 'reversed'];
const SUM_ROLES = ['cost', 'nrv', 'shouldAccrue', 'beginBal', 'accrued', 'reversed', 'endBal'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|合计金额)$/;

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
  if (!/^[-+]?\d*\.?\d+$/.test(s)) return null;
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/** 允许空白的列：空白按 0 计（计提表里"本期没有转回"通常就留空）；读不出数字则返回 null（该行这条检查跳过） */
function optNumber(raw) {
  if (isBlank(raw)) return 0;
  return normNumber(raw);
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, headers: [] };
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
      if ((role === 'period' || role === 'item') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns, headers };
}

const who = (it) => {
  const per = it && it.period ? String(it.period).trim() : '';
  const name = it && it.item ? String(it.item).trim() : '';
  const tag = [per, name].filter(Boolean).join(' ');
  return tag ? `${tag}（第 ${it.line} 行）` : `第 ${it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

function checkProvisionAccrual(it) {
  const cost = normNumber(it.cost);
  const nrv = normNumber(it.nrv);
  const stated = normNumber(it.shouldAccrue);
  if (cost === null || nrv === null || stated === null) return null;
  const expect = round2(Math.max(cost - nrv, 0));
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应计提额与复算不符', line: it.line,
    message: `${who(it)}：存货成本 ${cost.toFixed(2)} − 可变现净值 ${nrv.toFixed(2)} = ${round2(cost - nrv).toFixed(2)}`
      + `，孰低后应为 ${expect.toFixed(2)}，表里应计提是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}`
      + '（小于 0 的部分不确认，取 0）。',
  };
}

function checkBalanceRoll(it) {
  const begin = optNumber(it.beginBal);
  const acc = optNumber(it.accrued);
  const rev = optNumber(it.reversed);
  const end = optNumber(it.endBal);
  if (begin === null || acc === null || rev === null || end === null) return null;
  const expect = round2(begin + acc - rev);
  if (Math.abs(expect - end) <= TOL) return null;
  return {
    level: 'P0', category: '准备余额勾稽不符', line: it.line,
    message: `${who(it)}：期初 ${begin.toFixed(2)} + 本期计提 ${acc.toFixed(2)} − 本期转回或结转 ${rev.toFixed(2)}`
      + ` = ${expect.toFixed(2)}，但表里期末余额是 ${end.toFixed(2)}，相差 ${round2(end - expect).toFixed(2)}`
      + ' —— 余额链断了，利润会被直接带偏。',
  };
}

function checkTotalRows(totals, items, role) {
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

function findDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const per = String(it.period || '').trim();
    const name = String(it.item || '').trim();
    if (!per && !name) continue;
    const key = `${per}|${name}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一存货出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 同一存货同一期间计提两次，跌价准备会被重复计算。`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function findBlanks(items) {
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

function findNegativeAmounts(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 计提与转回请分列成正数；红字冲回单独列示。`,
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
    return insufficient('没有收到计提表正文（text）—— 请把「期间 / 存货名称 / 存货成本 / 可变现净值 / 应计提 / 期初余额 / 本期计提 / 本期转回 / 期末余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `计提表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${(t.headers || []).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何存货明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkProvisionAccrual(it); if (a) findings.push(a);
    const b = checkBalanceRoll(it); if (b) findings.push(b);
    for (const x of findNegativeAmounts(it)) findings.push(x);

  }
  for (const role of SUM_ROLES) {
    for (const x of checkTotalRows(t.totals, t.items, role)) findings.push(x);
  }
  for (const x of findDuplicates(t.items)) findings.push(x);
  for (const x of findBlanks(t.items)) findings.push(x);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const periodSet = new Set();
  for (const it of t.items) {
    const v = String(it.period || '').trim();
    if (v) periodSet.add(v);
  }
  const periods = periodSet.size || 1;

  let provisionTotal = 0;
  for (const it of t.items) {
    const v = normNumber(it.shouldAccrue);
    if (v !== null) provisionTotal += v;
  }

  const result = {
    status: 'success',
    service_type: 'INVENTORY_PROVISION_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods,
      provision_total: round2(provisionTotal),
      decline_rate_ref: DECLINE_RATE_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"成本与可变现净值孰低 = 应计提""期初 + 计提 − 转回 = 期末"这类内部勾稽，'
      + '**不判断可变现净值估计是否恰当、不处理税会差异**；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
