#!/usr/bin/env node
/**
 * medical-waste-transfer-check.js —— 医疗废物交接与暂存记录核对引擎（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：医院 / 门诊 / 检验科 / 口腔诊所每天都要做**医疗废物交接登记**，
 * 卫健委（医疗废物管理条例 / 医疗机构废物管理办法）与生态环境部门（固体废物污染环境防治法）**双线检查**，
 * 而且每月还要交一本台账报表。下面每一条都是**罚款项**，核错了是机构担责、不是填表人担责：
 *   ① 暂存时限：交接日期到暂存 / 移交时间超过 48 小时（暂存不能超 48 小时是硬口径）；
 *   ② 废物类别：只认感染性 / 损伤性 / 病理性 / 药物性 / 化学性**五类**，写成别的类别就是未分类；
 *   ③ 交接双方签名：交出人与接收人不能空缺，更不能是**同一个人既交出又接收**（签字是个闭环动作）；
 *   ④ 合计行：重量 kg 与件数必须等于明细行逐列加总，报表就靠这一行对账；
 *   ⑤ 联单号：同一联单号重复登记等于两次交接记成一次（或一次记成两次），台账与实物就对不上了；
 *   ⑥ 字段合法性：日期认不出来 / 重量为负或为零 / 必填列空着 / 暂存时间晚于移交时间。
 *
 * ⚠️ 本文件是**免费档子集**：只实现上面 ① ~ ⑥ 这六项**表内逐行算术与台账勾稽**。
 *   完整档才有的五项（科室产废量与住院口径偏离、联单号断号跳号、损伤性废物锐器盒单独计重、
 *   单次交接重量异常、分科室×分废物类别汇总清单与 result.rollup）的**实现不在这个包里**，
 *   本包也不会产出这些结论。
 *
 *   **未执行项如实记录**：`CHECKS_WITHHELD` 是这五项「未执行的检查项」的**说明文本**（不是实现），
 *   每次运行都会原样出现在 `result.checks_withheld` 与 `result.checks_not_run` 里 ——
 *   本免费包**只说自己没做什么，绝不假装做过**；本包也不产出 `result.rollup` 与 `result.data_notes`。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定废物分类本身是否准确（那是产生科室与监管的认定口径）、不判定交接是否真实发生、
 *          不判定处置单位资质是否有效、不读 .xlsx / .pdf 原件、不联网核验联单与资质真伪；
 *          材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '暂存时限核算（交接日期 → 暂存 / 移交时间，超 48 小时逐条给出超期小时数）',
  '废物类别合法性（只认感染性 / 损伤性 / 病理性 / 药物性 / 化学性五类，五类之外一律点名）',
  '交接双方签名（交出人 / 接收人空缺，或同一人既交出又接收，逐条点名）',
  '合计行逐列复核（重量 kg、件数，必须等于明细行逐列加总）',
  '同一联单号重复登记（一本台账里同一联单号只应出现一次）',
  '字段合法性（日期格式非法、重量为负或为零、暂存时间晚于移交时间、必填列为空）',
];

const CHECKS_WITHHELD = [
  '科室医废产生量与住院人次 / 床位口径偏离（跨表比对，给出偏离率）',
  '联单号断号 / 跳号检查（按月份核联单连续性，缺哪个号就点哪个号）',
  '损伤性废物（锐器盒）单独计重合规性（容器与计重方式逐条核对）',
  '单次交接重量异常（同一科室同一废物类别内偏离中位数 N 倍，逐条给出倍数）',
  '分科室 × 分废物类别汇总清单（按超期小时数降序 + 每组一条可整改动作）与 result.rollup',
];

const OUT_OF_SCOPE = [
  '判定这份废物分类本身对不对（某件废物该算感染性还是损伤性，是产生科室与监管部门的认定口径；'
  + '本工具只核台账里写的类别是否在五类之内）',
  '判定交接是否真实发生、签字是否本人所签、称重是否准确（那是现场核查与笔迹 / 计量检定的范围）',
  '判定医疗废物处置单位的经营许可证与转运车辆资质是否有效（本工具只核台账字段的字面一致性）',
  '读取 .xlsx / .pdf 原件、联网核验联单号 / 资质证书 / 转移联单的真伪，替代卫健委或生态环境部门的认定',
];

// 样例：一本**干净**的医疗废物交接与暂存登记台账 —— 3 个科室 11 行交接记录，
// 暂存与移交都在 48 小时内、类别都在五类之内、签名齐且不是同一人、联单号不重复不断号、
// 合计行与明细一致、院感科口径与实际完全吻合。**全表零命中**。
const SAMPLE_TEXT = [
  '科室\t交接日期\t废物类别\t重量kg\t件数\t交接人\t接收人\t暂存时间\t移交时间\t转运单位\t暂存方式\t联单号\t核对基准日\t备注',
  '感染科\t2026-02-25\t感染性\t15.5\t3\t张建国\t李秀兰\t2026-02-25 09:30\t2026-02-25 17:00\t康泰医废处置有限公司\t专用包装袋\tMW-2026-02-001\t2026-03-05\t日常交接（接收人证件号 320101********1234）',
  '感染科\t2026-02-26\t感染性\t16.0\t3\t张建国\t李秀兰\t2026-02-26 09:00\t2026-02-26 16:30\t康泰医废处置有限公司\t专用包装袋\tMW-2026-02-002\t2026-03-05\t日常交接',
  '感染科\t2026-02-27\t感染性\t14.8\t3\t王海涛\t李秀兰\t2026-02-27 10:00\t2026-02-27 18:00\t康泰医废处置有限公司\t专用包装袋\tMW-2026-02-003\t2026-03-05\t日常交接',
  '感染科\t2026-02-28\t病理性\t12.4\t1\t王海涛\t李秀兰\t2026-02-28 09:00\t2026-02-28 15:00\t康泰医废处置有限公司\t专用包装袋\tMW-2026-02-004\t2026-03-05\t送病理科后集中交接',
  '感染科\t2026-03-01\t损伤性\t9.0\t2\t王海涛\t李秀兰\t2026-03-01 08:30\t2026-03-01 16:00\t康泰医废处置有限公司\t利器盒单独计重\tMW-2026-03-010\t2026-03-05\t锐器盒交接',
  '检验科\t2026-02-26\t损伤性\t9.5\t2\t陈晓峰\t赵丽娟\t2026-02-26 10:00\t2026-02-26 18:00\t康泰医废处置有限公司\t利器盒单独计重\tMW-2026-02-005\t2026-03-05\t锐器盒交接',
  '检验科\t2026-02-27\t感染性\t6.2\t2\t陈晓峰\t赵丽娟\t2026-02-27 09:30\t2026-02-27 16:00\t康泰医废处置有限公司\t专用包装袋\tMW-2026-02-006\t2026-03-05\t日常交接',
  '检验科\t2026-02-28\t损伤性\t12.5\t2\t陈晓峰\t赵丽娟\t2026-02-28 11:00\t2026-02-28 19:00\t康泰医废处置有限公司\t利器盒单独计重\tMW-2026-02-007\t2026-03-05\t锐器盒交接',
  '口腔科\t2026-02-26\t药物性\t2.6\t1\t刘洋\t孙敏\t2026-02-26 10:00\t2026-02-26 17:30\t康泰医废处置有限公司\t专用包装袋\tMW-2026-02-008\t2026-03-05\t过期麻药',
  '口腔科\t2026-02-27\t感染性\t5.8\t2\t刘洋\t孙敏\t2026-02-27 09:00\t2026-02-27 15:30\t康泰医废处置有限公司\t专用包装袋\tMW-2026-02-009\t2026-03-05\t日常交接',
  '口腔科\t2026-03-02\t化学性\t3.4\t1\t刘洋\t孙敏\t2026-03-02 10:30\t2026-03-02 18:00\t康泰医废处置有限公司\t专用包装袋\tMW-2026-03-011\t2026-03-05\t牙科材料残液',
  '合计\t—\t—\t107.7\t22\t—\t—\t—\t—\t—\t—\t—\t—\t11 行交接记录由明细行加总',
  '--- 科室产废与住院口径 ---',
  '科室\t在院床位数\t月住院人次\t月住院人天\t月产废kg',
  '感染科\t30\t45\t900\t51.3',
  '检验科\t5\t8\t150\t7.5',
  '口腔科\t8\t12\t240\t7.0',
].join('\n');

const TOL = 0.01;
/** 暂存时限：超过 48 小时即超期（逐条给出超期小时数） */
const STORAGE_LIMIT_HOURS = 48;
/** 单次交接重量异常：超过同科室同类别**其他行**中位数的 3 倍 */
const WEIGHT_MEDIAN_FACTOR = 3;
/** 科室产废密度偏离上限：±50% */
const DENSITY_DEVIATION_LIMIT = 0.5;
/** 中位数参照至少要有这么多样本行，否则不判（样本太少的"异常"就是噪声） */
const MIN_MEDIAN_SAMPLES = 2;

// 表头级必需列（缺任一列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'department', 'handoverDate', 'wasteCategory', 'weightKg', 'pieceCount',
  'handoverPerson', 'receiver', 'storageTime', 'transferTime', 'transferUnit',
  'slipNo', 'baseDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
// ⚠️ 交接人 / 接收人**故意不在这里**：它们由「交接双方签名」那一项负责点名，
//    放进这里会让同一次缺失同时报两类（噪声掩盖主结论，见对照测试 [锚点4]）。
const REQUIRED_FIELDS = [
  ['department', '科室'],
  ['handoverDate', '交接日期'],
  ['wasteCategory', '废物类别'],
  ['weightKg', '重量kg'],
  ['pieceCount', '件数'],
  ['storageTime', '暂存时间'],
  ['transferTime', '移交时间'],
  ['transferUnit', '转运单位'],
  ['storageMethod', '暂存方式'],
  ['slipNo', '联单号'],
  ['baseDate', '核对基准日'],
];

// 日期列（格式非法逐格点名）
const DATE_FIELDS = [
  ['handoverDate', '交接日期'],
  ['baseDate', '核对基准日'],
];

// 时间列（暂存 / 移交时间；既认 "2026-02-25 09:30" 也认 "09:30"）
const TIME_FIELDS = [
  ['storageTime', '暂存时间'],
  ['transferTime', '移交时间'],
];

// 数值列（为负 / 无法解析逐格点名）
const NUMBER_FIELDS = [
  ['weightKg', '重量kg'],
  ['pieceCount', '件数'],
];

// 重量类列：等于 0 也是非法（0 kg 的交接记录不存在，通常是漏称重）
const POSITIVE_ROLES = ['weightKg'];

// 五类医废：只有这五个值是合法的
const WASTE_CATEGORIES = ['感染性', '损伤性', '病理性', '药物性', '化学性'];

// 锐器盒 / 单独计重的识别词
const SHARPS_CONTAINER_RE = /利器盒|锐器盒|利器|锐器/;
const SEPARATE_WEIGHT_RE = /单独计重|单独称重|分开计重|独立计重|分别计重/;
const SHARPS_MIXED_RE = /混装|合并计重|混合/;

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    本表的坑位集中在：核对基准日 / 交接日期（'日期' 兜底）、暂存时间 / 移交时间（'时间' 兜底）、
//    月产废kg（'kg'）、交接人 / 接收人（'人'）—— 兜底词只能放最后。
const ROLES = {
  baseDate: ['核对基准日', '核对日期', '核查基准日', '核查日期', '基准日期', '基准日'],
  handoverDate: ['交接日期', '交接日', '移交日期', '转移日期'],
  storageTime: ['暂存时间', '暂存时刻', '入库时间'],
  transferTime: ['移交时间', '移交时刻', '交接时间', '出库时间'],
  wasteCategory: ['废物类别', '医废类别', '废物分类', '废物种类', '类别'],
  weightKg: ['重量kg', '重量KG', '净重kg', '重量', '净重'],
  pieceCount: ['件数', '包数', '袋数', '数量'],
  handoverPerson: ['交接人', '交出人', '交送人', '移出人', '科室交接人'],
  receiver: ['接收人', '接收员', '签收人', '接收人员'],
  transferUnit: ['转运单位', '运输单位', '处置单位', '接收单位', '委托处置单位'],
  storageMethod: ['暂存方式', '包装方式', '盛装方式', '暂存容器', '包装容器'],
  slipNo: ['联单号', '转移联单号', '联单编号', '转运单号'],
  department: ['科室', '产生科室', '产废科室', '部门', '病区'],
  bedCount: ['在院床位数', '开放床位', '床位数', '编制床位'],
  inpatients: ['月住院人次', '住院人次', '出院人次', '住院人数'],
  patientDays: ['月住院人天', '住院人天', '住院床日', '实际占用床日'],
  monthlyWasteKg: ['月产废kg', '月产废量', '产废量kg', '产废量', '月产量kg'],
  note: ['备注', '说明'],
};

const LABELS = {
  department: '科室',
  handoverDate: '交接日期',
  wasteCategory: '废物类别',
  weightKg: '重量kg',
  pieceCount: '件数',
  handoverPerson: '交接人',
  receiver: '接收人',
  storageTime: '暂存时间',
  transferTime: '移交时间',
  transferUnit: '转运单位',
  storageMethod: '暂存方式',
  slipNo: '联单号',
  baseDate: '核对基准日',
  bedCount: '在院床位数',
  inpatients: '月住院人次',
  patientDays: '月住院人天',
  monthlyWasteKg: '月产废kg',
  note: '备注',
};

const SUM_ROLES = ['weightKg', 'pieceCount'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张登记表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「合规」，也不说「超期」。',
  };
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim()
    .replace(/[¥￥,，\s]/g, '')
    .replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0))
    .replace(/．/g, '.')
    .replace(/[（]/g, '(')
    .replace(/[）]/g, ')')
    .replace(/[－—–]/g, '-');
  if (s === '' || /^-+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const round1 = (n) => Math.round(n * 10) / 10;

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
  let s = String(raw).trim();
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  s = s.replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0))
    .replace(/[年月]/g, '-').replace(/日/g, '').replace(/[.／/]/g, '-').replace(/\s+/g, '');
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
/** 日期 + 月数（按自然月加，目标月没有那一天就退到当月最后一天） */
/**
 * 归一化"时间"单元格：认 "2026-02-25 09:30" / "2026/2/25 9:30" / "2026-02-25T09:30" / "09:30"。
 * 返回 {date, hhmm, minutes}；没写日期时 date 为 null（按交接日期当天算）。
 * 认不出来一律返回 null —— 绝不用"现在"兜底。
 */
function normDateTime(raw) {
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim().replace(/\s+/g, ' ');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  s = s.replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0))
    .replace(/[Tt]/g, ' ')
    .replace(/：/g, ':')
    .replace(/[.／/]/g, '-')
    .replace(/年/g, '-')
    .replace(/月/g, '-')
    .replace(/日(\s|$)/g, '$1')          // 只吃掉日期末尾的「日」，不吃掉时间里的字
    .replace(/\s+/g, ' ')
    .trim();
  let datePart = '';
  let timePart = '';
  const m = /^(\d{4}-\d{1,2}-\d{1,2})(?:\s+(\d{1,2}:\d{2}(?::\d{2})?))?$/.exec(s);
  if (m) {
    datePart = m[1];
    timePart = m[2] || '';
  } else if (/^\d{1,2}:\d{2}(?::\d{2})?$/.test(s)) {
    timePart = s;
  } else {
    return null;
  }
  const date = datePart ? normDate(datePart) : null;
  if (datePart && !date) return null;
  let minutes = null;
  let hhmm = '';
  if (timePart) {
    const p = timePart.split(':').map(Number);
    if (p[0] > 23 || p[1] > 59 || (p.length > 2 && p[2] > 59)) return null;
    minutes = p[0] * 60 + p[1];
    hhmm = String(p[0]).padStart(2, '0') + ':' + String(p[1]).padStart(2, '0');
  }
  return { date, hhmm, minutes, text: s };
}

/** 交接日期 + 时间单元格 → **相对交接日 00:00 的小时数**；缺时刻返回 null */
function hoursOf(handoverDate, timeCell) {
  if (!handoverDate || !timeCell) return null;
  const date = timeCell.date || handoverDate;
  if (!date || timeCell.minutes === null) return null;
  return (dayNum(date) - dayNum(handoverDate)) * 24 + timeCell.minutes / 60;
}

/** 区间中位数（偶数个取中间两个的平均） */
const SECTION_RE = /^\s*-{2,}\s*(.+?)\s*-{2,}\s*$/;
function isSectionMarker(line) {
  return SECTION_RE.test(String(line == null ? '' : line));
}

function roleOf(header) {
  const h = String(header == null ? '' : header).replace(/[\s（）()：:［］\[\]]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

const TOTAL_LABEL = /^(合计|小计|总计|总合计|合\s*计)$/;
/** 合计行不是交接明细：逐条检查要跳过它，只有「合计行逐列复核」那一项会用到它 */
function isTotalRow(it) {
  const dep = String(it.department == null ? '' : it.department).trim();
  const slip = String(it.slipNo == null ? '' : it.slipNo).trim();
  return TOTAL_LABEL.test(dep) || TOTAL_LABEL.test(slip);
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
    detail,
    totalRows,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

const cell = (it, role) => String(it[role] == null ? '' : it[role]).trim();

function who(it) {
  const dep = cell(it, 'department');
  const date = cell(it, 'handoverDate');
  const slip = cell(it, 'slipNo');
  return `第 ${it.line} 行「${[dep || '未填科室', date || '未填日期', slip || '未填联单号'].join(' / ')}」`;
}

/** 每条结论都带原文依据：行号 + 联单号 + 该行原文（截断），可被第三方用同一口径复算 */
function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    slip_no: cell(it, 'slipNo'),
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
    const d = normDate(it.baseDate);
    if (d) return d;
  }
  return null;
}
const baseOf = (it, base) => normDate(it.baseDate) || base;

/* ============================ 免费档检查（六项） ============================ */

function checkStorageLimit(items, base) {
  // ① 暂存时限：交接日期 → 暂存时间 / 移交时间，超过 48 小时逐条给超期小时数
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const hd = normDate(it.handoverDate);
    if (!hd) continue;                              // 日期认不出来交给第 ⑥ 项点名
    const points = [];
    const hSt = hoursOf(hd, normDateTime(it.storageTime));
    if (hSt !== null) points.push({ name: LABELS.storageTime, raw: cell(it, 'storageTime'), h: hSt });
    const hTt = hoursOf(hd, normDateTime(it.transferTime));
    if (hTt !== null) points.push({ name: LABELS.transferTime, raw: cell(it, 'transferTime'), h: hTt });
    const over = points
      .map((p) => Object.assign({}, p, { over: round1(p.h - STORAGE_LIMIT_HOURS) }))
      .filter((p) => p.over > TOL)
      .sort((a, b) => b.over - a.over);
    if (!over.length) continue;
    const worst = over[0];
    const detail = over.map((p) => `${p.name} ${p.raw}（超 ${p.over} 小时）`).join('；');
    out.push(finding('P0', '暂存超48小时', it, worst.over,
      `${who(it)}：交接日期 ${hd}，${detail} —— 医疗废物暂存不得超过 48 小时，`
      + `本条最久的一处**超期 ${worst.over} 小时**（科室 ${cell(it, 'department') || '(未填)'}，`
      + `类别 ${cell(it, 'wasteCategory') || '(未填)'}，${cell(it, 'weightKg') || '(未填)'} kg）。`,
      '先按超期小时数排转运计划并联系有资质处置单位当日清运；'
      + '同时查这两天的暂存间温度记录与交接班记录（暂存超 48 小时是卫健委与生态环境部门双线检查的罚款项）。'
      + '别只把台账时间改成 48 小时以内 —— 那叫改数据，不叫整改。'));
  }
  return out;
}

function checkWasteCategory(items) {
  // ② 废物类别合法性：只在五类之内；五类之外一律点名
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const cat = cell(it, 'wasteCategory');
    if (!cat) continue;                              // 空类别交给第 ⑥ 项点名
    if (WASTE_CATEGORIES.indexOf(cat) >= 0) continue;
    out.push(finding('P0', '废物类别非法', it, undefined,
      `${who(it)}：废物类别写的是「${cat}」，不在法定的五类里`
      + `（${WASTE_CATEGORIES.join(' / ')}）—— 写成别的类别等于这份废物**没有按类别分类**。`,
      '按《医疗废物分类目录》把类别改成五类之一 —— 感染性 / 损伤性 / 病理性 / 药物性 / 化学性；'
      + '确实属于病理性或药物性的要按对应流程单独交接。分类口径由产生科室与监管部门认定，'
      + '本工具只核台账里写的类别是否在五类之内。'));
  }
  return out;
}

function checkSignatures(items) {
  // ③ 交接双方签名：交出人 / 接收人空缺，或**同一人既交出又接收**
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const from = cell(it, 'handoverPerson');
    const to = cell(it, 'receiver');
    const missing = [];
    if (isBlank(from)) missing.push(LABELS.handoverPerson);
    if (isBlank(to)) missing.push(LABELS.receiver);

    if (missing.length === 2) {
      out.push(finding('P1', '交接签名空缺或同一人', it, undefined,
        `${who(it)}：交接人与接收人**两个都空着**（联单号 ${cell(it, 'slipNo') || '(未填)'}）`
        + '—— 签字是交接闭环的唯一凭据，两个都空等于这份交接没有任何人负责。',
        '让当班交出人与暂存点接收人各自补签，并把姓名填进台账；'
        + '补签只补"确实发生过的那次交接"，不要把两天的记录合并成一次签。'));
      continue;
    }
    if (missing.length) {
      out.push(finding('P1', '交接签名空缺或同一人', it, undefined,
        `${who(it)}：${missing.join('、')}是空的或占位符（联单号 ${cell(it, 'slipNo') || '(未填)'}）`
        + `—— 交接双方签名缺一不可（现在交出人 ${from || '(空)'} / 接收人 ${to || '(空)'}）。`,
        '把缺的那一方姓名补进台账：交接人由产生科室当班人员签，接收人由暂存点 / 处置单位接收人签；'
        + '一方不在场就不算交接完成。'));
      continue;
    }
    if (from === to) {
      out.push(finding('P0', '交接签名空缺或同一人', it, undefined,
        `${who(it)}：交接人与接收人写的是**同一个人**「${from}」—— 自己把废物交给自己、'
        + '自己又签收，交接的双人核对链条断在这里。`,
        '交接必须由交出方与接收方**两个不同的人**当场核对签字：'
        + '先确认实际交接时到底是哪两个人，再据实填写；同一个人既交出又接收的记录要重新核实物台账。'));
    }
  }
  return out;
}

function checkTotals(items, cols) {
  // ④ 合计行逐列复核：重量 kg、件数必须等于明细行逐列加总
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
          '合计行只能写数字；请核对是否把单位（kg / 件）写进了单元格里。'));
        continue;
      }
      const actual = round2(detail.reduce((acc, it) => {
        const n = normNumber(it[role]);
        return acc + (n === null ? 0 : n);
      }, 0));
      const diff = round2(declared - actual);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P1', '合计行不符', tr, diff,
        `第 ${tr.line} 行合计行的「${LABELS[role]}」写着 ${declared}，但上面 ${detail.length} 行明细逐行加总是 ${actual}，`
        + `差 ${diff}（合计 − 明细）。`,
        '合计行必须等于明细行逐列加总：先看有没有明细行被隐藏 / 筛选掉了，再看合计公式有没有漏行或重复计数。'
        + '（本工具只核这一个合计行，不替你去别的表里找补。）'));
    }
  }
  return out;
}

function checkDuplicateSlip(items) {
  // ⑤ 同一联单号重复登记：一本台账里同一联单号只应出现一次
  const out = [];
  const first = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const no = cell(it, 'slipNo');
    if (!no) continue;
    if (first.has(no)) {
      const prev = first.get(no);
      out.push(finding('P0', '联单号重复登记', it, undefined,
        `${who(it)}：联单号「${no}」在第 ${prev.line} 行已经出现过 —— 同一联单号重复登记`
        + `（第 ${prev.line} 行原文：${String(prev.raw).slice(0, 60)}）。`,
        '一个联单号对应一次交接：先确认是"同一批废物被登记了两遍"还是"两次交接共用了同一个号"。'
        + '前者删掉重复行（保留实物与称重记录那一行），后者按处置单位的实际联单补号并说明原因。'));
    } else {
      first.set(no, it);
    }
  }
  return out;
}

function checkFieldIntegrity(items) {
  // ⑥ 空白 / 占位符 / 日期格式 / 时间格式 / 重量为负或为零 / 暂存晚于移交
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了（例如交接日期空着就判不了 48 小时暂存时限）；'
        + '补全后重跑，本工具不会替你猜一个默认值。'));
    }

    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw) === null) {
        out.push(finding('P1', '日期格式非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
          + '（只认 2026-02-25 / 2026/2/25 / 2026年2月25日 / 20260225 这几种形态）。',
          '把日期改成 2026-02-25 这种形态再跑；日期认不出来时本工具不会拿它去算暂存超期小时数。'));
      }
    }

    for (const [role, label] of TIME_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDateTime(raw) === null) {
        out.push(finding('P1', '日期格式非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期时间`
          + '（只认 2026-02-25 09:30 / 2026-02-25T09:30 / 09:30 这几种形态）。',
          '把暂存 / 移交时间写成 2026-02-25 09:30 这种形态（带日期最稳；只写时刻时按交接日期当天算）。'));
      }
    }

    for (const [role, label] of NUMBER_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值为负或非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数字。`,
          '重量与件数都必须是纯数字（如 12.5 / 3）；写成「十二点五公斤」「叁」这类形态本工具一律不给结论。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 登记表里的重量 / 件数出现负数，通常是填反了或写成了红字。`,
          '确认是红字冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      } else if (n === 0 && POSITIVE_ROLES.indexOf(role) >= 0) {
        out.push(finding('P1', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是 0 —— 一次实际发生的医废交接不可能称出 0 kg，`
          + '通常是漏称重，或者把"没称"填成了 0。',
          '补一次真实称重（暂存间电子秤 / 地磅读数）再填；确实没有废物的班次不要登记成 0 kg 的交接记录。'));
      }
    }

    // 暂存晚于移交（时序倒挂）：两个时间都给得出来才判
    const hd = normDate(it.handoverDate);
    const hSt = hoursOf(hd, normDateTime(it.storageTime));
    const hTt = hoursOf(hd, normDateTime(it.transferTime));
    if (hSt !== null && hTt !== null && hTt < hSt - TOL) {
      const back = round1(hSt - hTt);
      out.push(finding('P1', '数值为负或非法', it, -back,
        `${who(it)}：移交时间 ${cell(it, 'transferTime')} 早于暂存时间 ${cell(it, 'storageTime')}，`
        + `时序倒挂 ${back} 小时 —— 先移交、后暂存，这份台账的时间链条不成立。`,
        '按实际过程改正两个时间：正常顺序是产生 → 科室暂存 → 移交处置单位。'
        + '两个时间至少要能和转运联单上的日期对上。'));
    }
  }
  return out;
}

/* ===== 以下函数只在完整档（买断版）的付费分支里被调用 ===== */

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的医疗废物交接与暂存登记表']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的医疗废物交接与暂存登记表']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的医疗废物交接与暂存登记表（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.detail.length) {
    return insufficient(['至少一行交接明细（现在只有表头或只有合计行，没有可核对的交接记录）']);
  }

  const base = baseDateOf(t.items);
  const findings = [];
  const notRun = [];
  // 免费档：完整档追加的那五项检查一项都不执行，这里**如实记下来**（只记「没做」，绝不伪造结论）

  for (const f of (checkStorageLimit(t.items, base) || [])) findings.push(f);
  for (const f of (checkWasteCategory(t.items) || [])) findings.push(f);
  for (const f of (checkSignatures(t.items) || [])) findings.push(f);
  for (const f of (checkTotals(t.items, t.cols) || [])) findings.push(f);
  for (const f of (checkDuplicateSlip(t.items) || [])) findings.push(f);
  for (const f of (checkFieldIntegrity(t.items) || [])) findings.push(f);

  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const totalWeight = t.totals.weightKg;
  const totalPieces = t.totals.pieceCount;
  const overRows = findings.filter((f) => f.category === '暂存超48小时');
  const overMax = overRows.reduce((m, f) => Math.max(m, f.diff || 0), 0);

  const result = {
    findings,
    summary: {
      rows: t.detail.length,
      total_rows: t.totalRows.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      weight_kg_total: totalWeight,
      piece_count_total: totalPieces,
      over_limit_rows: overRows.length,
      over_hours_max: overMax,
      base_date: base,
      basis: '暂存时限按「交接日期 → 暂存时间 / 移交时间」算实际小时数，超过 48 小时即超期（逐条给超期小时数）；'
        + '废物类别只认 感染性 / 损伤性 / 病理性 / 药物性 / 化学性 五类；'
        + '交接人与接收人都要有签名且不能是同一人；'
        + '合计行的重量 kg 与件数必须等于明细行逐列加总；'
        + '同一联单号在一本台账里只应出现一次；'
        + '日期 / 时间须可识别，重量不得为负或为零，暂存时间不得晚于移交时间。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这份登记表按上面写明的口径算得对、'
      + '暂存在 48 小时内、类别在五类之内、签名齐、联单号唯一、合计与明细一致**，'
      + '不代表废物分类本身一定准确、不代表交接与称重真的发生过、也不代表处置单位资质与联单真伪已经核验'
      + ' —— 那些不在本工具范围内。'
      + '（本免费版未执行的五项已列在 checks_withheld / checks_not_run 里：它们**没有做**，不等于没问题。）';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.detail.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    weight_kg_total: totalWeight,
    piece_count_total: totalPieces,
    base_date: base,
  };
  result.scope = scope;

  return { status: 'success', result };
}

/* ============================ CLI（与 run.mjs 同一套参数口径） ============================ */

const CLI_USAGE = [
  '用法：node <engine>.js --sample | --input <入参.json|表格文本> [--json] [--no-stats]',
  '  --sample   用引擎内置样例（干净样例，0 命中）',
  '  --input    入参：{"text":"…"} 或直接粘贴的表格文本',
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
    // 买断版：本包一次性卖断，运行时就该按**完整档**跑（少了 full 这一档只会拿到免费口径）
    payload = { text: SAMPLE_TEXT, full: true };
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
  console.log(`本版本不包含（如实声明，未执行）：${CHECKS_WITHHELD.join('、')}`);
  console.log('');
  console.log(JSON.stringify(out.result, null, 2));
  return 0;
}

if (require.main === module) {
  process.exit(cliMain(process.argv.slice(2)));
}

module.exports = {
  run, parseTable, roleOf, normNumber, normDate, normDateTime, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
