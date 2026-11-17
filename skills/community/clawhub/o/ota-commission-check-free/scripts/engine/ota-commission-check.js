#!/usr/bin/env node
/**
 * ota-commission-check.js —— 酒店 OTA 佣金与净结算额核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**做酒店/民宿的每月都要核携程、美团、飞猪等渠道的结算单**：
 *   ① 佣金       = 房费收入 × 佣金率
 *   ② 净结算额   = 房费收入 − 佣金 − 其他扣费（推广费、活动补贴、赔付…）
 * 佣金率按合同分档、活动价与挂牌价口径不同、其他扣费名目多 —— 每一处都能少结几百上千；
 * 一个月几个渠道、几十上百个订单，人眼核不动；而这些都是**纯算术**。
 *
 * 与已有能力的区别：`platform-settlement-check` 核的是**电商平台结算单**（商品成交、退款、技术服务费）；
 * `commission-check` 核的是**销售提成**（员工/代理商）；
 * 本能力核的是**酒店渠道的 OTA 佣金与净结算**，行业与口径都不同。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查渠道合同、不调用大模型；材料不足不给结论；不给税务意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '佣金勾稽（房费收入 × 佣金率）',
  '净结算额勾稽（房费收入 − 佣金 − 其他扣费）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复渠道检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '佣金率超出 0~30% 合理区间检测',
  '净结算额为负或超过房费收入检测',
  '其他扣费为负检测',
  '综合扣费率异常检测（(佣金 + 其他扣费) ÷ 房费收入 超过 35%）',
];

const OUT_OF_SCOPE = [
  '判断渠道佣金率是否符合合同约定（那是商务条款的事）',
  '处理按订单逐笔核对（本表是渠道汇总口径；逐笔核对请先把订单明细汇总）',
  '处理促销补贴、闪住、预付与现付的结算差异',
  '判断收入确认时点与开票口径；给出税务意见',
  '读取 .xlsx 或渠道账单文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '渠道\t房费收入\t佣金率\t佣金\t其他扣费\t净结算额',
  '携程\t300000.00\t15%\t45000.00\t2000.00\t253000.00',
  '美团\t200000.00\t12%\t24000.00\t1500.00\t174500.00',
  '合计\t500000.00\t\t69000.00\t3500.00\t427500.00',
].join('\n');

const TOL = 0.01;
const TOTAL_FEE_CAP = 0.35;

const ROLES = {
  party: ['渠道', '平台', '渠道名称'],
  revenue: ['房费收入', '房费', '间夜收入', '营业收入'],
  rate: ['佣金率', '费率', '佣金比例'],
  commission: ['佣金', '佣金金额'],
  otherFee: ['其他扣费', '其他费用', '推广费'],
  net: ['净结算额', '结算额', '净额'],
};

const LABELS = {
  party: '渠道', revenue: '房费收入', rate: '佣金率', commission: '佣金',
  otherFee: '其他扣费', net: '净结算额',
};

const REQUIRED = ['party', 'revenue', 'rate', 'commission', 'otherFee', 'net'];
const SUM_ROLES = ['revenue', 'commission', 'otherFee', 'net'];

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
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库踩过三次的坑，见 tools/header_map_check.py）：
  //    「净结算额」里的「结算额」不能被别的规则抢走；「佣金率」必须排在「佣金」之前。
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
const who = (it) => `渠道「${it.byRole.party || '(未命名)'}」`;

function checkCommission(it) {
  const revenue = num(it, 'revenue');
  const rate = num(it, 'rate');
  const stated = num(it, 'commission');
  if (revenue === null || rate === null || stated === null) return null;
  const expect = round2(revenue * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '佣金与复算不符', line: it.line,
    message: `${who(it)}的佣金是 ${stated.toFixed(2)}，按 房费收入 ${revenue.toFixed(2)} × ${rate}% 复算应为 ${expect.toFixed(2)}。`,
    advice: '渠道佣金常按分档费率（如 10%/12%/15%）；要确认本期适用哪一档，以及活动价是否单独计佣。',
  };
}

function checkNet(it) {
  const revenue = num(it, 'revenue');
  const commission = num(it, 'commission');
  const other = num(it, 'otherFee');
  const stated = num(it, 'net');
  if (revenue === null || commission === null || other === null || stated === null) return null;
  const expect = round2(revenue - commission - other);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '净结算额与复算不符', line: it.line,
    message: `${who(it)}的净结算额是 ${stated.toFixed(2)}，`
      + `按 房费收入 ${revenue.toFixed(2)} − 佣金 ${commission.toFixed(2)} − 其他扣费 ${other.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '净结算 = 房费收入 − 佣金 − 其他扣费；漏一项扣费就是少收一笔钱。',
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
        advice: '要么明细行漏了渠道，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一渠道出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一渠道按月/按门店分行是正常的；但若本表按渠道汇总，重复行会让收入与佣金一起翻倍。',
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
          advice: '缺这一格这笔结算就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的渠道结算核对表（要能认出「房费收入」「佣金率」「佣金」「其他扣费」「净结算额」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从渠道结算单导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个渠道的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkCommission(it); if (a) findings.push(a);
    const b = checkNet(it); if (b) findings.push(b);
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
      channels: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      revenue_total: sumOf('revenue'),
      commission_total: sumOf('commission'),
      other_fee_total: sumOf('otherFee'),
      net_total: sumOf('net'),
      net_margin_pct: sumOf('revenue') > 0 ? round2(sumOf('net') / sumOf('revenue') * 100) : null,
      basis: '佣金 = 房费收入 × 佣金率；净结算额 = 房费收入 − 佣金 − 其他扣费；合计行逐列复核。',
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
      + '不代表渠道佣金率符合合同、也不代表没有其他未列示的扣款 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
