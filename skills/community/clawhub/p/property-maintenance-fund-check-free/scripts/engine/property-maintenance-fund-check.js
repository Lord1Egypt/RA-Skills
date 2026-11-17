#!/usr/bin/env node
/**
 * property-maintenance-fund-check.js —— 物业专项维修资金使用与分摊核对（**免费档**；确定性、纯 Node 标准库）
 *
 * 真实痛点：住宅专项维修资金是**业主共有**的钱 —— 动用要满足"双三分之二"表决、要公示、
 * 要按**建筑面积分摊到户**，还要与首期归集额、历年使用额、利息收入、账户余额逐项对上。
 * 物业公司与业委会**每年公示前**、以及**每一次使用之后**，都必须把
 * 「归集台账 − 使用台账 − 分摊明细 − 银行余额」核对清楚：
 *   ① 期初余额 + 本期归集 + 利息收入 − 本期使用 = 期末余额（逐户逐行复算）
 *   ② 某次使用总额 × 该户建筑面积 ÷ 参与分摊建筑面积 = 该户分摊额（逐户，分币容差）
 *   ③ 分摊明细合计 = 使用总额（逐项目复核）
 *   ④ 同一户 + 同一项目不得重复分摊
 *   ⑤ 同意面积 ÷ 参与面积 ≥ 规定比例（"双三分之二"）
 * 算错就是**业主投诉、审计与监管问题**。这些表都能手算复现 ⇒ 可机械核对。
 *
 * 本文件是**免费档子集**：只实现上面这六项逐行算术与逐项目勾稽（归集勾稽 / 分摊勾稽 /
 * 分摊明细合计 / 重复分摊 / 表决比例 / 空白与格式）。**完整档（付费）的实现不在这个包里** ——
 * 分摊到户后余额不为负与单户超归集额点名、各家银行账户利息口径核对、跨期重复动用、
 * 表决资料与使用金额的对应性、分楼栋×分项目汇总整改清单（`consolidated_actions`）都不在这里。
 * `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定动用维修资金是否符合法定实体条件、不判定表决程序本身是否合法、
 *          不代替审计与审价结论、不读 .xlsx/.pdf 原件、不联网核验银行流水真伪；
 *          材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '归集勾稽（逐行复算 期初余额 + 本期归集 + 利息收入 − 本期使用 = 期末余额，差额不为零即列出）',
  '分摊勾稽（逐户复算 分摊额 = 使用总额 × 该户建筑面积 ÷ 参与分摊建筑面积，分币容差 0.01）',
  '分摊明细合计与使用总额一致（逐项目复核 Σ分摊额 = 使用总额）',
  '同一户同一项目重复分摊（同一期间内 楼栋+房号+项目名称 出现两次即点名）',
  '使用事项表决比例核对（同意面积 ÷ 参与面积 ≥ 规定比例，不达标即报出实际比例）',
  '空白/占位符/认不出格式（必需列缺失、关键单元格空白、金额无法解析或为负、证件号未脱敏）',
];

const CHECKS_WITHHELD = [
  '分摊到户后余额不为负 + 单户累计使用超过其归集额的部分点名',
  '利息收入按各家银行账户口径核对（多个账户利息合计 vs 入账利息）',
  '同一项目在多个期间重复动用（跨期重复）检测',
  '表决资料与使用金额的对应性（同一项目多次表决、金额不一致）检测',
  '分楼栋×分项目的汇总清单（按差额排序，给出可整改动作 consolidated_actions）',
];

const OUT_OF_SCOPE = [
  '判定动用维修资金是否符合法定实体条件（是否属于共用部位/共用设施设备、是否属于应急使用情形）—— 那是主管部门与街道的认定权，本工具不做',
  '判定表决程序本身是否合法（是否真的召开过业主大会、签字是否真实、公示是否到位、是否有人冒名表决），本工具只按材料里给出的同意面积/参与面积做算术比对',
  '代替审计结论与工程审价（维修工程造价是否虚高、工程量是否真实、票据是否合规），本工具只做表内算术与分摊勾稽',
  '读取 .xlsx / .pdf 原件、联网核验银行流水与专户余额真伪、代为入户催缴或代为公示',
];

// 样例：一张**干净**的维修资金归集与分摊明细表 —— 同一栋楼 3 户、2 个使用事项，
// 归集勾稽逐行成立、分摊额按建筑面积精确到分、每个项目 Σ分摊额 = 使用总额、
// 同一户同一项目不重复、表决比例均达标、分户账户余额不为负、账户结息与入账利息一致。
// 口径说明：「使用总额 / 表决金额 / 参与面积 / 同意面积 / 规定比例」是**项目级**取值，
// 在属于同一项目的每行上重复填写；「期初/期末余额」是**分户滚动**余额（同一户的下一行接着上一行）。
const SAMPLE_TEXT = [
  '期间\t楼栋\t房号\t业主证件号\t建筑面积\t期初余额\t本期归集\t利息收入\t本期使用\t期末余额\t银行账户\t账户利息\t项目名称\t使用总额\t表决金额\t参与面积\t同意面积\t规定比例\t分摊额\t备注',
  '2025年度\t3栋\t1单元501\t320101********1234\t89.50\t30000.00\t2000.00\t120.00\t8950.00\t23170.00\t建行南京城南支行维修资金专户\t120.00\t电梯曳引机更换\t30050.00\t30050.00\t300.50\t240.40\t66.67%\t8950.00\t2025-03-18 业主大会表决通过',
  '2025年度\t3栋\t1单元501\t320101********1234\t89.50\t23170.00\t0.00\t0.00\t13425.00\t9745.00\t建行南京城南支行维修资金专户\t0.00\t屋面防水维修\t45075.00\t45075.00\t300.50\t300.50\t66.67%\t13425.00\t2025-09-06 公示后实施',
  '2025年度\t3栋\t1单元502\t320102********5678\t112.30\t38000.00\t2500.00\t150.00\t11230.00\t29420.00\t建行南京城南支行维修资金专户\t150.00\t电梯曳引机更换\t30050.00\t30050.00\t300.50\t240.40\t66.67%\t11230.00\t2025-03-18 业主大会表决通过',
  '2025年度\t3栋\t1单元502\t320102********5678\t112.30\t29420.00\t0.00\t0.00\t16845.00\t12575.00\t建行南京城南支行维修资金专户\t0.00\t屋面防水维修\t45075.00\t45075.00\t300.50\t300.50\t66.67%\t16845.00\t2025-09-06 公示后实施',
  '2025年度\t3栋\t2单元601\t320103********9012\t98.70\t32000.00\t1800.00\t96.00\t9870.00\t24026.00\t工行南京新城支行维修资金专户\t96.00\t电梯曳引机更换\t30050.00\t30050.00\t300.50\t240.40\t66.67%\t9870.00\t2025-03-18 业主大会表决通过',
  '2025年度\t3栋\t2单元601\t320103********9012\t98.70\t24026.00\t0.00\t0.00\t14805.00\t9221.00\t工行南京新城支行维修资金专户\t0.00\t屋面防水维修\t45075.00\t45075.00\t300.50\t300.50\t66.67%\t14805.00\t2025-09-06 公示后实施',
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'building', 'room', 'area', 'openingBalance', 'collectAmount', 'interestIncome',
  'usageAmount', 'closingBalance', 'projectName', 'usageTotal', 'shareAmount', 'agreeArea', 'joinArea',
];

// 单元格级必需字段（空白/占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['building', '楼栋'],
  ['room', '房号'],
  ['area', '建筑面积'],
  ['openingBalance', '期初余额'],
  ['collectAmount', '本期归集'],
  ['interestIncome', '利息收入'],
  ['usageAmount', '本期使用'],
  ['closingBalance', '期末余额'],
  ['projectName', '项目名称'],
  ['usageTotal', '使用总额'],
  ['shareAmount', '分摊额'],
  ['agreeArea', '同意面积'],
  ['joinArea', '参与面积'],
];

// 金额/面积/比例列（用于「为负 / 无法解析」判定）
const AMOUNT_FIELDS = [
  ['area', '建筑面积'],
  ['openingBalance', '期初余额'],
  ['collectAmount', '本期归集'],
  ['interestIncome', '利息收入'],
  ['usageAmount', '本期使用'],
  ['closingBalance', '期末余额'],
  ['usageTotal', '使用总额'],
  ['voteAmount', '表决金额'],
  ['shareAmount', '分摊额'],
  ['agreeArea', '同意面积'],
  ['joinArea', '参与面积'],
  ['bankInterest', '账户利息'],
];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会抢走更具体的列（本仓库踩过 6 次，见 tools/header_map_check.py）：
//    · 「账户利息」必须排在「利息收入」之前（否则「利息」两字会抢走账户利息列）；
//    · 「使用总额」必须排在「本期使用」之前；
//    · 「参与面积 / 分摊额」必须排在通用「面积」之前（否则「面积」两字会抢走面积列）。
const ROLES = {
  period: ['期间', '账期', '所属期间', '归集期间', '月份', '年度'],
  building: ['楼栋', '楼号', '幢号', '栋号', '座号'],
  room: ['房号', '室号', '房间号', '门牌号', '单元房号'],
  ownerId: ['业主证件号', '业主身份证号', '身份证号', '证件号码', '证件号'],
  bankInterest: ['账户利息', '银行利息', '对账利息', '结息金额', '账户实付利息'],
  bankAccount: ['银行账户', '开户行', '账户名称', '存款账户', '专户名称', '专户'],
  openingBalance: ['期初余额', '期初结存', '年初余额', '上期结余', '期初'],
  collectAmount: ['本期归集', '归集金额', '归集额', '首期归集', '归集'],
  interestIncome: ['利息收入', '本期利息', '存款利息', '利息'],
  usageTotal: ['使用总额', '使用总金额', '动用总额', '项目使用金额'],
  usageAmount: ['本期使用', '本期动用', '使用金额', '使用额', '动用额'],
  closingBalance: ['期末余额', '期末结存', '年末余额', '本期结存', '期末'],
  projectName: ['项目名称', '维修项目', '改造项目', '工程项目', '项目'],
  voteAmount: ['表决金额', '决议金额', '表决通过金额', '表决批准金额'],
  agreeArea: ['同意面积', '赞成面积', '同意表决面积', '已同意面积'],
  joinArea: ['参与面积', '参与分摊面积', '参与表决面积', '参与分摊建筑面积', '分摊面积'],
  minRatio: ['规定比例', '法定比例', '要求比例', '最低比例', '表决比例'],
  shareAmount: ['分摊额', '应分摊额', '户分摊金额', '分摊金额', '分摊'],
  note: ['备注', '说明', '附注'],
  area: ['建筑面积', '产权面积', '套内面积', '面积'],
};

const LABELS = {
  period: '期间',
  building: '楼栋',
  room: '房号',
  ownerId: '业主证件号',
  bankInterest: '账户利息',
  bankAccount: '银行账户',
  openingBalance: '期初余额',
  collectAmount: '本期归集',
  interestIncome: '利息收入',
  usageTotal: '使用总额',
  usageAmount: '本期使用',
  closingBalance: '期末余额',
  projectName: '项目名称',
  voteAmount: '表决金额',
  agreeArea: '同意面积',
  joinArea: '参与面积',
  minRatio: '规定比例',
  shareAmount: '分摊额',
  note: '备注',
  area: '建筑面积',
};

// 逐行口径的合计（**项目级取值在属于同一项目的每行上重复填写**，
// 所以「使用总额 / 参与面积 / 同意面积 / 表决金额」不在这里逐行累加 —— 它们的口径合计在逐项目复核里算）。
const SUM_ROLES = ['area', 'openingBalance', 'collectAmount', 'interestIncome', 'usageAmount', 'closingBalance', 'shareAmount'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「分摊对得上」，也不说「对不上」。',
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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核|未知)$/i.test(s);
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

/** 解析成 {header, cols, items, totals, missingRoles, missingColumns, error}；行是**扁平**对象：{line, raw, 角色:值…} */
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
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(items.reduce((acc, it) => {
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

const txt = (v) => String(v == null ? '' : v).trim();

/** 逐项检查的结果一律当数组处理：某一项没给出结论时，只让**那一项**没结论，不把整份核对打崩 */
const buildingOf = (it) => txt(it.building);
const roomOf = (it) => txt(it.room);
const projectOf = (it) => txt(it.projectName);
const periodOf = (it) => txt(it.period);
const householdOf = (it) => `${buildingOf(it)}${roomOf(it) ? ' ' + roomOf(it) : ''}`;

/** 结论必须带原文依据：行号 + 原文行内容（source）+ 数字 */
function who(it) {
  const h = householdOf(it);
  const proj = projectOf(it);
  return `第 ${it.line} 行「${h || '未填楼栋房号'}${proj ? ' · ' + proj : ''}」`;
}

function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: (it && it.line) || 0,
    source: txt(it && it.raw),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

function groupBy(items, keyFn) {
  const map = new Map();
  for (const it of items) {
    const key = keyFn(it);
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(it);
  }
  return map;
}

/** 去重后的数值列表（保留**首次出现**的顺序：口径以第一行为准，便于回溯原文） */
function distinctNums(items, role) {
  const out = [];
  for (const it of items) {
    const n = normNumber(it[role]);
    if (n === null) continue;
    if (!out.some((x) => Math.abs(x - n) < TOL / 100)) out.push(n);
  }
  return out;
}

/** 18 位身份证号真实形态（业主证件号必须脱敏成 320101********1234 这类掩码） */
const RAW_ID_RE = /(^|\D)\d{17}[\dXx](\D|$)/;

/* ============================ 免费档检查（六项） ============================ */

/** 1. 归集勾稽：期初余额 + 本期归集 + 利息收入 − 本期使用 = 期末余额（逐行复算） */
function checkLedgerBalance(items) {
  const out = [];
  for (const it of items) {
    const ob = normNumber(it.openingBalance);
    const ca = normNumber(it.collectAmount);
    const ii = normNumber(it.interestIncome);
    const ua = normNumber(it.usageAmount);
    const cb = normNumber(it.closingBalance);
    if (ob === null || ca === null || ii === null || ua === null || cb === null) continue;   // 缺失/认不出交给第 6 项
    const expect = round2(ob + ca + ii - ua);
    const diff = round2(cb - expect);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '归集勾稽不符', it, diff,
      `${who(it)}：期初余额 ${money(ob)} + 本期归集 ${money(ca)} + 利息收入 ${money(ii)} − 本期使用 ${money(ua)} = ${money(expect)}，`
      + `与期末余额 ${money(cb)} 差 ${money(diff)}（${diff > 0 ? '期末偏大' : '期末偏小'}）。`,
      '拿专户银行流水与归集台账逐笔对：常见原因是归集额漏记、利息未入账、或本期使用额没同步到分户账。'
      + '本工具只列出差额，不认定是哪种原因。'));
  }
  return out;
}

/** 2. 分摊勾稽：分摊额 = 使用总额 × 该户建筑面积 ÷ 参与分摊建筑面积（逐户，分币容差） */
function checkApportionment(items) {
  const out = [];
  for (const it of items) {
    const area = normNumber(it.area);
    const total = normNumber(it.usageTotal);
    const join = normNumber(it.joinArea);
    const share = normNumber(it.shareAmount);
    if (area === null || total === null || share === null) continue;      // 缺失/认不出交给第 6 项
    if (join === null || join <= 0) continue;                            // 参与分摊建筑面积为零 ⇒ 无法复算，不给结论
    const expect = round2(total * area / join);
    const diff = round2(share - expect);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '分摊额与建筑面积不符', it, diff,
      `${who(it)}：使用总额 ${money(total)} × 建筑面积 ${money(area)} ÷ 参与分摊建筑面积 ${money(join)} = ${money(expect)}，`
      + `与本行分摊额 ${money(share)} 差 ${money(diff)}（${diff > 0 ? '多分摊' : '少分摊'}）。`,
      '按"使用总额 ÷ 参与分摊建筑面积 × 该户建筑面积"重算：先核参与分摊建筑面积是否含了不该分摊的户，'
      + '再核该户建筑面积口径（产权面积 / 套内面积）是否与表决资料一致。'));
  }
  return out;
}

/** 3. 分摊明细合计 = 使用总额（逐项目复核；同一项目的口径取第一行，并如实指出多个不同值） */
function checkShareTotal(items) {
  const out = [];
  const by = groupBy(items, projectOf);
  for (const [proj, list] of by) {
    if (!proj) continue;
    const totals = distinctNums(list, 'usageTotal');
    if (!totals.length) continue;                                        // 使用总额认不出来 ⇒ 不给结论
    const usage = totals[0];
    const sum = round2(list.reduce((acc, it) => acc + num(it, 'shareAmount'), 0));
    const diff = round2(sum - usage);
    if (Math.abs(diff) < TOL) continue;
    const lines = list.map((it) => it.line);
    const extra = totals.length >= 2
      ? `；本项目「使用总额」列出现 ${totals.length} 个不同值（${totals.map(money).join('、')}），此处以第 ${list[0].line} 行的 ${money(usage)} 为准`
      : '';
    out.push(finding('P0', '分摊明细合计与使用总额不符', list[0], diff,
      `第 ${lines.join('、')} 行「${proj}」：分摊明细合计 ${money(sum)} 与使用总额 ${money(usage)} 差 ${money(diff)}`
      + `（${diff > 0 ? '多分摊' : '少分摊'}）${extra}。`,
      '逐户把分摊额加一遍：确认参与分摊的户数与建筑面积是否齐（未交存 / 未售 / 非受益户要能说清），'
      + '以及使用总额有没有串行登记到别的项目上。'));
  }
  return out;
}

/** 4. 同一户 + 同一项目（同一期间）重复分摊 */
function checkDuplicateShare(items) {
  const out = [];
  const reported = new Set();
  const seen = new Map();
  for (const it of items) {
    if (!householdOf(it) || !projectOf(it)) continue;
    const key = `${periodOf(it)}|${householdOf(it)}|${projectOf(it)}`;
    if (seen.has(key) && !reported.has(it.line)) {
      reported.add(it.line);
      out.push(finding('P0', '同一户同一项目重复分摊', it, undefined,
        `${who(it)}：期间「${periodOf(it) || '(未填期间)'}」里，这一户 + 这个项目在第 ${seen.get(key)} 行已经分摊过一次 —— 同一户同一项目重复分摊。`,
        '同一户同一项目只应有一条分摊记录；分次实施请拆成不同项目名称并各自留表决资料，不要为同一笔分摊再录一行。'));
    }
    if (!seen.has(key)) seen.set(key, it.line);
  }
  return out;
}

/** 5. 使用事项表决比例核对：同意面积 ÷ 参与面积 ≥ 规定比例 */
function checkVoteRatio(items) {
  const out = [];
  const by = groupBy(items, projectOf);
  for (const [proj, list] of by) {
    if (!proj) continue;
    const lines = list.map((it) => it.line);
    const ratios = distinctNums(list, 'minRatio');
    const agrees = distinctNums(list, 'agreeArea');
    const joins = distinctNums(list, 'joinArea');
    const first = list[0];

    if (!ratios.length || ratios[0] <= 0) {
      out.push(finding('P1', '表决比例规定值无法使用', first, undefined,
        `第 ${lines.join('、')} 行「${proj}」：本项目的「规定比例」是空白或认不出来（原文：${isBlank(first.minRatio) ? '(空白)' : String(first.minRatio)}），`
        + '无法判断同意面积是否达到规定比例。',
        '按业主大会决定或当地规定把阈值写成百分数（如 66.67%）再跑；本工具不会替你套用一个默认阈值。'));
      continue;
    }
    if (agrees.length !== 1 || joins.length !== 1) {
      out.push(finding('P1', '表决面积口径不一致', first, undefined,
        `第 ${lines.join('、')} 行「${proj}」：同一使用事项在不同行上填了不同的表决面积口径 —— `
        + `同意面积 ${agrees.length ? agrees.map((x) => x.toFixed(2)).join('、') : '(认不出)'}，`
        + `参与面积 ${joins.length ? joins.map((x) => x.toFixed(2)).join('、') : '(认不出)'}。`,
        '一个使用事项只有一组表决面积：把同意面积 / 参与面积按本项目统一口径（通常整栋或整单元）填一次，逐行保持一致。'));
      continue;
    }
    const agree = agrees[0];
    const join = joins[0];
    if (join <= 0) continue;
    const ratio = round2(agree / join * 100);
    const min = ratios[0];
    if (ratio + TOL >= min) continue;
    out.push(finding('P0', '表决比例不达标', first, round2(ratio - min),
      `第 ${lines.join('、')} 行「${proj}」：同意面积 ${money(agree)} ÷ 参与面积 ${money(join)} = ${ratio.toFixed(2)}%，`
      + `低于规定的 ${min.toFixed(2)}% —— 表决比例不达标。`,
      '按"双三分之二"口径重算同意面积（含同意户的建筑面积，不含未参与表决的户），或在表决资料补齐后重新表决；'
      + '不达标的动用结论不能成立。本工具只做算术比对，不认定表决程序是否合法。'));
  }
  return out;
}

/** 6. 空白/占位符/认不出格式：关键字段缺失、金额无法解析或为负、证件号未脱敏 */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }
    for (const [role, label] of AMOUNT_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '金额无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${txt(raw)}」不是可识别的数字（只认数字、千分位、¥、括号负数、百分数）。`,
          '把金额改成纯数字形态（如 1200000.00）再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '金额为负', it, n,
          `${who(it)}：「${label}」是负数（${money(n)}）—— 归集、分摊与面积类台账里出现负数通常是填反了方向、`
          + '写成了红字冲销，或把退回 / 冲抵记在了分摊列。',
          '确认是红字冲销还是填错借贷方向；确属冲销的请写在「备注」里并保留原值，别直接改成正数。'));
      }
    }
    const id = txt(it.ownerId);
    if (id && RAW_ID_RE.test(id)) {
      out.push(finding('P1', '证件号未脱敏', it, undefined,
        `${who(it)}：业主证件号是 18 位身份证号真实形态（原文长度 ${id.length} 位）—— 公示与流转材料里不应出现完整证件号。`,
        '按脱敏口径改写（如 320101********1234）后再跑；本工具只核形态，不解析证件号本身。'));
    }
  }
  return out;
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的维修资金归集与分摊明细表']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的维修资金归集与分摊明细表']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的维修资金归集与分摊明细表（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行按户（或按使用事项）分摊的明细（现在只有表头，没有可核对的明细行）']);
  }

  const hasRatioCol = t.cols.some((c) => c.role === 'minRatio');
  const hasPeriodCol = t.cols.some((c) => c.role === 'period');
  const hasBankCol = t.cols.some((c) => c.role === 'bankAccount');
  const findings = [];
  const notRun = [];

  for (const f of checkLedgerBalance(t.items)) findings.push(f);
  for (const f of checkApportionment(t.items)) findings.push(f);
  for (const f of checkShareTotal(t.items)) findings.push(f);
  for (const f of checkDuplicateShare(t.items)) findings.push(f);
  if (hasRatioCol) {
    for (const f of checkVoteRatio(t.items)) findings.push(f);
  } else {
    notRun.push('使用事项表决比例核对：材料里没有「规定比例」列 ⇒ 不知道法定/约定的比例阈值，这一项不给结论');
  }
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  // 免费档：上面这六项之外，完整档的检查一项都不执行 —— 这里如实记下来（只记「没做」，不伪造结论）
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const households = new Set(t.items.map(householdOf)).size;
  const projects = new Set(t.items.map(projectOf).filter((x) => x !== '')).size;
  const periods = new Set(t.items.map(periodOf).filter((x) => x !== '')).size;

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      households,
      projects,
      periods,
      collect_total: t.totals.collectAmount,
      interest_total: t.totals.interestIncome,
      usage_amount_total: t.totals.usageAmount,
      share_total: t.totals.shareAmount,
      closing_total: t.totals.closingBalance,
      basis: '期初余额 + 本期归集 + 利息收入 − 本期使用 = 期末余额（逐行复算）；'
        + '分摊额 = 使用总额 × 该户建筑面积 ÷ 参与分摊建筑面积（分币容差 0.01）；'
        + '同一项目 Σ分摊额 = 使用总额；同一期间内同一户同一项目不得重复分摊；'
        + '同意面积 ÷ 参与面积 ≥ 规定比例（双三分之二口径）；必需列与关键单元格不得空白、金额不得为负、证件号须脱敏。'
        + '「使用总额 / 表决金额 / 参与面积 / 同意面积 / 规定比例」是项目级取值，在属于同一项目的每行上重复填写，因此不逐行累加。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对、表决面积与资料对得上**，'
      + '不代表动用维修资金的实体条件、表决程序本身是否合法、工程造价是否合理已经过关 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.items.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    households,
    projects,
    periods,
    collect_total: t.totals.collectAmount,
    interest_total: t.totals.interestIncome,
    usage_amount_total: t.totals.usageAmount,
    share_total: t.totals.shareAmount,
    closing_total: t.totals.closingBalance,
    paid_in_total: t.totals.collectAmount,
    outstanding_total: t.totals.closingBalance,
  };
  result.scope = scope;

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
