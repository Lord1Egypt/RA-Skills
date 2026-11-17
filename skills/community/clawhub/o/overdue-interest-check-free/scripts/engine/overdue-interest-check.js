#!/usr/bin/env node
/**
 * overdue-interest-check.js —— 逾期利息与违约金核算核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**有应收账款的公司在月结、催收、诉讼前都要算一次逾期利息**，
 * 而利息 = 本金 × 利率 × 天数，天数怎么数（算头不算尾）、利率超过司法保护上限没有、
 * 起止日填错没有 —— 每一项都能算错，且算错的代价直接是钱（多收要不回来、少收自己亏）。
 * 单量一多（几十上百笔），人眼核不动；而这些都是**纯算术**。
 *
 * 与已有能力的区别：`ar-aging-check` 只做**账龄分桶**（30/60/90 天），
 * **不算法定利率上限、不核算利息金额、不检查天数口径**；本能力核的是**逐笔利息算得对不对**。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不调用大模型；材料不足不给结论；不给法律意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '计息天数与起止日勾稽（按算头不算尾复算，并同时给出算头算尾的口径）',
  '已计利息勾稽（本金 × 年利率 ÷ 365 × 天数，容差 0.01 元）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复客户检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '约定利率超过司法保护上限检测（一年期 LPR 的 4 倍，LPR 由入参给出）',
  '日期异常检测（截止日不晚于起算日、起算日在未来）',
  '本金或年利率非正检测',
  '已计利息为负检测',
];

const OUT_OF_SCOPE = [
  '判断债权是否成立、是否已过诉讼时效（那是法务与法院的事，本工具只算你给的表）',
  '给出法律意见或预测法院裁判结果',
  '复利、罚息与违约金**并行**时的叠加口径（各合同差异过大，需按合同逐条确认）',
  '判断还款抵扣顺序（给了还款记录才能算；本版本不接收还款流水）',
  '读取 .xlsx（需要你先从系统导出、复制成文本贴进来）',
];

const SAMPLE_TEXT = [
  '客户\t本金\t年利率\t起算日\t截止日\t计息天数\t已计利息',
  '甲公司\t100000.00\t12%\t2026-01-01\t2026-03-31\t89\t2926.03',
  '乙公司\t50000.00\t8.5%\t2026-02-01\t2026-03-31\t58\t675.34',
  '合计\t150000.00\t\t\t\t\t3601.37',
].join('\n');

const TOL = 0.01;

const ROLES = {
  party: ['客户', '单位', '公司', '名称', '债务人', '欠款方', '对方'],
  principal: ['本金', '欠款', '未付', '应收', '金额'],
  rate: ['年利率', '利率', '年化'],
  start: ['起算日', '起始日', '开始日', '起息日', '计息起始'],
  end: ['截止日', '截止日期', '计算截止', '结息日', '到'],
  days: ['计息天数', '天数', '逾期天数'],
  interest: ['已计利息', '利息', '利息金额'],
};

const LABELS = {
  party: '客户', principal: '本金', rate: '年利率', start: '起算日',
  end: '截止日', days: '计息天数', interest: '已计利息',
};

const SUM_ROLES = ['principal', 'interest'];

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

/** 金额：去掉 ¥、千分位、货币前缀；百分比原样返回数值。 */
function normNumber(raw) {
  if (isBlank(raw)) return null;
  let s = String(raw).trim().replace(/[,，\s¥￥$]/g, '');
  const pct = /%$/.test(s);
  s = s.replace(/%$/, '');
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return pct ? n : n;
}

/** 日期 -> UTC 毫秒（只认 YYYY-MM-DD / YYYY/M/D / YYYY.M.D；不认的返回 null，绝不猜）。 */
function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[年月]/g, '-').replace(/日/g, '').replace(/[./]/g, '-');
  const m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]); const mo = Number(m[2]); const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const t = Date.UTC(y, mo - 1, d);
  const back = new Date(t);
  if (back.getUTCFullYear() !== y || back.getUTCMonth() !== mo - 1 || back.getUTCDate() !== d) return null;
  return t;
}

const DAY = 86400000;
const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).map((l) => l).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const need = ['principal', 'rate', 'start', 'end', 'interest'];
  const missingRoles = need.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {}, isTotal: false };
    cols.forEach((c, idx) => { if (c.role) row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx]; });
    const first = String(cells[0] || '').trim();
    if (/^(合计|总计|小计|total)$/i.test(first) || /^(合计|总计|小计)/.test(first)) {
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

/** 天数真值：算头不算尾 = 差值；算头算尾 = 差值 + 1。 */
function dayTruth(it) {
  const a = normDate(it.byRole.start);
  const b = normDate(it.byRole.end);
  if (a === null || b === null) return null;
  const diff = Math.round((b - a) / DAY);
  return { headNoTail: diff, headAndTail: diff + 1, inverted: diff <= 0 };
}

function checkDays(it) {
  const t = dayTruth(it);
  if (!t) return null;
  const stated = normNumber(it.byRole.days);
  if (stated === null) return null;
  if (stated === t.headNoTail || stated === t.headAndTail) return null;
  return {
    level: 'P0', category: '计息天数与起止日不符', line: it.line,
    message: `${LABELS.party}「${it.byRole.party || ''}」的计息天数是 ${stated} 天，`
      + `但按起止日（${it.byRole.start} → ${it.byRole.end}）算头不算尾应为 ${t.headNoTail} 天、`
      + `算头算尾应为 ${t.headAndTail} 天。`,
    advice: '先确认合同约定的天数口径（算头/算尾）；天数错一天，利息就错一天的本金×利率。',
  };
}

function checkInterest(it) {
  const principal = normNumber(it.byRole.principal);
  const rate = normNumber(it.byRole.rate);
  const stated = normNumber(it.byRole.interest);
  if (principal === null || rate === null) return null;
  let days = normNumber(it.byRole.days);
  if (days === null) {
    const t = dayTruth(it);
    days = t ? t.headNoTail : null;
  }
  if (days === null || stated === null) return null;
  const expect = round2(principal * (rate / 100) / 365 * days);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '已计利息与复算不符', line: it.line,
    message: `${LABELS.party}「${it.byRole.party || ''}」的已计利息是 ${stated.toFixed(2)}，`
      + `按 ${principal.toFixed(2)} × ${rate}% ÷ 365 × ${days} 天复算应为 ${expect.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)} 元。`,
    advice: '核对本金、年利率、计息天数三者；若合同按 360 天计息，请先在天数或利率上按同一口径折算后再核。',
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
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
          + `相差 ${round2(stated - sum).toFixed(2)} 元。`,
        advice: '要么明细行漏了一笔，要么合计行没跟着更新。',
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
        advice: '同一客户多笔应收是正常的；但若本表按客户汇总，重复行会让合计翻倍 —— 请确认口径。',
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
    for (const role of ['principal', 'rate', 'start', 'end', 'interest']) {
      const v = it.byRole[role];
      const s = String(v === undefined ? '' : v).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${LABELS.party}「${it.byRole.party || '(未命名)'}」的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格就算不出利息来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的利息计算表（要能同时认出「本金」「年利率」「起算日」「截止日」「已计利息」这几列）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一笔的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkDays(it); if (a) findings.push(a);
    const b = checkInterest(it); if (b) findings.push(b);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = normNumber(it.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0));

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      principal_total: sumOf('principal'),
      interest_total: sumOf('interest'),
      basis: '逐笔复算「本金 × 年利率 ÷ 365 × 计息天数」，并核天数与起止日是否一致；'
        + '合计行逐列复核；付费档另核利率上限、日期异常、非正数与负利息',
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
      + '不代表债权成立、时效未过或合同约定本身合法 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, normDate, isBlank, dayTruth, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
