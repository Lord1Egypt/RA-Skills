#!/usr/bin/env node
/**
 * ap-reconciliation.js —— 供应商应付对账引擎（确定性、纯 Node 标准库）。
 *
 * 为什么做这个：
 *   **每月（至少每季）财务都要跟供应商对一次账**：把「我方应付余额」和
 *   「对方发来的对账单金额」逐家对上。逐家核「期初应付 + 本期采购 − 本期付款 = 期末应付」、
 *   「差异 = 我方期末 − 对方对账金额」、合计行、有没有重复供应商、有没有该填没填 —— 这些**全是算术**。
 *   对不上的那几家必须先查清再付款，否则就是多付或少付。
 *
 * 与已有能力的区别（不是重复品）：
 *   · `bank-reconciliation` 核的是「银行流水 ↔ 企业账面」；
 *   · `three-way-match` 核的是「采购订单 / 入库单 / 发票」三单；
 *   · 本能力核的是「**我方应付台账 ↔ 供应商对账单**」—— 材料是对方发来的对账金额，判据是差异清单。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（与其它引擎一致）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *
 * 刻意不做的事：不联网、不调用大模型；材料不足不给结论；不判断该不该付款、不核合同价格。
 */
'use strict';

const CHECKS_GIVEN = [
  '逐家期末应付勾稽（期初应付 + 本期采购 − 本期付款 = 期末应付）',
  '逐家差异复核（我方期末应付 − 对方对账金额 = 差异）',
  '差异不为零的供应商清单（对账要跟进的就是这几家）',
  '合计行复核（每一列的合计是否等于各供应商之和）',
  '重复供应商检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '付款方向异常（本期付款 > 期初应付 + 本期采购）',
  '差异率超阈值提示（|差异| ÷ 期末应付，默认阈值 1%）',
  '期初应付为负（异常余额）检测',
  '本期无采购无付款但有余额（长期挂账供应商）',
];

const OUT_OF_SCOPE = [
  '判断该不该给某家供应商付款、付款优先级（那是资金计划与审批的事）',
  '核对采购合同价格、订单条款是否被违反（那要拿合同与订单来比）',
  '判断对方对账单本身是否真实（本工具只按你贴进来的数算）',
  '给出审计、税务或法律意见',
  '读取 .xlsx / PDF（需要你先从系统导出、复制成文本贴进来）',
];

/* 干净样例：三家都严丝合缝，差异全 0（干净样例必须零发现）。
   甲：100000 + 50000 − 30000 = 120000，对方也是 120000 → 差异 0
   乙：50000 + 20000 − 60000 = 10000，对方也是 10000 → 差异 0
   丙：0 + 80000 − 30000 = 50000，对方也是 50000 → 差异 0 */
const SAMPLE_TEXT = [
  '供应商\t期初应付\t本期采购\t本期付款\t期末应付\t对方对账金额\t差异',
  '甲物资有限公司\t100000.00\t50000.00\t30000.00\t120000.00\t120000.00\t0.00',
  '乙建材有限公司\t50000.00\t20000.00\t60000.00\t10000.00\t10000.00\t0.00',
  '丙设备有限公司\t0.00\t80000.00\t30000.00\t50000.00\t50000.00\t0.00',
  '合计\t150000.00\t150000.00\t120000.00\t180000.00\t180000.00\t0.00',
].join('\n');

const DIFF_RATIO_THRESHOLD = 0.01;
const AMOUNT_TOLERANCE = 0.01;

const ROLE_LABELS = {
  name: '供应商', code: '供应商编码', opening: '期初应付', purchase: '本期采购',
  payment: '本期付款', closing: '期末应付', theirs: '对方对账金额', diff: '差异',
};
const labelOf = (r) => ROLE_LABELS[r] || r;
const MONEY_ROLES = ['opening', 'purchase', 'payment', 'closing', 'theirs', 'diff'];

const COLUMN_ROLES = [
  [/供应商编码|供应商代码|往来编码/, 'code'],
  [/供应商|往来单位|单位名称|公司名称/, 'name'],
  [/期初应付|期初余额|上期期末|期初数/, 'opening'],
  [/本期采购|本期发生|采购金额|本期应付|借方发生/, 'purchase'],
  [/本期付款|本期支付|已付款|付款金额|贷方发生/, 'payment'],
  [/期末应付|期末余额|应付余额|期末数/, 'closing'],
  [/对方对账金额|对方金额|供应商对账|对账单金额|对方余额/, 'theirs'],
  [/差异|差额/, 'diff'],
];

const NON_AMOUNT_KWS = /备注|状态|日期|月份|账期|信用期|联系人|电话|发票号/;

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t');
  if (line.indexOf(',') >= 0) return line.split(',');
  return line.trim().split(/\s{2,}|\s+/);
}

function roleOf(header) {
  const h = String(header || '').replace(/\s/g, '');
  if (!h) return 'skip';
  if (NON_AMOUNT_KWS.test(h)) return 'skip';
  for (const pair of COLUMN_ROLES) if (pair[0].test(h)) return pair[1];
  return 'extra';
}

function normAmount(v) {
  if (v === null || v === undefined) return null;
  let s = String(v).trim();
  if (!s) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  s = s.replace(/[¥￥,\s]/g, '').replace(/元$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  return neg ? -n : n;
}

function isBlank(v) {
  const s = String(v === null || v === undefined ? '' : v).trim();
  if (!s) return true;
  return /^(--+|\?\?+|N\/?A|na|待填|TODO|xxx|\*\*\*?)$/i.test(s);
}

function findHeader(lines) {
  for (let i = 0; i < Math.min(lines.length, 10); i += 1) {
    const cells = splitRow(lines[i]).map((c) => c.trim());
    const roles = cells.map(roleOf);
    const known = roles.filter((r) => r !== 'skip' && r !== 'extra');
    const hasKey = known.includes('name') || known.includes('code');
    const money = MONEY_ROLES.filter((r) => known.includes(r)).length;
    if (hasKey && money >= 3) return { index: i, cells, roles };
  }
  return null;
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/);
  const header = findHeader(lines);
  if (!header) return { error: 'no_header' };
  const rows = [];
  const totals = [];
  for (let i = header.index + 1; i < lines.length; i += 1) {
    const raw = lines[i];
    if (!raw || !raw.trim()) continue;
    const cells = splitRow(raw).map((c) => c.trim());
    const rec = { line: i + 1, raw: raw.trim(), byRole: {} };
    header.roles.forEach((role, ci) => {
      if (role === 'skip' || role === 'extra') return;
      rec.byRole[role] = cells[ci] === undefined ? '' : cells[ci];
    });
    const nm = String(rec.byRole.name || rec.byRole.code || '').trim();
    if (/^(合计|总计|小计|total)/i.test(nm)) totals.push(rec); else rows.push(rec);
  }
  return { header, items: rows, totals, cols: header.cells };
}

function finding(level, category, line, message, evidence, advice) {
  return { level, category, line, message, evidence, advice };
}

const tag = (rec) => String(rec.byRole.name || rec.byRole.code || '（未命名供应商）').trim();

function checkClosing(rec) {
  const o = normAmount(rec.byRole.opening);
  const p = normAmount(rec.byRole.purchase);
  const pay = normAmount(rec.byRole.payment);
  const c = normAmount(rec.byRole.closing);
  if (o === null || p === null || pay === null || c === null) return null;
  const expect = Math.round((o + p - pay) * 100) / 100;
  if (Math.abs(expect - c) <= AMOUNT_TOLERANCE) return null;
  return finding('P0', '期末应付不平', rec.line,
    tag(rec) + ' 的期末应付是 ' + c.toFixed(2) + '，但「期初 ' + o.toFixed(2) + ' + 本期采购 '
      + p.toFixed(2) + ' − 本期付款 ' + pay.toFixed(2) + '」应为 ' + expect.toFixed(2)
      + '（差 ' + (c - expect).toFixed(2) + '）',
    rec.raw, '先确认口径：如果有退货折让、预付冲抵、暂估调整，请把它们也列成一列再核。');
}

function checkDiff(rec) {
  const c = normAmount(rec.byRole.closing);
  const t = normAmount(rec.byRole.theirs);
  const d = normAmount(rec.byRole.diff);
  if (c === null || t === null || d === null) return null;
  const expect = Math.round((c - t) * 100) / 100;
  if (Math.abs(expect - d) <= AMOUNT_TOLERANCE) return null;
  return finding('P0', '差异不等于我方减对方', rec.line,
    tag(rec) + ' 的差异是 ' + d.toFixed(2) + '，但「我方期末 ' + c.toFixed(2) + ' − 对方 '
      + t.toFixed(2) + '」应为 ' + expect.toFixed(2) + '（差 ' + (d - expect).toFixed(2) + '）',
    rec.raw, '差异列算错会让真正对不上的供应商被漏掉。');
}

/** 核心产出：差异不为零的供应商。这不是"错误"，而是**对账要跟进的对象**。 */
function checkUnmatched(rec) {
  const c = normAmount(rec.byRole.closing);
  const t = normAmount(rec.byRole.theirs);
  if (c === null || t === null) return null;
  const d = Math.round((c - t) * 100) / 100;
  if (Math.abs(d) <= AMOUNT_TOLERANCE) return null;
  const side = d > 0 ? '我方比对方多' : '我方比对方少';
  return finding('P1', '与对方对不上', rec.line,
    tag(rec) + '：我方期末应付 ' + c.toFixed(2) + '，对方对账金额 ' + t.toFixed(2)
      + '，差异 ' + d.toFixed(2) + '（' + side + '）',
    rec.raw, '对不上的必须先查清再付款。常见原因：在途发票未入账、退货未冲、'
      + '我方已付对方未核销、或对方把别的合同也算进来了。');
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals.length) return out;
  const t = totals[0];
  for (const role of MONEY_ROLES) {
    const claimed = normAmount(t.byRole[role]);
    if (claimed === null) continue;
    let sum = 0;
    let ok = true;
    for (const it of items) {
      const n = normAmount(it.byRole[role]);
      if (n === null) { ok = false; break; }
      sum += n;
    }
    if (!ok) continue;
    sum = Math.round(sum * 100) / 100;
    if (Math.abs(sum - claimed) <= AMOUNT_TOLERANCE) continue;
    out.push(finding('P0', '合计行算错', t.line,
      '合计行的「' + labelOf(role) + '」写的是 ' + claimed.toFixed(2) + '，但各供应商相加是 '
        + sum.toFixed(2) + '（差 ' + (claimed - sum).toFixed(2) + '）',
      t.raw, '合计行常是从系统导出后手工改过，改了一处忘了另一处。'));
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.code || it.byRole.name || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push(finding('P0', '同一供应商出现两行', it.line,
        key + ' 出现了两次（上一次在第 ' + seen.get(key) + ' 行）',
        it.raw, '同一供应商两行会让应付余额和对账差异都算错，请先合并。'));
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  const roles = Object.keys(items[0] ? items[0].byRole : {})
    .filter((r) => r !== 'name' && r !== 'code');
  for (const it of items) {
    if (!String(it.byRole.name || it.byRole.code || '').trim()) {
      out.push(finding('P0', '供应商无名称也无编码', it.line, '这一行认不出是哪家供应商', it.raw,
        '请确认这一行是否有效。'));
      continue;
    }
    for (const r of roles) {
      const v = it.byRole[r];
      if (isBlank(v)) {
        out.push(finding('P1', '该填没填', it.line,
          tag(it) + ' 的「' + labelOf(r) + '」是空的或还是占位符（' + (String(v).trim() || '空') + '）',
          it.raw, '对账表出现空列，通常是从系统导出时漏选，或对方对账单没导全。'));
      } else if (normAmount(v) === null) {
        out.push(finding('P1', '金额无法解析', it.line,
          tag(it) + ' 的「' + labelOf(r) + '」写作「' + String(v).trim() + '」，不是能计算的金额',
          it.raw, '请确认列是否串位。'));
      }
    }
  }
  return out;
}

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['供应商对账表原文（text）']);
  const t = parseTable(text);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的对账表（要能认出「供应商」+ 至少三个金额列，例如「期末应付」「对方对账金额」）',
      '从系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一家供应商的明细行']);

  const threshold = payload && typeof payload.diffRatio === 'number'
    ? payload.diffRatio : DIFF_RATIO_THRESHOLD;

  const findings = [];
  const notRun = [];
  const unmatched = [];
  for (const it of t.items) {
    const a = checkClosing(it); if (a) findings.push(a);
    const b = checkDiff(it); if (b) findings.push(b);
    const u = checkUnmatched(it);
    if (u) { findings.push(u); unmatched.push({ name: tag(it), line: it.line }); }

  }
  for (const f of checkTotalRow(t.totals, t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const sumOf = (role) => Math.round(t.items.reduce((s, it) => {
    const n = normAmount(it.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0) * 100) / 100;
  const closingTotal = sumOf('closing');
  const diffTotal = sumOf('diff');
  const ratio = closingTotal > 0 ? Math.abs(diffTotal) / closingTotal : 0;


  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const result = {
    findings,
    summary: {
      suppliers: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      closing_total: closingTotal,
      diff_total: diffTotal,
      diff_ratio: Math.round(ratio * 10000) / 10000,
      unmatched_count: unmatched.length,
      basis: '逐家「期初+采购−付款=期末」与「我方期末−对方金额=差异」比对；差异不为零的单独列出',
    },
    unmatched,
    columns: t.cols,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明这几家的数**算得对、也对得上**，'
      + '不代表对方对账单本身真实、也不代表该不该付款 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normAmount, isBlank, labelOf, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, ROLE_LABELS, MONEY_ROLES, DIFF_RATIO_THRESHOLD,
};
