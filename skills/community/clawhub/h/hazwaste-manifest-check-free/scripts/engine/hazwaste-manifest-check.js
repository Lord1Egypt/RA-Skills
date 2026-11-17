#!/usr/bin/env node
/**
 * hazwaste-manifest-check-full.js —— 危险废物转移联单与台账核对（确定性、纯 Node 标准库）。
 *
 * 真实痛点：产生危险废物（HW 类）的单位，按《固体废物污染环境防治法》必须建**管理台账**、
 *   转移危险废物时要执行**电子/纸质转移联单**、要按**危险废物管理计划**申报与执行，
 *   每年还要在固体废物管理信息系统里申报上一年度的产生量 / 贮存量 / 转移量 / 利用处置量。
 *   财务与安环岗位每月（每季）结账时必须把「台账 − 联单 − 出入库/贮存 − 处置合同结算」对一遍：
 *     · 每一类废物的「期初贮存 + 本期产生 − 本期转移 = 期末贮存」要成立；
 *     · 同一张联单：台账转移量 = 联单转移量、联单金额 = 处置单价 × 数量 + 运费 + 包装费；
 *     · 联单号是唯一凭证，重复登记会把同一次转移算两遍；
 *     · Excel 里常见的「合计行」每一列都要等于明细之和 —— 贮存列也要对，不能只核金额。
 *   数量或金额对不上就要查（查不出原因就没法结账、没法在年度申报前放心填报），错报会被处罚。
 *   这些格子**都能手算复现**，所以完全可以机械核对；材料不足时本工具**不给结论**。
 *
 * 检查范围分两档：免费档六项逐行核对（默认执行）；完整档在此之上追加 管理计划与执行量对比、贮存超期、
 *   跨期归属、接收单位单价一致性、分废物类别 × 接收单位的汇总整改清单。
 * ⚠️ 免费包里的同名文件由 tools/strip_free_engine.py 从本文件摘出：追加项的整块实现被删掉，
 *   因此免费包里没有这五项的代码 —— 未执行项在 CHECKS_WITHHELD 里如实列出，绝不伪造结论。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定废物是否真的属于所填 HW 类别、不判定产生/贮存/转移是否真实合规、
 *          不核验接收单位资质真伪、不读 .xlsx/.pdf 原件、不联网；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '产生量与贮存量勾稽（逐行复算 期初贮存 + 本期产生 − 本期转移 = 期末贮存，差额不为零即列出并给出差额）',
  '转移联单与台账的数量一致性（同一联单号：台账本期转移合计 = 联单转移量合计）',
  '转移联单金额勾稽（联单转移量 × 处置单价 + 运费 + 包装费 = 联单金额，逐行复算）',
  '同一联单号重复登记检测（联单号是唯一凭证，同一联单号在台账里出现两次以上即列出）',
  '合计行逐列复核（合计行每一列 = 明细之和，贮存列与金额列都要对）',
  '必需字段缺失与数值格式检测（废物类别/废物代码/单位/期初贮存/本期产生/本期转移/期末贮存/联单号/转移量/处置单价/联单金额；空白、占位符或认不出的数值逐处点名）',
];

const CHECKS_WITHHELD = [
  '管理计划与执行量对比（按废物类别汇总 计划转移量 vs 本期实际转移量，超出计划即提示）',
  '危险废物贮存超期检测（期末仍有贮存的，按入库日期与统计截止日期判断是否超过一年）',
  '跨期归属检测（联单日期不在统计期间内的，单独列出）',
  '接收单位合同单价一致性（同一接收单位在不同联单上处置单价不一致即列出）',
  '分废物类别 × 接收单位的汇总清单（按差额从大到小排序，给出可整改动作）',
];

const OUT_OF_SCOPE = [
  '判定废物是否真的属于所填 HW 类别（类别鉴定靠鉴别标准与检测报告，本工具只核字面与算术）',
  '判定危险废物的产生、贮存、转移是否真实合规（那是现场核查、执法检查与审计的职责）',
  '核验接收单位（处置单位）资质真伪、许可证是否覆盖该类别（需要官方查询，本工具不联网）',
  '替代危险废物管理计划备案、转移联单申领与年度申报等法定手续',
  '读取 .xlsx / .pdf 原件、从扫描件或图片里识别表格、联网核验联单真伪',
];

// 样例：一张**干净**的危险废物管理台账与转移联单对照表 —— 四类废物、一个统计期间（2025Q4），
// 逐行「期初 + 产生 − 转移 = 期末」成立、台账转移量与联单转移量一致、
// 联单金额 = 数量 × 单价 + 运费 + 包装费、联单号不重复、合计行各列都等于明细之和。
const SAMPLE_TEXT = [
  '废物类别\t废物代码\t单位\t期初贮存\t本期产生\t本期转移\t期末贮存\t联单号\t联单日期\t转移量\t接收单位\t处置单价\t联单金额\t运费\t包装费\t计划转移量\t入库日期\t统计起始日期\t统计截止日期\t备注',
  '废矿物油\tHW08 900-249-08\t吨\t0.50\t3.20\t3.00\t0.70\tLX2025-1001\t2025-10-18\t3.00\t江苏环泰固废处置有限公司\t1200.00\t3900.00\t300.00\t0.00\t4.00\t2025-09-20\t2025-10-01\t2025-12-31\t2025-10-18 已转移',
  '废乳化液\tHW09 900-006-09\t吨\t0.20\t2.50\t2.40\t0.30\tLX2025-1002\t2025-11-05\t2.40\t江苏环泰固废处置有限公司\t1200.00\t3120.00\t240.00\t0.00\t3.00\t2025-10-12\t2025-10-01\t2025-12-31\t2025-11-05 已转移',
  '废铅蓄电池\tHW31 900-052-31\t吨\t0.80\t1.60\t1.50\t0.90\tLX2025-1003\t2025-11-26\t1.50\t江苏中再资源循环有限公司\t800.00\t1400.00\t150.00\t50.00\t2.00\t2025-08-15\t2025-10-01\t2025-12-31\t2025-11-26 已转移',
  '废活性炭\tHW49 900-039-49\t吨\t0.00\t1.20\t1.20\t0.00\tLX2025-1004\t2025-12-08\t1.20\t江苏中再资源循环有限公司\t800.00\t1080.00\t120.00\t0.00\t1.50\t2025-12-01\t2025-10-01\t2025-12-31\t2025-12-08 已转移',
  '合计\t\t\t1.50\t8.50\t8.10\t1.90\t\t\t8.10\t\t\t9500.00\t810.00\t50.00\t10.50\t\t\t\t',
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺任何一列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'wasteCategory', 'wasteCode', 'unit', 'openingStock', 'generatedQty', 'ledgerTransfer',
  'closingStock', 'manifestNo', 'manifestQty', 'unitPrice', 'manifestAmount',
];

// 单元格级必需字段（空白/占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['wasteCategory', '废物类别'],
  ['wasteCode', '废物代码'],
  ['unit', '单位'],
  ['openingStock', '期初贮存'],
  ['generatedQty', '本期产生'],
  ['ledgerTransfer', '本期转移'],
  ['closingStock', '期末贮存'],
  ['manifestNo', '联单号'],
  ['manifestQty', '转移量'],
  ['unitPrice', '处置单价'],
  ['manifestAmount', '联单金额'],
];

// 数值列（认不出格式 ⇒ 逐处点名，绝不悄悄当成 0）
const NUMBER_FIELDS = [
  ['openingStock', '期初贮存'],
  ['generatedQty', '本期产生'],
  ['ledgerTransfer', '本期转移'],
  ['closingStock', '期末贮存'],
  ['manifestQty', '转移量'],
  ['unitPrice', '处置单价'],
  ['manifestAmount', '联单金额'],
  ['freight', '运费'],
  ['packingFee', '包装费'],
  ['plannedQty', '计划转移量'],
];

// 合计行（Excel 导出常见）：第一列写「合计/总计/小计…」的那一行不是明细
const TOTAL_ROW_RE = /^(合计|总计|小计|累计|合计行|总计行)$/;

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（本仓库踩过 6 次，见 tools/header_map_check.py）。
//    本表的三个高危点：①「接收单位」「处置单位」必须排在「单位」前面；
//    ②「本期转移」「计划转移量」必须排在「转移量」前面；③各种「…日期」必须排在「日期」前面。
const ROLES = {
  wasteCode: ['废物代码', '危废代码', '废物编号', '危废编号', '代码'],
  wasteCategory: ['废物类别', '危废类别', '废物名称', '危废名称', '类别'],
  receivingUnit: ['接收单位', '接收方', '处置单位', '受托单位', '接收企业', '处置方'],
  unit: ['计量单位', '单位'],
  openingStock: ['期初贮存', '期初库存', '期初结存', '期初贮存量', '期初量', '期初'],
  generatedQty: ['本期产生', '本期产生量', '产生量', '产生'],
  plannedQty: ['计划转移量', '管理计划量', '计划处置量', '计划转移', '计划量'],
  ledgerTransfer: ['本期转移', '台账转移量', '转移总量', '台账量'],
  manifestQty: ['联单转移量', '联单数量', '转移量', '联单量'],
  closingStock: ['期末贮存', '期末库存', '期末结存', '期末贮存量', '期末量', '期末'],
  manifestNo: ['联单号', '转移联单号', '危废联单号', '联单编号', '单据号', '凭证号'],
  stockInDate: ['入库日期', '最早入库日期', '贮存起始日期', '入库时间', '入库'],
  periodStart: ['统计起始日期', '本期起始日期', '起始日期', '期初日期'],
  periodEnd: ['统计截止日期', '本期截止日期', '数据截止日期', '截止日期', '期末日期'],
  manifestDate: ['联单日期', '转移日期', '联单时间', '出库日期', '日期'],
  unitPrice: ['处置单价', '合同单价', '处置费单价', '单价'],
  manifestAmount: ['联单金额', '联单总金额', '联单合计金额', '转移金额', '金额'],
  freight: ['运费', '运输费', '运输费用'],
  packingFee: ['包装费', '包装材料费', '包装费用'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  wasteCategory: '废物类别',
  wasteCode: '废物代码',
  unit: '单位',
  openingStock: '期初贮存',
  generatedQty: '本期产生',
  ledgerTransfer: '本期转移',
  closingStock: '期末贮存',
  manifestNo: '联单号',
  manifestDate: '联单日期',
  manifestQty: '转移量',
  receivingUnit: '接收单位',
  unitPrice: '处置单价',
  manifestAmount: '联单金额',
  freight: '运费',
  packingFee: '包装费',
  plannedQty: '计划转移量',
  stockInDate: '入库日期',
  periodStart: '统计起始日期',
  periodEnd: '统计截止日期',
  note: '备注',
};

// 可加的列（合计行逐列复核与总量口径都用这一组；单价不可加，刻意不列）
const SUM_ROLES = [
  'openingStock', 'generatedQty', 'ledgerTransfer', 'closingStock',
  'manifestQty', 'plannedQty', 'manifestAmount', 'freight', 'packingFee',
];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「对得上」，也不说「对不上」，更不会给出「全部对上了」这类结论。',
  };
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核|见附页)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
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

function cell(it, role) {
  return it[role] === undefined ? '' : it[role];
}

/** 合计行判定：第一列写「合计/总计/小计…」（或废物代码列这样写）的那一行不是明细 */
function isTotalRow(it) {
  const cat = String(cell(it, 'wasteCategory')).trim();
  const code = String(cell(it, 'wasteCode')).trim();
  return TOTAL_ROW_RE.test(cat) || TOTAL_ROW_RE.test(code);
}

function groupBy(rows, keyOf) {
  const map = new Map();
  for (const it of rows) {
    const k = keyOf(it);
    if (!map.has(k)) map.set(k, []);
    map.get(k).push(it);
  }
  return map;
}

/** 解析成 {header, cols, items, totals, missingRoles, missingColumns, error}；行是**扁平**对象：{line, raw, 角色:值…, isTotal} */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], totals: {},
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

  const detail = items.filter((it) => !it.isTotal);
  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(detail.reduce((acc, it) => {
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

const num = (it, role) => {
  const n = normNumber(it[role]);
  return n === null ? 0 : n;
};

function money(n) {
  const v = Math.abs(n) < 0.005 ? 0 : n;
  return v.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function who(it) {
  const cat = String(cell(it, 'wasteCategory')).trim();
  const code = String(cell(it, 'wasteCode')).trim();
  const label = cat && code ? cat + ' ' + code : (cat || code || '未命名废物');
  return '第 ' + it.line + ' 行「' + label + '」';
}

function lineList(rows) {
  return rows.map((it) => it.line).join('、');
}

function finding(level, category, it, diff, message, advice) {
  const f = { level, category, line: it.line, message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/* ============================ 免费档检查（六项） ============================ */

/** 1. 产生量与贮存量勾稽：期初贮存 + 本期产生 − 本期转移 = 期末贮存 */
function checkMassBalance(items) {
  const out = [];
  for (const it of items) {
    const o = normNumber(it.openingStock);
    const g = normNumber(it.generatedQty);
    const t = normNumber(it.ledgerTransfer);
    const c = normNumber(it.closingStock);
    if (o === null || g === null || t === null || c === null) continue;   // 缺失/认不出交给「必需字段」那一项
    const diff = round2(o + g - t - c);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '贮存量勾稽不平', it, diff,
      who(it) + '：期初贮存 ' + money(o) + ' + 本期产生 ' + money(g) + ' − 本期转移 ' + money(t)
      + ' = ' + money(round2(o + g - t)) + '，与期末贮存 ' + money(c) + ' 差 ' + money(diff)
      + '（期末' + (diff > 0 ? '少记了' : '多记了') + ' ' + money(Math.abs(diff)) + '）。',
      '按「期初 + 产生 − 转移 = 期末」逐行复算：常见原因是漏记一次转移、期末结存抄错、或把上期数据混进本期。'
      + '本工具只列出差额，不认定是哪种原因。'));
  }
  return out;
}

/** 2. 转移联单与台账的数量一致性（同一联单号：台账本期转移合计 = 联单转移量合计） */
function checkManifestQty(items) {
  const out = [];
  const groups = groupBy(items, (it) => String(cell(it, 'manifestNo')).trim());
  for (const [no, rows] of groups) {
    if (!no) continue;                                                  // 空联单号交给「必需字段」那一项
    const ledger = rows.map((it) => normNumber(it.ledgerTransfer));
    const manifest = rows.map((it) => normNumber(it.manifestQty));
    if (ledger.some((x) => x === null) || manifest.some((x) => x === null)) continue;
    const sumLedger = round2(ledger.reduce((a, b) => a + b, 0));
    const sumManifest = round2(manifest.reduce((a, b) => a + b, 0));
    const diff = round2(sumLedger - sumManifest);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '联单与台账数量不符', rows[0], diff,
      '联单号「' + no + '」（第 ' + lineList(rows) + ' 行）：台账本期转移合计 ' + money(sumLedger)
      + '，联单转移量合计 ' + money(sumManifest) + '，差 ' + money(diff) + '。',
      '一张联单对应一次转移：先按联单原件核对数量，差额不为零时查是否漏抄/多抄，'
      + '再查是否有分次转移共用一张联单。本工具只列差额。'));
  }
  return out;
}

/** 3. 转移联单金额勾稽：联单转移量 × 处置单价 + 运费 + 包装费 = 联单金额 */
function checkManifestAmount(items) {
  const out = [];
  for (const it of items) {
    const q = normNumber(it.manifestQty);
    const price = normNumber(it.unitPrice);
    const amt = normNumber(it.manifestAmount);
    if (q === null || price === null || amt === null) continue;
    const fr = normNumber(it.freight);
    const pk = normNumber(it.packingFee);
    const freight = fr === null ? 0 : fr;
    const packing = pk === null ? 0 : pk;
    const expect = round2(q * price + freight + packing);
    const diff = round2(amt - expect);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '联单金额勾稽不符', it, diff,
      who(it) + '：转移量 ' + money(q) + ' × 处置单价 ' + money(price) + ' + 运费 ' + money(freight)
      + ' + 包装费 ' + money(packing) + ' = ' + money(expect) + '，联单金额写的是 ' + money(amt)
      + '，差 ' + money(diff) + '。',
      '按联单原件逐行复算：数量、单价、运费、包装费四项里至少有一项与合同/联单不一致；'
      + '若运费与包装费已含在单价里，请把这两列清空（空白按 0 参与勾稽）。'));
  }
  return out;
}

/** 4. 同一联单号重复登记（联单号是唯一凭证，重复即可能重复计转移量） */
function checkDuplicateManifest(items) {
  const out = [];
  const groups = groupBy(items, (it) => String(cell(it, 'manifestNo')).trim());
  for (const [no, rows] of groups) {
    if (!no || rows.length < 2) continue;
    out.push(finding('P0', '联单号重复登记', rows[rows.length - 1], undefined,
      '联单号「' + no + '」在台账里出现 ' + rows.length + ' 次（第 ' + lineList(rows) + ' 行）—— '
      + '联单号是唯一凭证，重复登记可能把同一次转移的数量与金额算了两遍。',
      '核对联单原件：确属同一次转移的，删掉多余行只留一行；确属分次转移的，每次转移应各有联单号，请补正确的联单号。'));
  }
  return out;
}

/** 5. 合计行逐列复核（合计行每一列 = 明细之和；贮存列也要对，不能只核金额） */
function checkTotalRow(items) {
  const out = [];
  const totalsRows = items.filter((it) => it.isTotal);
  const details = items.filter((it) => !it.isTotal);
  for (const tr of totalsRows) {
    for (const role of SUM_ROLES) {
      if (tr[role] === undefined) continue;                             // 表里没有这一列
      const declared = normNumber(tr[role]);
      const sum = round2(details.reduce((a, it) => a + num(it, role), 0));
      if (declared === null) {
        out.push(finding('P1', '合计行与明细不符', tr, undefined,
          '第 ' + tr.line + ' 行「合计」：「' + LABELS[role] + '」是空的或认不出的数值，'
          + '而 ' + details.length + ' 行明细按这一列相加应为 ' + money(sum) + '。',
          '合计行本工具不补算：请把合计行改成公式（=SUM(明细区域)）后再复制，别手改数值，贮存列与金额列都要是公式。'));
        continue;
      }
      const diff = round2(declared - sum);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P1', '合计行与明细不符', tr, diff,
        '第 ' + tr.line + ' 行「合计」：「' + LABELS[role] + '」写的是 ' + money(declared)
        + '，但 ' + details.length + ' 行明细按这一列相加为 ' + money(sum) + '，差 ' + money(diff) + '。',
        '合计行只该是明细的算术和（期初/期末贮存列与金额列一样要能对上）；请把合计行改成公式后再复制。'));
    }
  }
  return out;
}

/** 6. 必需字段缺失与数值格式检测（空白/占位符/认不出格式 ⇒ 逐处点名） */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(cell(it, role))).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '必需字段缺失', it, undefined,
        who(it) + '：这些必需单元格是空的或占位符 —— ' + miss.join('、') + '。',
        '空着的格子会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }
    const bad = [];
    for (const [role, label] of NUMBER_FIELDS) {
      if (it[role] === undefined) continue;
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normNumber(raw) === null) bad.push(label + '「' + String(raw).trim() + '」');
    }
    if (bad.length) {
      out.push(finding('P1', '数值无法解析', it, undefined,
        who(it) + '：这些格子的值不是可识别的数值 —— ' + bad.join('、') + '（只认数字、千分位、¥ 与括号负数）。',
        '把数值改成纯数字形态（如 3.00 / 1200.00）再跑；看不懂的值本工具**不会**当成 0，也不会替你补算。'));
    }
  }
  return out;
}

/* ===== 补充检查（完整档）：管理计划 / 贮存超期 / 跨期归属 / 单价一致性 / 汇总清单 =====
   免费档不执行这一节的任何一项（未执行项在 CHECKS_WITHHELD 里如实列出，不在这里实现）。 */

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的危险废物管理台账与转移联单对照表']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的危险废物管理台账与转移联单对照表']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的危险废物管理台账与转移联单对照表（至少要能认出「'
        + REQUIRED_ROLES.map((r) => LABELS[r]).join('」「') + '」）',
      t.missingRoles.length
        ? '本次没认出来的必需列：' + t.missingColumns.join('、')
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行废物明细（现在只有表头，没有可核对的明细行）']);
  }

  const details = t.items.filter((it) => !it.isTotal);
  if (!details.length) {
    return insufficient(['至少一行废物明细（现在只有表头与合计行，没有可逐行核对的明细）']);
  }

  const findings = [];
  const notRun = [];

  for (const f of checkMassBalance(details)) findings.push(f);
  for (const f of checkManifestQty(details)) findings.push(f);
  for (const f of checkManifestAmount(details)) findings.push(f);
  for (const f of checkDuplicateManifest(details)) findings.push(f);
  for (const f of checkTotalRow(t.items)) findings.push(f);
  for (const f of checkFieldIntegrity(details)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const openingTotal = t.totals.openingStock;
  const generatedTotal = t.totals.generatedQty;
  const transferTotal = t.totals.ledgerTransfer;
  const closingTotal = t.totals.closingStock;
  const manifestQtyTotal = t.totals.manifestQty;
  const amountTotal = t.totals.manifestAmount;
  const planTotal = t.totals.plannedQty;
  const balanceDiff = round2(openingTotal + generatedTotal - transferTotal - closingTotal);
  const qtyDiff = round2(transferTotal - manifestQtyTotal);

  const result = {
    findings,
    summary: {
      rows: details.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      opening_total: openingTotal,
      generated_total: generatedTotal,
      transfer_total: transferTotal,
      closing_total: closingTotal,
      manifest_qty_total: manifestQtyTotal,
      manifest_amount_total: amountTotal,
      plan_total: planTotal,
      balance_diff_total: balanceDiff,
      qty_diff_total: qtyDiff,
      basis: '逐行「期初贮存 + 本期产生 − 本期转移 = 期末贮存」；同一联单号 台账转移量 = 联单转移量；'
        + '联单金额 = 联单转移量 × 处置单价 + 运费 + 包装费；联单号在本表内唯一；'
        + '合计行每一列 = 明细之和（含贮存列）；数量与金额按两位小数复算，差 0.01 以内视为相等。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表的算术与勾稽按上面写明的口径都对得上**，'
      + '不代表废物类别鉴定、产生/贮存/转移的真实合规性、接收单位资质或年度申报数据已经过关 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: details.length,
    total_rows_ignored: t.items.length - details.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    opening_total: openingTotal,
    generated_total: generatedTotal,
    transfer_total: transferTotal,
    closing_total: closingTotal,
    manifest_qty_total: manifestQtyTotal,
    manifest_amount_total: amountTotal,
    plan_total: planTotal,
    balance_diff_total: balanceDiff,
    qty_diff_total: qtyDiff,
  };
  result.scope = scope;



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
