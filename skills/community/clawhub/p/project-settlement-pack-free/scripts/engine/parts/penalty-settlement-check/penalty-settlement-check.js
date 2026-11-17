#!/usr/bin/env node
/**
 * penalty-settlement-check-full.js —— 罚款与违约金台账核对引擎（完整档源码；确定性、纯 Node 标准库）。
 *
 * 真实痛点：**每个月做账、以及年度汇算清缴之前，都要把罚款与违约金台账核一遍**。
 * 合同违约金、行政处罚、税收滞纳金、赔付款项几类款项混在一张表里，方向（应收/应付）、依据文件、
 * 已收已付与余额、跨期与重复登记，任何一处错都会一路带到报表和汇算：
 *   · 方向记反 ⇒ 该收的变成该付，余额归属整个反过来，对账怎么都对不上；
 *   · 该收未收 ⇒ 挂在账上的应收没人催，到年底直接变坏账；
 *   · 把行政罚款、税收滞纳金的金额计进了成本费用 ⇒ 汇算清缴时要作纳税调增，忘了调就是补税加滞纳金。
 *
 * 与已有能力的区别：`invoice-consistency-check` 核的是单张发票的要素；`ap-aging-plan-check` 核的是
 * 应付账龄与付款排期；本能力核的是**"罚款与违约金"这一本台账内部的可算关系与口径一致性**
 * （余额复算、合计勾稽、单号与事项重复、方向与金额符号、日期倒挂；完整档再加税前扣除与回收判定 + 处理清单）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} 或 {status:'insufficient_input',missing,advice}。
 * 刻意不做：不联网、不查法规文库、不调用大模型、不给税务或法律意见；
 * 材料不足时**不给结论**（不会输出"未发现问题"式的假通过）；只在表内做算术与口径一致性核对。
 */
'use strict';

const CHECKS_GIVEN = [
  '余额 = 应计金额 − 已收付金额（逐行复算）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '同一单号重复检测',
  '关键字段空缺与占位符检测',
  '方向（应收/应付）与金额符号一致性检测',
  '日期倒挂检测（发生日期不得晚于到期日期或实际收付日期）',
];

const CHECKS_WITHHELD = [
  '不得税前扣除项（行政罚款、税收滞纳金）被计入费用的纳税调整判定（逐条列出调整金额）',
  '应收未收与逾期天数判定（按核对基准日算逾期天数；缺到期日期时如实指出无法判定）',
  '已付未取得依据文件的判定（已付了钱却没有依据文件的那几笔）',
  '跨期未结转判定（发生日期与所属期间不一致、余额还挂着）',
  '同一事项重复登记判定（同类型、同对方、同金额的行）',
  '按金额排序的处理清单（每条带原文行号与建议动作）',
];

const OUT_OF_SCOPE = [
  '判断某笔罚款或违约金在税法上到底能不能税前扣除（那要按具体法条与主管税务机关口径；本工具只按台账里的事项类型做口径一致性提示，不给税务意见）',
  '判断行政罚款该不该缴、金额是否合规，或代理行政复议与诉讼（那是法律判断）',
  '处理外币折算、分期收付与已核销坏账（请先折算成人民币、按本期数填列）',
  '读取 .xlsx 或从财务系统直接取数（需要你先导出成文本贴进来）',
];

const HEADER = [
  '单号', '事项类型', '方向', '对方单位', '依据文件', '应计金额', '已收付金额', '余额',
  '所属期间', '发生日期', '到期日期', '收付日期', '计入费用金额',
];

// 干净样例：五笔明细的余额都能复算、方向合法、日期不倒挂、依据文件齐全、无重复、无跨期、
// 无"不得税前扣除项计入费用"，所以免费档与完整档跑出来都是 0 条。
const SAMPLE_ROWS = [
  ['FK-2026-001', '合同违约金', '应收', '华北建材有限公司', 'HT-2025-118', '50000.00', '50000.00', '0.00', '2026-03', '2026-03-05', '2026-03-31', '2026-03-20', '0.00'],
  ['FK-2026-002', '合同违约金', '应付', '杭州物流有限公司', 'HT-2025-207', '18000.00', '18000.00', '0.00', '2026-03', '2026-03-08', '2026-03-25', '2026-03-18', '18000.00'],
  ['FK-2026-003', '赔付款项', '应付', '苏州安装工程有限公司', 'PC-2026-014', '26000.00', '10000.00', '16000.00', '2026-03', '2026-03-12', '2026-04-10', '2026-03-20', '10000.00'],
  ['FK-2026-004', '赔付款项', '应收', '江苏机电有限公司', 'PC-2026-019', '32000.00', '32000.00', '0.00', '2026-03', '2026-03-15', '2026-03-31', '2026-03-28', '0.00'],
  ['FK-2026-005', '合同违约金', '应付', '合肥科技有限公司', 'HT-2026-003', '9000.00', '0.00', '9000.00', '2026-03', '2026-03-22', '2026-04-20', '', '0.00'],
  ['合计', '', '', '', '', '135000.00', '110000.00', '25000.00', '', '', '', '', '28000.00'],
];

const SAMPLE_TEXT = [HEADER].concat(SAMPLE_ROWS).map((r) => r.join('\t')).join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 更具体的词必须排在更宽泛的前面（tools/header_map_check.py 会钉这一点）：
  //    「实际收付日期」排在「收付日期」前；「实际收付金额」排在「已收金额」前。
  docId: ['单号', '编号', '序号'],
  kind: ['事项类型', '款项类型', '罚款类型', '违约金类型'],
  direction: ['收付方向', '应收应付', '方向'],
  counterparty: ['对方单位', '往来单位', '单位名称', '对方'],
  basis: ['依据文件', '文件依据', '处罚决定书号', '法律文书号', '合同编号'],
  accrued: ['应计金额', '计提金额', '应收金额', '应付金额', '应计'],
  settled: ['实际收付金额', '已收付金额', '已结算金额', '已收金额', '已付金额', '已收付'],
  balance: ['未收付金额', '未结金额', '余额'],
  period: ['所属期间', '会计期间', '所属期', '期间'],
  occurDate: ['发生日期', '业务日期', '开单日期'],
  dueDate: ['到期日期', '到期日', '约定期限'],
  settleDate: ['实际收付日期', '收付日期', '收款日期', '付款日期', '结算日期'],
  expensed: ['计入费用金额', '费用化金额', '计入成本费用', '计入费用'],
};

const LABELS = {
  docId: '单号', kind: '事项类型', direction: '方向', counterparty: '对方单位', basis: '依据文件',
  accrued: '应计金额', settled: '已收付金额', balance: '余额', period: '所属期间',
  occurDate: '发生日期', dueDate: '到期日期', settleDate: '收付日期', expensed: '计入费用金额',
};

// 免费档要能核出东西所必需的结构列；「依据文件」「计入费用金额」只在完整档用，
// 缺了它们完整档会如实报"这项没跑"，不会猜。
const REQUIRED = ['docId', 'kind', 'direction', 'counterparty', 'accrued', 'settled', 'balance',
  'period', 'occurDate', 'dueDate', 'settleDate'];
const SUM_ROLES = ['accrued', 'settled', 'balance', 'expensed'];
const ALWAYS_FILLED = ['docId', 'kind', 'direction', 'counterparty', 'accrued', 'settled', 'balance'];

// 台账口径：事项类型里出现下面这些词 ⇒ 视为不得税前扣除项。
// （合同违约金、赔付款项不属于这一类 —— 「合同违约金」不含"罚款/罚金/滞纳金"，不会被误判。）
const NON_DEDUCTIBLE_RE = /行政罚款|行政处罚|罚款|罚金|税收滞纳金|税务滞纳金|滞纳金/;
const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值，更不会输出"未发现问题"。',
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

/** 把各种写法（2026/3/5、2026年3月5日、2026-03-05）归一成 YYYY-MM-DD；认不出来返回 null */
function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[年月]/g, '-').replace(/日/g, '').replace(/[./]/g, '-');
  const m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
  if (!m) return null;
  const y = Number(m[1]); const mo = Number(m[2]); const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = new Date(Date.UTC(y, mo - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return `${m[1]}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
}

/** 期间（所属期间）归一成 YYYY-MM；认不出来返回 null */
function parseTable(text) {
  const lines = String(text).split(/\r?\n/);
  const rows = [];
  lines.forEach((l, i) => { if (l.trim() !== '') rows.push({ no: i + 1, text: l }); });
  if (!rows.length) return { error: 'empty' };
  const cols = splitRow(rows[0].text).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < rows.length; i++) {
    const cells = splitRow(rows[i].text);
    const row = { line: rows[i].no, raw: rows[i].text, byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const first = String(cells[0] || '').trim();
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true; totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);

function who(it) {
  const id = String(it.byRole.docId === undefined ? '' : it.byRole.docId).trim();
  const cp = String(it.byRole.counterparty === undefined ? '' : it.byRole.counterparty).trim();
  const tag = [id || '未填单号', cp].filter(Boolean).join('／');
  return `第 ${it.line} 行的「${tag}」`;
}

function dirOf(it) {
  const s = String(it.byRole.direction === undefined ? '' : it.byRole.direction)
    .replace(/[\s（）()]/g, '');
  if (!s) return null;
  if (s.indexOf('应付') >= 0 || s.indexOf('付款') >= 0) return 'payable';
  if (s.indexOf('应收') >= 0 || s.indexOf('收款') >= 0) return 'receivable';
  return null;
}

/* ===== 免费档检查（这部分在免费包里也有，完整档是它的超集） ===== */

function checkBalance(it) {
  const accrued = num(it, 'accrued');
  const settled = num(it, 'settled');
  const stated = num(it, 'balance');
  if (accrued === null || settled === null || stated === null) return null;
  const expect = round2(accrued - settled);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '余额与复算不符', line: it.line, source: it.raw,
    amount: round2(stated - expect),
    message: `${who(it)}的余额是 ${stated.toFixed(2)}，`
      + `按 应计金额 ${accrued.toFixed(2)} − 已收付金额 ${settled.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '余额只能由这一行的应计与已收付推出来；对不上多半是补记了收付没改余额，或改了应计没重算。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line, source: t.raw,
        amount: round2(stated - sum),
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
          + `相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了一笔，要么合计行没跟着更新；两种都会让上报的余额与账上不一致。',
      });
    }
  }
  return out;
}

function checkDocDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.docId === undefined ? '' : it.byRole.docId).trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P0', category: '单号重复', line: it.line, source: it.raw,
        message: `单号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行又出现一次。`,
        advice: '同一单号只能有一行；重复行会让应计、已收付、余额一起翻倍。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of ALWAYS_FILLED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或占位符', line: it.line, source: it.raw,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '这一格缺了这笔就核不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

function checkDirectionSign(it) {
  const raw = String(it.byRole.direction === undefined ? '' : it.byRole.direction).trim();
  const negs = [];
  for (const role of ['accrued', 'settled', 'balance']) {
    const n = num(it, role);
    if (n !== null && n < -TOL) negs.push(`${LABELS[role]} ${n.toFixed(2)}`);
  }
  if (!isBlank(raw) && dirOf(it) === null) {
    return {
      level: 'P1', category: '方向与金额符号不一致', line: it.line, source: it.raw,
      message: `${who(it)}的方向填的是「${raw}」，认不出是应收还是应付。`,
      advice: '方向列只填「应收」（我们要收回来）或「应付」（我们要付出去）；方向错了余额归属整个反过来。',
    };
  }
  if (negs.length) {
    return {
      level: 'P1', category: '方向与金额符号不一致', line: it.line, source: it.raw,
      message: `${who(it)}的方向是「${raw}」，但金额出现了负数：${negs.join('、')}。`,
      advice: '方向已经由方向列表达，金额一律填正数；负数等于把方向又反着记了一遍，合计与余额都会错。',
    };
  }
  return null;
}

function checkDateOrder(it) {
  const out = [];
  const occur = normDate(it.byRole.occurDate);
  const due = normDate(it.byRole.dueDate);
  const settle = normDate(it.byRole.settleDate);
  if (occur && due && due < occur) {
    out.push({
      level: 'P1', category: '日期倒挂', line: it.line, source: it.raw,
      message: `${who(it)}的到期日期 ${due} 早于发生日期 ${occur}。`,
      advice: '到期日早于发生日，通常是年份或月份填错（例如 2025 写成 2026）；先改日期再谈逾期天数。',
    });
  }
  if (occur && settle && settle < occur) {
    out.push({
      level: 'P1', category: '日期倒挂', line: it.line, source: it.raw,
      message: `${who(it)}的收付日期 ${settle} 早于发生日期 ${occur}。`,
      advice: '钱不可能在事项发生之前就收付；这两列至少有一列填错了。',
    });
  }
  return out;
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的罚款与违约金台账（要能认出「单号」「事项类型」「方向」「对方单位」「应计金额」'
      + '「已收付金额」「余额」「所属期间」「发生日期」「到期日期」「收付日期」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从台账或表格导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一笔明细行（只有合计行的表核不出东西）']);

  const findings = [];
  const notRun = [];
  const basisParts = [
    '余额 = 应计金额 − 已收付金额（逐行复算）',
    '合计行逐列复核（每一列都要等于各行之和）',
    '同一单号只能出现一次；关键字段不得空缺或写占位符',
    '方向只认应收/应付，金额一律填正数（符号不再表达方向）',
    '发生日期不得晚于到期日期或实际收付日期',
  ];
  let actions = [];
  let extraSummary = {};
  let extraScope = {};
  let checksExecuted = CHECKS_GIVEN;

  for (const it of t.items) {
    const a = checkBalance(it); if (a) findings.push(a);
    const b = checkDirectionSign(it); if (b) findings.push(b);
    for (const f of checkDateOrder(it)) findings.push(f);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDocDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line)
    || (String(x.category) < String(y.category) ? -1 : (String(x.category) > String(y.category) ? 1 : 0)));

  const sumRole = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const sumDir = (want) => round2(t.items.reduce((s, it) => {
    if (dirOf(it) !== want) return s;
    const n = num(it, 'balance');
    return s + (n === null ? 0 : n);
  }, 0));

  const summary = Object.assign({
    rows: t.items.length,
    total: findings.length,
    p0: findings.filter((f) => f.level === 'P0').length,
    p1: findings.filter((f) => f.level === 'P1').length,
    p2: findings.filter((f) => f.level === 'P2').length,
    accrued_total: sumRole('accrued'),
    settled_total: sumRole('settled'),
    balance_total: sumRole('balance'),
    receivable_balance_total: sumDir('receivable'),
    payable_balance_total: sumDir('payable'),
    basis: basisParts.join('；') + '。',
  }, extraSummary);

  const scope = Object.assign({
    rows: t.items.length,
    checks_run: checksExecuted,
    checks_not_run: notRun,
    checks_out_of_scope: OUT_OF_SCOPE,
    accrued_total: summary.accrued_total,
    settled_total: summary.settled_total,
    balance_total: summary.balance_total,
    receivable_balance_total: summary.receivable_balance_total,
    payable_balance_total: summary.payable_balance_total,
  }, extraScope);

  const result = {
    findings: findings,
    summary: summary,
    scope: scope,
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: checksExecuted,
    checks_not_run: notRun,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (actions.length) result.actions = actions;
  if (findings.length === 0) {
    result.note = '本次**实际执行**的检查项都通过了（没执行的项见 checks_not_run，不计入本次结论）。'
      + '这只说明这张台账按上面写明的口径算得对，不代表这些罚款或违约金在税法上一定能扣除或一定不能扣除 —— '
      + '那不在本工具范围内';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, normDate, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, REQUIRED, SUM_ROLES, ALWAYS_FILLED,
};
