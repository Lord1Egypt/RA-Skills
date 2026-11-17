/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * insurance-commission-check.js —— 保险佣金与手续费结算核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月（或每季）保司结算单到手之后**。保险中介 / 代理公司 /
 * 银保渠道的财务，必须把保司结算过来的佣金与手续费逐笔和保单结算明细勾稽：
 * 应收佣金多少、手续费多少、退保冲回多少、代扣税费多少、实际到账多少。
 * 这张表对不上，方向只有两个 —— **少结（白干）** 或 **多结 / 重复计佣**（要被保司追回），
 * 两个都会传导到开票与增值税申报上，而且**结完账就很难倒查**。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   应收佣金 = 保费金额 × 佣金率
 *   实收净额 = 应收佣金 + 手续费 + 退保冲回 − 代扣税费   （退保冲回以**负数**填列，即红字冲回）
 *   合计行各列 = 明细行相加
 *
 * 本文件是**免费档与完整档共用的同一份源码**：
 *   · 免费档执行 6 项逐行 / 逐表核对（见 CHECKS_GIVEN）；
 *   · 完整档在免费档之外多一种能力 —— 跨机构 / 跨险种汇总台账、按差异金额排序的处理清单、
 *     以及把差异归因到佣金率档位 / 保费口径 / 退保冲回 / 跨期归属四大类（见 CHECKS_WITHHELD）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件；
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）；
 * **不写盘、不读环境变量**（同样的输入永远给同样的输出）。
 *
 * 材料不足时**绝不给结论**：返回 insufficient_input 并列出缺什么，绝不输出「未发现问题」。
 * 每条结论都带**原文行号**与原文片段，第三方可用同一份输入复算。
 *
 * 本工具**不判断**：佣金率该定多少、是否符合监管对佣金上限或手续费口径的规定、
 * 退保冲回该冲减哪一期、手续费是否已经到账 —— 表里填多少就以多少为准，
 * 只核**表内勾稽**（完整清单见 OUT_OF_SCOPE）。
 *
 * 引擎契约（与仓库其它引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *   CHECKS_GIVEN / CHECKS_WITHHELD   免费档执行 / 不执行的检查项（免费包据此**如实列出未执行项**）
 *   CHECKS_OUT_OF_SCOPE              本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT                      样例输入（免费包 --sample 用它自检）
 *
 * ⚠️ 完整档（付费）的实现集中在下面那行带「以下为完整档」的 MARKER 之后、`run` 之前：
 *    免费包由 tools/strip_free_engine.py 按**形态 A** 整块摘掉，所以
 *      · 付费检查函数与付费专用工具一律写在 MARKER 之后；
 *      · 免费档也要用的工具函数写在 MARKER 之前（摘除后免费引擎仍然跑得起来）。
 *    ⛔ 付费开关**只声明一次**（在 run 里，形态固定），注释里也不写它的字面量：
 *       strip 的残渣断言是**纯字符串包含**判断，注释里写一遍就会被判「没删干净」而整包回滚；
 *       也**不要**在注释里写出开关那一行的字面量（同一条断言）。
 */

const CHECKS_GIVEN = [
  '应收佣金逐行复算（保费金额 × 佣金率 = 应收佣金）',
  '手续费与佣金合计勾稽（实收净额 = 应收佣金 + 手续费 + 退保冲回 − 代扣税费）',
  '合计行逐列复核（合计行各列 = 明细行相加）',
  '首期 / 续期佣金口径与保单年度一致（首期对应第 1 年、续期从第 2 年起）',
  '同一保单号同一期间重复结算检测（同一保单号 + 同一所属期间 + 同一佣金类型）',
  '退保冲回符号与关键字段空缺检测（退保冲回以负数填列；单号 / 期间 / 金额列不可为空）',
];

const CHECKS_WITHHELD = [
  '跨机构/跨险种汇总台账（按机构与险种汇总笔数、保费、应收佣金与实收净额，并与全表明细对平）',
  '按差异金额排序的处理清单（把需要处理的差异按金额降序排列，≥2 条才出清单）',
  '差异归因（把差异归到佣金率档位、保费口径、退保冲回、跨期归属四类）',
];

const OUT_OF_SCOPE = [
  '判断佣金率 / 手续费率该定多少、是否符合监管对保险中介佣金上限与手续费口径的规定（那属于代理协议与合规口径，请找合规负责人）',
  '判断退保冲回该不该跨期分摊、该冲减哪一期的佣金收入（那属于收入确认的会计判断，请咨询会计师）',
  '核对开票金额、发票税率与发票信息是否正确，也不做增值税申报（本工具只核结算表内的算术勾稽）',
  '判断佣金与手续费是否已经到账（以银行流水与保司结算单为准，需要你先导出成文本贴进来）',
  '校验保单本身的承保信息（投保人、险种、保额、生效日与佣金结算的对应关系，一律以保司结算单为准）',
  '识别佣金类型 / 险种的命名是否合规（只按表内已认得的写法做口径核对）',
  '给出税务、审计或法律意见',
];

/* 干净样例：单一机构、单一险种的 5 行明细 + 1 行合计，**两档都必须 0 命中**。
   第 1 行 100000.00 × 15% = 15000.00，净额 15000.00 + 0.00 + 0.00 − 900.00 = 14100.00
   第 2 行  50000.00 × 12% =  6000.00，净额  6000.00 + 200.00 + 0.00 − 360.00 =  5840.00
   第 3 行 100000.00 ×  5% =  5000.00，净额  5000.00 + 0.00 + 0.00 − 300.00 =  4700.00（续期，第 2 年）
   第 4 行  50000.00 ×  5% =  2500.00，净额  2500.00 + 0.00 + 0.00 − 150.00 =  2350.00（续期，第 2 年）
   第 5 行  80000.00 × 10% =  8000.00，净额  8000.00 + 500.00 + (−1000.00) − 480.00 =  7020.00（含一笔退保冲回）
   合计行 = 各列之和：保费 380000.00 / 应收佣金 36500.00 / 手续费 700.00 / 退保冲回 −1000.00 / 代扣税费 2190.00 / 实收净额 34010.00
   样例刻意**只有一家机构、一个险种**：把多机构 / 多险种的表一起贴进来时，
   完整档的「跨机构/跨险种汇总台账」才有东西可汇总（单机构单险种不叫台账）。 */
const SAMPLE_HEADER = [
  '所属期间', '保险公司', '险种', '分支机构', '保单号', '佣金类型', '保单年度',
  '保费金额', '佣金率', '应收佣金', '手续费', '退保冲回', '代扣税费', '实收净额', '备注',
];
const SAMPLE_ROWS = [
  ['2026-01', '中国人寿', '终身寿险', '华东分公司', 'P2026001', '首期佣金', '1',
    '100000.00', '15.00%', '15000.00', '0.00', '0.00', '900.00', '14100.00', '首年保费一次缴清'],
  ['2026-01', '中国人寿', '终身寿险', '华东分公司', 'P2026002', '首期佣金', '1',
    '50000.00', '12.00%', '6000.00', '200.00', '0.00', '360.00', '5840.00', '本月另有手续费 200'],
  ['2026-02', '中国人寿', '终身寿险', '华东分公司', 'P2026001', '续期佣金', '2',
    '100000.00', '5.00%', '5000.00', '0.00', '0.00', '300.00', '4700.00', '第二期续期'],
  ['2026-02', '中国人寿', '终身寿险', '华东分公司', 'P2026002', '续期佣金', '2',
    '50000.00', '5.00%', '2500.00', '0.00', '0.00', '150.00', '2350.00', ''],
  ['2026-02', '中国人寿', '终身寿险', '华东分公司', 'P2026003', '首期佣金', '1',
    '80000.00', '10.00%', '8000.00', '500.00', '-1000.00', '480.00', '7020.00', '本月一笔退保冲回 -1000'],
];
const SAMPLE_TOTAL = ['合计', '', '', '', '', '', '',
  '380000.00', '', '36500.00', '700.00', '-1000.00', '2190.00', '34010.00', ''];
const SAMPLE_TEXT = [SAMPLE_HEADER.join('\t')]
  .concat(SAMPLE_ROWS.map((r) => r.join('\t')))
  .concat([SAMPLE_TOTAL.join('\t')])
  .join('\n');

const TOL = 0.01;              // 金额容差：1 分
const RATE_TOL = 0.00005;      // 费率容差：0.005 个百分点

const LABELS = {
  period: '所属期间',
  insurer: '保险公司',
  insuranceType: '险种',
  branch: '分支机构',
  policyNo: '保单号',
  commissionType: '佣金类型',
  policyYear: '保单年度',
  premium: '保费金额',
  commissionRate: '佣金率',
  commissionDue: '应收佣金',
  handlingFee: '手续费',
  clawback: '退保冲回',
  taxWithheld: '代扣税费',
  netReceived: '实收净额',
  memo: '备注',
};

/* 表头关键词表：**更具体的别名必须排在更宽泛的别名前面**，
   否则宽泛词会抢走具体列（本仓库 header_map_check 专门钉这个坑）。
   顺序安排的理由：
     · 「佣金类型」必须排在「佣金率」「应收佣金」前，否则含「佣金」的列会被整列抢走；
     · 「手续费」只作金额列的别名，且「佣金类型」先认（它认的是「手续费类型」这种写法）；
     · 「退保冲回」不许出现在佣金类型的别名里，否则整列冲回金额会被当成类型；
     · 「保费金额」排在所有带「金额」的列（应收佣金 / 手续费 / 净额）前。 */
const HEADER_KEYS = [
  ['period', ['所属期间', '结算期间', '会计期间', '结算月份', '所属期', '期间', '月份']],
  ['insurer', ['保险公司名称', '保险公司', '承保公司', '保司']],
  ['insuranceType', ['险种名称', '险种类别', '保险类型', '险种']],
  ['branch', ['分支机构', '所属机构', '机构名称', '支公司', '机构']],
  ['policyNo', ['保单编号', '保单号码', '保单号', '投保单号']],
  ['commissionType', ['佣金类型', '手续费类型', '佣金项目', '手续费项目', '费用类型',
    '佣金科目', '手续费科目', '续期佣金', '首期佣金', '附加佣金']],
  ['policyYear', ['保单年度', '保险年度', '承保年度', '年度']],
  ['premium', ['保费金额', '保费收入', '承保保费', '规模保费', '保费']],
  ['commissionRate', ['佣金率', '手续费率', '佣金比例', '手续费比例', '费率']],
  ['commissionDue', ['应收佣金金额', '应收佣金', '应结佣金', '应收手续费', '应结手续费', '佣金']],
  ['handlingFee', ['手续费金额', '手续费收入', '手续费']],
  ['clawback', ['退保冲回', '退保追回', '退保追偿', '退保扣回', '追回金额', '扣回金额']],
  ['taxWithheld', ['代扣税费', '代扣税金', '代扣增值税', '代扣税', '税费', '税金']],
  ['netReceived', ['实收净额', '实收佣金', '结算净额', '净结算额', '实收金额', '净额']],
  ['memo', ['备注', '说明', '原因']],
];

/** 表里必须认出来的列（缺任何一列都**不给结论**）；备注是选填。 */
const REQUIRED_ROLES = ['period', 'insurer', 'insuranceType', 'branch', 'policyNo', 'commissionType',
  'policyYear', 'premium', 'commissionRate', 'commissionDue', 'handlingFee', 'clawback',
  'taxWithheld', 'netReceived'];

/** 能按明细行相加的列（导出给外部核对口径用，用来核合计行） */
const SUM_ROLES = ['premium', 'commissionDue', 'handlingFee', 'clawback', 'taxWithheld', 'netReceived'];

/** 行里**必须填**的列（手续费与退保冲回可以为空 —— 空按 0 参与勾稽；备注本来就是选填） */
const ROW_REQUIRED = ['period', 'insurer', 'insuranceType', 'branch', 'policyNo', 'commissionType',
  'policyYear', 'premium', 'commissionRate', 'commissionDue', 'taxWithheld', 'netReceived'];

const TEXT_ROLES = ['period', 'insurer', 'insuranceType', 'branch', 'policyNo', 'commissionType', 'memo'];
const NUM_ROLES = ['policyYear', 'premium', 'commissionRate', 'commissionDue', 'handlingFee',
  'clawback', 'taxWithheld', 'netReceived'];

const FIRST_WORDS = /首期|首年|首次|新单/;
const RENEW_WORDS = /续期|续年|续保|续收/;
const TOTAL_WORDS = /^(合计|小计|总计|共计|汇总|总合计)/;

const ADVICE = '请把「保险佣金与手续费结算明细表」连同**表头行**一起贴进来（从 Excel 直接复制、Tab 分隔最稳）。'
  + '必需列：' + REQUIRED_ROLES.map((r) => LABELS[r]).join('、') + '。'
  + '每行一笔结算，形如「2026-01\t中国人寿\t终身寿险\t华东分公司\tP2026001\t首期佣金\t1'
  + '\t100000.00\t15.00%\t15000.00\t0.00\t0.00\t900.00\t14100.00」。材料不足时本工具不做任何认定，也不套用默认值。';

function insufficient(missing) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice: ADVICE };
}

/* ================================ 共用工具 ================================ */

const str = (v) => (v === undefined || v === null) ? '' : String(v).trim();

function splitRow(line) {
  if (String(line).indexOf('\t') >= 0) return String(line).split('\t').map((s) => s.trim());
  return String(line).split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
}

function roleOf(header) {
  const h = str(header).replace(/[\s（）()]/g, '');
  if (!h) return null;
  for (const pair of HEADER_KEYS) {
    for (const key of pair[1]) {
      if (h.indexOf(key) >= 0) return pair[0];
    }
  }
  return null;
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  s = s.replace(/[()]/g, '').replace(/%$/, '');
  if (!/^[+-]?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -Math.abs(n) : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

/** 佣金率 / 费率归一化成小数：`15%` ⇒ 0.15；`0.15` ⇒ 0.15；`15` ⇒ 0.15 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

const fmt = (n) => (n === null || n === undefined || !Number.isFinite(Number(n)))
  ? '(空)' : Number(n).toFixed(2);

const shortRaw = (s) => String(s === undefined || s === null ? '' : s).replace(/\s+/g, ' ').trim().slice(0, 90);

const ev = (list) => [].concat(list)
  .filter((x) => x !== null && x !== undefined && String(x).trim() !== '')
  .map(shortRaw).join(' ‖ ');

function finding(level, category, line, message, advice, evidence) {
  return { level, category, line, message, advice, evidence };
}

/** 检查函数一律返回数组；万一被改成返回 null 之类的非数组，也只当「没报」，
    不让整条流水线抛异常（真正被短路时，对照测试必须因此失败）。 */
const asList = (x) => (Array.isArray(x) ? x : []);

const policyKeyOf = (r) => str(r.policyNo) || '(未填保单号)';
const typeKeyOf = (r) => str(r.commissionType) || '(未填佣金类型)';

/** 只有明细行才需要报「行」；所有结论的 line 都是**原文行号**（1 起算） */
function parseTable(text) {
  const src = (text === undefined || text === null) ? '' : String(text);
  const lines = src.split(/\r?\n/);
  const rows = [];
  lines.forEach((l, i) => { if (String(l).trim() !== '') rows.push({ text: String(l), line: i + 1 }); });
  const missingAll = REQUIRED_ROLES.map((r) => LABELS[r]);
  if (rows.length === 0) {
    return { error: 'empty', items: [], totals: { line: 0, raw: '' }, header: [], roles: [],
      headerLine: 0, missingColumns: missingAll };
  }
  // 表头行 = 前 6 个非空行里「认出的角色数」最多的一行（容忍标题行 / 说明行）
  let best = null;
  for (let i = 0; i < Math.min(6, rows.length); i++) {
    const cells = splitRow(rows[i].text);
    const roles = cells.map((c) => roleOf(c));
    const n = roles.filter(Boolean).length;
    if (!best || n > best.n) best = { n, i, cells, roles };
  }
  if (!best || best.n < 2) {
    return { error: 'no_header', items: [], totals: { line: 0, raw: '' }, header: [], roles: [],
      headerLine: 0, missingColumns: missingAll };
  }
  const header = best.cells;
  const roles = best.roles;
  const missingColumns = REQUIRED_ROLES.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = { line: 0, raw: '' };
  for (let k = best.i + 1; k < rows.length; k++) {
    const cells = splitRow(rows[k].text);
    const first = str(cells[0]);
    const row = { line: rows[k].line, raw: rows[k].text };
    TEXT_ROLES.forEach((r) => { row[r] = ''; });
    NUM_ROLES.forEach((r) => { row[r] = null; });
    header.forEach((_h, ci) => {
      const role = roles[ci];
      if (!role) return;
      const cell = cells[ci] === undefined ? '' : cells[ci];
      row[role] = NUM_ROLES.indexOf(role) >= 0 ? normNumber(cell) : str(cell);
    });
    if (!totals.line && TOTAL_WORDS.test(first)) {
      totals.line = row.line;
      totals.raw = row.raw;
      NUM_ROLES.forEach((r) => { totals[r] = row[r]; });
      continue;
    }
    items.push(row);
  }
  return { error: null, items, totals, header, roles, headerLine: rows[best.i].line, missingColumns };
}

/** 表内口径的应收佣金（保费金额 × 佣金率）；认不出就返回 null（不猜） */
function expectedDue(r) {
  const rate = rateValue(r.commissionRate);
  if (r.premium === null || rate === null) return null;
  return round2(r.premium * rate);
}

/* ============================ 免费档检查项（6 项） ============================ */
/* 契约：每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

/** 1. 应收佣金 = 保费金额 × 佣金率（逐行复算，差 1 分钱也报） */
function checkCommissionRecompute(it) {
  const out = [];
  it.items.forEach((r) => {
    const due = expectedDue(r);
    if (due === null || r.commissionDue === null) return;      // 列空缺由「关键字段空缺」负责
    const diff = round2(r.commissionDue - due);
    if (Math.abs(diff) < 0.005) return;
    out.push(finding('P0', '应收佣金复算不符', r.line,
      `第 ${r.line} 行「${policyKeyOf(r)}／${typeKeyOf(r)}」：保费金额 ${fmt(r.premium)} × 佣金率 `
      + `${fmt((rateValue(r.commissionRate) || 0) * 100)}% = ${fmt(due)}，`
      + `表里「应收佣金」是 ${fmt(r.commissionDue)}，相差 ${fmt(diff)}。`
      + '应收佣金就是"保费 × 佣金率"：算少了是白干，算多了保司对账时会追回，两头都是钱。',
      '按表内口径重算这一行的应收佣金，或把保费金额 / 佣金率改成与结算单一致的档位。',
      ev([r.raw])));
  });
  return out;
}

/** 2. 手续费与佣金合计勾稽：实收净额 = 应收佣金 + 手续费 + 退保冲回 − 代扣税费 */
function checkNetRecompute(it) {
  const out = [];
  it.items.forEach((r) => {
    const cb = r.clawback === null ? 0 : r.clawback;
    if (cb > TOL) return;                                     // 冲回填成正数 → 由「退保冲回符号」负责，不重复报
    if (r.netReceived === null || r.taxWithheld === null) return;   // 空缺由「关键字段空缺」负责
    const base = r.commissionDue;
    if (base === null) return;
    const fee = r.handlingFee === null ? 0 : r.handlingFee;
    const expect = round2(base + fee + cb - r.taxWithheld);
    const diff = round2(r.netReceived - expect);
    if (Math.abs(diff) < 0.005) return;
    out.push(finding('P0', '手续费与佣金合计勾稽不符', r.line,
      `第 ${r.line} 行「${policyKeyOf(r)}／${typeKeyOf(r)}」：应收佣金 ${fmt(base)} + 手续费 ${fmt(fee)} `
      + `+ 退保冲回 ${fmt(cb)} − 代扣税费 ${fmt(r.taxWithheld)} = ${fmt(expect)}，`
      + `表里「实收净额」是 ${fmt(r.netReceived)}，相差 ${fmt(diff)}。`
      + '实收净额是打款与开票的口径：差一分，账上的佣金收入与增值税都会跟着差。',
      '按这一行的四项重算实收净额；退保冲回要按**负数**加进来（红字冲回），代扣税费按实际代扣数填。',
      ev([r.raw])));
  });
  return out;
}

/** 3. 合计行逐列复核（合计行各列 = 明细行相加） */
function checkTotalRow(it) {
  const out = [];
  if (!it.totals || !it.totals.line) return out;
  SUM_ROLES.forEach((role) => {
    const stated = it.totals[role];
    if (stated === null || stated === undefined) return;
    let sum = 0;
    let n = 0;
    it.items.forEach((r) => {
      const v = r[role];
      if (v === null || v === undefined) return;
      sum = round2(sum + v);
      n += 1;
    });
    if (!n) return;
    const diff = round2(stated - sum);
    if (Math.abs(diff) < 0.005) return;
    out.push(finding('P0', '合计行与明细之和不符', it.totals.line,
      `第 ${it.totals.line} 行合计行的「${LABELS[role]}」是 ${fmt(stated)}，本表 ${n} 行明细的`
      + `「${LABELS[role]}」相加是 ${fmt(sum)}，相差 ${fmt(diff)}。`
      + '合计行是保司对账与开票的取数口径：对不上说明明细或合计有一边错。',
      '先把明细行逐行核一遍（前两项），再重算合计行；不要用合计行倒推明细。',
      ev([it.totals.raw])));
  });
  return out;
}

/** 4. 首期 / 续期佣金口径与保单年度一致 */
function checkCommissionTypeVsYear(it) {
  const out = [];
  it.items.forEach((r) => {
    const type = str(r.commissionType);
    const year = r.policyYear;
    if (!type || year === null) return;
    const isFirst = FIRST_WORDS.test(type);
    const isRenew = RENEW_WORDS.test(type);
    if (!isFirst && !isRenew) return;
    const bad = (isFirst && year >= 2) || (isRenew && year <= 1);
    if (!bad) return;
    out.push(finding('P1', '首期/续期佣金口径与保单年度不一致', r.line,
      `第 ${r.line} 行「${policyKeyOf(r)}」的「佣金类型」是「${type}」，但「保单年度」是第 ${year} 年。`
      + '首期佣金只对应保单年度第 1 年，续期佣金从第 2 年才开始；'
      + '首期与续期的费率本来就不一样（首期高、续期低），标识与年度不一致时，'
      + '这笔该按哪一档费率结就成了扯皮点，也最容易把两档费率混用。',
      '把「佣金类型」或「保单年度」改成与结算单一致；两档费率混用请分开列示。',
      ev([r.raw])));
  });
  return out;
}

/** 5. 同一保单号同一期间重复结算 */
function checkDuplicateSettlement(it) {
  const out = [];
  const groups = new Map();
  it.items.forEach((r) => {
    const period = str(r.period);
    const no = str(r.policyNo);
    if (!period || !no) return;                                // 空缺由「关键字段空缺」负责
    const key = period + '|' + no + '|' + typeKeyOf(r);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(r);
  });
  groups.forEach((list) => {
    if (list.length < 2) return;
    const last = list[list.length - 1];
    const detail = list.map((x) => `第 ${x.line} 行（应收佣金 ${fmt(x.commissionDue)}，实收净额 ${fmt(x.netReceived)}）`).join('、');
    out.push(finding('P1', '同一保单号同一期间重复结算', last.line,
      `同一保单「${policyKeyOf(last)}」在 ${str(last.period)} 被按同一佣金类型「${typeKeyOf(last)}」`
      + `结算了 ${list.length} 次：${detail}。`
      + '同一保单、同一期间、同一类佣金只应结一次：重复结算会让应收佣金与实收净额被重复统计一遍。',
      '核对是重复录入，还是把同一笔佣金拆成了两行；确实是分次结算就把期间或佣金类型写清楚（例如续期第一期 / 第二期）。',
      ev(list.map((x) => x.raw).slice(0, 3))));
  });
  return out;
}

/** 6a. 退保冲回必须按负数填列（红字冲回）；填正数即报 */
function checkClawbackSign(it) {
  const out = [];
  it.items.forEach((r) => {
    const cb = r.clawback;
    if (cb === null || cb === undefined) return;
    if (cb <= TOL) return;
    out.push(finding('P1', '退保冲回符号与口径不符', r.line,
      `第 ${r.line} 行「${policyKeyOf(r)}」的「退保冲回」是 ${fmt(cb)}（正数）。`
      + '本表口径里退保冲回按**负数**填列（红字冲回），因为它要从应收佣金里减掉；'
      + '填正数时净额会被反向加上这笔钱，越核越乱。',
      '把这一列改成负数（例如 -1000.00）；若这一列记的其实是"追回收入"，请另立一列并改表头。',
      ev([r.raw])));
  });
  return out;
}

/** 6b. 关键字段空缺（空缺 / 占位符会让对应的复算静默跳过） */
function checkBlanks(it) {
  const out = [];
  it.items.forEach((r) => {
    const miss = ROW_REQUIRED.filter((k) => isBlank(r[k]));
    if (!miss.length) return;
    out.push(finding('P0', '关键字段空缺', r.line,
      `第 ${r.line} 行的必需字段为空或写了占位符：${miss.map((k) => LABELS[k]).join('、')}`
      + `（原文：${shortRaw(r.raw) || '(空行)'}）。`
      + '这些字段是逐行复算与重复结算检测的前提；缺哪列就补哪列，本工具不会替它套默认值，也不会跳过这一行。',
      '补齐这些列后再跑；确实没有金额的列请填 0.00，不要留空白。',
      ev([r.raw])));
  });
  return out;
}

function run(payload) {
  if (payload !== undefined && payload !== null && (typeof payload !== 'object' || Array.isArray(payload))) {
    return insufficient([`入参不是对象（收到的是 ${Array.isArray(payload) ? 'array' : typeof payload}）：`
      + '请用 {"text": "…"} 把保险佣金与手续费结算明细表传进来']);
  }
  const p = (payload && typeof payload === 'object') ? payload : {};
  let text = '';
  if (typeof p.text === 'string') text = p.text;
  else if (Array.isArray(p.text)) text = p.text.join('\n');

  const it = parseTable(text);
  const missing = [];
  if (it.error === 'empty') {
    missing.push('没有收到任何材料（text 是空的）');
  } else if (it.error === 'no_header') {
    missing.push('认不出表头：前几行里没有任何一行能认出 2 个以上的列名（例如 '
      + REQUIRED_ROLES.slice(0, 4).map((r) => LABELS[r]).join('、') + ' …）');
  }
  if (!it.error && (it.missingColumns || []).length) {
    missing.push('缺少必需列：' + it.missingColumns.join('、'));
  }
  if (!it.error && !(it.missingColumns || []).length && !it.items.length) {
    missing.push('只有表头（或只有合计行），没有任何佣金结算明细行');
  }
  if (missing.length) return insufficient(missing);

  const findings = [].concat(
    asList(checkCommissionRecompute(it)),
    asList(checkNetRecompute(it)),
    asList(checkTotalRow(it)),
    asList(checkCommissionTypeVsYear(it)),
    asList(checkDuplicateSettlement(it)),
    asList(checkClawbackSign(it)),
    asList(checkBlanks(it)),
  );

  const scope = {
    given: CHECKS_GIVEN.slice(),
    checks: CHECKS_GIVEN.slice(),
    checks_not_run: CHECKS_WITHHELD.slice(),
    withheld: CHECKS_WITHHELD.slice(),
    rows: it.items.length,
    totals_row: Boolean(it.totals && it.totals.line),
    header_line: it.headerLine,
    executed_locally: true,
    network_used: false,
  };
  let note = '本版本只执行免费检查项：' + CHECKS_GIVEN.join('、') + '；未执行的检查项见 scope.checks_not_run。';



  findings.sort((a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category)));
  const summary = { rows: it.items.length, p0: 0, p1: 0, p2: 0, total: 0, omitted: 0, by_category: {} };
  findings.forEach((f) => {
    const lv = String(f.level || 'P1');
    if (lv === 'P0') summary.p0 += 1;
    else if (lv === 'P2') summary.p2 += 1;
    else summary.p1 += 1;
    summary.by_category[f.category] = (summary.by_category[f.category] || 0) + 1;
  });
  summary.total = findings.length;
  summary.verdict = summary.p0 > 0 ? 'ERROR_FOUND'
    : (summary.total > 0 ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND');

  const sums = {};
  SUM_ROLES.forEach((r) => {
    let s = 0;
    it.items.forEach((x) => { if (x[r] !== null && x[r] !== undefined) s = round2(s + x[r]); });
    sums[r] = s;
  });

  const result = {
    findings,
    summary,
    sums,
    rows: it.items.length,
    header: it.header.slice(),
    header_line: it.headerLine,
    totals_line: it.totals && it.totals.line ? it.totals.line : null,
    scope,
    checks_given: scope.given.slice(),
    checks_withheld: scope.checks_not_run.slice(),
    checks_executed: scope.checks.slice(),
    checks_out_of_scope: OUT_OF_SCOPE.slice(),
    note,
    disclaimer: '只核「保费金额 × 佣金率 = 应收佣金」与「应收佣金 + 手续费 + 退保冲回 − 代扣税费 = 实收净额」'
      + '这类**表内勾稽**，以及合计行、重复结算、档位与差异归因；'
      + '**不判断**佣金率该定多少、是否符合监管上限，**不判断**退保冲回该冲减哪一期'
      + '（以代理协议、保司结算单与会计师口径为准）。结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
