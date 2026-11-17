#!/usr/bin/env node
/**
 * promo-price-compliance-check.js —— 促销价格与划线价合规核对引擎（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：电商 / 零售每次大促都要挂「原价 / 划线价 / 到手价」，运营每晚都要对一遍活动价：
 *   到手价是**每一行都要能复算的算术**（标价 − 优惠券 − 满减 − 会员折扣 = 到手价）；
 *   折扣率必须与划线价自洽；同一商品同一时段不许两个活动价并存；
 *   「促销反而更贵」、合计行对不上、字段填错都会被点名。
 *   《价格法》《明码标价和禁止价格欺诈规定》把「虚构原价 / 划线价无依据 / 虚假折价」列为价格欺诈，
 *   平台会罚、市场监管会查 —— 所以每条结论都带原文行号，可被第三方用同一口径复算。
 *
 * ⚠️ 本文件是 **免费档子集**：只实现下面这六项**表内逐行算术与台账勾稽**：
 *     ① 到手价复算；② 折扣率与划线价一致性；③ 同一商品同一时段重复登记；
 *     ④ 活动价高于日常价；⑤ 合计行逐列复核（商品数 / 优惠总额）；⑥ 字段合法性。
 *    **完整档（付费）的实现不在这个包里** —— 划线价依据链核对、券期与活动期是否匹配、
 *    库存与活动量矛盾、跨活动到手价倒挂、分商品 × 分活动汇总清单都不在这里。
 *    `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定某个价格在各平台规则下是否违规、不判定是否构成价格欺诈、不联网抓页面实时价、
 *          不读 .xlsx / .pdf 原件；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '到手价复算（标价 − 优惠券 − 满减 − 会员折扣 = 到手价，逐行复算并给出差额）',
  '折扣率与划线价一致性（到手价 ÷ 划线价 与「折扣标注」是否相符，按百分点给差）',
  '同一商品同一时段重复登记（同一商品ID 的活动期重叠、两个活动价并存即点名）',
  '活动价高于日常价（到手价高于日常价 = 促销反而更贵）',
  '合计行逐列复核（商品数、优惠总额）',
  '字段合法性（必需字段缺失、日期与活动期格式非法、价格为负或为零、折扣标注无法识别、货币单位混用）',
];

const CHECKS_WITHHELD = [
  '划线价依据链核对（跨表：划线价必须能在「近7日最低成交价」段里找到依据，找不到即点名）',
  '活动期与优惠券有效期不匹配（券在活动期之外生效或失效，逐行点名日期）',
  '库存与活动量矛盾（活动计划量 > 可售库存，报出缺口数量）',
  '跨活动比价（同一商品在两个活动里的到手价倒挂，点名两个活动与价差）',
  '分商品 × 分活动汇总清单（按差额降序 + 每组一条可整改动作，result.rollup）',
];

const OUT_OF_SCOPE = [
  '判定某个价格在各家电商平台 / 各地监管口径下到底违不违规（各平台规则不同，本工具只核台账里的算术与依据链）',
  '判定是否构成价格欺诈、该罚多少、要不要退差价（那是市场监管部门的认定权，不是本工具的结论）',
  '联网抓取平台页面上的实时价格、核验划线价或历史价的真实性（本工具只看你贴进来的材料）',
  '读取 .xlsx / .pdf / 促销海报原件，替代法务或合规官对促销文案的审查',
];

// 样例：一张**干净**的促销活动价格台账 —— 4 个商品（4 个活动），到手价逐行复算一致、
// 折扣标注与「到手价 ÷ 划线价」相符、同一商品同一时段只有一条活动价、到手价都低于日常价、
// 合计行（商品数 4 / 优惠总额 144.10）与明细一致、字段全部合法；
// 并且附一段「近7日最低成交价」：每个商品的近7日最低成交价都等于它的划线价（依据链成立）、
// 券期都在活动期之内、活动计划量都没超过可售库存、同一商品没有跨活动倒挂。**全表零命中**。
const SAMPLE_TEXT = [
  '商品名称\t商品ID\t日常价\t划线价\t标价\t优惠券\t满减\t会员折扣\t折扣标注\t到手价\t活动名称\t活动起止\t优惠券有效期\t近7日最低成交价\t活动计划量\t可售库存\t商品数\t优惠总额\t核对基准日\t备注',
  '轻氧保温杯\tSP-2026-001\t119.00\t119.00\t119.00\t20.00\t10.00\t5.70\t0.70\t83.30\t618大促\t2026-06-13~2026-06-20\t2026-06-13~2026-06-20\t119.00\t200\t260\t—\t—\t2026-06-12\t划线价与近7日最低成交价一致',
  '云感毛巾两条装\tSP-2026-002\t199.00\t199.00\t199.00\t30.00\t15.00\t4.75\t75%\t149.25\t618大促\t2026-06-14~2026-06-22\t2026-06-14~2026-06-20\t199.00\t120\t150\t—\t—\t2026-06-12\t券期在活动期之内',
  '晨光笔记本套装\tSP-2026-003\t99.00\t99.00\t99.00\t10.00\t5.00\t4.80\t8折\t79.20\t618大促\t2026-06-13~2026-06-18\t2026-06-13~2026-06-18\t99.00\t300\t400\t—\t—\t2026-06-12\t折扣标注用「8折」形态也认',
  '静音落地风扇\tSP-2026-004\t259.00\t259.00\t259.00\t20.00\t12.00\t6.85\t0.85\t220.15\t清凉一夏\t2026-06-15~2026-06-25\t2026-06-16~2026-06-24\t259.00\t80\t100\t—\t—\t2026-06-12\t库存足够覆盖活动计划量',
  '合计\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t4\t144.10\t—\t4 个商品、优惠总额 144.10 由明细行加总',
  '--- 近7日最低成交价 ---',
  '商品ID\t商品名称\t成交日期\t当日最低成交价',
  'SP-2026-001\t轻氧保温杯\t2026-06-05\t125.00',
  'SP-2026-001\t轻氧保温杯\t2026-06-08\t119.00',
  'SP-2026-001\t轻氧保温杯\t2026-06-11\t129.00',
  'SP-2026-002\t云感毛巾两条装\t2026-06-05\t205.00',
  'SP-2026-002\t云感毛巾两条装\t2026-06-09\t199.00',
  'SP-2026-002\t云感毛巾两条装\t2026-06-12\t209.00',
  'SP-2026-003\t晨光笔记本套装\t2026-06-06\t105.00',
  'SP-2026-003\t晨光笔记本套装\t2026-06-10\t99.00',
  'SP-2026-004\t静音落地风扇\t2026-06-07\t265.00',
  'SP-2026-004\t静音落地风扇\t2026-06-11\t259.00',
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺任一 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'productName', 'productId', 'normalPrice', 'listPrice', 'tagPrice',
  'coupon', 'fullReduce', 'memberDiscount', 'discountLabel', 'finalPrice',
  'activityName', 'activityPeriod', 'minPrice7d', 'checkDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['productName', '商品名称'],
  ['productId', '商品ID'],
  ['normalPrice', '日常价'],
  ['listPrice', '划线价'],
  ['tagPrice', '标价'],
  ['coupon', '优惠券'],
  ['fullReduce', '满减'],
  ['memberDiscount', '会员折扣'],
  ['discountLabel', '折扣标注'],
  ['finalPrice', '到手价'],
  ['activityName', '活动名称'],
  ['activityPeriod', '活动起止'],
  ['minPrice7d', '近7日最低成交价'],
  ['checkDate', '核对基准日'],
];

// 单日期列（格式非法逐格点名）
const DATE_FIELDS = [
  ['checkDate', '核对基准日'],
];

// 期间列（活动起止 / 优惠券有效期：必须能认出起止日期）
const PERIOD_FIELDS = [
  ['activityPeriod', '活动起止'],
  ['couponExpiry', '优惠券有效期'],
];

// 金额列（为负 / 为零 / 无法解析逐格点名）
const PRICE_ROLES = ['normalPrice', 'listPrice', 'tagPrice', 'finalPrice', 'minPrice7d'];
const DEDUCTION_ROLES = ['coupon', 'fullReduce', 'memberDiscount'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    本表的坑位：①「会员折扣」必须排在「折扣标注」之前，否则「会员折扣」被「折扣」抢走；
//    ②「优惠券有效期」必须排在「优惠券」之前，否则券期列会顶掉券金额列；
//    ③「核对基准日」必须排在兜底的「日期」之前，否则核对日期会被当成成交日期。
const ROLES = {
  productName: ['商品名称', '商品名', '品名'],
  productId: ['商品ID', '商品id', '商品编号', '商品编码', '货号', 'SKU'],
  normalPrice: ['日常价', '日常销售价', '平时价', '常规价', '非活动价'],
  tagPrice: ['标价', '标示价', '挂牌价', '页面标价'],
  listPrice: ['划线价', '划线价格', '原价', '吊牌价', '市场价', '参考价'],
  couponExpiry: ['优惠券有效期', '优惠券有效期至', '券有效期', '券有效期至'],
  coupon: ['优惠券金额', '优惠券面额', '优惠券抵扣', '优惠券', '券金额', '券面额'],
  fullReduce: ['满减金额', '满立减', '满减'],
  memberDiscount: ['会员折扣金额', '会员折扣', '会员立减', '会员优惠'],
  discountLabel: ['折扣标注', '标注折扣', '折扣率', '折扣'],
  finalPrice: ['到手价', '实付价', '用户实付', '实付金额'],
  activityPeriod: ['活动起止', '活动期间', '活动时间', '活动周期'],
  activityName: ['活动名称', '活动名', '促销活动名'],
  minPrice7d: ['近7日最低成交价', '近7日最低价', '近七日最低成交价', '7日最低成交价',
    '历史最低价', '最低成交价', '成交价'],
  planQty: ['活动计划量', '计划量', '活动量'],
  stockQty: ['可售库存', '可售数量', '库存数量', '库存'],
  itemCount: ['商品数', '商品数量', '商品件数'],
  discountTotal: ['优惠总额', '优惠合计', '优惠总金额', '优惠金额合计'],
  checkDate: ['核对基准日', '核对日期', '基准日', '核查日期'],
  recordDate: ['成交日期', '记录日期', '运行日期', '日期'],
  note: ['备注', '说明'],
};

const LABELS = {
  productName: '商品名称',
  productId: '商品ID',
  normalPrice: '日常价',
  listPrice: '划线价',
  tagPrice: '标价',
  coupon: '优惠券',
  couponExpiry: '优惠券有效期',
  fullReduce: '满减',
  memberDiscount: '会员折扣',
  discountLabel: '折扣标注',
  finalPrice: '到手价',
  activityName: '活动名称',
  activityPeriod: '活动起止',
  minPrice7d: '近7日最低成交价',
  planQty: '活动计划量',
  stockQty: '可售库存',
  itemCount: '商品数',
  discountTotal: '优惠总额',
  checkDate: '核对基准日',
  recordDate: '成交日期',
  note: '备注',
};

// 合计行要复核的列：商品数（= 明细行数）、优惠总额（= 各行优惠加总）
const SUM_ROLES = ['itemCount', 'discountTotal'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这本促销活动价格台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来'
      + '（Tab 分隔最稳）。材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「合规」，'
      + '也不说「不合规」。',
  };
}

/** 全角数字 / 全角符号 → 半角（中文输入法和 Excel 粘贴最常见的坑） */
function toHalfWidth(raw) {
  return String(raw)
    .replace(/[\uFF10-\uFF19]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0))
    .replace(/\uFF0E/g, '.')
    .replace(/\uFF0C/g, ',')
    .replace(/\uFF0D/g, '-')
    .replace(/\uFF05/g, '%')
    .replace(/\uFF0B/g, '+');
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = toHalfWidth(raw).trim().replace(/[¥￥$€£,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const round4 = (n) => Math.round(n * 10000) / 10000;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

/** 日期归一化成 YYYY-MM-DD；认不出来返回 null（认不出来绝不当成今天） */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  let s = toHalfWidth(raw).trim();
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  s = s.replace(/[年月]/g, '-').replace(/日/g, '').replace(/[.／/]/g, '-').replace(/\s+/g, '');
  if (/^\d{8}$/.test(s)) s = s.slice(0, 4) + '-' + s.slice(4, 6) + '-' + s.slice(6, 8);
  const m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = new Date(Date.UTC(y, mo - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return m[1] + '-' + String(mo).padStart(2, '0') + '-' + String(d).padStart(2, '0');
}

const DAY_MS = 86400000;
function dayNum(iso) {
  const p = iso.split('-').map(Number);
  return Date.UTC(p[0], p[1] - 1, p[2]) / DAY_MS;
}
/** b − a（整天数，正数表示 b 在 a 之后） */
function daysBetween(a, b) {
  return dayNum(b) - dayNum(a);
}

/**
 * 期间解析：`2026-06-13~2026-06-20` / `2026/6/13 至 2026/6/20` / `2026年6月13日-2026年6月20日`
 * 都认；只给一个日期时视为当天起止；认不出来返回 null（不猜）。
 */
function parsePeriod(raw) {
  const s = toHalfWidth(raw == null ? '' : raw).trim();
  if (!s || /^[-—–]+$/.test(s)) return null;
  const toks = s.match(/\d{4}\s*[-/.年]\s*\d{1,2}\s*[-/.月]\s*\d{1,2}\s*日?/g);
  if (!toks || !toks.length) return null;
  const a = normDate(toks[0]);
  const b = toks.length > 1 ? normDate(toks[1]) : a;
  if (!a || !b) return null;
  return a <= b ? { start: a, end: b, days: daysBetween(a, b) + 1 } : { start: b, end: a, days: daysBetween(b, a) + 1 };
}

/**
 * 折扣标注：只认三种形态 —— 小数（0.70）、百分数（70%）、几折（7折 / 8折 / 7.5折）。
 * 认不出来返回 null（裸写 7 / 8 这种歧义写法一律不认，交给字段合法性那一项点名）。
 */
function normDiscount(raw) {
  if (raw === undefined || raw === null) return null;
  const s = toHalfWidth(raw).trim().replace(/[，,\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  let m = /^(\d+(?:\.\d+)?)折$/.exec(s);
  if (m) {
    const v = Number(m[1]) / 10;
    return v > 0 && v <= 1 ? round4(v) : null;
  }
  m = /^(\d+(?:\.\d+)?)%$/.exec(s);
  if (m) {
    const v = Number(m[1]) / 100;
    return v > 0 && v <= 1 ? round4(v) : null;
  }
  const n = normNumber(s);
  if (n === null) return null;
  if (n > 0 && n <= 1) return round4(n);
  if (n >= 10 && n < 100) return round4(n / 100);
  return null;
}

const SECTION_RE = /^\s*-{2,}\s*(.+?)\s*-{2,}\s*$/;
function isSectionMarker(line) {
  return SECTION_RE.test(String(line == null ? '' : line));
}

function roleOf(header) {
  const h = String(header == null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

const TOTAL_LABEL = /^(合计|小计|总计|总合计|合\s*计)$/;
/** 合计行不是商品明细：逐行检查要跳过它，只有「合计行逐列复核」那一项会用到它 */
function isTotalRow(it) {
  const no = String(it.productId == null ? '' : it.productId).trim();
  const name = String(it.productName == null ? '' : it.productName).trim();
  return TOTAL_LABEL.test(no) || TOTAL_LABEL.test(name);
}

/**
 * 解析成 {header, cols, items, detail, totalRows, totals, missingRoles, missingColumns, error}。
 * items 是**扁平**对象：{line, raw, isTotal, 角色:值…}；遇到 `--- 段名 ---` 就停（后面是另一张表）。
 */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (isSectionMarker(rawLines[i])) break;
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], detail: [], totalRows: [], totals: {},
      missingRoles: REQUIRED_ROLES.slice(), missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }

  const header = splitRow(rows[0].raw);
  const cols = header.map((h, k) => ({ header: h, role: roleOf(h), index: k }));
  const items = [];
  for (let r = 1; r < rows.length; r++) {
    const cells = splitRow(rows[r].raw);
    const it = { line: rows[r].line, raw: rows[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    it.isTotal = isTotalRow(it);
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = role === 'itemCount'
      ? detail.length
      : round2(detail.reduce((acc, it) => acc + rowDiscount(it), 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    detail,
    totalRows,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

/** 一行上的优惠金额合计（优惠券 + 满减 + 会员折扣），认不出的数按 0 计（那一格由字段合法性点名） */
function rowDiscount(it) {
  let sum = 0;
  for (const role of DEDUCTION_ROLES) {
    const n = normNumber(it[role]);
    if (n !== null) sum += n;
  }
  return round2(sum);
}

function money(n) {
  const v = Math.abs(n) < 0.005 ? 0 : n;
  return v.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function who(it) {
  const name = String(it.productName == null ? '' : it.productName).trim();
  const no = String(it.productId == null ? '' : it.productId).trim();
  return `第 ${it.line} 行「${name || no || '未命名商品'}${name && no ? ' / ' + no : ''}」`;
}

const cell = (it, role) => String(it[role] == null ? '' : it[role]).trim();

/** 每条结论都带原文依据：行号 + 商品ID + 该行原文（截断），可被第三方用同一口径复算 */
function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    product_no: String(it.productId == null ? '' : it.productId).trim(),
    evidence: String(it.raw == null ? '' : it.raw).slice(0, 200),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/** 台账里第一个能认出来的核对基准日（逐行没填时兜底；逐行填了就以逐行为准） */
function baseDateOf(items) {
  for (const it of items) {
    const d = normDate(it.checkDate);
    if (d) return d;
  }
  return null;
}
const baseOf = (it, base) => normDate(it.checkDate) || base;

/* ============================ 免费档检查（六项） ============================ */

function checkFinalPrice(items) {
  // ① 到手价复算：标价 − 优惠券 − 满减 − 会员折扣 = 到手价（逐行复算，给差额）
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const tag = normNumber(it.tagPrice);
    const c = normNumber(it.coupon);
    const f = normNumber(it.fullReduce);
    const m = normNumber(it.memberDiscount);
    const fin = normNumber(it.finalPrice);
    if (tag === null || c === null || f === null || m === null || fin === null) continue;  // 缺格交给 ⑥
    const replay = round2(tag - c - f - m);
    const diff = round2(fin - replay);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding(diff > 0 ? 'P0' : 'P1', '到手价复算不符', it, diff,
      `${who(it)}：标价 ${money(tag)} − 优惠券 ${money(c)} − 满减 ${money(f)} − 会员折扣 ${money(m)}`
      + ` = ${money(replay)}，但台账（页面）写的到手价是 ${money(fin)}，`
      + `差 ${money(diff)}（台账 − 复算）。`,
      diff > 0
        ? '到手价写高了：消费者按页面到手价下单却被多收钱，属于「虚假优惠折价」的典型形态。'
          + '先按「标价 − 优惠券 − 满减 − 会员折扣」把这一行的到手价改对，再重跑；'
          + '若是某一项优惠在页面上没展示（例如会员折扣只在 App 里生效），把那项写进备注并在页面上标清。'
        : '到手价写低了：页面宣传的到手价高于实际可享优惠，顾客会拿着页面截图来要差价。'
          + '把这一行按优惠明细重算后改回真实到手价，或把少算的那项优惠补进对应列。'));
  }
  return out;
}

function checkDiscountRate(items) {
  // ② 折扣率与划线价一致性：到手价 ÷ 划线价 与「折扣标注」必须相符（按百分点给差）
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const list = normNumber(it.listPrice);
    const fin = normNumber(it.finalPrice);
    const lbl = normDiscount(it.discountLabel);
    if (list === null || fin === null || lbl === null) continue;   // 缺格 / 认不出交给 ⑥
    if (list <= 0) continue;
    const actual = round4(fin / list);
    const gap = round2((actual - lbl) * 100);                      // 百分点
    if (Math.abs(gap) < 0.5) continue;
    const pct = (x) => round2(x * 100).toFixed(2) + '%';
    out.push(finding(fin > list ? 'P0' : 'P1', '折扣率与划线价不符', it, gap,
      `${who(it)}：到手价 ${money(fin)} ÷ 划线价 ${money(list)} = ${pct(actual)}，`
      + `但「折扣标注」写的是 ${pct(lbl)}，差 ${gap} 个百分点`
      + `（${fin > list ? '到手价甚至高于划线价 —— 折价口径根本不成立' : '这两个数只能有一个是对的'}）。`,
      '折扣率与划线价必须自洽：划线价是被比较价格，标注的折扣必须等于「到手价 ÷ 划线价」。'
      + '先确认划线价有没有依据（完整档会逐条核对依据链），再把折扣标注改成算出来的真实折扣；'
      + '两个都改不动就先别挂折扣标，只写「到手价」更安全。'));
  }
  return out;
}

function checkDuplicateRegistration(items) {
  // ③ 同一商品同一时段重复登记：同一商品ID 的活动期重叠 ⇒ 两个活动价并存
  const out = [];
  const seen = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const key = cell(it, 'productId') || cell(it, 'productName');
    const p = parsePeriod(it.activityPeriod);
    if (!key || !p) continue;                       // 商品ID 空 / 活动期认不出交给 ⑥
    const prevs = seen.get(key) || [];
    const hit = prevs.find((x) => x.start <= p.end && p.start <= x.end);
    if (hit) {
      const ov = Math.min(dayNum(p.end), dayNum(hit.end)) - Math.max(dayNum(p.start), dayNum(hit.start)) + 1;
      out.push(finding('P0', '同一商品同一时段重复登记', it, ov,
        `${who(it)}：商品 ${key} 的第 ${hit.line} 行已经登记过活动「${hit.activity || '(未填)'}」`
        + `（${hit.start}~${hit.end}，到手价 ${hit.final || '(未填)'}），`
        + `本行活动「${cell(it, 'activityName') || '(未填)'}」（${p.start}~${p.end}，`
        + `到手价 ${cell(it, 'finalPrice') || '(未填)'}）与它**重叠 ${ov} 天** —— 同一商品同一时段两个活动价并存。`,
        '同一商品同一时段只能有一个到手价：重叠的两个活动会让结算、客服话术、平台比价各拿一套数。'
        + '要么把两个活动合成一个（优惠券/满减挂在同一个活动下），要么把活动期错开，'
        + '要么明确写清哪一个活动优先并只保留一条登记。'));
    }
    prevs.push({
      start: p.start, end: p.end, line: it.line,
      activity: cell(it, 'activityName'), final: cell(it, 'finalPrice'),
    });
    seen.set(key, prevs);
  }
  return out;
}

function checkPromoAboveNormal(items) {
  // ④ 活动价高于日常价：到手价 > 日常价 ⇒ 促销反而更贵
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const fin = normNumber(it.finalPrice);
    const normal = normNumber(it.normalPrice);
    if (fin === null || normal === null) continue;
    const diff = round2(fin - normal);
    if (diff <= TOL) continue;
    out.push(finding('P0', '活动价高于日常价', it, diff,
      `${who(it)}：到手价 ${money(fin)} 高于日常价 ${money(normal)}，`
      + `贵了 ${money(diff)} —— 挂着「${cell(it, 'activityName') || '促销'}」反而更贵。`,
      '「先涨价再打折」和「促销比平时更贵」都是被监管点名的价格欺诈形态：'
      + '要么把到手价压到日常价以下，要么这次活动就别挂「折扣 / 大促」的字样；'
      + '如果是日常价本身填错了（例如填的是划线价），先把日常价改成真实的平时成交价再重跑。'));
  }
  return out;
}

function checkTotals(items, cols) {
  // ⑤ 合计行逐列复核：商品数（= 明细行数）、优惠总额（= 各行优惠加总）
  const out = [];
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  for (const tr of totalRows) {
    for (const role of SUM_ROLES) {
      if (!cols.some((c) => c.role === role)) continue;
      const raw = tr[role];
      if (isBlank(raw)) continue;
      const declared = normNumber(raw);
      if (declared === null) {
        out.push(finding('P1', '合计行不符', tr, undefined,
          `第 ${tr.line} 行合计行的「${LABELS[role]}」值是「${String(raw).trim()}」，不是可识别的数字。`,
          '合计行只能写数字：请核对是否把单位（个 / 元）写进了单元格里，改完再重跑。'));
        continue;
      }
      const actual = role === 'itemCount'
        ? detail.length
        : round2(detail.reduce((acc, it) => acc + rowDiscount(it), 0));
      const diff = round2(declared - actual);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P1', '合计行不符', tr, diff,
        role === 'itemCount'
          ? `第 ${tr.line} 行合计行的「商品数」写着 ${declared}，但上面 ${detail.length} 行明细一共 ${actual} 个商品，`
            + `差 ${diff}（合计 − 明细）。`
          : `第 ${tr.line} 行合计行的「优惠总额」写着 ${money(declared)}，但上面 ${detail.length} 行明细的`
            + `「优惠券 + 满减 + 会员折扣」加总是 ${money(actual)}，差 ${money(diff)}（合计 − 明细）。`,
        '合计行必须等于明细行逐列加总：先看有没有明细行被隐藏 / 筛选掉了，再看合计公式有没有漏行或重复计数。'
        + '（本工具只核这一个合计行，不替你去别的表里找补。）'));
    }
  }
  return out;
}

const FOREIGN_CUR_RE = /[$€£]|USD|EUR|GBP|JPY|HKD|美元|欧元|英镑|日元|港币/i;

function checkFieldIntegrity(items) {
  // ⑥ 必需字段 / 日期与活动期格式 / 金额为负或为零 / 折扣标注 / 货币单位
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;

    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '字段非法', it, undefined,
        `${who(it)}：这些必需字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了（例如到手价空着就复算不了、划线价空着就判不了折扣率）；'
        + '补全后重跑，本工具不会替你猜一个默认值。'));
    }

    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw) === null) {
        out.push(finding('P1', '字段非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
          + '（只认 2026-06-12 / 2026/6/12 / 2026年6月12日 / 20260612 这几种形态）。',
          '把日期改成 2026-06-12 这种形态再跑；日期认不出来时本工具不会拿它去判任何时限。'));
      }
    }

    for (const [role, label] of PERIOD_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (parsePeriod(raw) === null) {
        out.push(finding('P1', '字段非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」认不出起止日期`
          + '（写成 2026-06-13~2026-06-20 或 2026/6/13 至 2026/6/20 这种形态）。',
          '起止日期要能认出两个日期（只写「6月大促」这种描述认不出来）；'
          + '认不出时本工具既不会判重叠、也不会判券期是否匹配 —— 那两项会如实报「没有执行」。'));
      }
    }

    for (const role of PRICE_ROLES.concat(DEDUCTION_ROLES)) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const label = LABELS[role];
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '字段非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的金额。`,
          '金额只填数字（小数用点，千分位可有可无，不要带「约」「左右」「元」这类字）；'
          + '满减要填**优惠金额**，「满300减50」这种规则写在备注里。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '字段非法', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 金额出现负数通常是填反了方向或写成了红字。`,
          '确认是红字冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      } else if (n === 0 && PRICE_ROLES.indexOf(role) >= 0) {
        out.push(finding('P1', '字段非法', it, n,
          `${who(it)}：「${label}」是 0 —— ${label}为 0 时对应的核对整项都不成立`
          + '（到手价 0、划线价 0 都不是真实的促销价格）。',
          `按真实价格填「${label}」；确实没有这项（例如不设划线价）请留空，而不是写 0。`));
      }
    }

    const dl = cell(it, 'discountLabel');
    if (dl && normDiscount(dl) === null) {
      out.push(finding('P1', '字段非法', it, undefined,
        `${who(it)}：「折扣标注」的值「${dl}」认不出来`
        + '（只认 0.70 / 70% / 7折 / 7.5折 这几种形态；裸写 7 或 8 有歧义，一律不认）。',
        '把折扣标注写成 0.70 / 70% / 7折 之一；认不出来时本工具不会拿它去和「到手价 ÷ 划线价」比对，'
        + '只会如实报「这一格没法核」。'));
    }

    for (const role of PRICE_ROLES.concat(DEDUCTION_ROLES)) {
      const v = cell(it, role);
      if (!v) continue;
      if (FOREIGN_CUR_RE.test(v)) {
        out.push(finding('P1', '字段非法', it, undefined,
          `${who(it)}：「${LABELS[role]}」的值「${v}」带了非人民币的货币单位 —— 本表按人民币口径核对。`,
          '整本台账统一成人民币（可以完全不写货币符号，也可以统一写 ¥）；'
          + '混着 $ / 美元 / USD 会在复算时被静默当成同一个数，比报错更危险。'));
      }
    }
  }

  // 表级：同一本台账里 ¥ 与 ￥ 混着写（Excel 粘贴常见的坑）
  const symRows = [];
  for (const it of items) {
    if (it.isTotal) continue;
    for (const role of PRICE_ROLES.concat(DEDUCTION_ROLES)) {
      const v = cell(it, role);
      const m = /[¥￥]/.exec(v);
      if (m) symRows.push({ sym: m[0], it });
    }
  }
  const syms = [...new Set(symRows.map((r) => r.sym))];
  if (syms.length > 1) {
    const first = symRows[0].sym;
    const bad = symRows.find((r) => r.sym !== first);
    if (bad) {
      out.push(finding('P2', '字段非法', bad.it, undefined,
        `这本台账里「¥」与「￥」混着写（第 ${bad.it.line} 行用的是「${bad.sym}」，`
        + `前面第 ${symRows[0].it.line} 行用的是「${first}」）—— 货币符号混用。`,
        '货币符号只是显示差异，但混用时不同系统导出会各自认一半：统一成一种写法（或统一不写符号）再对账。'));
    }
  }
  return out;
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的促销活动价格台账']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的促销活动价格台账']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的促销活动价格台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.detail.length) {
    return insufficient(['至少一行商品明细（现在只有表头或只有合计行，没有可核对的活动价）']);
  }

  const base = baseDateOf(t.items);
  const findings = [];
  const notRun = [];
  const dataNotes = [];

  for (const f of checkFinalPrice(t.items)) findings.push(f);
  for (const f of checkDiscountRate(t.items)) findings.push(f);
  for (const f of checkDuplicateRegistration(t.items)) findings.push(f);
  for (const f of checkPromoAboveNormal(t.items)) findings.push(f);
  for (const f of checkTotals(t.items, t.cols)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  // 免费档：完整档追加的那五项检查一项都不执行，这里如实记下来（只记「没做」，绝不伪造结论）
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const replayRows = findings.filter((f) => f.category === '到手价复算不符');
  const basisRows = findings.filter((f) => f.category === '划线价依据链');

  let noteTail = '本版本**没有**执行划线价依据链等跨表核对（未执行项见 checks_not_run）'
    + ' —— 不等于划线价有依据、也不等于券期与库存没问题。';


  const result = {
    findings,
    summary: {
      rows: t.detail.length,
      total_rows: t.totalRows.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      item_count: t.totals.itemCount,
      discount_total: t.totals.discountTotal,
      replay_mismatch_rows: replayRows.length,
      replay_diff_total: round2(replayRows.reduce((acc, f) => acc + Math.abs(f.diff || 0), 0)),
      basis_issue_rows: basisRows.length,
      check_date: base,
      basis: '到手价 = 标价 − 优惠券 − 满减 − 会员折扣（逐行复算，优惠券/满减/会员折扣三列都填**金额**）；'
        + '折扣标注必须等于「到手价 ÷ 划线价」（认 0.70 / 70% / 7折 三种形态）；'
        + '同一商品ID 的活动期不许重叠；到手价不得高于日常价；'
        + '合计行的商品数（= 明细行数）与优惠总额（= 各行优惠加总）必须等于明细行加总；'
        + '价格为负或为零、日期与活动期格式非法、折扣标注认不出一律点名。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这本台账按上面写明的口径算得对、'
      + '折扣标注与划线价自洽、合计行与明细一致**，不代表这些价格在各平台规则下一定合规、'
      + '也不代表已经过法务或监管确认 —— 那些不在本工具范围内。'
      + (notRun.length
        ? '（注意：本版本另有 ' + notRun.length + ' 项**没有执行**，未执行不等于没问题；'
          + (dataNotes.length ? dataNotes.join('；') : '') + '）'
        : (dataNotes.length ? '（注意：' + dataNotes.join('；') + '）' : ''))
      + noteTail;
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.detail.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    item_count: t.totals.itemCount,
    discount_total: t.totals.discountTotal,
    check_date: base,
  };
  result.scope = scope;
  if (dataNotes.length) result.data_notes = dataNotes;



  return { status: 'success', result };
}

/* ============================ CLI（与 run.mjs 同一套参数口径） ============================ */

const CLI_USAGE = [
  '用法：node <engine>.js --sample | --input <入参.json|台账文本> [--json] [--no-stats]',
  '  --sample   用引擎内置样例（干净样例，0 命中）',
  '  --input    入参：{"text":"…"} 或直接粘贴的促销活动价格台账文本',
  '  --json     以 JSON 输出',
  '  --no-stats 不做任何统计输出（离线）',
].join('\n');

function cliMain(argv) {
  const args = { input: '', sample: false, json: false, noStats: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--input' || a === '-i') args.input = argv[++i] || '';
    else if (a === '--sample') args.sample = true;
    else if (a === '--json') args.json = true;
    else if (a === '--no-stats') args.noStats = true;
    else if (a === '--help' || a === '-h') args.help = true;
  }
  if (args.help) {
    if (args.json) {
      console.log(JSON.stringify({ ok: true, usage: CLI_USAGE }, null, 2));
      return 0;
    }
    console.log(CLI_USAGE);
    return 0;
  }

  let payload = null;
  if (args.input) {
    let raw = '';
    try {
      raw = require('node:fs').readFileSync(args.input, 'utf8');
    } catch (e) {
      if (args.json) {
        console.log(JSON.stringify({ ok: false, error: '读不到入参文件：' + args.input }, null, 2));
        return 4;
      }
      console.error('读不到入参文件：' + args.input);
      return 4;
    }
    const trimmed = String(raw).replace(/^\uFEFF/, '').trim();
    try {
      payload = JSON.parse(trimmed);
    } catch (e) {
      payload = { text: String(raw) };
    }
  } else if (args.sample) {
    // 免费档：本包只跑免费六项，样例按免费口径跑（完整档的开关不在这个包里）
    payload = { text: SAMPLE_TEXT };
  } else {
    if (args.json) {
      console.log(JSON.stringify({ ok: false, error: '缺少入参：用 --sample 或 --input' }, null, 2));
      return 1;
    }
    console.error('缺少入参：用 --sample 或 --input');
    return 1;
  }

  let out;
  try {
    out = run(payload);
  } catch (e) {
    if (args.json) {
      console.log(JSON.stringify({ ok: false, error: String((e && e.message) || e) }, null, 2));
      return 9;
    }
    console.error('引擎执行出错：' + ((e && e.message) || e));
    return 9;
  }

  // 免费档：本包里没有付费实现，CLI 永远按免费口径输出
  if (out.status !== 'success') {
    if (args.json) {
      console.log(JSON.stringify({
        ok: false, tier: 'free', status: out.status,
        missing: out.missing, advice: out.advice,
      }, null, 2));
      return 3;
    }
    console.log('材料不足，本次没有执行任何检查，因此不出结论。');
    for (const m of (out.missing || [])) console.log('  - ' + m);
    console.log('怎么补：' + out.advice);
    return 3;
  }

  if (args.json) {
    console.log(JSON.stringify({
      ok: true,
      tier: 'free',
      checks: CHECKS_GIVEN.length,
      checks_given: CHECKS_GIVEN,
      checks_withheld: CHECKS_WITHHELD,
      omitted_findings: 0,
      result: out.result,
    }, null, 2));
    return 0;
  }
  console.log('免费档核对完成');
  console.log(`本次执行的检查项：${CHECKS_GIVEN.join('、')}`);
  console.log(`本版本不包含：${CHECKS_WITHHELD.join('、')}`);
  console.log('');
  console.log(JSON.stringify(out.result, null, 2));
  return 0;
}

if (require.main === module) {
  process.exit(cliMain(process.argv.slice(2)));
}

module.exports = {
  run, parseTable, roleOf, normNumber, normDate, round2, isBlank, splitRow, parsePeriod, normDiscount, rowDiscount, money, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
