#!/usr/bin/env node
/**
 * property-fee-check.js —— 物业费与滞纳金核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**物业公司/园区每月要出收费单，还要算欠费的滞纳金**：
 *   ① 应收物业费 = 计费面积 × 单价 × 计费月数
 *   ② 滞纳金     = 上期欠费 × 日费率 × 逾期天数（常见日万分之五）
 *   ③ 应缴合计   = 应收物业费 + 上期欠费 + 滞纳金
 * 面积口径（建筑面积/套内）、月数跨期、滞纳金日费率与天数 —— 每一项都能让业主投诉或让公司少收；
 * 几百上千户，人眼核不动；而这些都是**纯算术**。
 *
 * 与已有能力的区别：`utility-allocation-check` 核的是**公共费用按面积分摊给租户**（电费/水费）；
 * `lease-rent-check` 核的是**租金账单**；本能力核的是**物业费应收与滞纳金**（按面积×单价×月数 + 罚息）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查物业服务合同、不调用大模型；材料不足不给结论；不给法律意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '应收物业费勾稽（计费面积 × 单价 × 计费月数）',
  '滞纳金勾稽（上期欠费 × 日费率 × 逾期天数）',
  '应缴合计勾稽（应收物业费 + 上期欠费 + 滞纳金）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复客户/房号检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '滞纳金日费率超出 0~0.1% 检测',
  '逾期天数超出 0~1095 检测',
  '计费月数超出 0~12 检测',
  '计费面积非正 / 单价为负检测',
  '滞纳金超过上期欠费 100%（滚存过久）检测',
];

const OUT_OF_SCOPE = [
  '判断物业服务合同约定的单价、面积口径（建筑面积 or 套内）与滞纳金条款',
  '处理空置房减免、政府指导价与业主大会决议的优惠',
  '处理分期缴纳、预收与退款',
  '判断滞纳金是否超过法定上限（那是司法裁量与合同条款的事）',
  '读取 .xlsx 或收费系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '客户\t计费面积\t单价\t计费月数\t应收物业费\t上期欠费\t逾期天数\t滞纳金日费率\t滞纳金\t应缴合计',
  '甲公司\t500\t5.00\t3\t7500.00\t2000.00\t30\t0.05%\t30.00\t9530.00',
  '乙公司\t300\t4.00\t3\t3600.00\t0.00\t0\t0.05%\t0.00\t3600.00',
  '合计\t800\t\t6\t11100.00\t2000.00\t30\t\t30.00\t13130.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  party: ['客户', '房号', '业主', '房间'],
  area: ['计费面积', '建筑面积', '面积'],
  price: ['单价', '物业费单价'],
  months: ['计费月数', '月数', '计费月份'],
  fee: ['应收物业费', '物业费'],
  arrears: ['上期欠费', '欠费', '期初欠费'],
  days: ['逾期天数', '滞纳天数'],
  dayRate: ['滞纳金日费率', '日费率', '滞纳金费率'],
  lateFee: ['滞纳金', '违约金'],
  total: ['应缴合计', '应缴金额', '合计应缴'],
};

const LABELS = {
  party: '客户', area: '计费面积', price: '单价', months: '计费月数', fee: '应收物业费',
  arrears: '上期欠费', days: '逾期天数', dayRate: '滞纳金日费率', lateFee: '滞纳金', total: '应缴合计',
};

const REQUIRED = ['party', 'area', 'price', 'months', 'fee', 'arrears', 'days', 'dayRate', 'lateFee', 'total'];
const SUM_ROLES = ['area', 'months', 'fee', 'arrears', 'lateFee', 'total'];

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
  // ⚠️ 顺序即优先级（更具体在前）：「应收物业费」要排在「上期欠费」类之前；
  //    「滞纳金日费率」要排在「滞纳金」之前；「应缴合计」不能被「欠费」类抢走。
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
const who = (it) => `客户「${it.byRole.party || '(未命名)'}」`;

function checkFee(it) {
  const area = num(it, 'area'); const price = num(it, 'price'); const months = num(it, 'months');
  const stated = num(it, 'fee');
  if (area === null || price === null || months === null || stated === null) return null;
  const expect = round2(area * price * months);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应收物业费与复算不符', line: it.line,
    message: `${who(it)}的应收物业费是 ${stated.toFixed(2)}，按 面积 ${area} × 单价 ${price} × ${months} 个月 应为 ${expect.toFixed(2)}。`,
    advice: '面积口径（建筑面积/套内）与单价要在合同里对齐；**跨期月数是第二个易错点**。',
  };
}

function checkLateFee(it) {
  const arrears = num(it, 'arrears'); const rate = num(it, 'dayRate'); const days = num(it, 'days');
  const stated = num(it, 'lateFee');
  if (arrears === null || rate === null || days === null || stated === null) return null;
  const expect = round2(arrears * rate / 100 * days);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '滞纳金与复算不符', line: it.line,
    message: `${who(it)}的滞纳金是 ${stated.toFixed(2)}，`
      + `按 上期欠费 ${arrears.toFixed(2)} × 日费率 ${rate}% × ${days} 天 应为 ${expect.toFixed(2)}。`,
    advice: '滞纳金按**日费率 × 逾期天数**累计；日费率常见"日万分之五"=0.05%。'
      + '若合同是按月费率或年化写的，请先折算成日费率再填。',
  };
}

function checkTotal(it) {
  const fee = num(it, 'fee'); const arrears = num(it, 'arrears'); const late = num(it, 'lateFee');
  const stated = num(it, 'total');
  if (fee === null || arrears === null || late === null || stated === null) return null;
  const expect = round2(fee + arrears + late);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应缴合计与复算不符', line: it.line,
    message: `${who(it)}的应缴合计是 ${stated.toFixed(2)}，`
      + `按 应收物业费 ${fee.toFixed(2)} + 上期欠费 ${arrears.toFixed(2)} + 滞纳金 ${late.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '应缴合计 = 本期物业费 + 上期欠费 + 滞纳金；漏掉欠费或滞纳金都会让催收金额偏小。',
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
        advice: '注意：**单价与滞纳金日费率是比率/单价，不能按行相加**（合计行里应为空）。',
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
        level: 'P1', category: '同一客户出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一客户多个房号分行是正常的；但若本表按客户汇总，重复行会让面积与金额一起翻倍。',
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
          advice: '缺这一格这笔费用就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的物业费计算表（要能认出「计费面积」「单价」「计费月数」「应收物业费」'
      + '「上期欠费」「逾期天数」「滞纳金日费率」「滞纳金」「应缴合计」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从收费系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个客户的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkFee(it); if (a) findings.push(a);
    const b = checkLateFee(it); if (b) findings.push(b);
    const c = checkTotal(it); if (c) findings.push(c);
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
      customers: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      area_total: sumOf('area'),
      fee_total: sumOf('fee'),
      arrears_total: sumOf('arrears'),
      late_fee_total: sumOf('lateFee'),
      payable_total: sumOf('total'),
      basis: '应收物业费 = 计费面积 × 单价 × 计费月数；滞纳金 = 上期欠费 × 日费率 × 逾期天数；'
        + '应缴合计 = 应收物业费 + 上期欠费 + 滞纳金；合计行逐列复核（单价与费率列不参与求和）。',
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
      + '不代表合同单价与滞纳金条款合理、也不代表诉讼时效判断正确 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
