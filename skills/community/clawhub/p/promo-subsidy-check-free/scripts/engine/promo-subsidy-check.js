#!/usr/bin/env node
/**
 * promo-subsidy-check.js —— 促销补贴与核销核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**做零售/电商的每个活动结束后都要核一遍补贴**（品牌方给补贴、平台给补贴、自己给渠道补贴）：
 *   ① 应结补贴 = 实际销量 × 单件补贴
 *   ② 封顶：应结补贴不得高于活动封顶金额（**封顶这一条最容易被忽略**）
 *   ③ 差异   = 应结补贴 − 已结补贴（**正数=还没结到**）
 * 销量口径（含不含退货）、单件补贴（阶梯/分档）、封顶与"满减叠加" —— 每一项都能差出几万；
 * 一个活动几十个 SKU，人眼核不动；而这些全是**纯算术**。
 *
 * 与已有能力的区别：`platform-settlement-check` 核**平台结算单**（成交/退款/技术服务费）；
 * `purchase-rebate-check` 核**采购返利**；本能力核的是**促销补贴的应结与核销**（按销量计提 + 封顶）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查活动方案、不调用大模型；材料不足不给结论；不给税务意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '应结补贴勾稽（实际销量 × 单件补贴）',
  '差异勾稽（应结补贴 − 已结补贴）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复行检测（同一 SKU/活动出现两次）',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '封顶校验（应结补贴不得超过活动封顶金额）',
  '单件补贴大于售价检测（补贴高于售价，通常是政策或数据填错）',
  '实际销量为负检测（退货冲销应单列）',
  '已结补贴为负检测',
  '差异超过阈值检测（阈值由入参 tolerance 给出，默认 0.01 元；正数=尚未结到）',
];

const OUT_OF_SCOPE = [
  '判断活动方案、补贴政策是否合理（那要看活动申请与批复文件）',
  '处理阶梯补贴、满减叠加、平台与品牌分摊比例（请先把"单件补贴"算成等效值再填）',
  '核对销量本身的真实性（那要与订单/退货明细比对）',
  '判断补贴的税务处理（是否冲减收入、是否需开票）',
  '读取 .xlsx 或活动核销台账（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '活动\tSKU\t实际销量\t单件补贴\t应结补贴\t活动封顶\t已结补贴\t差异',
  '618大促\tA-100\t2000\t5.00\t10000.00\t20000.00\t10000.00\t0.00',
  '618大促\tB-200\t1500\t8.00\t12000.00\t20000.00\t12000.00\t0.00',
  '合计\t\t3500\t\t22000.00\t\t22000.00\t0.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级（更具体在前）：「活动封顶」必须排在「活动」之前，
  //    否则 `party` 的宽泛别名会把「活动封顶」整列抢走（发版前守卫第三次拦下这类错）。
  cap: ['活动封顶', '封顶金额', '封顶'],
  party: ['活动', '活动名称', '促销活动'],
  sku: ['SKU', '商品', '货号', '单品'],
  qty: ['实际销量', '销量', '核销量'],
  unit: ['单件补贴', '补贴单价', '每件补贴'],
  // 可选列：有「售价」时才能做"补贴高于售价"的判断（不放进 REQUIRED）
  price: ['售价', '商品售价'],
  payable: ['应结补贴', '应结金额', '应付补贴'],
  settled: ['已结补贴', '已结', '实结补贴'],
  diff: ['差异', '差额', '未结补贴'],
};

const LABELS = {
  party: '活动', sku: 'SKU', qty: '实际销量', unit: '单件补贴', payable: '应结补贴',
  cap: '活动封顶', settled: '已结补贴', diff: '差异', price: '售价',
};

const REQUIRED = ['party', 'sku', 'qty', 'unit', 'payable', 'cap', 'settled', 'diff'];
const SUM_ROLES = ['qty', 'payable', 'settled', 'diff'];

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
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库五次踩过的坑）：
  //    「活动封顶」要排在「活动」之前；「单件补贴」要排在「补贴」类之前；「应结补贴」不能被「已结补贴」抢。
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
const who = (it) => `「${it.byRole.party || '(未命名活动)'}／${it.byRole.sku || '(未命名SKU)'}」`;

function checkPayable(it) {
  const qty = num(it, 'qty'); const unit = num(it, 'unit'); const stated = num(it, 'payable');
  if (qty === null || unit === null || stated === null) return null;
  const expect = round2(qty * unit);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应结补贴与复算不符', line: it.line,
    message: `${who(it)}的应结补贴是 ${stated.toFixed(2)}，按 实际销量 ${qty} × 单件补贴 ${unit} 应为 ${expect.toFixed(2)}。`,
    advice: '销量口径要先对齐（**含不含退货**）；退货运费与冲销该不该计入销量，必须与活动方案一致。',
  };
}

function checkDiff(it) {
  const payable = num(it, 'payable'); const settled = num(it, 'settled'); const stated = num(it, 'diff');
  if (payable === null || settled === null || stated === null) return null;
  const expect = round2(payable - settled);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '差异与复算不符', line: it.line,
    message: `${who(it)}的差异是 ${stated.toFixed(2)}，按 应结补贴 ${payable.toFixed(2)} − 已结补贴 ${settled.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '差异 = 应结 − 已结；**正数表示还没结到**，活动结束后要据此向品牌方/平台追。',
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
        advice: '注意：**单件补贴与活动封顶不能相加**（合计行里应为空），只有销量与金额类列才求和。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = `${String(it.byRole.party || '').trim()}||${String(it.byRole.sku || '').trim()}`;
    if (key === '||') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一活动+SKU 出现多行', line: it.line,
        message: `「${key.replace('||', '／')}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同活动同 SKU 重复行会让销量与补贴一起翻倍；若是分批核销，请加"批次"列区分。',
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
          advice: '缺这一格这笔补贴就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的促销补贴核销表（要能认出「活动」「SKU」「实际销量」「单件补贴」「应结补贴」'
      + '「活动封顶」「已结补贴」「差异」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从活动核销台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一行明细']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkPayable(it); if (a) findings.push(a);
    const b = checkDiff(it); if (b) findings.push(b);
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

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      qty_total: sumOf('qty'),
      payable_total: sumOf('payable'),
      settled_total: sumOf('settled'),
      diff_total: sumOf('diff'),
      basis: '应结补贴 = 实际销量 × 单件补贴（**且不得高于活动封顶**）；差异 = 应结补贴 − 已结补贴；'
        + '合计行逐列复核（单件补贴与封顶列不参与求和）。',
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
      + '不代表活动方案与销量口径判断正确 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
