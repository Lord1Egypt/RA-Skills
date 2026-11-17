#!/usr/bin/env node
/**
 * tuition-refund-check.js —— 学费与退费核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**教培机构每天都在处理退费**，而退费金额最容易吵起来：
 *   ① 已耗课费   = 已上课时 × 课时单价
 *   ② 应退学费   = 已缴学费 − 已耗课费
 *   ③ 差额       = 应退学费 − 实退学费（**正数=还欠学员**，这类差额最后往往变成投诉与投诉监管）
 * 争议点几乎都在这两处：**课时单价按"折扣价"还是"原价"**、**已耗课时算到哪一天**。
 * 学员一多，人眼核不动；而这些全是**纯算术**。
 *
 * 与已有能力的区别：`lesson-hour-check` 核的是**课时核销台账**（销课与剩余课时是否对得上）；
 * 本能力核的是**退费金额**（已耗课费 → 应退 → 实退 → 差额），环节不同。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不判合同条款、不调用大模型；材料不足不给结论；不给法律意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '已耗课费勾稽（已上课时 × 课时单价）',
  '应退学费勾稽（已缴学费 − 已耗课费）',
  '差额勾稽（应退学费 − 实退学费）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复学员检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '已上课时超过总课时检测（超上，需按合同另议）',
  '已耗课费超过已缴学费检测',
  '应退学费为负检测',
  '差额绝对值超过给定阈值检测（阈值由入参 tolerance 给出；未给出则本项不执行）',
  '课时单价或总课时非正检测',
];

const OUT_OF_SCOPE = [
  '判断退费条款（按折扣价还是原价折算、是否收违约金）是否合法或合理',
  '处理赠课、优惠券、转班与转校',
  '处理跨期收入确认与开票红冲',
  '判断是否涉及预付费监管要求；给出法律意见',
  '读取 .xlsx 或教务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '学员\t已缴学费\t已上课时\t总课时\t课时单价\t已耗课费\t应退学费\t实退学费\t差额',
  '甲同学\t12000.00\t30\t60\t200.00\t6000.00\t6000.00\t6000.00\t0.00',
  '乙同学\t8000.00\t20\t40\t200.00\t4000.00\t4000.00\t4000.00\t0.00',
  '合计\t20000.00\t50\t100\t\t10000.00\t10000.00\t10000.00\t0.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  party: ['学员', '学生', '姓名'],
  paid: ['已缴学费', '已缴金额', '实缴学费'],
  usedHours: ['已上课时', '已耗课时', '已上课'],
  totalHours: ['总课时', '购买课时', '总课次'],
  unitPrice: ['课时单价', '单价'],
  costUsed: ['已耗课费', '已消耗金额', '已耗学费'],
  refundable: ['应退学费', '应退金额'],
  refunded: ['实退学费', '已退金额'],
  diff: ['差额', '差异'],
};

const LABELS = {
  party: '学员', paid: '已缴学费', usedHours: '已上课时', totalHours: '总课时', unitPrice: '课时单价',
  costUsed: '已耗课费', refundable: '应退学费', refunded: '实退学费', diff: '差额',
};

const REQUIRED = ['party', 'paid', 'usedHours', 'totalHours', 'unitPrice', 'costUsed', 'refundable', 'refunded', 'diff'];
const SUM_ROLES = ['paid', 'usedHours', 'totalHours', 'costUsed', 'refundable', 'refunded', 'diff'];

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  // ⚠️ 顺序即优先级（更具体在前）：「已缴学费」要排在「应退学费/实退学费」的宽泛别名之前；
  //    「已耗课费」不能被「已上课时」抢；「总课时」与「已上课时」互不包含。
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
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {} };
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
const who = (it) => `学员「${it.byRole.party || '(未命名)'}」`;

function checkCostUsed(it) {
  const hours = num(it, 'usedHours'); const unit = num(it, 'unitPrice'); const stated = num(it, 'costUsed');
  if (hours === null || unit === null || stated === null) return null;
  const expect = round2(hours * unit);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '已耗课费与复算不符', line: it.line,
    message: `${who(it)}的已耗课费是 ${stated.toFixed(2)}，按 已上课时 ${hours} × 课时单价 ${unit} 应为 ${expect.toFixed(2)}。`,
    advice: '**课时单价口径是退费争议的第一现场**：按折扣后的实收单价，还是按课程原价？'
      + '本工具按表里给出的"课时单价"复算，口径必须与合同/协议一致。',
  };
}

function checkRefundable(it) {
  const paidAmt = num(it, 'paid'); const cost = num(it, 'costUsed'); const stated = num(it, 'refundable');
  if (paidAmt === null || cost === null || stated === null) return null;
  const expect = round2(paidAmt - cost);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应退学费与复算不符', line: it.line,
    message: `${who(it)}的应退学费是 ${stated.toFixed(2)}，按 已缴学费 ${paidAmt.toFixed(2)} − 已耗课费 ${cost.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '应退 = 已缴 − 已耗；若还要扣违约金/手续费，应在本表显式列示，不要悄悄并进已耗课费。',
  };
}

function checkDiff(it) {
  const refundable = num(it, 'refundable'); const refunded = num(it, 'refunded'); const stated = num(it, 'diff');
  if (refundable === null || refunded === null || stated === null) return null;
  const expect = round2(refundable - refunded);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '差额与复算不符', line: it.line,
    message: `${who(it)}的差额是 ${stated.toFixed(2)}，按 应退学费 ${refundable.toFixed(2)} − 实退学费 ${refunded.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '差额 = 应退 − 实退；**正数表示还欠学员**，这类余额不清会直接变成投诉。',
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
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '注意：**课时单价是单价，不能按行相加**（合计行里应为空）。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.party || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一学员出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一学员多笔报名分行是正常的；但若本表按学员汇总，重复行会让已缴与应退一起翻倍。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔退费就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
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
      '含表头的退费核对表（要能认出「已缴学费」「已上课时」「总课时」「课时单价」'
      + '「已耗课费」「应退学费」「实退学费」「差额」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从教务系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一名学员的明细行']);

  const tolParam = normNumber(payload && payload.tolerance);
  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkCostUsed(it); if (a) findings.push(a);
    const b = checkRefundable(it); if (b) findings.push(b);
    const c = checkDiff(it); if (c) findings.push(c);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const owed = t.items.filter((it) => {
    const v = num(it, 'diff');
    return v !== null && v > TOL;
  }).length;

  const result = {
    findings,
    summary: {
      students: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      paid_total: sumOf('paid'),
      cost_used_total: sumOf('costUsed'),
      refundable_total: sumOf('refundable'),
      refunded_total: sumOf('refunded'),
      diff_total: sumOf('diff'),
      students_owed: owed,
      basis: '已耗课费 = 已上课时 × 课时单价；应退学费 = 已缴学费 − 已耗课费；'
        + '差额 = 应退学费 − 实退学费（正数=还欠学员）；合计行逐列复核。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表退费条款合法、也不代表课时记录真实 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
