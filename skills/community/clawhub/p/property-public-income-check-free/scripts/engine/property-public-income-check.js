#!/usr/bin/env node
/**
 * property-public-income-check.js —— 物业公共收益公示与分成核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**物业公司每季度公示前必须把公共收益台账算一遍**（业委会/街道每年审计也看这张表）。
 * 台账本身只有几条算式，但每一条都直接决定公示出去的数字对不对：
 *   ① 应分成业主金额 = 实收金额 × 业主分成比例（合同约定比例）
 *   ② 季度小计行 = 本季度各明细行之和；合计行 = 全部明细行之和（逐列）
 *   ③ 公示金额必须能与台账复算一致（否则就是"公示数与台账不符"）
 *   ④ 约定要转存公共维修资金的，公示前必须真的转存；已到期合同不能只有合同金额没有实收
 * 电梯/道闸广告、场地租赁、快递柜、临时停车这些收益笔数多、比例不一、跨季重复，
 * 人眼算一遍极易错，而错一次就是业主投诉 + 监管处罚的高发点。
 *
 * 与已有能力的区别：`lease-rent-check` 核的是**租赁合同的租金与欠租**（单一合同口径）；
 * 本能力核的是**小区公共收益按季公示口径**（分成、公示、维修资金转存、欠收），
 * 输入是一张"合同号 × 季度"的收益台账，输出是"公示前必须处理清单"。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查地方物业管理条例、不调用大模型；材料不足不给结论；不给法律/审计意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '应分成业主金额复算（实收金额 × 业主分成比例）',
  '按季汇总勾稽（季度小计行 = 本季度各明细行之和）',
  '合计行逐列复核（合同金额、实收金额、应分成业主金额、公示金额）',
  '同一合同号在同一季度重复登记检测',
  '关键字段空缺与占位符检测',
  '业主分成比例不在 0~1 的检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '公示合规判定：公示金额与台账差额归因（漏登实收 / 分成比例用错 / 跨期计入）',
  '公共维修资金转存核对（应转存未转存 / 已转存超过应转存）',
  '欠收检测（合同金额已到期未收足）',
  '公示前必须处理清单（按影响金额排序，逐条带原文行号）',
];

const OUT_OF_SCOPE = [
  '判断合同约定的分成比例本身是否合法：分成比例以你提供的合同约定为准，不判断地方物业管理条例的适用性与比例下限',
  '推算公共维修资金应转存比例：按台账给出的「应转存维修资金」认定，不替你算地方规定比例',
  '判断合同到期日的算法与法律效力：按台账给出的「到期状态」认定，不推算账龄、也不判断诉讼时效',
  '给法律或审计意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '合同号\t收益项目\t所属季度\t合同金额\t实收金额\t业主分成比例\t应分成业主金额\t公示金额\t应转存维修资金\t已转存维修资金\t到期状态',
  'HT-2026-A01\t电梯广告\t2026Q1\t60000.00\t60000.00\t0.70\t42000.00\t42000.00\t16800.00\t16800.00\t已到期',
  'HT-2026-B02\t道闸广告\t2026Q1\t24000.00\t24000.00\t0.70\t16800.00\t16800.00\t6720.00\t6720.00\t已到期',
  'HT-2026-C03\t快递柜场地\t2026Q1\t12000.00\t12000.00\t50%\t6000.00\t6000.00\t2400.00\t2400.00\t已到期',
  'HT-2026-D04\t临时停车\t2026Q1\t8000.00\t8000.00\t0.50\t4000.00\t4000.00\t1600.00\t1600.00\t已到期',
  '季度小计\t\t2026Q1\t104000.00\t104000.00\t\t68800.00\t68800.00\t27520.00\t27520.00\t',
  'HT-2026-A01\t电梯广告\t2026Q2\t60000.00\t60000.00\t0.70\t42000.00\t42000.00\t16800.00\t16800.00\t已到期',
  'HT-2026-E05\t场地租赁\t2026Q2\t30000.00\t30000.00\t0.60\t18000.00\t18000.00\t7200.00\t7200.00\t已到期',
  'HT-2026-F06\t道闸广告\t2026Q2\t18000.00\t18000.00\t0.70\t12600.00\t12600.00\t5040.00\t5040.00\t已到期',
  '季度小计\t\t2026Q2\t108000.00\t108000.00\t\t72600.00\t72600.00\t29040.00\t29040.00\t',
  '合计\t\t\t212000.00\t212000.00\t\t141400.00\t141400.00\t56560.00\t56560.00\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  contract: ['合同号', '合同编号', '合同编码'],
  item: ['收益项目', '项目名称', '收益类型', '广告位', '项目'],
  quarter: ['所属季度', '季度', '所属期'],
  contractAmt: ['合同金额', '合同总额', '合同应收'],
  received: ['实收金额', '实收', '已收金额', '已收账款'],
  ownerRate: ['业主分成比例', '分成比例', '业主比例', '分成率'],
  ownerShare: ['应分成业主金额', '应分成金额', '应分给业主金额', '业主分成金额'],
  publicized: ['公示金额', '公示的收入金额', '公示收益金额'],
  fundDue: ['应转存维修资金', '应转存维修基金', '应转存金额', '应转存'],
  fundPaid: ['已转存维修资金', '已转存维修基金', '已转存金额', '已转存'],
  dueStatus: ['到期状态', '应收状态', '是否到期'],
};

const LABELS = {
  contract: '合同号', item: '收益项目', quarter: '所属季度', contractAmt: '合同金额',
  received: '实收金额', ownerRate: '业主分成比例', ownerShare: '应分成业主金额',
  publicized: '公示金额', fundDue: '应转存维修资金', fundPaid: '已转存维修资金',
  dueStatus: '到期状态',
};

const REQUIRED = ['contract', 'item', 'quarter', 'contractAmt', 'received', 'ownerRate', 'ownerShare', 'publicized'];
const SUM_ROLES = ['contractAmt', 'received', 'ownerShare', 'publicized'];
const AMOUNT_ROLES = ['contractAmt', 'received', 'ownerShare', 'publicized', 'fundDue', 'fundPaid'];
const OPTIONAL_ROLES = ['fundDue', 'fundPaid', 'dueStatus'];
const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

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
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库踩过两次的坑，见 tools/header_map_check.py）：
  //    「业主分成比例」必须排在「应分成业主金额」之前，否则比例列会被分成金额抢走；
  //    「应转存维修资金」必须排在「已转存维修资金」之前，否则一列被另一列覆盖（算错但不报缺列）。
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

/** 比例：`0.7` 与 `70%` 都认；**不带百分号的 70 按 70 处理**（会被"比例不在 0~1"报出来，不猜）。 */
function normRate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s]/g, '');
  const isPct = /%$/.test(s);
  const n = Number(s.replace(/%$/, ''));
  if (!Number.isFinite(n)) return null;
  return isPct ? n / 100 : n;
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
  const subtotals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const first = String(cells[0] || '').trim();
    if (/^(合计|总计|total)/i.test(first)) {
      row.isTotal = true; totals.push(row);
    } else if (/^(季度小计|本季小计|季小计|小计)/.test(first)) {
      row.isSubtotal = true; subtotals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals, subtotals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const rateOf = (it) => normRate(it.byRole.ownerRate);
const who = (it) => {
  const c = String(it.byRole.contract === undefined ? '' : it.byRole.contract).trim() || '(未填合同号)';
  const q = String(it.byRole.quarter === undefined ? '' : it.byRole.quarter).trim();
  const n = String(it.byRole.item === undefined ? '' : it.byRole.item).trim();
  const tail = [q, n].filter(Boolean).join(' / ');
  return `合同「${c}」` + (tail ? `（${tail}）` : '');
};

function checkOwnerShare(it) {
  const received = num(it, 'received');
  const rate = rateOf(it);
  const stated = num(it, 'ownerShare');
  if (received === null || rate === null || stated === null) return null;
  const expect = round2(received * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应分成业主金额与复算不符', line: it.line,
    message: `${who(it)}的应分成业主金额是 ${stated.toFixed(2)}，`
      + `按 实收金额 ${received.toFixed(2)} × 业主分成比例 ${rate} 应为 ${expect.toFixed(2)}。`,
    advice: '分成金额必须能由「实收金额 × 合同约定比例」复算出来；比例填错或实收没更新都会在这里露出来。',
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
        advice: '要么明细行漏了合同/季度，要么合计行没跟着更新；对外公示的总数就是这一行。',
      });
    }
  }
  return out;
}

function checkQuarterSubtotal(subtotals, items) {
  const out = [];
  for (const t of subtotals) {
    const q = String(t.byRole.quarter === undefined ? '' : t.byRole.quarter).trim();
    if (!q) continue;
    const rows = items.filter((it) => String(it.byRole.quarter === undefined ? '' : it.byRole.quarter).trim() === q);
    if (!rows.length) continue;
    for (const role of SUM_ROLES) {
      const stated = num(t, role);
      if (stated === null) continue;
      const sum = round2(rows.reduce((s, it) => {
        const n = num(it, role);
        return s + (n === null ? 0 : n);
      }, 0));
      if (Math.abs(sum - stated) > TOL) {
        out.push({
          level: 'P0', category: '季度小计行与季度明细之和不符', line: t.line,
          message: `「${q}」季度小计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，该季度 ${rows.length} 行明细相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
          advice: '按季公示的数字来自这条小计行；小计与明细不符时，公示出去的季度汇总就是错的。',
        });
      }
    }
  }
  return out;
}

function checkDuplicateContracts(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const c = String(it.byRole.contract === undefined ? '' : it.byRole.contract).trim();
    const q = String(it.byRole.quarter === undefined ? '' : it.byRole.quarter).trim();
    if (!c || !q) continue;
    const key = c + '|' + q;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一合同号在同一季度重复登记', line: it.line,
        message: `合同「${c}」在 ${q} 第 ${seen.get(key)} 行已登记过，第 ${it.line} 行再次出现。`,
        advice: '同一笔收益登记两次会让实收与公示金额一起翻倍；若确实是两份合同，请分别给合同号（或注明分广告位/分点位）。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

function checkBlanks(items, roles) {
  const out = [];
  for (const it of items) {
    for (const role of roles) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔收益就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

function checkNegative(items, roles) {
  const out = [];
  for (const it of items) {
    for (const role of roles) {
      const v = num(it, role);
      if (v !== null && v < -TOL) {
        out.push({
          level: 'P0', category: '金额为负', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}。`,
          advice: '公共收益的合同额、实收、分成、公示与转存金额都不该为负；红字冲销请单列一行并注明原因。',
        });
      }
    }
  }
  return out;
}

function checkRateRange(items) {
  const out = [];
  for (const it of items) {
    const rate = rateOf(it);
    if (rate === null) continue;
    if (rate < 0 || rate > 1) {
      out.push({
        level: 'P0', category: '业主分成比例不在 0~1', line: it.line,
        message: `${who(it)}的业主分成比例是 ${rate}，不在 0~1 之间。`,
        advice: '比例请写成 0.7 或 70% 两种形式之一；写成 70 会被当成 70 倍，分成金额当场算错。',
      });
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
      '含表头的小区公共收益台账（要能认出「合同号」「收益项目」「所属季度」「合同金额」'
      + '「实收金额」「业主分成比例」「应分成业主金额」「公示金额」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从 Excel 把表头和数据行一起复制成文本贴进来（Tab 分隔最稳；季度小计行与合计行也一起带上）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一行收益明细（合同/项目行），而不是只有表头或只有合计/小计行']);

  const presentRoles = t.cols.map((c) => c.role).filter(Boolean);
  const blankRoles = REQUIRED.concat(OPTIONAL_ROLES).filter((r) => presentRoles.indexOf(r) >= 0);
  const amountRoles = AMOUNT_ROLES.filter((r) => presentRoles.indexOf(r) >= 0);
  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkOwnerShare(it); if (a) findings.push(a);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkQuarterSubtotal(t.subtotals, t.items)) findings.push(f);
  for (const f of checkDuplicateContracts(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items, blankRoles)) findings.push(f);
  for (const f of checkRateRange(t.items)) findings.push(f);
  for (const f of checkNegative(t.items, amountRoles)) findings.push(f);

  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const scope = {
    material: '小区公共收益台账（合同号 / 收益项目 / 所属季度 / 合同金额 / 实收金额 / 业主分成比例 / 应分成业主金额 / 公示金额 / 应转存维修资金 / 已转存维修资金 / 到期状态）',
    rows: t.items.length,
    checks_not_run: notRun,
    contract_total: sumOf('contractAmt'),
    paid_in_total: sumOf('received'),
    owner_share_total: sumOf('ownerShare'),
    publicized_total: sumOf('publicized'),
    basis: '应分成业主金额 = 实收金额 × 业主分成比例；季度小计行 = 本季度明细行之和；合计行 = 全部明细行之和；'
      + '公示金额应与台账口径（实收金额 × 业主分成比例）一致；应转存维修资金按台账给出的应转存金额认定。',
  };

  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  scope.checks_not_run = notRun;

  const result = {
    findings: findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      contract_total: sumOf('contractAmt'),
      received_total: sumOf('received'),
      owner_share_total: sumOf('ownerShare'),
      publicized_total: sumOf('publicized'),
      basis: scope.basis,
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    checks_not_run: notRun,
    scope: scope,
  };
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对**，'
      + '不代表分成比例、应转存比例或到期状态本身合规 —— 那些以你的合同与地方规定为准，不在本工具范围内。';
  }
  return { status: 'success', result: result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, normRate, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, REQUIRED, SUM_ROLES,
};
