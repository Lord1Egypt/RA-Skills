/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * prepaid-card-consumption-check.js —— 预付卡消费核销核对（**免费档**；本包不含完整档实现）
 *
 * 谁在什么时候必须做这件事：**教培 / 健身 / 美容 / 餐饮这类预付费行业，每月结账前**，
 * 财务要按**预付卡（会员卡）逐张核销**：期初余额 + 本期充值 − 本期消费 = 期末余额，
 * 并且**核销必须与收入确认匹配**（本期确认收入 = 消费金额 − 退卡退款）。
 * 这两条都能手算复现，算错的后果是**预收账款与收入同时错**，还牵涉退款纠纷与增值税。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   期末余额     = 期初余额 + 充值金额 − 消费金额
 *   本期确认收入 = 消费金额 − 退卡退款
 *   合计行       = 各明细行逐列相加
 *
 * 免费档执行 6 项；完整档追加的 5 项见 CHECKS_WITHHELD（**本包只有说明文本，没有实现**）。
 * 材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**口径：赠送金额、退卡退款是否参与上面两条等式，一律**按你这张表给定的关系**复算，
 *    只对"明显异常"做提示并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '期末余额勾稽（期初余额 + 充值金额 − 消费金额 = 期末余额）',
  '确认收入勾稽（消费金额 − 退卡退款 = 本期确认收入）',
  '合计行逐列复核',
  '同一卡号重复行检测（卡号 + 期间）',
  '空白与占位符检测',
  '金额为负检测（充值 / 赠送 / 消费 / 退款 / 确认收入）',
];

const CHECKS_WITHHELD = [
  '余额为负（超支）检测（期初余额或期末余额为负）',
  '消费金额超过期初余额与充值之和检测',
  '退卡退款超过累计充值提示',
  '长期无消费卡（连续未消费月数超过参考值 12 个月）提示',
  '充值金额为零却有赠送金额提示',
];

const OUT_OF_SCOPE = [
  '判断预收卡款何时确认收入、是否适用新收入准则与履约义务分摊（属会计政策判断）',
  '核对赠送金额、退卡退款是否应当参与卡内余额与收入的两条等式（本工具按你这张表给定的口径复算，不替你们定口径）',
  '核对充值资金是否真实到账、手续费与资金存管（属资金与银行流水核对）',
  '读取会员系统 / 收银 POS 导出文件（需要你先导出成文本贴进来）',
];

/* 参考值：仅供"长期无消费"提示，不是监管口径 */
const REF_IDLE_MONTHS = 12;

const SAMPLE_TEXT = [
  '卡号\t会员名称\t期间\t期初余额\t充值金额\t赠送金额\t消费金额\t退卡退款\t本期确认收入\t期末余额\t连续未消费月数',
  'PC-2026-0001\t张伟\t2026-06\t2000.00\t1000.00\t100.00\t600.00\t0.00\t600.00\t2400.00\t0',
  'PC-2026-0002\t李娜\t2026-06\t800.00\t0.00\t0.00\t300.00\t0.00\t300.00\t500.00\t1',
  'PC-2026-0003\t王强\t2026-06\t5000.00\t2000.00\t200.00\t1200.00\t0.00\t1200.00\t5800.00\t2',
  '合计\t\t\t7800.00\t3000.00\t300.00\t2100.00\t0.00\t2100.00\t8700.00\t',
].join('\n');

const TOL = 0.01;
const TOTAL_WORDS = /^(合计|总计|小计|共计|合计行)$/;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的别名前面。
  //   「连续未消费月数」里含「消费」二字 ⇒ 必须排在 consume 之前，否则会被 consume 抢走；
  //   period 里**绝对不能**写「本期」二字，否则「本期确认收入」会被 period 抢走。
  cardNo: ['会员卡号', '卡号', '卡编号', '卡券号'],
  member: ['会员名称', '会员姓名', '客户名称', '持卡人', '会员'],
  period: ['所属期间', '所属期', '期间', '月份', '账期'],
  idleMonths: ['连续未消费月数', '未消费月数', '停用月数', '休眠月数'],
  openBal: ['期初余额', '期初卡余额', '上期结存', '期初'],
  recharge: ['充值金额', '充值额', '充值'],
  bonus: ['赠送金额', '赠送余额', '赠金', '赠送'],
  consume: ['消费金额', '核销金额', '实际消费', '消费', '核销'],
  refund: ['退卡退款', '退款金额', '退卡金额', '退卡', '退款'],
  revenue: ['本期确认收入', '确认收入金额', '确认收入', '本期收入'],
  closeBal: ['期末余额', '期末卡余额', '期末结存', '期末'],
};

const LABELS = {
  cardNo: '卡号', member: '会员名称', period: '期间', idleMonths: '连续未消费月数',
  openBal: '期初余额', recharge: '充值金额', bonus: '赠送金额', consume: '消费金额',
  refund: '退卡退款', revenue: '本期确认收入', closeBal: '期末余额',
};

const REQUIRED = ['period', 'openBal', 'recharge', 'consume', 'closeBal'];
const SUM_ROLES = ['openBal', 'recharge', 'bonus', 'consume', 'refund', 'revenue', 'closeBal'];
/* 关键字段：出现即必须填（按表头里真的有的列来判，缺列不误报） */
const BLANK_WATCH = ['cardNo', 'period', 'openBal', 'recharge', 'consume', 'closeBal'];
/* 发生额列：出现负数基本是录错方向或串行（余额列为负属完整档的"超支"检查） */
const FLOW_NEG = ['recharge', 'bonus', 'consume', 'refund', 'revenue'];

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|待确认)$/i.test(s);
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
const money = (n) => Number(n).toFixed(2);

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, present: [] };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const present = [];
  roles.forEach((r) => { if (r && present.indexOf(r) < 0) present.push(r); });
  const missingColumns = REQUIRED.filter((r) => present.indexOf(r) < 0).map((r) => LABELS[r]);
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
      if ((role === 'period' || role === 'cardNo') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns, present };
}

/** 定位用语：优先「卡号（期间）」，再退到期间 / 行号 —— 每条结论都要能被第三方找到原文那一行 */
const who = (it) => {
  const card = it && it.cardNo ? String(it.cardNo).trim() : '';
  const per = it && it.period ? String(it.period).trim() : '';
  if (card && per) return `卡号 ${card}（${per}）`;
  if (card) return `卡号 ${card}`;
  if (per) return `${per} 期`;
  return `第 ${it && it.line} 行`;
};

/** 同一张卡的键：卡号优先；没有卡号列时退化为按期间查重 */
function cardKey(it) {
  const card = String((it && it.cardNo) || '').trim();
  const per = String((it && it.period) || '').trim();
  if (card) return `${card}|${per}`;
  return per ? `|${per}` : '';
}

const rawText = (it, role) => String(it[role] === undefined ? '' : it[role]).trim();

/* ================================ 免费档检查项 ================================ */

function checkBalance(it) {
  const open = normNumber(it.openBal);
  const add = normNumber(it.recharge);
  const use = normNumber(it.consume);
  const close = normNumber(it.closeBal);
  if (open === null || add === null || use === null || close === null) return null;
  const expect = round2(open + add - use);
  if (Math.abs(expect - close) <= TOL) return null;
  return {
    line: it.line, level: 'P0', category: '期末余额复算不符',
    message: `${who(it)}：期初余额 ${money(open)} + 充值 ${money(add)} − 消费 ${money(use)} `
      + `= ${money(expect)}，表里期末余额填的是 ${money(close)}，相差 ${money(round2(close - expect))} —— `
      + '卡内余额是这三者唯一的结果，对不上就说明有漏记或多记。',
    evidence: `期初余额=${rawText(it, 'openBal')}；充值金额=${rawText(it, 'recharge')}；`
      + `消费金额=${rawText(it, 'consume')}；期末余额=${rawText(it, 'closeBal')}`,
  };
}

function checkRevenue(it) {
  const use = normNumber(it.consume);
  const refund = normNumber(it.refund);
  const rev = normNumber(it.revenue);
  if (use === null || refund === null || rev === null) return null;
  const expect = round2(use - refund);
  if (Math.abs(expect - rev) <= TOL) return null;
  return {
    line: it.line, level: 'P0', category: '确认收入复算不符',
    message: `${who(it)}：消费金额 ${money(use)} − 退卡退款 ${money(refund)} = ${money(expect)}，`
      + `表里本期确认收入填的是 ${money(rev)}，相差 ${money(round2(rev - expect))} —— `
      + '核销与收入确认必须一一对应，否则收入跨期。',
    evidence: `消费金额=${rawText(it, 'consume')}；退卡退款=${rawText(it, 'refund')}；`
      + `本期确认收入=${rawText(it, 'revenue')}`,
  };
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
    line: totals.line, level: 'P0', category: '合计行与明细之和不符',
    message: `合计行的「${LABELS[role]}」是 ${money(stated)}，各明细行相加是 ${money(sum)}，`
      + `相差 ${money(round2(stated - sum))} —— 合计行必须等于逐张卡相加。`,
    evidence: `合计行 ${LABELS[role]}=${rawText(totals.row, role)}；明细合计=${money(sum)}（${n} 行）`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const k = cardKey(it);
    if (!k || k === '|') continue;
    if (seen.has(k)) {
      out.push({
        line: it.line, level: 'P1', category: '同一卡号重复行',
        message: `${who(it)}在第 ${seen.get(k)} 行已经出现过，第 ${it.line} 行又出现一次 —— `
          + '同一张卡同一期间只能有一行，重复行会让消费与收入被算两遍。',
        evidence: `卡号=${rawText(it, 'cardNo')}；期间=${rawText(it, 'period')}；首次出现在第 ${seen.get(k)} 行`,
      });
    } else seen.set(k, it.line);
  }
  return out;
}

function checkBlanks(items, watch) {
  const out = [];
  const cols = watch && watch.length ? watch : REQUIRED;
  for (const it of items) {
    const miss = cols.filter((r) => isBlank(it[r]));
    if (!miss.length) continue;
    out.push({
      line: it.line, level: 'P0', category: '关键字段缺失或为占位符',
      message: `${who(it)}有 ${miss.length} 个关键字段是空的或占位符：`
        + `${miss.map((r) => `「${LABELS[r]}」=${rawText(it, r) || '空'}`).join('、')}。`,
      evidence: `缺失列=${miss.map((r) => LABELS[r]).join('、')}`,
    });
  }
  return out;
}

function checkNegatives(it) {
  const out = [];
  for (const role of FLOW_NEG) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      line: it.line, level: 'P1', category: '金额为负',
      message: `${who(it)}的「${LABELS[role]}」是 ${money(v)}（负数）—— `
        + '发生额出现负数基本是录错方向或串行串卡，请回原始单据核对。',
      evidence: `${LABELS[role]}=${rawText(it, role)}`,
    });
  }
  return out;
}

/* ====================== 完整档（付费）检查项（不进免费包） ====================== */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到核销表正文（text）—— 请把「卡号 / 会员名称 / 期间 / 期初余额 / 充值金额 / 消费金额 / 期末余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `核销表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(String(text).split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何预付卡核销明细行');
  }

  const watch = BLANK_WATCH.filter((r) => t.present.indexOf(r) >= 0);
  const findings = [];
  for (const it of t.items) {
    const a = checkBalance(it); if (a) findings.push(a);
    const b = checkRevenue(it); if (b) findings.push(b);
    for (const f of checkNegatives(it)) findings.push(f);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items, watch)) findings.push(f);



  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let openTotal = 0; let rechargeTotal = 0; let consumeTotal = 0;
  let refundTotal = 0; let revenueTotal = 0; let closeTotal = 0;
  const periods = new Set();
  const cards = new Set();
  for (const it of t.items) {
    const o = normNumber(it.openBal); if (o !== null) openTotal += o;
    const a = normNumber(it.recharge); if (a !== null) rechargeTotal += a;
    const u = normNumber(it.consume); if (u !== null) consumeTotal += u;
    const r = normNumber(it.refund); if (r !== null) refundTotal += r;
    const v = normNumber(it.revenue); if (v !== null) revenueTotal += v;
    const c = normNumber(it.closeBal); if (c !== null) closeTotal += c;
    const per = String(it.period || '').trim(); if (per) periods.add(per);
    const card = String(it.cardNo || '').trim(); if (card) cards.add(card);
  }
  const rows = t.items.length;
  const periodCount = periods.size || rows;

  return {
    status: 'success',
    result: {
      status: 'success',
      service_type: 'PREPAID_CARD_CONSUMPTION_CHECK',
      scope: {
        checks: CHECKS_GIVEN,
        checks_not_run: notRun,
        rows,
        periods: periodCount,
        cards: cards.size,
        open_balance_total: round2(openTotal),
        recharge_total: round2(rechargeTotal),
        consume_total: round2(consumeTotal),
        refund_total: round2(refundTotal),
        revenue_total: round2(revenueTotal),
        close_balance_total: round2(closeTotal),
        // 批量入口（batch.mjs）按这两个名字汇总：本期收到的预收卡款 / 期末还没核销的余额
        paid_in_total: round2(rechargeTotal),
        outstanding_total: round2(closeTotal),
        idle_ref_months: REF_IDLE_MONTHS,
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
      findings,
      summary: {
        rows,
        periods: periodCount,
        total: findings.length,
        p0, p1, p2,
        verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
        omitted: 0,
      },
      checks_out_of_scope: OUT_OF_SCOPE,
      note: '本版本只执行：' + CHECKS_GIVEN.join('、') + '；未执行的检查项见 scope.checks_not_run。',
      disclaimer: '只核"期初余额 + 充值 − 消费 = 期末余额""消费 − 退卡退款 = 确认收入"这类内部勾稽，'
        + '**不规定赠送金额与退卡退款是否参与等式、也不判断何时确认收入**（以你们的会计政策与合同约定为准）；'
        + '结论可由第三方用同一份输入复算。',
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
};
