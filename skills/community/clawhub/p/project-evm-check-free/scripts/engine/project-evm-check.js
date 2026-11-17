#!/usr/bin/env node
/**
 * project-evm-check.js —— 项目挣值分析（EVM）核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**做项目（工程/IT/研发）的人每月都要报进度与成本**，标准做法是挣值分析：
 *   ① CV（成本偏差）= EV − AC        ② SV（进度偏差）= EV − PV
 *   ③ CPI（成本绩效）= EV ÷ AC       ④ SPI（进度绩效）= EV ÷ PV
 * 这四条式子极简，但**分母写错（CPI 用 AC、SPI 用 PV）是最常见的错**，
 * 而且它直接决定"要不要追加预算/要不要延工期"的管理判断 —— 报错了会误导决策。
 * 一个项目几十个工作包，人眼核不动；而这些全是**纯算术**。
 *
 * 与已有能力的区别：`progress-payment-check` 核**工程进度款与质保金**（钱怎么付）；
 * 本能力核**进度与成本的绩效指标**（EV/PV/AC 派生量），是管理口径而非结算口径。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不判工程量真实性、不调用大模型；材料不足不给结论；不给项目管理建议。
 */
'use strict';

const CHECKS_GIVEN = [
  'CV 勾稽（EV − AC）',
  'SV 勾稽（EV − PV）',
  'CPI 勾稽（EV ÷ AC）',
  'SPI 勾稽（EV ÷ PV）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复工作包检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  'CPI / SPI 与「好于/差于 1」的定性结论一致性检测',
  'PV / EV / AC 为负检测',
  '完工预测 EAC（BAC ÷ CPI）与表内值一致性检测',
  '完工尚需估算 ETC（EAC − AC）一致性检测',
  'BAC 小于 EV（已完成价值超过总预算）异常检测',
];

const OUT_OF_SCOPE = [
  '判断 PV/EV 的计量口径（那要按合同计量规则与组织流程确定）',
  '处理多级 WBS 汇总、以及管理储备与应急储备',
  '处理尚未开始或已取消的工作包（请先在表里剔除）',
  '给出项目管理建议或预测工期；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '工作包\tPV\tEV\tAC\tCV\tSV\tCPI\tSPI',
  '设计\t100000.00\t100000.00\t95000.00\t5000.00\t0.00\t1.05\t1.00',
  '采购\t200000.00\t180000.00\t200000.00\t-20000.00\t-20000.00\t0.90\t0.90',
  '施工\t300000.00\t240000.00\t260000.00\t-20000.00\t-60000.00\t0.92\t0.80',
  '合计\t600000.00\t520000.00\t555000.00\t-35000.00\t-80000.00\t',
].join('\n');

const TOL = 0.01;
const IDX_TOL = 0.005;      // CPI/SPI 保留两位小数，容差按百分点算

const ROLES = {
  party: ['工作包', '项目', '任务', '活动'],
  pv: ['PV', '计划价值', '计划值'],
  ev: ['EV', '挣值', '已完价值'],
  ac: ['AC', '实际成本', '实际费用'],
  cv: ['CV', '成本偏差'],
  sv: ['SV', '进度偏差'],
  cpi: ['CPI', '成本绩效'],
  spi: ['SPI', '进度绩效'],
};

const LABELS = {
  party: '工作包', pv: 'PV', ev: 'EV', ac: 'AC', cv: 'CV', sv: 'SV', cpi: 'CPI', spi: 'SPI',
};

const REQUIRED = ['party', 'pv', 'ev', 'ac', 'cv', 'sv', 'cpi', 'spi'];
const SUM_ROLES = ['pv', 'ev', 'ac', 'cv', 'sv', 'cpi', 'spi'];

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
  const h = String(header).replace(/[\s（）()]/g, '').toUpperCase();
  // ⚠️ PV/EV/AC/CV/SV 这些**两字母缩写互为子串风险极低**，但仍要按"先长后短"写：
  //    CPI/SPI 必须排在 CV/SV/PV/EV/AC 之前？——实际不会互相包含，这里保留顺序说明以防未来加别名。
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k.toUpperCase()) >= 0)) return role;
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
const who = (it) => `工作包「${it.byRole.party || '(未命名)'}」`;

function checkCv(it) {
  const ev = num(it, 'ev'); const ac = num(it, 'ac'); const stated = num(it, 'cv');
  if (ev === null || ac === null || stated === null) return null;
  const expect = round2(ev - ac);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: 'CV 与复算不符', line: it.line,
    message: `${who(it)}的 CV 是 ${stated.toFixed(2)}，按 EV ${ev.toFixed(2)} − AC ${ac.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: 'CV（成本偏差）与 SV（进度偏差）都要用 **EV 打头**：CV = EV − AC，SV = EV − PV；写反是最常见的错。',
  };
}

function checkSv(it) {
  const ev = num(it, 'ev'); const pv = num(it, 'pv'); const stated = num(it, 'sv');
  if (ev === null || pv === null || stated === null) return null;
  const expect = round2(ev - pv);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: 'SV 与复算不符', line: it.line,
    message: `${who(it)}的 SV 是 ${stated.toFixed(2)}，按 EV ${ev.toFixed(2)} − PV ${pv.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: 'SV = EV − PV（都按"价值"口径）；用 AC 去减 PV 会把成本差异混进进度差异里。',
  };
}

function checkIndex(it, role, denomRole, name) {
  const ev = num(it, 'ev'); const denom = num(it, denomRole); const stated = num(it, role);
  if (ev === null || denom === null || stated === null) return null;
  if (Math.abs(denom) <= 1e-9) return null;
  const expect = Math.round(ev / denom * 100) / 100;
  if (Math.abs(expect - stated) <= IDX_TOL) return null;
  return {
    level: 'P0', category: `${name} 与复算不符`, line: it.line,
    message: `${who(it)}的 ${name} 是 ${stated}，按 EV ${ev.toFixed(2)} ÷ ${LABELS[denomRole]} ${denom.toFixed(2)} 应为 ${expect}。`,
    advice: `${name} 的分子永远是 **EV**：CPI = EV ÷ AC，SPI = EV ÷ PV。分母写错会得出方向完全相反的结论。`,
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
    const tol = (role === 'cpi' || role === 'spi') ? IDX_TOL : TOL;
    if (Math.abs(sum - stated) > tol) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: role === 'cpi' || role === 'spi'
          ? '**CPI/SPI 是比率，不能按行相加**：整体指标要用"合计 EV ÷ 合计 AC"重算，合计行里不该填比率。'
          : '要么明细行漏了工作包，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一工作包出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一工作包按子项分行是正常的；但若本表按工作包汇总，重复行会让 PV/EV/AC 一起翻倍。',
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
          advice: '缺这一格这条绩效指标就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的挣值分析表（要能认出「工作包」「PV」「EV」「AC」「CV」「SV」「CPI」「SPI」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从项目管理/成本系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个工作包的明细行']);

  const bac = normNumber(payload && payload.bac);
  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkCv(it); if (a) findings.push(a);
    const b = checkSv(it); if (b) findings.push(b);
    const c = checkIndex(it, 'cpi', 'ac', 'CPI'); if (c) findings.push(c);
    const d = checkIndex(it, 'spi', 'pv', 'SPI'); if (d) findings.push(d);
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
  const evT = sumOf('ev'); const acT = sumOf('ac'); const pvT = sumOf('pv');

  const result = {
    findings,
    summary: {
      packages: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      pv_total: pvT,
      ev_total: evT,
      ac_total: acT,
      cv_total: round2(evT - acT),
      sv_total: round2(evT - pvT),
      cpi_overall: acT > 0 ? Math.round(evT / acT * 100) / 100 : null,
      spi_overall: pvT > 0 ? Math.round(evT / pvT * 100) / 100 : null,
      basis: 'CV = EV − AC；SV = EV − PV；CPI = EV ÷ AC；SPI = EV ÷ PV；'
        + '**整体 CPI/SPI 要用合计重算，不能把各行的比率相加**；合计行逐列复核。',
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
      + '不代表 PV/EV 的计量口径正确、也不代表项目判断成立 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
