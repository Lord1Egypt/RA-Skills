#!/usr/bin/env node
/**
 * utility-tier-billing-check.js —— 电费分时计价核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**工商业用电是按"尖峰平谷"分时计价的**，每月电费单上是一张多行表：
 *   ① 电度电费（尖峰/高峰/平段/低谷各一行）= 用电量 × 该时段单价
 *   ② 基本电费（按容量或需量收，与用电量无关）
 *   ③ 其他费用（力率调整、政府性基金及附加等）
 *   ④ 应付合计 = 电度电费 + 基本电费 + 其他费用
 * 单价分时段、电量抄表、基本电费口径（按容量还是按需量）—— 任一处错就是几千块的差额；
 * 而**分时电价单子结构复杂**，人眼核不动；这些都是**纯算术**。
 *
 * 与已有能力的区别：`utility-allocation-check` 核的是**公共费用按面积分摊给租户**；
 * `payment-fee-check` 核**收款手续费**；本能力核的是**一张电费单本身算得对不对**（分时电价）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查电价文件、不调用大模型；材料不足不给结论。
 */
'use strict';

const CHECKS_GIVEN = [
  '电度电费勾稽（用电量 × 单价，仅对同时填了电量与单价的行）',
  '应付合计勾稽（电度电费 + 基本电费 + 其他费用）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复计费项目检测',
  '关键字段缺失检测（计费项目、应付合计）',
];

const CHECKS_WITHHELD = [
  '单价超出 0~2 元/度常见区间检测',
  '用电量为负检测',
  '应付合计为负检测',
  '基本电费为负检测',
  '电度电费为负检测',
];

const OUT_OF_SCOPE = [
  '判断分时时段划分（尖/峰/平/谷各几点到几点）是否符合当地电价文件',
  '核对抄表数是否真实（那需要与电表底度比对）',
  '处理力率调整电费的方向与计算（请把结果填进"其他费用"并列示明细）',
  '处理转供电加价、容量改需量等合同变更',
  '读取 .xlsx 或电网账单文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '计费项目\t用电量\t单价\t电度电费\t基本电费\t其他费用\t应付合计',
  '尖峰\t1000\t1.20\t1200.00\t\t\t1200.00',
  '高峰\t3000\t1.00\t3000.00\t\t\t3000.00',
  '平段\t5000\t0.70\t3500.00\t\t\t3500.00',
  '低谷\t2000\t0.40\t800.00\t\t\t800.00',
  '基本电费\t\t\t\t5000.00\t\t5000.00',
  '其他费用\t\t\t\t\t300.00\t300.00',
  '合计\t11000\t\t8500.00\t5000.00\t300.00\t13800.00',
].join('\n');

const TOL = 0.01;
const UNIT_PRICE_CAP = 2;

const ROLES = {
  party: ['计费项目', '项目', '时段', '费用项目'],
  qty: ['用电量', '电量', '抄见电量'],
  price: ['单价', '电价'],
  energyFee: ['电度电费', '电度'],
  baseFee: ['基本电费', '基本电费金额'],
  otherFee: ['其他费用', '其他'],
  total: ['应付合计', '应付金额', '合计电费'],
};

const LABELS = {
  party: '计费项目', qty: '用电量', price: '单价', energyFee: '电度电费',
  baseFee: '基本电费', otherFee: '其他费用', total: '应付合计',
};

// 只强制要求"计费项目"与"应付合计"；电量/单价/各项费用允许为空（不同时段行结构不同）
const REQUIRED = ['party', 'total'];
const SUM_ROLES = ['qty', 'energyFee', 'baseFee', 'otherFee', 'total'];

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
  //    「电度电费」不能在「单价」之前被抢，也不能让「其他」抢走「其他费用」（同一关键词，无碍）；
  //    关键是「基本电费」「电度电费」都要排在宽泛的 `其他费用/单价` 规则之前。
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
const who = (it) => `计费项目「${it.byRole.party || '(未命名)'}」`;

function checkEnergyFee(it) {
  const qty = num(it, 'qty');
  const price = num(it, 'price');
  const stated = num(it, 'energyFee');
  if (qty === null || price === null || stated === null) return null;
  const expect = round2(qty * price);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '电度电费与复算不符', line: it.line,
    message: `${who(it)}的电度电费是 ${stated.toFixed(2)}，按 用电量 ${qty} × 单价 ${price} 应为 ${expect.toFixed(2)}。`,
    advice: '分时电价每个时段单价不同；把高峰单价用到平段上是最常见的错。',
  };
}

function checkTotal(it) {
  const e = num(it, 'energyFee');
  const b = num(it, 'baseFee');
  const o = num(it, 'otherFee');
  const stated = num(it, 'total');
  if (stated === null) return null;
  const sum = round2((e === null ? 0 : e) + (b === null ? 0 : b) + (o === null ? 0 : o));
  if (Math.abs(sum - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应付合计与复算不符', line: it.line,
    message: `${who(it)}的应付合计是 ${stated.toFixed(2)}，`
      + `按 电度电费 ${(e === null ? 0 : e).toFixed(2)} + 基本电费 ${(b === null ? 0 : b).toFixed(2)} `
      + `+ 其他费用 ${(o === null ? 0 : o).toFixed(2)} 应为 ${sum.toFixed(2)}。`,
    advice: '应付合计 = 电度 + 基本 + 其他；漏掉"基本电费"（与用电量无关的那一笔）是最常见的错。',
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
        advice: '要么明细行漏了项目，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一计费项目出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一时段分表计量是正常的；但若本表按时段汇总，重复行会让电量与电费一起翻倍。',
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
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '') {
        out.push({
          level: 'P0', category: '关键字段缺失', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的。`,
          advice: '缺这一格这行电费就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的电费账单核对表（要能认出「计费项目」「用电量」「单价」「电度电费」'
      + '「基本电费」「其他费用」「应付合计」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从电网账单或电费发票导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个计费项目的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkEnergyFee(it); if (a) findings.push(a);
    const b = checkTotal(it); if (b) findings.push(b);
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
      items: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      qty_total: sumOf('qty'),
      energy_fee_total: sumOf('energyFee'),
      base_fee_total: sumOf('baseFee'),
      other_fee_total: sumOf('otherFee'),
      payable_total: sumOf('total'),
      avg_price: sumOf('qty') > 0 ? round2(sumOf('energyFee') / sumOf('qty')) : null,
      basis: '电度电费 = 用电量 × 单价（分时段各自算）；应付合计 = 电度电费 + 基本电费 + 其他费用；合计行逐列复核。',
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
      + '不代表分时时段划分正确、也不代表抄表数真实 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
