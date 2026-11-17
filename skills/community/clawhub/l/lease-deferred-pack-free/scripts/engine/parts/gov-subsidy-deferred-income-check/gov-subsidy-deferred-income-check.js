/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * gov-subsidy-deferred-income-check.js —— 政府补助与递延收益核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**年度 / 每月结账前**。企业收到的政府补助分两类，两类都要
 * 按 CAS 16（政府补助）逐期"搬"进损益：
 *
 *   · 与资产相关的补助 —— 先全额挂**递延收益**，在相关资产的**使用寿命内**按合理、
 *     系统的方法分期计入损益（其他收益 / 营业外收入）；
 *   · 与收益相关的补助 —— 用于补偿以后期间费用的，先挂递延收益，在**确认相关费用的期间**
 *     计入损益；用于补偿已发生费用的，直接计入当期损益。
 *
 * 所以这张表每个月都在滚两条账，而且两条互相咬死：
 *
 *   本期分摊额     = 补助总额 ÷ 分摊期数（直线法，按分摊期数分摊）
 *   期末递延余额   = 期初递延余额 + 本期新增补助 − 本期确认收益
 *
 * 分摊错了就是**利润与递延收益双错**：摊多了 → 其他收益虚增、递延收益虚减；摊少了则相反。
 * 递延收益是审计必查的科目（"递延收益的摊销是否与资产使用寿命匹配"是标准审计程序），
 * 而这张表每一格都能手算复现，所以"对不对"完全可以机械核出来。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某笔补助属于与资产相关还是与收益相关、该用总额法还是净额法、
 *    什么时候确认（那属于会计判断）：表里给的补助总额、分摊期数、资产使用年限一律
 *    **以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 if 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '本期分摊额复算（补助总额 ÷ 分摊期数 = 本期分摊额）',
  '期末递延余额滚动复算（期初递延余额 + 本期新增补助 − 本期确认收益 = 期末递延余额）',
  '合计行逐列复核',
  '同一补助文件号重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '分摊额超过补助总额提示',
  '递延余额为负检测',
  '与资产相关但无对应资产入账提示',
  '分摊期数与资产使用年限不一致提示',
  '已全额确认仍有递延余额提示',
];

const OUT_OF_SCOPE = [
  '判断某笔政府补助属于与资产相关还是与收益相关、该用总额法还是净额法（属于会计判断，请咨询会计师）',
  '判断补助的确认时点（收到时 / 满足所附条件时）以及是否需要返还（附条件补助的会计处理）',
  '核对补助文件条款本身（专项用途、配套自筹、验收条件、拨付进度）对分摊口径的影响',
  '处理企业所得税（不征税收入与递延收益的税会差异）、增值税以及补助资金的专账管理',
  '读取财政一体化系统 / 银行流水 / ERP 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t补助项目名称\t补助文件号\t补助类型\t补助总额\t资产入账金额\t资产使用年限\t分摊期数\t期初递延余额\t本期新增补助\t本期分摊额\t本期确认收益\t期末递延余额\t累计已确认收益',
  '2026-01\t智能制造设备补助\t财建〔2026〕15号\t与资产相关\t600000.00\t600000.00\t120\t120\t0.00\t600000.00\t5000.00\t5000.00\t595000.00\t5000.00',
  '2026-02\t智能制造设备补助\t财建〔2026〕15号\t与资产相关\t600000.00\t600000.00\t120\t120\t595000.00\t0.00\t5000.00\t5000.00\t590000.00\t10000.00',
  '2026-01\t稳岗补贴\t财建〔2026〕22号\t与收益相关\t30000.00\t0.00\t0\t3\t0.00\t30000.00\t10000.00\t10000.00\t20000.00\t10000.00',
  '2026-02\t稳岗补贴\t财建〔2026〕22号\t与收益相关\t30000.00\t0.00\t0\t3\t20000.00\t0.00\t10000.00\t10000.00\t10000.00\t20000.00',
  '合计\t\t\t\t630000.00\t600000.00\t\t\t\t630000.00\t30000.00\t30000.00\t\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「期初递延余额」不能被别的余额列抢走、
  //    「累计已确认收益」必须排在「本期确认收益」前面、「补助总额」不能被更宽的「补助」抢走）
  period: ['会计期间', '所属期间', '所属期', '期间', '月份', '月度'],
  item: ['补助项目名称', '政府补助项目', '补助项目', '项目名称', '补助名称', '项目'],
  docNo: ['补助文件号', '补助文号', '拨付文件号', '补助编号', '文件号', '批文号', '文号'],
  subsidyType: ['政府补助类型', '补助类型', '补助类别', '补助性质', '补助分类', '类型', '性质'],
  subsidyTotal: ['政府补助总额', '补助总金额', '补助金额合计', '补助款总额', '补助总额', '补助金额'],
  assetAmount: ['固定资产入账金额', '资产入账金额', '资产入账价值', '资产原值', '资产金额', '入账金额'],
  usefulLife: ['资产使用寿命', '资产使用年限', '折旧年限', '资产年限', '使用年限', '使用寿命'],
  periods: ['递延收益分摊期数', '本期分摊期数', '分摊期数', '摊销期数', '分摊月数', '摊销月数', '分摊期限', '期数'],
  deferredBegin: ['期初递延收益余额', '期初递延收益', '期初递延余额', '期初未分摊', '期初余额'],
  addition: ['本期新增补助', '本期收到补助', '本期补助增加', '本期新增', '本期增加'],
  amort: ['本期分摊金额', '本期摊销金额', '本期分摊额', '本期摊销额', '本期分摊'],
  cumulative: ['累计已确认收益', '累计确认收益', '累计已计入损益', '累计已摊销', '累计已确认', '累计确认金额'],
  recognized: ['本期确认收益', '本期计入损益', '本期确认收入', '本期确认', '确认收益'],
  deferredEnd: ['期末递延收益余额', '期末递延收益', '期末递延余额', '期末未分摊', '期末余额'],
};

const LABELS = {
  period: '期间', item: '补助项目名称', docNo: '补助文件号', subsidyType: '补助类型',
  subsidyTotal: '补助总额', assetAmount: '资产入账金额', usefulLife: '资产使用年限',
  periods: '分摊期数', deferredBegin: '期初递延余额', addition: '本期新增补助',
  amort: '本期分摊额', recognized: '本期确认收益', deferredEnd: '期末递延余额',
  cumulative: '累计已确认收益',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'item', 'docNo', 'subsidyType', 'subsidyTotal', 'assetAmount',
  'usefulLife', 'periods', 'deferredBegin', 'addition', 'amort', 'recognized', 'deferredEnd',
  'cumulative'];
/** 合计行逐列复核的列（余额类列不入合计：把各期余额相加没有会计含义） */
const SUM_ROLES = ['subsidyTotal', 'assetAmount', 'addition', 'amort', 'recognized'];
/**
 * 这几列是**按补助文件**的口径：同一份文件会在多个期间各占一行，
 * 补助总额与资产入账金额是文件级属性，合计时只算一次（否则会被重复加总）。
 */
const PER_DOC_ROLES = ['subsidyTotal', 'assetAmount'];
/**
 * 免费档负值检测覆盖的列：**发生额侧**的金额。
 * ⚠️ 刻意**不含**期初 / 期末递延余额 —— "递延余额为负"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出来就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['subsidyTotal', 'assetAmount', 'addition', 'amort', 'recognized'];
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
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null };
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
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.item, it && it.docNo]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const docKeyOf = (it) => {
  const d = it && it.docNo !== undefined ? String(it.docNo).trim() : '';
  return d || `第 ${it && it.line} 行`;
};

/** 补助类型判定：只认**表里填的类型词**，不替用户做会计判断 */
const isAssetRelated = (it) => {
  const t = it && it.subsidyType !== undefined ? String(it.subsidyType).trim() : '';
  return t.indexOf('资产') >= 0;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkAmortRecompute(it) {
  const out = [];
  const total = normNumber(it.subsidyTotal);
  const periods = normNumber(it.periods);
  const stated = normNumber(it.amort);
  if (total === null || periods === null || stated === null) return out;
  if (periods <= 0) return out;                // 分摊期数填 0 或负：算不出每期分摊额（负值由负值检测报）
  const expect = round2(total / periods);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '本期分摊额与分摊复算不符', line: it.line,
    message: `${who(it)}：补助总额 ${total.toFixed(2)} ÷ 分摊期数 ${periods} = ${expect.toFixed(2)}，`
      + `表里「本期分摊额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '与资产相关的补助在资产使用寿命内、与收益相关的补助在确认相关费用的期间，按分摊期数直线摊进损益，'
      + '每期分摊额就是补助总额 ÷ 分摊期数。',
  });
  return out;
}

function checkDeferredRolling(it) {
  const out = [];
  const begin = normNumber(it.deferredBegin);
  const add = normNumber(it.addition);
  const recognized = normNumber(it.recognized);
  const stated = normNumber(it.deferredEnd);
  if (begin === null || add === null || recognized === null || stated === null) return out;
  const expect = round2(begin + add - recognized);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '期末递延余额滚动不符', line: it.line,
    message: `${who(it)}：期初递延余额 ${begin.toFixed(2)} + 本期新增补助 ${add.toFixed(2)} − 本期确认收益 ${recognized.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「期末递延余额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '递延收益就是"已收到但还没摊进损益"的那部分，滚不动后面每一期都会连锁错，'
      + '期末余额还会和资产负债表上的递延收益对不上。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let expect = null;
    let how = '';
    if (PER_DOC_ROLES.indexOf(role) >= 0) {
      const first = new Map();
      for (const it of items) {
        const v = normNumber(it[role]);
        if (v !== null && !first.has(docKeyOf(it))) first.set(docKeyOf(it), v);
      }
      if (!first.size) continue;
      expect = round2(Array.from(first.values()).reduce((a, b) => a + b, 0));
      how = `按补助文件去重后 ${first.size} 份文件的「${LABELS[role]}」相加`;
    } else {
      let sum = 0;
      let n = 0;
      for (const it of items) {
        const v = normNumber(it[role]);
        if (v !== null) { sum += v; n += 1; }
      }
      if (!n) continue;
      expect = round2(sum);
      how = `本表 ${n} 行明细的「${LABELS[role]}」相加`;
    }
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，${how}是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行是月报与审计底稿的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const d = it.docNo !== undefined ? String(it.docNo).trim() : '';
    if (!p || !d) continue;
    const key = `${p}|${d}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一补助文件号重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一补助文件号再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一笔补助被拆成两行（比如分期到账各建一行），'
          + '多出来的那一行会把分摊额与递延余额都重复计一遍。',
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
            + '这一列缺失或写占位符时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查'
            + '（与收益相关的补助没有对应资产时，「资产入账金额」与「资产使用年限」填 0，不要留空）。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 补助总额、资产入账金额、`
        + '本期新增补助、本期分摊额与本期确认收益都不该为负，冲回 / 红字应单独列示并在备注里说明。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到政府补助与递延收益核对表正文（text）—— 请把「期间 / 补助项目名称 / 补助文件号 / 补助类型 / 补助总额 / 资产入账金额 / 资产使用年限 / 分摊期数 / 期初递延余额 / 本期新增补助 / 本期分摊额 / 本期确认收益 / 期末递延余额 / 累计已确认收益」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `政府补助与递延收益核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何补助明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkAmortRecompute(it));
    findings.push(...checkDeferredRolling(it));
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

  const firstTotal = new Map();
  let recognizedTotal = 0;
  for (const it of t.items) {
    const v = normNumber(it.subsidyTotal);
    if (v !== null && !firstTotal.has(docKeyOf(it))) firstTotal.set(docKeyOf(it), v);
    const r = normNumber(it.recognized);
    if (r !== null) recognizedTotal += r;
  }
  let subsidyTotal = 0;
  for (const v of firstTotal.values()) subsidyTotal += v;

  const result = {
    status: 'success',
    service_type: 'GOV_SUBSIDY_DEFERRED_INCOME_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      subsidy_total: round2(subsidyTotal),
      recognized_total: round2(recognizedTotal),
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
    disclaimer: '只核"补助总额 ÷ 分摊期数 = 本期分摊额"与"期初递延余额 + 本期新增补助 − 本期确认收益 = 期末递延余额"'
      + '这类**表内勾稽**与档位提示，**不判断某笔补助属于与资产相关还是与收益相关、该在哪个时点确认**'
      + '（以政府补助准则与会计师口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
