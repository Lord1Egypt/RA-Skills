#!/usr/bin/env node
/**
 * lab-sample-retention-check.js —— 检测样品流转与留样期限核对（**免费档**；确定性、纯 Node 标准库）
 *
 * 真实痛点：第三方检测机构与企业实验室按 CMA、CNAS 与质量体系要求，样品必须
 *   **唯一标识、状态受控、留样到规定期限、到期处置有记录**，并且
 *   「收样 — 流转 — 检测 — 留样 — 处置」每个环节的数量都要对得上。
 *   评审与飞行检查最常见的整改项就是这三条：**留样数量对不上、留样超期未处置、流转与交接记录断档**。
 *   样品管理员与质量部每个月都得把样品台账、交接单、留样期限、处置记录、样品状态与数量勾稽核一遍。
 *
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 *    `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 *    本版本**只做**表内逐行算术、清单勾稽与字段校验，
 *    **不做**超期未处置清单、处置记录核对、样品状态与检测记录冲突、同类样品留样期限一致性、
 *    分检测项目 × 分委托单位的超期汇总清单。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定样品是否合格、不判定检测结论是否成立、不替你认定「这类样品该留多久」是否符合某部标准、
 *          不读 .xlsx / .pdf 原件、不联网核验委托单与资质证书真伪；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '样品数量勾稽（逐行复算 收样数量 − 已检数量 − 退样数量 = 留样数量，差额不为零即列出并给出差额）',
  '留样期限核对（留样开始日期 + 留样期限 = 应处置日期，按核对基准日给出超期天数；已处置的核对处置是否逾期）',
  '交接单与台账一致性（交接数量 vs 收样数量、交接样品编号 vs 样品编号，不一致即给两处原文）',
  '同一委托编号 + 同一检测项目重复登记检测（同一组合第二次出现即点名后出现的那一行）',
  '合计行逐列复核（数量类列：合计行写的数与逐行相加的数不一致即报出差额）',
  '空白/占位符/日期格式/样品状态值非法检测（含数量无法解析、数量为负、留样期限无法解析）',
];

const CHECKS_WITHHELD = [
  '超期未处置清单（应处置日期已过但仍为「留样」状态的样品，点名样品编号与超期天数，按超期天数排序）',
  '处置记录与交接单不一致（处置数量 > 台账留样数量、已登记处置日期却缺处置人）',
  '样品状态与检测记录冲突（已检但无检测完成日期 / 在检但已过承诺完成日期）',
  '留样期限按样品类型/检测标准不一致（同类样品出现多个期限值，给两处原文）',
  '分检测项目 × 分委托单位的超期汇总清单（按超期数量排序并给出可整改动作）与 consolidated_actions',
];

const OUT_OF_SCOPE = [
  '判定样品是否合格、检测结论是否成立（那是检测人员与授权签字人的职责），本工具只核台账字面与算术',
  '替你认定「这类样品/这个检测标准应该留多久」（那是标准与体系文件的规定值），本工具只核表内同类样品的期限是否自相矛盾',
  '判定样品唯一性标识体系、留样室环境与双人双锁等实物管理是否达标（那是内审与现场评审的事）',
  '读取 .xlsx / .pdf 原件、联网核验委托单与 CMA/CNAS 资质证书真伪、替代内审或管理评审',
];

// 样例：一张**干净**的检测样品台账（含交接、留样期限、处置与合计行）——
// 六件样品四条流转状态：留样 3 件、已检 1 件、在检 2 件、已处置 1 件；
// 逐行「收样 − 已检 − 退样 = 留样」成立、交接数量与样品编号两边一致、
// 留样都在期限内、已处置的在应处置日期当天处置、合计行逐列等于明细相加。
const SAMPLE_TEXT = [
  '样品编号\t委托编号\t委托单位\t样品名称\t样品类型\t检测项目\t检测标准\t收样日期\t收样数量\t已检数量\t退样数量\t留样数量\t交接数量\t交接样品编号\t留样开始日期\t留样期限(天)\t样品状态\t检测完成日期\t承诺完成日期\t处置日期\t处置数量\t处置人\t备注',
  'YP2506-001\tWT2025-0612\t江苏远望化工材料有限公司\t工业氢氧化钠\t化工原料\t氢氧化钠含量\tGB/T 209-2018\t2025-06-12\t6\t2\t1\t3\t6\tYP2506-001\t2025-06-13\t90\t留样\t2025-06-18\t2025-06-25\t\t\t\t留样至 2025-09-11',
  'YP2506-002\tWT2025-0612\t江苏远望化工材料有限公司\t工业氢氧化钠\t化工原料\t碳酸钠含量\tGB/T 209-2018\t2025-06-12\t4\t4\t0\t0\t4\tYP2506-002\t\t\t已检\t2025-06-20\t2025-06-25\t\t\t\t已检毕，无需留样',
  'YP2506-003\tWT2025-0618\t苏州新岭建材科技有限公司\t水泥胶砂试块\t建材\t抗压强度\tGB/T 17671-2021\t2025-06-18\t9\t3\t0\t6\t9\tYP2506-003\t2025-06-19\t180\t留样\t2025-06-24\t2025-06-30\t\t\t\t留样 6 件',
  'YP2506-005\tWT2025-0620\t苏州新岭建材科技有限公司\t水泥胶砂试块\t建材\t抗压强度\tGB/T 17671-2021\t2025-06-20\t6\t2\t0\t4\t6\tYP2506-005\t2025-06-21\t180\t留样\t2025-06-26\t2025-07-02\t\t\t\t留样 4 件',
  'YP2506-006\tWT2025-0622\t无锡泰嘉电子有限公司\t印制电路板\t电子\t可焊性\tIPC J-STD-003\t2025-06-22\t8\t1\t0\t7\t8\tYP2506-006\t2025-06-23\t60\t在检\t\t2025-08-05\t\t\t\t尚在检测中',
  'YP2506-007\tWT2025-0624\t常州博汇食品有限公司\t速冻水饺\t食品\t菌落总数\tGB 4789.2-2022\t2025-06-24\t5\t3\t0\t2\t5\tYP2506-007\t2025-06-25\t30\t已处置\t2025-06-28\t2025-07-03\t2025-07-25\t2\t沈悦\t留样期满当日销毁',
  '合计\t\t\t\t\t\t\t\t38\t15\t1\t22\t38\t\t\t\t\t\t\t\t2\t\t本批 6 件',
].join('\n');

const TOL = 0.01;
const DAY_MS = 86400000;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'sampleNo', 'clientNo', 'sampleName', 'testItem', 'receiveDate', 'receiveQty', 'testedQty',
  'returnQty', 'retainQty', 'retainStartDate', 'retainDays', 'status', 'disposeDate', 'disposer',
];

// 单元格级必填字段（空白/占位符 ⇒ 逐行点名）。处置日期与处置人**故意不列**：
// 还在留样的样品本来就没有这两项，缺了不算错。
const REQUIRED_FIELDS = [
  ['sampleNo', '样品编号'],
  ['clientNo', '委托编号'],
  ['sampleName', '样品名称'],
  ['testItem', '检测项目'],
  ['receiveDate', '收样日期'],
  ['receiveQty', '收样数量'],
  ['testedQty', '已检数量'],
  ['returnQty', '退样数量'],
  ['retainQty', '留样数量'],
  ['status', '样品状态'],
];

// 数量类列（用于「无法解析 / 为负」判定）
const QTY_FIELDS = [
  ['receiveQty', '收样数量'],
  ['testedQty', '已检数量'],
  ['returnQty', '退样数量'],
  ['retainQty', '留样数量'],
  ['handoverQty', '交接数量'],
  ['disposeQty', '处置数量'],
];

// 日期列（用于「格式非法」判定）
const DATE_FIELDS = [
  ['receiveDate', '收样日期'],
  ['retainStartDate', '留样开始日期'],
  ['disposeDate', '处置日期'],
  ['testDoneDate', '检测完成日期'],
  ['promisedDate', '承诺完成日期'],
];

// 核对基准日的默认来源：只认**发生过的事实日期**（承诺完成日期是承诺、不是事实，不参与取最大值）
const BASELINE_DATE_ROLES = ['receiveDate', 'retainStartDate', 'testDoneDate', 'disposeDate'];

// 样品状态只认这五个值
const LEGAL_STATUS = ['待检', '在检', '已检', '留样', '已处置'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，**更具体的词必须排在更宽泛的前面**（本仓库踩过 6 次，见 tools/header_map_check.py）。
//    · `交接样品编号` 必须排在 `样品编号` 前面：否则前者会被后者抢走，两列落到同一个角色、互相覆盖。
//    · `承诺完成日期` 必须排在 `检测完成日期` 前面：否则「完成日期」这个宽泛词会把承诺那一列抢走。
//    · `留样数量` 只认「留样数量/留样数」，**不许**用光秃秃的「留样」——那会把「留样开始日期」「留样期限」也抢走。
const ROLES = {
  handoverNo: ['交接样品编号', '交接单样品编号', '交接样品号', '交接编号'],
  sampleNo: ['样品编号', '样品序号', '样品编码', '样品号'],
  clientNo: ['委托编号', '委托单号', '受理编号', '合同编号', '委托号'],
  clientUnit: ['委托单位', '委托方', '送检单位', '客户名称'],
  sampleName: ['样品名称', '样品名', '检品名称'],
  sampleType: ['样品类型', '样品类别', '样品种类', '样品基质'],
  testItem: ['检测项目', '检验项目', '测试项目', '检测参数', '项目'],
  testStandard: ['检测标准', '检验标准', '测试标准', '执行标准', '标准依据'],
  receiveDate: ['收样日期', '收样时间', '样品接收日期', '接收日期'],
  receiveQty: ['收样数量', '收样数', '收到数量'],
  testedQty: ['已检数量', '已检数', '检测完成数量'],
  returnQty: ['退样数量', '退样数', '退回数量'],
  retainQty: ['留样数量', '留样件数', '留样数'],
  handoverQty: ['交接数量', '交接单数量', '交接数'],
  retainStartDate: ['留样开始日期', '留样起始日期', '开始留样日期', '留样日期'],
  retainDays: ['留样期限', '留样保存期限', '保存期限', '留样期'],
  status: ['样品状态', '当前状态', '状态'],
  promisedDate: ['承诺完成日期', '承诺完成时间', '约定完成日期', '合同完成日期', '承诺日期'],
  testDoneDate: ['检测完成日期', '检验完成日期', '测试完成日期', '检测完成时间', '完成日期'],
  disposeDate: ['处置日期', '销毁日期', '处置时间'],
  disposeQty: ['处置数量', '销毁数量', '处置数'],
  disposer: ['处置人', '处置人员', '销毁人', '经办人'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  handoverNo: '交接样品编号',
  sampleNo: '样品编号',
  clientNo: '委托编号',
  clientUnit: '委托单位',
  sampleName: '样品名称',
  sampleType: '样品类型',
  testItem: '检测项目',
  testStandard: '检测标准',
  receiveDate: '收样日期',
  receiveQty: '收样数量',
  testedQty: '已检数量',
  returnQty: '退样数量',
  retainQty: '留样数量',
  handoverQty: '交接数量',
  retainStartDate: '留样开始日期',
  retainDays: '留样期限(天)',
  status: '样品状态',
  promisedDate: '承诺完成日期',
  testDoneDate: '检测完成日期',
  disposeDate: '处置日期',
  disposeQty: '处置数量',
  disposer: '处置人',
  note: '备注',
};

const SUM_ROLES = ['receiveQty', 'testedQty', 'returnQty', 'retainQty', 'handoverQty', 'disposeQty'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「对得上」，也不说「对不上」。',
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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核)$/i.test(s);
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

/** 取单元格原文（去首尾空格） */
function cell(it, role) {
  const v = it == null ? '' : it[role];
  return v === undefined || v === null ? '' : String(v).trim();
}

/** 取数量，解析不了按 0 计（只在「字段完整性」已单独点名之后使用） */
function itNum(it, role) {
  const n = normNumber(cell(it, role));
  return n === null ? 0 : n;
}

function sumRole(items, role) {
  return round2(items.reduce((acc, it) => acc + itNum(it, role), 0));
}

/** 合计行判定：靠**角色值**而不是整行字符串，避免备注里出现「合计」两个字就误判 */
function isTotalRow(it) {
  const marks = [cell(it, 'sampleNo'), cell(it, 'clientNo'), cell(it, 'sampleName'), cell(it, 'testItem')];
  return marks.some((v) => /^(合计|小计|总计|共计|总合计|合 计)$/.test(v));
}

/** 解析日期：认 2025-06-12 / 2025/6/12 / 2025.6.12 / 2025年6月12日；返回 {y,m,d,day} 或 null */
function parseDate(raw) {
  const s = raw === undefined || raw === null ? '' : String(raw).trim();
  if (!s || isBlank(s)) return null;
  const m = /(\d{4})\s*[-/.年]\s*(\d{1,2})\s*[-/.月]\s*(\d{1,2})\s*日?/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = Date.UTC(y, mo - 1, d);
  const chk = new Date(dt);
  if (chk.getUTCFullYear() !== y || chk.getUTCMonth() !== mo - 1 || chk.getUTCDate() !== d) return null;
  return { y, m: mo, d, day: Math.round(dt / DAY_MS) };
}

function fmtDate(d) {
  if (!d || typeof d.day !== 'number') return '';
  const dt = new Date(d.day * DAY_MS);
  const p = (x) => (x < 10 ? '0' + x : String(x));
  return dt.getUTCFullYear() + '-' + p(dt.getUTCMonth() + 1) + '-' + p(dt.getUTCDate());
}

/** 留样期限：纯数字 或 `N天` 按天；`N个月`/`N月` 按 30 天/月折算（折算会在结论里写明） */
function parseRetentionDays(raw) {
  const s = raw === undefined || raw === null ? '' : String(raw).trim().replace(/\s/g, '');
  if (!s || isBlank(s)) return null;
  let m = /^(\d+(?:\.\d+)?)(?:天|日|d|D)?$/.exec(s);
  if (m) return { days: Number(m[1]), approx: false };
  m = /^(\d+(?:\.\d+)?)(?:个?月|m|M)$/.exec(s);
  if (m) return { days: round2(Number(m[1]) * 30), approx: true };
  return null;
}

/** 应处置日期 = 留样开始日期 + 留样期限 */
function dueDate(it) {
  const start = parseDate(it == null ? '' : it.retainStartDate);
  const term = parseRetentionDays(cell(it, 'retainDays'));
  if (!start || !term) return null;
  return { day: start.day + Math.round(term.days), start, term };
}

function dueText(due) {
  const base = fmtDate(due);
  return due.term && due.term.approx ? `${base}（留样期限写的是月，按 30 天/月折算）` : base;
}

function statusOf(it) {
  return cell(it, 'status');
}

function qfmt(n) {
  return String(round2(n));
}

function who(it) {
  const no = cell(it, 'sampleNo');
  const name = cell(it, 'sampleName');
  return `第 ${it.line} 行「${no || '(无样品编号)'}${name ? ' ' + name : ''}」`;
}

function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    raw: String(it.raw == null ? '' : it.raw),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/** 解析成 {header, cols, items, details, totalRows, totals, missingRoles, missingColumns, error}；
 *  行是**扁平**对象：{line, raw, 角色:值…}。`totals` 只累加明细行（不含合计行，避免双重计数）。 */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], details: [], totalRows: [], totals: {},
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
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const details = items.filter((it) => !isTotalRow(it));
  const totalRows = items.filter((it) => isTotalRow(it));
  const totals = {};
  for (const role of SUM_ROLES) totals[role] = sumRole(details, role);

  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    details,
    totalRows,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

/** 核对基准日：入参 asOf 优先；否则取**表内事实日期**的最大值（这批材料的记录截止日） */
function resolveBaseline(p, items) {
  const raw = p.asOf != null ? p.asOf : (p.as_of != null ? p.as_of : (p.baseline != null ? p.baseline : null));
  if (raw !== null && raw !== undefined && String(raw).trim() !== '') {
    const d = parseDate(raw);
    if (d) return { day: d.day, date: fmtDate(d), source: '入参 asOf 给定' };
  }
  let best = null;
  for (const it of items) {
    if (isTotalRow(it)) continue;
    for (const role of BASELINE_DATE_ROLES) {
      const d = parseDate(it[role]);
      if (d && (!best || d.day > best.day)) best = d;
    }
  }
  if (!best) return null;
  return {
    day: best.day,
    date: fmtDate(best),
    source: '表内事实日期（收样/留样开始/检测完成/处置）的最大值，即这批材料的记录截止日；可用入参 asOf 覆盖',
  };
}

/* ============================ 免费档检查（六项） ============================ */

/** 1. 样品数量勾稽：收样数量 − 已检数量 − 退样数量 = 留样数量（逐行复算） */
function checkQuantityBalance(details) {
  const out = [];
  for (const it of details) {
    const r = normNumber(cell(it, 'receiveQty'));
    const t = normNumber(cell(it, 'testedQty'));
    const b = normNumber(cell(it, 'returnQty'));
    const k = normNumber(cell(it, 'retainQty'));
    if (r === null || t === null || b === null || k === null) continue;   // 交给「字段完整性」那一项
    const left = round2(r - t - b);
    const diff = round2(left - k);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '样品数量勾稽不符', it, diff,
      `${who(it)}：收样数量 ${qfmt(r)} − 已检数量 ${qfmt(t)} − 退样数量 ${qfmt(b)} = ${qfmt(left)}，`
      + `与留样数量 ${qfmt(k)} 差 ${qfmt(diff)}（原文：收样「${cell(it, 'receiveQty')}」、已检「${cell(it, 'testedQty')}」、`
      + `退样「${cell(it, 'returnQty')}」、留样「${cell(it, 'retainQty')}」）。`,
      '样品每流转一步都要有交接记录：先看退样是否有回执、已检是否把备样也算进去了、留样是否漏登一件。'
      + '本工具只列出差额，不认定是哪一环丢的。'));
  }
  return out;
}

/** 2. 留样期限核对：算应处置日期；已处置的看是否逾期处置，未处置的看是否已超期 */
function checkRetentionDeadline(details, baseline) {
  const out = [];
  if (!baseline) return out;
  for (const it of details) {
    const due = dueDate(it);
    if (!due) continue;
    const disposed = parseDate(it == null ? '' : it.disposeDate);
    if (disposed) {
      const late = disposed.day - due.day;
      if (late > 0) {
        out.push(finding('P1', '逾期处置', it, late,
          `${who(it)}：留样开始日期 ${cell(it, 'retainStartDate')} + 留样期限 ${cell(it, 'retainDays')} ⇒ `
          + `应处置日期 ${dueText(due)}，实际处置日期 ${cell(it, 'disposeDate')}，**逾期处置 ${late} 天**。`,
          '处置记录要能说明逾期原因（委托方要求延长、复检占用、流程卡住），并留审批痕迹；'
          + '下次按应处置日期提前一周排处置计划。'));
      }
      continue;
    }
    const over = baseline.day - due.day;
    if (over > 0) {
      const st = statusOf(it);
      out.push(finding('P0', '留样期限超期', it, over,
        `${who(it)}：留样开始日期 ${cell(it, 'retainStartDate')} + 留样期限 ${cell(it, 'retainDays')} ⇒ `
        + `应处置日期 ${dueText(due)}，核对基准日 ${baseline.date}，**超期 ${over} 天**`
        + `（登记状态：${st || '空'}，处置日期：${cell(it, 'disposeDate') || '空'}）。`,
        '到期未处置的留样必须立刻排处置：核对是否还能处置（食品/化工类留样超期可能已经变质），'
        + '处置完把处置日期与处置人补进台账。'));
    }
  }
  return out;
}

/** 3. 交接单与台账一致性：交接数量 vs 收样数量、交接样品编号 vs 样品编号（不一致给两处原文） */
function checkHandover(details) {
  const out = [];
  for (const it of details) {
    const hq = normNumber(cell(it, 'handoverQty'));
    const rq = normNumber(cell(it, 'receiveQty'));
    if (hq !== null && rq !== null && Math.abs(round2(hq - rq)) >= TOL) {
      out.push(finding('P0', '交接单与台账不一致', it, round2(hq - rq),
        `${who(it)}：台账「收样数量」写的是「${cell(it, 'receiveQty')}」，`
        + `交接单「交接数量」写的是「${cell(it, 'handoverQty')}」，两边差 ${qfmt(round2(hq - rq))} 件 —— 数量对不上。`,
        '以收样时双方签字的交接单为准：先确认是不是退货/补样没在交接单上体现，改完两边都要签字留痕。'));
    }
    const hn = cell(it, 'handoverNo');
    const sn = cell(it, 'sampleNo');
    const key = (s) => s.replace(/\s/g, '').toUpperCase();
    if (hn && sn && key(hn) !== key(sn)) {
      out.push(finding('P0', '交接单与台账不一致', it, undefined,
        `${who(it)}：台账「样品编号」写的是「${sn}」，交接单「交接样品编号」写的是「${hn}」—— 两边编号对不上，`
        + '样品唯一性标识在这一环断了。',
        '样品编号是唯一性标识的根：确认是抄写错误还是真的交接错了样品；错了要追回并做不符合工作记录。'));
    }
  }
  return out;
}

/** 4. 同一委托编号 + 同一检测项目重复登记检测 */
function checkDuplicateTest(details) {
  const out = [];
  const seen = new Map();
  for (const it of details) {
    const client = cell(it, 'clientNo');
    const item = cell(it, 'testItem');
    if (!client || !item) continue;
    const key = client + '||' + item;
    if (seen.has(key)) {
      out.push(finding('P0', '同一委托同一项目重复登记', it, undefined,
        `${who(it)}：委托编号「${client}」+ 检测项目「${item}」在本表第 ${seen.get(key)} 行已经登记过一次 —— `
        + '同一样品的同一项目重复登记会虚增检测数量，也说明流转记录断档。',
        '确认是同一样品被登记两次（删掉重复那一行），还是真的做了两次（补做要写明原因与依据）；'
        + '同一委托下多件样品做同一项目时，样品编号必须逐件不同。'));
    }
    if (!seen.has(key)) seen.set(key, it.line);
  }
  return out;
}

/** 5. 合计行逐列复核（数量类列） */
function checkTotalRow(details, totalRows) {
  const out = [];
  if (!totalRows.length) return out;
  const tr = totalRows[0];
  for (const role of SUM_ROLES) {
    const declared = normNumber(cell(tr, role));
    if (declared === null) continue;                 // 合计行这一列没写数 ⇒ 没有可比对的数，不猜
    const computed = sumRole(details, role);
    const diff = round2(declared - computed);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P1', '合计行复核不符', tr, diff,
      `第 ${tr.line} 行「${LABELS[role]}」合计行写的是 ${qfmt(declared)}，`
      + `下面 ${details.length} 行明细逐行相加是 ${qfmt(computed)}，差 ${qfmt(diff)}`
      + `（原文：合计行该列「${cell(tr, role)}」）。`,
      '合计行必须等于明细相加：一般是漏加了新补录的行，或合计行还是上一版没重算；重算后把合计行一起更新。'));
  }
  return out;
}

/** 6. 空白/占位符、日期格式、状态值、数量可解析性 */
function checkFieldIntegrity(details) {
  const out = [];
  for (const it of details) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '必填字段缺失', it, undefined,
        `${who(it)}：这些必填字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }
    for (const [role, label] of DATE_FIELDS) {
      const v = cell(it, role);
      if (!v) continue;
      if (!parseDate(v)) {
        out.push(finding('P1', '日期格式非法', it, undefined,
          `${who(it)}：「${label}」的值「${v}」不是一个可识别的日期（认 2025-06-12 / 2025/6/12 / 2025.6.12 / 2025年6月12日，`
          + '且必须是真实存在的日期）。',
          '统一改成 YYYY-MM-DD 再跑；写成「6月12日」「上周」「已检完」这类都不算日期，本工具不会替你补年份。'));
      }
    }
    const st = cell(it, 'status');
    if (st && LEGAL_STATUS.indexOf(st) < 0) {
      out.push(finding('P0', '样品状态值非法', it, undefined,
        `${who(it)}：「样品状态」的值「${st}」不在允许的五个状态里（${LEGAL_STATUS.join(' / ')}）—— `
        + '状态写错会让数量勾稽和留样期限整项算错。',
        '状态是样品受控的核心字段，只允许 待检/在检/已检/留样/已处置 五个值；'
        + '要表达「已退样」「已销毁」请用处置类字段或备注，别新造状态值。'));
    }
    for (const [role, label] of QTY_FIELDS) {
      const v = cell(it, role);
      if (!v) continue;
      const n = normNumber(v);
      if (n === null) {
        out.push(finding('P1', '数量无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${v}」不是可识别的数量（只认数字、千分位、¥、括号负数）。`,
          '把数量改成纯数字形态（如 6）再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数量为负', it, n,
          `${who(it)}：「${label}」是负数（${qfmt(n)}）—— 样品流转数量出现负数，通常是退样登记反了方向或写成了红字冲销。`,
          '确认是冲销还是填错方向；确属冲销的请在备注里写明并保留原值，别直接改成正数。'));
      }
    }
    const term = cell(it, 'retainDays');
    if (term && !parseRetentionDays(term)) {
      out.push(finding('P1', '留样期限无法解析', it, undefined,
        `${who(it)}：「留样期限(天)」的值「${term}」读不出期限（认天数如 90、90天，或 6个月）。`,
        '留样期限要在表里写明可计算的数值；「按标准」「视情况」这类写法让留样到期日根本算不出来，'
        + '请按体系文件把每个样品类型的期限定死。'));
    }
  }
  return out;
}

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的检测样品流转与留样台账（样品台账 + 交接 + 留样期限 + 处置）']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的检测样品流转与留样台账（样品台账 + 交接 + 留样期限 + 处置）']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的检测样品流转与留样台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }

  const details = t.details;
  const totalRows = t.totalRows;
  if (!details.length) {
    return insufficient(['至少一行样品明细（现在只有表头或只有合计行，没有可逐行核对的样品记录）']);
  }

  const baseline = resolveBaseline(p, t.items);

  const findings = [];
  const notRun = [];

  for (const f of checkQuantityBalance(details)) findings.push(f);
  for (const f of checkRetentionDeadline(details, baseline)) findings.push(f);
  for (const f of checkHandover(details)) findings.push(f);
  for (const f of checkDuplicateTest(details)) findings.push(f);
  for (const f of checkTotalRow(details, totalRows)) findings.push(f);
  for (const f of checkFieldIntegrity(details)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const result = {
    findings,
    summary: {
      rows: details.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      as_of: baseline ? baseline.date : null,
      as_of_source: baseline ? baseline.source : null,
      total_rows: totalRows.length,
      receive_total: sumRole(details, 'receiveQty'),
      tested_total: sumRole(details, 'testedQty'),
      return_total: sumRole(details, 'returnQty'),
      retain_total: sumRole(details, 'retainQty'),
      basis: '收样数量 − 已检数量 − 退样数量 应等于 留样数量（逐行复算）；'
        + '应处置日期 = 留样开始日期 + 留样期限（认天数；写「N个月」按 30 天/月折算并在结论里写明）；'
        + '核对基准日默认取表内事实日期（收样/留样开始/检测完成/处置）的最大值，可用入参 asOf 覆盖；'
        + '样品状态只认 待检/在检/已检/留样/已处置；合计行按数量类列与明细逐列相加比对。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对、表内自洽**，'
      + '不代表样品合格、检测结论成立、留样期限符合某部标准的规定值，也不代表样品流转体系整体合规 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: details.length,
    total_rows: totalRows.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    as_of: baseline ? baseline.date : null,
    as_of_source: baseline ? baseline.source : null,
    receive_total: sumRole(details, 'receiveQty'),
    tested_total: sumRole(details, 'testedQty'),
    return_total: sumRole(details, 'returnQty'),
    retain_total: sumRole(details, 'retainQty'),
  };
  result.scope = scope;



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
