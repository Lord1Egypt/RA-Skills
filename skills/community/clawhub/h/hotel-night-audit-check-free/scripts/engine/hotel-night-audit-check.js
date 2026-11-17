/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * hotel-night-audit-check.js —— 酒店夜审与房费收入核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**酒店每天夜审（Night Audit）**。前台当班的房费收入、
 * 现金与刷卡收款、渠道预付、协议单位挂账与免单，必须在交班前**当场平账** ——
 * 差一分钱都要翻单查一夜。这张表里的关系全是可复算的算术，能不能平、差在哪里，
 * 完全能算出来。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应收房费 = 出租间夜 × 平均房价
 *   实收合计 = 前台现金 + 前台刷卡 + 渠道预付 + 挂账
 *   合计行   = 各明细行同列相加（「平均房价」这类均价列不参与加总）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**房价体系、免单审批权限与挂账账期：参考区间只用于"明显偏离"时**提示**，
 *    并明确标注是参考口径，最终以本单位价格文件与授权制度为准。
 *
 * 实现约束：付费检查项用**形态 B** —— 一个付费开关常量 + 把付费检查整块包进它的分支里；
 *    不要另留"完整档才执行的检查"那类 MARKER（两种形态同时存在时，
 *    strip_free_engine 会按形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 */

const CHECKS_GIVEN = [
  '应收房费复算（出租间夜 × 平均房价 = 应收房费）',
  '实收合计复算（前台现金 + 前台刷卡 + 渠道预付 + 挂账 = 实收合计）',
  '合计行逐列复核（均价列不参与加总）',
  '同一房号同一营业日期重复行检测',
  '空白与占位符检测',
  '金额或间夜为负检测',
];

const CHECKS_WITHHELD = [
  '实收与应收差额超过参考容差（1%）提示（参考口径）',
  '出租间夜超过可售间夜检测',
  '平均房价偏离参考区间（100~5000 元）提示（参考口径）',
  '免费房（免单）比例超过参考上限（10%）提示（参考口径）',
  '渠道预付与渠道订单金额不符提示',
];

const OUT_OF_SCOPE = [
  '判断房价体系、免单审批权限与折扣政策是否合规（以本单位价格文件与授权制度为准）',
  '核对前台 PMS/POS 流水与银行到账（需要你先从系统导出成文本贴进来）',
  '处理跨夜未离店、凌晨房、钟点房与跨日切账的时间口径',
  '计算渠道佣金、平台服务费与 OTA 结算净额',
  '识别挂账单位（协议客户）的信用额度与账期',
];

/* 参考区间：仅供"明显偏离"时提示，不是判定标准 */
const ADR_REF = [100, 5000];          // 平均房价参考区间（元）
const REVENUE_TOL_RATIO = 0.01;       // 实收与应收差额参考容差（1%）
const FREE_RATIO_MAX = 0.10;          // 免费房（免单）比例参考上限（10%）

const SAMPLE_TEXT = [
  '营业日期\t房号\t出租间夜\t可售间夜\t平均房价\t应收房费\t前台现金\t前台刷卡\t渠道预付\t挂账\t实收合计\t免费房间夜\t渠道订单金额',
  '2026-06-01\t8801\t12\t20\t380.00\t4560.00\t1000.00\t1500.00\t1200.00\t860.00\t4560.00\t0\t1200.00',
  '2026-06-02\t8802\t15\t20\t400.00\t6000.00\t2000.00\t1500.00\t1500.00\t1000.00\t6000.00\t0\t1500.00',
  '2026-06-03\t8803\t12\t20\t350.00\t4200.00\t700.00\t1000.00\t1500.00\t1000.00\t4200.00\t1\t1500.00',
  '合计\t\t39\t60\t\t14760.00\t3700.00\t4000.00\t4200.00\t2860.00\t14760.00\t1\t4200.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的前面。
  //    「可售间夜」「免费房间夜」都含「间夜」，排在 nights 后面就会被 nights 抢走 ——
  //    不报缺列、不报错，只是那一列从此静默算错（header_map_check 会当场报出来）。
  period: ['营业日期', '营业日', '入住日期', '账期', '期间', '日期'],
  roomNo: ['房号', '房间号', '客房号'],
  availableNights: ['可售间夜', '可售房晚', '可用间夜', '可售房数'],
  freeRooms: ['免费房间夜', '免单间夜', '免费房晚', '免费房数', '免费房', '免单房', '免单'],
  nights: ['出租间夜', '已售间夜', '出租房晚', '出租间数', '间夜数', '间夜'],
  adr: ['平均房价', '平均出租房价', '平均房价ADR', 'ADR', '均价'],
  roomRevenue: ['应收房费', '房费收入', '应收房费收入', '房费小计'],
  cash: ['前台现金', '现金收入', '现金'],
  card: ['前台刷卡', '刷卡收入', '银行卡', '刷卡'],
  channelPrepay: ['渠道预付', '渠道预付款', 'OTA预付', '平台预付'],
  cityLedger: ['签单挂账', '应收挂账', '挂账'],
  totalReceived: ['实收合计', '实收金额', '当日实收', '实收'],
  channelOrderAmt: ['渠道订单金额', '渠道订单额', 'OTA订单金额', '平台订单金额'],
};

const LABELS = {
  period: '营业日期', roomNo: '房号', availableNights: '可售间夜', freeRooms: '免费房间夜',
  nights: '出租间夜', adr: '平均房价', roomRevenue: '应收房费', cash: '前台现金',
  card: '前台刷卡', channelPrepay: '渠道预付', cityLedger: '挂账',
  totalReceived: '实收合计', channelOrderAmt: '渠道订单金额',
};

const REQUIRED = ['period', 'roomNo', 'nights', 'adr', 'roomRevenue', 'totalReceived'];
/* 合计行要逐列复核的列：**均价列（平均房价）不参与加总** */
const SUM_ROLES = ['nights', 'availableNights', 'roomRevenue', 'cash', 'card',
  'channelPrepay', 'cityLedger', 'totalReceived', 'freeRooms', 'channelOrderAmt'];
/* 为负即异常的列（间夜与金额） */
const NEG_ROLES = ['nights', 'availableNights', 'roomRevenue', 'cash', 'card',
  'channelPrepay', 'cityLedger', 'totalReceived', 'freeRooms', 'channelOrderAmt'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|本日合计|全店合计)$/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值 —— 既不说"平账"，也不说"不平账"。',
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
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const d = it && it.period ? String(it.period).trim() : '';
  const r = it && it.roomNo ? String(it.roomNo).trim() : '';
  if (d && r) return `${d} 房号 ${r}`;
  if (d) return `${d} 第 ${it.line} 行`;
  if (r) return `房号 ${r}（第 ${it.line} 行）`;
  return `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

/** 应收房费 = 出租间夜 × 平均房价 */
function checkRoomRevenue(it) {
  const nights = normNumber(it.nights);
  const adr = normNumber(it.adr);
  const stated = normNumber(it.roomRevenue);
  if (nights === null || adr === null || stated === null) return null;
  const expect = round2(nights * adr);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应收房费与复算不符', line: it.line,
    message: `${who(it)}：出租间夜 ${nights} × 平均房价 ${adr.toFixed(2)} 应为 ${expect.toFixed(2)}，`
      + `表里应收房费是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

/** 实收合计 = 前台现金 + 前台刷卡 + 渠道预付 + 挂账 */
function checkReceivedSum(it) {
  const roles = ['cash', 'card', 'channelPrepay', 'cityLedger'];
  const parts = roles.map((r) => normNumber(it[r]));
  const stated = normNumber(it.totalReceived);
  if (parts.some((v) => v === null) || stated === null) return null;
  const sum = round2(parts.reduce((s, v) => s + v, 0));
  if (Math.abs(sum - stated) <= TOL) return null;
  const detail = roles.map((r, i) => `${LABELS[r]} ${parts[i].toFixed(2)}`).join(' + ');
  return {
    level: 'P0', category: '实收合计与分项之和不符', line: it.line,
    message: `${who(it)}：${detail} = ${sum.toFixed(2)}，但表里实收合计是 ${stated.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)} —— 这四路的和就是实收合计，必须相等。`,
  };
}

/** 间夜或金额为负 */
function checkNegative(it) {
  const bad = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) bad.push(`${LABELS[role]} ${v.toFixed(2)}`);
  }
  if (!bad.length) return null;
  return {
    level: 'P0', category: '金额或间夜为负', line: it.line,
    message: `${who(it)}：${bad.join('、')} 是负数 —— 冲回、退款或调整建议单独列示，`
      + '不要直接冲减本班收入，否则四路分项与合计都会被拉偏。',
  };
}

/** 合计行逐列复核（均价列不参与加总） */
function collectTotalRows(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
    if (!n) continue;
    sum = round2(sum);
    if (Math.abs(stated - sum) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
        + `相差 ${round2(stated - sum).toFixed(2)}。`,
    });
  }
  return out;
}

/** 同一房号同一营业日期出现多行 */
function collectDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const room = String(it.roomNo === undefined ? '' : it.roomNo).trim();
    const day = String(it.period === undefined ? '' : it.period).trim();
    if (!room || !day) continue;
    const key = `${day}|${room}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一房号同一营业日期出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— `
          + '房费收入与间夜会被重复计算，夜审必须先确认是重录还是换房。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 关键字段空白或占位符 */
function collectBlanks(items) {
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

/** 实收与应收差额超过参考容差（参考口径） */
/** 出租间夜超过可售间夜 */
/** 平均房价偏离参考区间（参考口径） */
/** 免费房（免单）比例超过参考上限（参考口径） */
/** 渠道预付与渠道订单金额不符 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到夜审表正文（text）—— 请把「营业日期 / 房号 / 出租间夜 / 可售间夜 / 平均房价 / 应收房费 / 前台现金 / 前台刷卡 / 渠道预付 / 挂账 / 实收合计」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `夜审表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何房费收入明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkRoomRevenue(it); if (a) findings.push(a);
    const b = checkReceivedSum(it); if (b) findings.push(b);
    const c = checkNegative(it); if (c) findings.push(c);

  }
  for (const x of collectTotalRows(t.totals, t.items)) findings.push(x);
  for (const x of collectDuplicates(t.items)) findings.push(x);
  for (const x of collectBlanks(t.items)) findings.push(x);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let revenueTotal = 0;
  let receivedTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.roomRevenue); if (a !== null) revenueTotal += a;
    const b = normNumber(it.totalReceived); if (b !== null) receivedTotal += b;
  }
  const days = new Set();
  for (const it of t.items) {
    const d = String(it.period === undefined ? '' : it.period).trim();
    if (d) days.add(d);
  }

  const result = {
    status: 'success',
    service_type: 'HOTEL_NIGHT_AUDIT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: days.size,
      revenue_total: round2(revenueTotal),
      received_total: round2(receivedTotal),
      tolerance: TOL,
      adr_ref: ADR_REF,
      revenue_gap_ratio_max: REVENUE_TOL_RATIO,
      free_ratio_max: FREE_RATIO_MAX,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: days.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"出租间夜 × 平均房价 = 应收房费""现金 + 刷卡 + 渠道预付 + 挂账 = 实收合计"这类内部勾稽，'
      + '**不规定房价体系、免单权限与挂账账期**（以本单位价格文件与授权制度为准）；'
      + '参考区间只用于提示；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
