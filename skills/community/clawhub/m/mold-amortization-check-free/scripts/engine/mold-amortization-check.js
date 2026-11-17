/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * mold-amortization-check.js —— 模具与工装摊销核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月成本核算与结账之前**，制造企业要把模具与工装
 * （注塑模、冲压模、压铸模、检具、夹具、专用工装等）的摊销台账核一遍。
 * 模具/工装**单体金额大**（几万到几百万），按产量（或按月份）摊进产品成本，
 * 摊销额直接进**当期产品成本与毛利**；而这张表必须和**产量**、**剩余价值**勾稽：
 * 摊销总额、摊销总产量、本期产量、本期摊销、累计摊销、未摊销余额，这几列得自洽。
 * 完全能用手算复现，所以对错可以机械判定。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   本期摊销额 = 可摊销总额 ÷ 摊销总产量 × 本期产量   （产量法）
 *   未摊销余额 = 可摊销总额 − 累计摊销
 *   摊销单价   = 可摊销总额 ÷ 摊销总产量（参考口径：同一副模具各期单价应为常数）
 *   合计行     = 各明细行**逐列**相加
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**该不该资本化、按产量还是按月份摊销、摊销年限与残值率（各厂各产品不同），
 *    只核台账**内部勾稽**；摊销单价的参考区间取**同表理论单价中位数 ±50%**，只作提示，不是定价标准。
 *
 * 返回值形状提醒（维护者）：所有逐行检查函数**一律返回数组**，调用处一律 `for...of` 展开；
 * 混用"对象或 null"会让空数组被 `if (x)` 当成一条发现（静默多报），不要再改回去。
 */

const CHECKS_GIVEN = [
  '本期摊销额复算（可摊销总额 ÷ 摊销总产量 × 本期产量）',
  '未摊销余额复算（可摊销总额 − 累计摊销）',
  '合计行逐列复核',
  '同一模具编号重复行检测',
  '空白与占位符检测',
  '金额或数量为负检测',
];

const CHECKS_WITHHELD = [
  '累计摊销超过可摊销总额提示',
  '本期产量超过摊销总产量检测',
  '摊销总额为零却有摊销额检测',
  '未摊销余额为负检测',
  '摊销单价偏离参考区间（同表理论单价中位数 ±50%）提示',
];

const OUT_OF_SCOPE = [
  '判断模具/工装该不该资本化、按产量法还是按月份摊销、摊销年限与残值率是否合理（那属于会计政策与产品工艺）',
  '核对「摊销总产量」这个预计总量本身是否靠谱（要工艺与生产部门确认）',
  '处理模具报废、处置、对外销售或移交供应商时未摊销余额的结转',
  '核对摊销额在在制品/产成品/主营业务成本之间的分摊与结转',
  '读取 ERP 或 Excel 导出文件（需要你先导出成文本贴进来）',
];

/* 摊销单价的参考区间：同表理论单价中位数 ±50%，只用于"明显偏离"时提示 */
const UNIT_RATE_DEV = 0.5;

const SAMPLE_TEXT = [
  '模具编号\t模具名称\t期间\t可摊销总额\t摊销总产量\t本期产量\t摊销单价\t本期摊销额\t累计摊销\t未摊销余额',
  'MJ-001\tA产品外壳注塑模\t2026-06\t480000.00\t120000\t12000\t4.00\t48000.00\t144000.00\t336000.00',
  'MJ-002\tB产品面板冲压模\t2026-06\t240000.00\t60000\t6000\t4.00\t24000.00\t72000.00\t168000.00',
  'GZ-003\t焊接工装夹具\t2026-06\t360000.00\t90000\t9000\t4.00\t36000.00\t108000.00\t252000.00',
  '合计\t\t\t1080000.00\t270000\t27000\t\t108000.00\t324000.00\t756000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的别名前面，角色之间也一样。
  //    「摊销总产量」排「产量」前面（否则被抢走）；「摊销单价」排「摊销额」前面；
  //    「可摊销总额」排「摊销总额」前面（否则两列落到同一角色，后一列盖掉前一列）。
  moldNo: ['模具编号', '模具编码', '工装编号', '模具号', '工装号', '夹具编号', '检具编号'],
  moldName: ['模具名称', '工装名称', '模具品名', '工装品名', '名称'],
  period: ['所属期间', '会计期间', '摊销期间', '所属月份', '期间', '月份'],
  amortTotal: ['可摊销总额', '待摊销总额', '应摊销总额', '可摊销金额', '摊销总额', '模具原值', '工装原值'],
  totalOutput: ['摊销总产量', '预计总产量', '计划总产量', '标准总产量', '总产量'],
  periodOutput: ['本期产量', '当期产量', '本月产量', '本期完工量', '本期产出', '产量'],
  unitRate: ['摊销单价', '单位摊销额', '单位摊销', '摊销率'],
  // ⚠️「累计摊销额」必须排在「摊销额」前面（实测踩过：'累计摊销额'.indexOf('摊销额') >= 0，
  //    顺序写反时本期摊销额整列被累计摊销抢走，两列落到同一角色，静默算错）。
  accumAmort: ['累计摊销额', '累计已摊销', '已摊销金额', '累计摊销'],
  periodAmort: ['本期摊销额', '当期摊销额', '本期摊销', '本月摊销', '摊销额'],
  remaining: ['未摊销余额', '未摊销金额', '未摊余额', '剩余价值', '摊余价值', '账面余额'],
};

const LABELS = {
  moldNo: '模具编号', moldName: '模具名称', period: '期间', amortTotal: '可摊销总额',
  totalOutput: '摊销总产量', periodOutput: '本期产量', unitRate: '摊销单价',
  periodAmort: '本期摊销额', accumAmort: '累计摊销', remaining: '未摊销余额',
};

const REQUIRED = ['moldNo', 'period', 'amortTotal', 'totalOutput', 'periodOutput', 'periodAmort', 'accumAmort', 'remaining'];
const SUM_ROLES = ['amortTotal', 'totalOutput', 'periodOutput', 'periodAmort', 'accumAmort', 'remaining'];
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|暂估)$/i.test(s);
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
      if ((role === 'moldNo' || role === 'period') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  if (!it) return '该行';
  const no = it.moldNo ? String(it.moldNo).trim() : '';
  const pd = it.period ? String(it.period).trim() : '';
  if (no && pd) return `${no}（${pd}）`;
  if (no) return no;
  return `第 ${it.line} 行`;
};

const fmt = (v) => (Math.abs(v - Math.round(v)) <= 1e-9 ? String(Math.round(v)) : String(round2(v)));

/* ================================ 免费档检查项 ================================ */

function checkPeriodAmort(it) {
  const total = normNumber(it.amortTotal);
  const totalOut = normNumber(it.totalOutput);
  const out = normNumber(it.periodOutput);
  const stated = normNumber(it.periodAmort);
  if (total === null || totalOut === null || out === null || stated === null) return [];
  if (totalOut <= 0) return [];
  const expect = round2(total / totalOut * out);
  if (Math.abs(expect - stated) <= TOL) return [];
  return [{
    level: 'P0', category: '本期摊销额与复算不符', line: it.line,
    message: `${who(it)}：可摊销总额 ${total.toFixed(2)} ÷ 摊销总产量 ${fmt(totalOut)} × 本期产量 ${fmt(out)} 应为 ${expect.toFixed(2)}，表里本期摊销额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  }];
}

function checkRemaining(it) {
  const total = normNumber(it.amortTotal);
  const acc = normNumber(it.accumAmort);
  const stated = normNumber(it.remaining);
  if (total === null || acc === null || stated === null) return [];
  const expect = round2(total - acc);
  if (Math.abs(expect - stated) <= TOL) return [];
  return [{
    level: 'P0', category: '未摊销余额与复算不符', line: it.line,
    message: `${who(it)}：可摊销总额 ${total.toFixed(2)} − 累计摊销 ${acc.toFixed(2)} 应为 ${expect.toFixed(2)}，表里未摊销余额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  }];
}

function checkNegatives(it) {
  const out = [];
  // ⚠️ 只查**输入列**（可摊销总额/产量/本期摊销/累计摊销/单价）为负；
  //    「未摊销余额为负」是**派生结果**的反常，属完整档的增量检查，这里不重复报
  //    （重复报会让"完整档命中、免费档不报"的对照用例失去区分力）。
  for (const [role, label] of [['amortTotal', '可摊销总额'], ['totalOutput', '摊销总产量'], ['periodOutput', '本期产量'],
    ['periodAmort', '本期摊销额'], ['accumAmort', '累计摊销'], ['unitRate', '摊销单价']]) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '金额或数量为负', line: it.line,
        message: `${who(it)}的「${label}」是 ${round2(v).toFixed(2)}（负数）—— 冲回或处置请单独列示，负数会让本期分摊与余额反向。`,
      });
    }
  }
  return out;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const no = String(it.moldNo || '').trim();
    if (!no) continue;
    const pd = String(it.period || '').trim();
    const key = `${no}|${pd}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一模具编号重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过（同一模具编号 + 同一期间），第 ${it.line} 行再次出现 —— 摊销会被重复计算。`,
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
        });
      }
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 参考基准：同表各行的理论单价（可摊销总额 ÷ 摊销总产量）的中位数 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到摊销台账正文（text）—— 请把「模具编号 / 期间 / 可摊销总额 / 摊销总产量 / 本期产量 / 本期摊销额 / 累计摊销 / 未摊销余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `摊销台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何模具/工装明细行');
  }

  const findings = [];
  for (const it of t.items) {
    for (const f of checkPeriodAmort(it)) findings.push(f);
    for (const f of checkRemaining(it)) findings.push(f);
    for (const f of checkNegatives(it)) findings.push(f);
  }

  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const periodSet = new Set();
  let amortTotal = 0; let accumTotal = 0; let remainTotal = 0;
  for (const it of t.items) {
    const pd = String(it.period || '').trim();
    if (pd) periodSet.add(pd);
    const a = normNumber(it.amortTotal); if (a !== null) amortTotal += a;
    const b = normNumber(it.accumAmort); if (b !== null) accumTotal += b;
    const c = normNumber(it.remaining); if (c !== null) remainTotal += c;
  }

  const result = {
    status: 'success',
    service_type: 'MOLD_AMORTIZATION_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periodSet.size,
      period_list: [...periodSet].sort(),
      amort_total: round2(amortTotal),
      amortized_total: round2(accumTotal),
      remaining_total: round2(remainTotal),
      unit_rate_ref_dev: UNIT_RATE_DEV,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periodSet.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行 ${CHECKS_GIVEN.length} 项（见 scope.checks）；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核台账内部勾稽（可摊销总额 / 摊销总产量 / 本期产量 / 本期摊销额 / 累计摊销 / 未摊销余额），'
      + '**不判断该不该资本化、摊销方法与年限是否合理**；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
