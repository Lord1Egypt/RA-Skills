#!/usr/bin/env node
/**
 * import-duty-check.js —— 进口税费核算核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**进口商/货代每票货都要核一遍税费再对外付款** ——
 * 关税 = 完税价格 × 关税率；消费税 = (完税价格 + 关税) ÷ (1 − 消费税率) × 消费税率；
 * 增值税 = (完税价格 + 关税 + 消费税) × 增值税率。三步都是**串行依赖**：
 * 第一行错一点，后面全错，而且完税价格、税率、汇率里任何一格录错都会放大成真金白银。
 * 一个月几十票，人眼复算不动；而这些都是**纯算术**。
 *
 * 与已有能力的区别：`trade-doc-consistency` 核的是**单证之间是否一致**（品名/数量/金额对不对得上），
 * **完全不碰税额计算**；本能力核的是**这张税费计算表本身算得对不对**。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查海关税则、不调用大模型；材料不足不给结论；不给报关/税务意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '关税勾稽（完税价格 × 关税率）',
  '消费税勾稽（从价：(完税价格 + 关税) ÷ (1 − 消费税率) × 消费税率）',
  '增值税勾稽（(完税价格 + 关税 + 消费税) × 增值税率）',
  '税费合计勾稽（关税 + 消费税 + 增值税）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复商品行检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '税率区间异常检测（关税率 / 消费税率 / 增值税率 小于 0 或大于 100%）',
  '完税价格非正检测',
  '税费为负检测',
  '综合税负率异常检测（税费合计 ÷ 完税价格 超过给定阈值，默认 100%）',
];

const OUT_OF_SCOPE = [
  '查海关税则、判断商品该适用哪个税号与税率（那是报关行与海关的事）',
  '判断完税价格是否被海关接受（本工具只按你给的完税价格复算）',
  '处理从量税、复合计税、反倾销税与保证金（需按具体税号另算）',
  '处理汇率折算（请在表里就把外币折成人民币后再核）',
  '给出报关或税务意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '商品\t完税价格\t关税率\t关税\t消费税率\t消费税\t增值税率\t增值税\t税费合计',
  'A型设备\t100000.00\t8%\t8000.00\t0%\t0.00\t13%\t14040.00\t22040.00',
  'B型化妆品\t50000.00\t5%\t2500.00\t15%\t9264.71\t13%\t8029.41\t19794.12',
  '合计\t150000.00\t\t10500.00\t\t9264.71\t\t22069.41\t41834.12',
].join('\n');

const TOL = 0.01;

const ROLES = {
  party: ['商品', '品名', '料号', '货品', '名称'],
  price: ['完税价格', '计税价格', '到岸价', 'CIF'],
  dutyRate: ['关税率', '关税税率'],
  duty: ['关税'],
  ctRate: ['消费税率', '消费税税率'],
  ct: ['消费税'],
  vatRate: ['增值税率', '增值税税率'],
  vat: ['增值税'],
  total: ['税费合计', '合计税费', '应缴税费', '税费总计'],
};

const LABELS = {
  party: '商品', price: '完税价格', dutyRate: '关税率', duty: '关税',
  ctRate: '消费税率', ct: '消费税', vatRate: '增值税率', vat: '增值税', total: '税费合计',
};

const SUM_ROLES = ['price', 'duty', 'ct', 'vat', 'total'];
const REQUIRED = ['party', 'price', 'dutyRate', 'duty', 'vatRate', 'vat', 'total'];

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
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

/** 数字：去千分位与货币符号；带 % 的原样返回百分数（15% -> 15）。 */
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

function label(it) {
  return `${LABELS.party}「${it.byRole.party || '(未命名)'}」`;
}

function checkDuty(it) {
  const price = normNumber(it.byRole.price);
  const rate = normNumber(it.byRole.dutyRate);
  const stated = normNumber(it.byRole.duty);
  if (price === null || rate === null || stated === null) return null;
  const expect = round2(price * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '关税与复算不符', line: it.line,
    message: `${label(it)}的关税是 ${stated.toFixed(2)}，按 ${price.toFixed(2)} × ${rate}% 复算应为 ${expect.toFixed(2)}。`,
    advice: '关税是后面两道税的计算基数：它错了，消费税和增值税会一起错。',
  };
}

function checkConsumptionTax(it) {
  const price = normNumber(it.byRole.price);
  const duty = normNumber(it.byRole.duty);
  const rate = normNumber(it.byRole.ctRate);
  const stated = normNumber(it.byRole.ct);
  if (price === null || duty === null || rate === null || stated === null) return null;
  if (rate <= 0) return null;                       // 不征消费税的商品，本行不适用
  if (rate >= 100) return null;                     // 异常税率由付费档负责报，不在免费档下结论
  const expect = round2((price + duty) / (1 - rate / 100) * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '消费税与复算不符', line: it.line,
    message: `${label(it)}的消费税是 ${stated.toFixed(2)}，按 (${price.toFixed(2)} + ${duty.toFixed(2)}) `
      + `÷ (1 − ${rate}%) × ${rate}% 复算应为 ${expect.toFixed(2)}。`,
    advice: '从价消费税要先组成计税价格（含关税）再乘税率；直接用完税价格乘税率是最常见的错法。',
  };
}

function checkVat(it) {
  const price = normNumber(it.byRole.price);
  const duty = normNumber(it.byRole.duty);
  const rate = normNumber(it.byRole.vatRate);
  const stated = normNumber(it.byRole.vat);
  if (price === null || duty === null || rate === null || stated === null) return null;
  const ct = normNumber(it.byRole.ct);
  if (ct === null && it.byRole.ct !== undefined) return null;   // 有消费税列但没填 -> 由空白检测负责
  const ctBase = ct === null ? 0 : ct;
  const expect = round2((price + duty + ctBase) * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '增值税与复算不符', line: it.line,
    message: `${label(it)}的增值税是 ${stated.toFixed(2)}，`
      + `按 (${price.toFixed(2)} + ${duty.toFixed(2)} + ${ctBase.toFixed(2)}) × ${rate}% 复算应为 ${expect.toFixed(2)}。`,
    advice: '进口增值税的计税基数是「完税价格 + 关税 + 消费税」，漏掉消费税是常见错法。',
  };
}

function checkTotal(it) {
  const stated = normNumber(it.byRole.total);
  if (stated === null) return null;
  const duty = normNumber(it.byRole.duty);
  const vat = normNumber(it.byRole.vat);
  if (duty === null || vat === null) return null;
  const ct = normNumber(it.byRole.ct);
  const sum = round2(duty + vat + (ct === null ? 0 : ct));
  if (Math.abs(sum - stated) <= TOL) return null;
  return {
    level: 'P0', category: '税费合计与各税之和不符', line: it.line,
    message: `${label(it)}的税费合计是 ${stated.toFixed(2)}，关税 + 消费税 + 增值税 = ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)} 元。`,
    advice: '通常是某一项税算完后没回写到合计，或合计里混进了不该计入的费用。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = normNumber(t.byRole[role]);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = normNumber(it.byRole[role]);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了票，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一商品出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一商品多票是正常的；但若本表按商品汇总，重复行会让税费翻倍 —— 请确认口径（是否同一报关单）。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items, hasCt) {
  const out = [];
  const roles = ['price', 'dutyRate', 'duty', 'vatRate', 'vat', 'total']
    .concat(hasCt ? ['ctRate', 'ct'] : []);
  for (const it of items) {
    for (const role of roles) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${label(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这道税就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的进口税费计算表（要能同时认出「完税价格」「关税率」「关税」「增值税率」「增值税」「税费合计」这几列；'
      + '有消费税的再加「消费税率」「消费税」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一票的明细行']);

  const hasCt = t.cols.some((c) => c.role === 'ctRate') && t.cols.some((c) => c.role === 'ct');
  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const d = checkDuty(it); if (d) findings.push(d);
    const c = checkConsumptionTax(it); if (c) findings.push(c);
    const v = checkVat(it); if (v) findings.push(v);
    const tt = checkTotal(it); if (tt) findings.push(tt);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items, hasCt)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  
  if (!hasCt) notRun.push(CHECKS_GIVEN[1]);
  else if (!t.items.some((it) => {
    const r = normNumber(it.byRole.ctRate);
    return r !== null && r > 0;
  })) notRun.push(CHECKS_GIVEN[1]);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = normNumber(it.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0));

  const priceTotal = sumOf('price');
  const taxTotal = sumOf('total');
  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      price_total: priceTotal,
      tax_total: taxTotal,
      burden_pct: priceTotal > 0 ? round2(taxTotal / priceTotal * 100) : null,
      basis: '关税 = 完税价格 × 关税率；消费税 = (完税价格 + 关税) ÷ (1 − 消费税率) × 消费税率；'
        + '增值税 = (完税价格 + 关税 + 消费税) × 增值税率；税费合计 = 三项之和；合计行逐列复核。',
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
      + '不代表税号、税率适用正确，也不代表完税价格被海关接受 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
