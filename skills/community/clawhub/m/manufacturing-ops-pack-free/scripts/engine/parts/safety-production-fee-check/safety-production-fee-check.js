/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * safety-production-fee-check.js —— 安全生产费用提取与使用核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月结账前**。矿山、建筑施工、危险化学品、交通运输等企业
 * 按规定比例（或按产量）从营业收入 / 产量里提取安全生产费用，**专户核算、专款专用**；
 * 提取不足、当期不提、或者把非安全支出挤进专户，都是监管检查与处罚的高发点。
 * 这张表的数算错，方向只有两个：**提取不足**（账面费用提少了，专户余额虚高却不够用）
 * 或 **挪用超支**（本期使用超过可用余额，期末余额为负）。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   应提取金额 = 计提基数（营业收入，或产量口径的产量）× 提取比例
 *   期末余额   = 期初余额 + 本期提取 − 本期使用
 *   合计行各列 = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某家企业应当适用哪个行业标准、按什么基数提取（那属于行业监管口径与
 *    会计判断）：表里给你的行业类别、营业收入、产量、提取比例一律**以你填的为准**，
 *    本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '应提取金额复算（营业收入或产量口径基数 × 提取比例 = 应提取金额）',
  '期末余额滚动复算（期初余额 + 本期提取 − 本期使用 = 期末余额）',
  '合计行逐列复核',
  '同一核算主体同一期间重复行检测',
  '空白与占位符检测',
  '金额或比例为负检测',
];

const CHECKS_WITHHELD = [
  '提取比例低于规定下限提示（按行业类别的内置参考下限，超容差才报）',
  '本期使用超过可用余额（挪用/超支）提示',
  '期末余额为负提示',
  '当期提取为 0 提示',
  '累计使用与累计提取比例异常（使用率超过 100%）提示',
];

const OUT_OF_SCOPE = [
  '判断某家企业该按哪个行业标准、哪个基数（含税或不含税营业收入、产量口径）提取（属于行业监管口径与会计判断，请以现行规定原文与主管部门口径为准）',
  '认定「提取比例低于下限」是否构成违规、是否应当补提或处罚（本工具只做提示，不出法律结论）',
  '判断哪些支出可以（或不可以）在安全生产费用专户里列支（专款专用范围、资本化与费用化，属于会计与安全管理部门判断）',
  '核对跨年度结转、上年结余在本年的动用与所得税税前扣除的税务处理',
  '读取专户银行流水 / 安全费用台账 / ERP 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t行业类别\t核算主体\t营业收入\t产量\t提取比例\t应提取金额\t期初余额\t本期提取\t本期使用\t期末余额',
  '2026-01\t建筑施工企业\t一号项目部\t8000000.00\t\t2.00%\t160000.00\t500000.00\t160000.00\t120000.00\t540000.00',
  '2026-02\t建筑施工企业\t一号项目部\t6000000.00\t\t2.00%\t120000.00\t540000.00\t120000.00\t100000.00\t560000.00',
  '2026-03\t建筑施工企业\t一号项目部\t6000000.00\t\t2.00%\t120000.00\t560000.00\t120000.00\t80000.00\t600000.00',
  '2026-01\t矿山企业\t二号矿区\t\t20000.00\t15元/吨\t300000.00\t800000.00\t300000.00\t200000.00\t900000.00',
  '2026-02\t矿山企业\t二号矿区\t\t18000.00\t15元/吨\t270000.00\t900000.00\t270000.00\t150000.00\t1020000.00',
  '2026-03\t矿山企业\t二号矿区\t\t22000.00\t15元/吨\t330000.00\t1020000.00\t330000.00\t250000.00\t1100000.00',
  '合计\t\t\t20000000.00\t60000.00\t\t1300000.00\t4320000.00\t1300000.00\t900000.00\t4720000.00',
].join('\n');

const TOL = 0.01;
/** 按单位产量计价的提取标准（元/吨、元/立方米…）——这种口径不能用"比例下限"去比 */
const PER_UNIT_RE = /元\s*[\/每]\s*(吨|立方米|m3|m³|台|件|人|车|公里|千米)/i;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  //    （「应提取金额」不能被「提取金额」抢走、「营业收入」不能被「收入」抢走、
  //      「期末余额」不能被「余额」抢走、「期初余额」也不能被「余额」抢走）
  period: ['所属期间', '会计期间', '所属期', '所属月份', '期间', '月份', '月度'],
  industry: ['行业类别', '所属行业', '行业类型', '行业标准', '行业'],
  subject: ['核算主体', '专户名称', '项目名称', '单位名称', '主体名称', '项目', '单位', '主体'],
  revenue: ['营业收入', '营业总收入', '主营业务收入', '销售收入', '收入'],
  output: ['产量', '本期产量', '产量基数', '开采量', '生产量'],
  rate: ['提取比例', '计提比例', '提取标准', '计提标准', '安全生产费用提取比例', '提取率', '比例'],
  shouldExtract: ['应提取金额', '应计提金额', '本期应提取', '应提金额', '应提取数', '应提安全费用'],
  balanceBegin: ['期初余额', '期初结余', '年初余额', '上期期末余额', '期初专项储备余额', '期初'],
  extract: ['本期提取', '已提取金额', '本期提取金额', '本期计提', '实际提取', '提取金额', '本期提取数'],
  use: ['本期使用', '本期使用金额', '本期已使用', '本期支出', '使用金额', '支出金额', '本期列支'],
  balanceEnd: ['期末余额', '期末结余', '本期期末余额', '期末专项储备余额', '余额'],
};

const LABELS = {
  period: '所属期间', industry: '行业类别', subject: '核算主体', revenue: '营业收入', output: '产量',
  rate: '提取比例', shouldExtract: '应提取金额', balanceBegin: '期初余额', extract: '本期提取',
  use: '本期使用', balanceEnd: '期末余额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'subject', 'rate', 'shouldExtract', 'balanceBegin', 'extract', 'use', 'balanceEnd'];
/** 合计行逐列复核的列 */
const SUM_ROLES = ['revenue', 'output', 'shouldExtract', 'balanceBegin', 'extract', 'use', 'balanceEnd'];
/**
 * 免费档负值检测覆盖的列：**提取侧与使用侧**的金额与比例。
 * ⚠️ 刻意**不算**期末余额 —— "期末余额为负"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出期末余额为负就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['revenue', 'output', 'shouldExtract', 'balanceBegin', 'extract', 'use', 'rate'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
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
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/[%％]$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/** 提取标准的归一化：
 *  · `2%` / `2.00%` ⇒ 0.02（比例口径）
 *  · `0.02` ⇒ 0.02；`2` ⇒ 0.02（裸数字一律当百分比）
 *  · `15元/吨` / `15 元/每吨` ⇒ 15（按单位产量计价的绝对标准，不做百分比折算）
 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  if (PER_UNIT_RE.test(s)) {
    const m = s.replace(/[,，\s¥￥$]/g, '').match(/-?\d+(?:\.\d+)?/);
    return m ? Number(m[0]) : null;
  }
  const n = normNumber(s);
  if (n === null) return null;
  if (/[%％]/.test(s)) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

/** 该行的计提基数口径：填了营业收入就按营业收入，只填产量就按产量口径 */
function caliberOf(it) {
  if (!isBlank(it && it.revenue)) return 'revenue';
  if (!isBlank(it && it.output)) return 'output';
  return null;
}

/** 提取标准是不是"按单位产量计价"（元/吨…） */
function isPerUnitRate(raw) {
  return PER_UNIT_RE.test(String(raw === undefined || raw === null ? '' : raw));
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, roles: [] };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns, roles };
}

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.subject, it && it.industry]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const subjectKeyOf = (it) => {
  const s = it && it.subject !== undefined ? String(it.subject).trim() : '';
  if (s) return s;
  const ind = it && it.industry !== undefined ? String(it.industry).trim() : '';
  return ind || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkShouldExtractRecompute(it) {
  const out = [];
  const caliber = caliberOf(it);
  const base = caliber === 'revenue' ? normNumber(it.revenue)
    : (caliber === 'output' ? normNumber(it.output) : null);
  const rate = rateValue(it.rate);
  const stated = normNumber(it.shouldExtract);
  if (base === null || rate === null || stated === null) return out;
  if (base <= 0 || rate <= 0) return out;      // 基数或比例为 0 / 负：由负值检测与完整档检查报，这里算不出应提取
  const expect = round2(base * rate);
  if (Math.abs(expect - stated) <= TOL) return out;
  const caliberName = caliber === 'revenue' ? '营业收入' : '产量';
  const rateShown = isPerUnitRate(it.rate) ? `${rate}（按单位产量计价）` : `${(rate * 100).toFixed(4)}%`;
  out.push({
    level: 'P0', category: '应提取金额复算不符', line: it.line,
    message: `${who(it)}：${caliberName}口径基数 ${base.toFixed(2)} × 提取比例 ${rateShown} = ${expect.toFixed(2)}，`
      + `表里「应提取金额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '应提取金额就是"计提基数 × 提取比例"：提少了是提取不足（监管处罚项），提多了是专户余额虚高。',
  });
  return out;
}

function checkBalanceRolling(it) {
  const out = [];
  const begin = normNumber(it.balanceBegin);
  const extract = normNumber(it.extract);
  const use = normNumber(it.use);
  const stated = normNumber(it.balanceEnd);
  if (begin === null || extract === null || use === null || stated === null) return out;
  const expect = round2(begin + extract - use);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '期末余额滚动复算不符', line: it.line,
    message: `${who(it)}：期初余额 ${begin.toFixed(2)} + 本期提取 ${extract.toFixed(2)} − 本期使用 ${use.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「期末余额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '专户余额滚不动，后面每一期的期初余额都会跟着错（下一期的期初就是这一期的期末）。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
    if (!n) continue;
    const expect = round2(sum);
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是月报与监管报表的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    if (!p) continue;
    const key = `${p}|${subjectKeyOf(it)}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一核算主体重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一核算主体再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一专户被拆成两行（比如按月又按项目各建一行），'
          + '多出来的那一行会把应提取金额与本期使用都重复计一遍。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列（本期没有使用也要写 0.00），别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = role === 'rate' ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = role === 'rate'
      ? (isPerUnitRate(it[role]) ? `${v}（按单位产量计价）` : `${(v * 100).toFixed(4)}%`)
      : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额或比例为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 营业收入、产量、应提取金额、余额、提取与使用都不该为负，`
        + '冲回 / 红字应单独列示并在备注里说明。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 按行业类别的**内置参考下限**（比例口径）。⚠️ 不是法律认定：取值保守，
 *  只用来抓"明显按旧标准提、或者行业类别填错"这类差一个量级的错。 */
function groupBySubject(items) {
  const m = new Map();
  for (const it of items) {
    const k = subjectKeyOf(it);
    if (!m.has(k)) m.set(k, { subject: k, rows: [] });
    m.get(k).rows.push(it);
  }
  return m;
}

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到安全生产费用提取与使用核对表正文（text）—— 请把「所属期间 / 行业类别 / 核算主体 / 营业收入 / 产量 / 提取比例 / 应提取金额 / 期初余额 / 本期提取 / 本期使用 / 期末余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `安全生产费用提取与使用核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (t.roles.indexOf('revenue') < 0 && t.roles.indexOf('output') < 0) {
    return insufficient([
      '核对表里既没有「营业收入」列，也没有「产量」列 —— 计提基数无从取数（营业收入口径与产量口径至少要有一列）',
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何安全生产费用提取明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkShouldExtractRecompute(it));
    findings.push(...checkBalanceRolling(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let shouldExtractTotal = 0;
  let extractTotal = 0;
  let useTotal = 0;
  let balanceEndTotal = 0;
  for (const it of t.items) {
    const se = normNumber(it.shouldExtract);
    if (se !== null) shouldExtractTotal += se;
    const ex = normNumber(it.extract);
    if (ex !== null) extractTotal += ex;
    const us = normNumber(it.use);
    if (us !== null) useTotal += us;
    const be = normNumber(it.balanceEnd);
    if (be !== null) balanceEndTotal += be;
  }

  const result = {
    status: 'success',
    service_type: 'SAFETY_PRODUCTION_FEE_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      subjects: groupBySubject(t.items).size,
      totals_row: Boolean(t.totals && t.totals.row),
      should_extract_total: round2(shouldExtractTotal),
      extracted_total: round2(extractTotal),
      used_total: round2(useTotal),
      balance_end_total: round2(balanceEndTotal),
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: groups.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"计提基数 × 提取比例 = 应提取金额"与"期初余额 + 本期提取 − 本期使用 = 期末余额"这类**表内勾稽**与档位提示，'
      + '**不判断某家企业该按哪个行业标准、哪个基数提取**（以现行规定原文与会计师口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
