#!/usr/bin/env node
/**
 * disability-fund-check-full.js —— 残疾人就业保障金申报核对引擎（完整档，确定性、纯 Node 标准库）。
 *
 * 真实痛点：**每年（部分地区按月或按季）都要申报缴纳残疾人就业保障金**，而这张表是三条串行算式：
 *   ① 应安排残疾人就业人数 = 上年在职职工人数 × 规定比例
 *   ② 应缴金额 = （应安排人数 − 实际安排人数）× 上年在职职工年平均工资（**负数按 0**）
 *   ③ 已缴金额与应缴金额的差异（多缴还是少缴）
 * 再叠上 30 人以下免征、分档减缴、残疾人证与一年以上劳动合同这些减免条件，
 * 算错一次就是多缴或漏缴，漏缴还有滞纳金 —— 纯算术，但口径一多，人眼极易错。
 *
 * 与已有能力的区别：本能力核的是**残保金申报表的口径与算术**（在职人数、年平均工资、
 * 安排比例、应缴与已缴、减免与申报处理清单）；不判残疾人证真伪、不判劳动合同有效性、
 * 不查各省政策参数 —— 政策参数一律由输入提供。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查政策文库、不调用大模型；材料不足不给结论；不给税务意见、不做筹划。
 */

'use strict';

const CHECKS_GIVEN = [
  '应安排残疾人就业人数勾稽（上年在职职工人数 × 规定比例）',
  '应缴金额勾稽（（应安排人数 − 实际安排人数）× 上年在职职工年平均工资，负数按 0）',
  '已缴金额与应缴金额差异勾稽（多缴 / 少缴）',
  '合计行逐列复核（每一列的合计是否等于各明细行之和）',
  '同一所属期重复行检测',
  '关键字段空缺与占位符检测',
];

const CHECKS_WITHHELD = [
  '免征条件判定（上年在职职工人数不超过输入给出的免征人数上限时，仍申报缴纳的部分）',
  '分档减缴档位与减缴金额核对（按输入给出的档位表算档位与减缴额）',
  '安排残疾人就业人数与残疾人证 / 一年以上劳动合同材料缺口',
  '上年在职职工人数与年平均工资口径复核（工资总额 ÷ 人数、与输入最低工资比较）',
  '多缴可退与少缴需补缴金额清单（按金额从大到小排）',
];

const OUT_OF_SCOPE = [
  '给出税务意见或做缴纳筹划（本工具只做口径一致的算术与清单）',
  '查证或套用任何地区政策参数（规定比例、免征人数上限、分档减缴档位、最低工资都由输入提供）',
  '判断残疾人证真伪、残疾人是否在岗、劳动合同是否有效（只管表内数字与材料数量是否对得上）',
  '处理按月 / 按季预缴的分期折算（请按所属期分行填列后再核对）',
  '读取 .xlsx（需要先把表头和明细复制成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期\t上年在职职工人数\t规定比例\t上年在职职工年平均工资\t应安排残疾人就业人数\t实际安排残疾人就业人数\t应缴金额\t已缴金额\t减免金额\t持证残疾人数\t一年以上劳动合同人数\t工资总额',
  '2024年度\t200\t1.5%\t120000.00\t3.00\t1.00\t240000.00\t240000.00\t0.00\t1\t1\t24000000.00',
  '2025年度\t220\t1.5%\t125000.00\t3.30\t2.00\t162500.00\t162500.00\t0.00\t2\t2\t27500000.00',
  '合计\t420\t\t\t6.30\t3.00\t402500.00\t402500.00\t0.00\t3\t3\t51500000.00',
].join('\n');

const TOL = 0.01;          // 金额容差：分
const RATIO_TOL = 1e-9;

const ROLES = {
  period: ['所属期', '所属年度', '期间', '年度', '年份'],
  // 「上年在职职工年平均工资」比「上年在职职工人数」更具体，必须排在前面：
  // 顺序错了宽泛别名会把更具体的列抢走，后果是**永远不给结论**（见 tools/header_map_check.py）。
  avgwage: ['上年在职职工年平均工资', '在职职工年平均工资', '上年在岗职工年平均工资', '年平均工资', '年均工资'],
  staff: ['上年在职职工人数', '在职职工人数', '在岗职工人数', '职工人数', '在职人数'],
  should: ['应安排残疾人就业人数', '应安排残疾人人数', '应安排人数'],
  actual: ['实际安排残疾人就业人数', '实际安排残疾人人数', '实际安排人数'],
  ratio: ['规定比例', '法定比例', '安排比例', '就业比例'],
  payable: ['应缴金额', '应缴残保金', '应缴纳金额', '应缴额'],
  paidamt: ['已缴金额', '已缴纳金额', '实缴金额', '已缴额'],
  relief: ['减免金额', '减缴金额', '减免额'],
  certcount: ['持证残疾人数', '残疾人证人数', '持证人数'],
  contractcount: ['一年以上劳动合同人数', '劳动合同人数', '签约人数'],
  wageref: ['上年工资总额', '工资总额'],
};

const LABELS = {
  period: '所属期', staff: '上年在职职工人数', ratio: '规定比例',
  avgwage: '上年在职职工年平均工资', should: '应安排残疾人就业人数',
  actual: '实际安排残疾人就业人数', payable: '应缴金额', paidamt: '已缴金额',
  relief: '减免金额', certcount: '持证残疾人数', contractcount: '一年以上劳动合同人数',
  wageref: '工资总额',
};

const REQUIRED = ['period', 'staff', 'ratio', 'avgwage', 'should', 'actual', 'payable', 'paidamt'];
const SUM_ROLES = ['staff', 'should', 'actual', 'payable', 'paidamt', 'relief', 'certcount', 'contractcount', 'wageref'];
const ROUNDING_MODES = ['none', 'round', 'ceil', 'floor'];

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值，更不会输出「未发现问题」。',
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

/**
 * 应安排人数的取整口径由输入给出（各地不同，引擎不写死）：
 *   none 不取整（默认） / round 四舍五入到人 / ceil 向上取整到人 / floor 向下取整到人
 */
function applyRounding(n, mode) {
  if (mode === 'ceil') return Math.ceil(n);
  if (mode === 'floor') return Math.floor(n);
  if (mode === 'round') return Math.round(n);
  return n;
}

function normRounding(v) {
  const s = String(v === undefined || v === null ? 'none' : v).trim().toLowerCase();
  return ROUNDING_MODES.indexOf(s) >= 0 ? s : 'none';
}

/**
 * 规定比例的口径归一：≤ 0.2 按小数比例（0.015 = 1.5%），否则按百分数（1.5 = 1.5%）。
 * 真实表里两种写法都出现过，写死一种就会把另一种整表判错 —— 所以两种都认，规则写进 basis。
 */
function ratioToPct(raw) {
  if (raw === null) return null;
  return raw <= 0.2 ? round2(raw * 100) : raw;
}

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
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `所属期「${it.byRole.period || '(未命名)'}」`;
const money = (n) => round2(n).toFixed(2);

/* ===== 免费档检查项：逐项复算，每一条都带原文行号 ===== */

function checkShould(it, rounding) {
  const staff = num(it, 'staff');
  const rawRatio = num(it, 'ratio');
  const stated = num(it, 'should');
  if (staff === null || rawRatio === null || stated === null) return null;
  const pct = ratioToPct(rawRatio);
  const expect = round2(applyRounding(staff * pct / 100, rounding));
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应安排残疾人就业人数与复算不符', line: it.line,
    message: `${who(it)}的应安排残疾人就业人数是 ${stated.toFixed(2)}，`
      + `按 上年在职职工人数 ${staff} × 规定比例 ${pct}% = ${round2(staff * pct / 100)}`
      + `${rounding === 'none' ? '' : `（按 ${rounding} 取整）`}，应为 ${expect.toFixed(2)}。`,
    advice: '应安排人数是下面应缴金额的乘数：这一格错，整行的应缴金额都跟着错。',
  };
}

function checkPayable(it) {
  const should = num(it, 'should');
  const actual = num(it, 'actual');
  const avgwage = num(it, 'avgwage');
  const stated = num(it, 'payable');
  if (should === null || actual === null || avgwage === null || stated === null) return null;
  const rawAmount = round2((should - actual) * avgwage);
  const expect = Math.max(0, rawAmount);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应缴金额与复算不符', line: it.line,
    message: `${who(it)}的应缴金额是 ${money(stated)}，按 （应安排人数 ${should.toFixed(2)} − 实际安排人数 ${actual.toFixed(2)}）`
      + ` × 上年在职职工年平均工资 ${money(avgwage)} = ${money(rawAmount)}`
      + `${rawAmount < 0 ? '（负值按 0 计）' : ''}，应为 ${money(expect)}。`,
    advice: '安排人数已达标时差额为负，应缴金额按 0 填（不是负数）。',
  };
}

function checkPaidDiff(it) {
  const payable = num(it, 'payable');
  const paidamt = num(it, 'paidamt');
  if (payable === null || paidamt === null) return null;
  const diff = round2(paidamt - payable);
  if (Math.abs(diff) <= TOL) return null;
  return {
    level: 'P1', category: '已缴与应缴金额不符', line: it.line,
    message: `${who(it)}的已缴金额是 ${money(paidamt)}，应缴金额是 ${money(payable)}，`
      + `相差 ${money(diff)}（${diff > 0 ? '已缴多于应缴' : '已缴少于应缴'}）。`,
    advice: diff > 0
      ? '已缴多于本表应缴的部分不会自己消失：先确认为什么多缴，再决定退还还是抵缴。'
      : '已缴少于应缴的部分属于未缴足：先确认是本表算错还是缴款漏记，别直接改数字平账。',
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
        message: `合计行的「${LABELS[role]}」是 ${money(stated)}，各明细行相加是 ${money(sum)}，相差 ${money(stated - sum)}。`,
        advice: '要么明细行漏了一个所属期，要么合计行没跟着更新。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.period || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一所属期出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一所属期分行列示是允许的（例如分部门），但那时要确认合计行没被重复统计一次。',
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
          advice: '缺这一格这一行的应缴金额就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的残疾人就业保障金申报表（要能认出「上年在职职工人数」「规定比例」'
      + '「上年在职职工年平均工资」「应安排残疾人就业人数」「实际安排残疾人就业人数」'
      + '「应缴金额」「已缴金额」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从申报底稿导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个所属期的明细行']);

  const rounding = normRounding(payload && payload.should_rounding);
  let actions = [];
  let paramsNeeded = [];

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkShould(it, rounding); if (a) findings.push(a);
    const b = checkPayable(it); if (b) findings.push(b);
    const c = checkPaidDiff(it); if (c) findings.push(c);
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
  const payableTotal = sumOf('payable');
  const paidTotal = sumOf('paidamt');
  const reliefTotal = sumOf('relief');
  const netDue = round2(payableTotal - reliefTotal);
  const diffTotal = round2(paidTotal - netDue);
  const actionAmount = round2(actions.reduce((s, x) => s + Math.abs(x.amount || 0), 0));

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      periods: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      action_count: actions.length,
      action_amount_total: actionAmount,
      should_total: sumOf('should'),
      actual_total: sumOf('actual'),
      payable_total: payableTotal,
      paid_total: paidTotal,
      relief_total: reliefTotal,
      payable_net_total: netDue,
      diff_total: diffTotal,
      basis: '应安排残疾人就业人数 = 上年在职职工人数 × 规定比例（取整口径由 should_rounding 给定，默认不取整；'
        + '规定比例 ≤ 0.2 按小数比例、否则按百分数）；'
        + '应缴金额 = （表内应安排人数 − 实际安排人数）× 上年在职职工年平均工资，负数按 0；'
        + '已缴与应缴按表内「应缴金额」列比较；合计行逐列复核；'
        + '减免与申报处理清单只在完整档产出（免征线、档位表、最低工资都由输入参数给定）。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    scope: {
      checks_run: CHECKS_GIVEN,
      checks_not_run: CHECKS_WITHHELD.slice(),
      checks_out_of_scope: OUT_OF_SCOPE,
      rounding: rounding,
      action_count: actions.length,
      paid_in_total: paidTotal,
      outstanding_total: diffTotal < 0 ? round2(-diffTotal) : 0,
      refundable_total: diffTotal > 0 ? diffTotal : 0,
    },
  };
  if (actions.length) result.actions = actions;
  if (paramsNeeded.length) result.params_needed = paramsNeeded;
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0 && actions.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表免征或分档减缴一定适用、也不代表残疾人证与劳动合同一定齐备 —— 那些要按你当地口径另行确认。';
  }
  if (paramsNeeded.length) {
    result.params_note = '以下政策参数没有给，所以对应的判定**没有执行**（本工具不套用任何地区的默认值）：'
      + paramsNeeded.join('；');
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, applyRounding, ratioToPct, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, REQUIRED, SUM_ROLES,
};
