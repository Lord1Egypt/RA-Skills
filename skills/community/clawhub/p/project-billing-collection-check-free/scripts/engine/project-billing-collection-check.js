/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * project-billing-collection-check.js —— 项目开票与回款核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**软件 / 工程服务类项目每月核账时**（月度结账、开票与回款例会、
 * 收入确认前），财务与项目经理要按**项目 × 期间**把这张台账核一遍 ——
 * **合同额、已验收、已开票、已回款、未开票余额**。
 * 这五个数直接决定**现金流预测**与**收入确认进度**：开票少了压现金流，开票超验收又会让收入确认站不住。
 * 完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   未开票余额   = 已验收 − 已开票          （已验收但还没开票的部分）
 *   未回款       = 已开票 − 已回款          （开了票但钱还没到）
 *   合计行各列   = 各项目各期间之和
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**发票真伪、收入确认时点与账龄口径：账期天数只作**参考**，
 *    超期只做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '已开票 + 未开票余额 = 已验收金额复算（未开票余额 = 已验收 − 已开票）',
  '未回款复算（未回款 = 已开票 − 已回款）',
  '合计行逐列复核',
  '同一项目同一期重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '已开票超过已验收金额提示（开票进度快于验收进度）',
  '回款超过开票金额检测（回款多于已开票，必有串期或记错）',
  '未回款超过参考账期（如 90 天）提示（参考口径）',
  '验收进度与开票进度严重不匹配（差超 30 个百分点）提示',
  '合同额为零却有开票检测',
];

const OUT_OF_SCOPE = [
  '判断发票真伪、是否已送达对方与对方是否已入账（请以发票查验平台与对账函为准）',
  '确定收入确认时点与完工百分比口径（以会计准则与合同约定的履约义务为准）',
  '判断账期本身是否合理、是否构成逾期违约（以合同付款条款为准）',
  '核对合同额本身的准确性（是否含税、是否含变更签证，需与合同原件核对）',
  '读取财务系统 / 发票系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考账期：仅供"明显超期"时提示，不是认定 */
const CREDIT_DAYS_REF = 90;
/* 验收与开票进度的"严重不匹配"阈值：30 个百分点 */
const PROGRESS_GAP_REF = 30;

const SAMPLE_TEXT = [
  '项目名称\t期间\t合同额\t已验收金额\t已开票金额\t已回款金额\t未开票余额\t未回款金额\t账期天数\t开票日期',
  '信贷核心系统\t2026-01\t1200000.00\t200000.00\t150000.00\t150000.00\t50000.00\t0.00\t30\t2026-01-20',
  '信贷核心系统\t2026-02\t1200000.00\t300000.00\t250000.00\t250000.00\t50000.00\t0.00\t30\t2026-02-20',
  '信贷核心系统\t2026-03\t1200000.00\t400000.00\t150000.00\t0.00\t250000.00\t150000.00\t30\t2026-03-20',
  '数据中台建设\t2026-01\t860000.00\t200000.00\t150000.00\t150000.00\t50000.00\t0.00\t45\t2026-01-25',
  '数据中台建设\t2026-02\t860000.00\t200000.00\t200000.00\t200000.00\t0.00\t0.00\t45\t2026-02-25',
  '数据中台建设\t2026-03\t860000.00\t300000.00\t300000.00\t0.00\t0.00\t300000.00\t45\t2026-03-25',
  '合计\t\t2060000.00\t1600000.00\t1200000.00\t750000.00\t400000.00\t450000.00\t\t',
].join('\n');

const TOL = 0.01;              // 金额容差（分）
const PCT_TOL = 0.0001;        // 进度百分点容差

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**，否则列会被抢走（静默算错）。
  //    「未开票余额」不能被「已开票」抢走；「未回款金额」不能被「已回款」抢走，也不能被「未回款」抢走；
  //    「开票日期」必须排在「已开票」之前；「未回款金额」必须排在「未回款」之前。
  // 「未X」在「已X」之前、「X金额」在「X」之前：`开票金额`/`回款金额` 这类宽泛词
  // 一旦排在前面，就会把 `未开票余额`/`未回款金额` 整列抢走（本轮被表头守卫实测抓出）。
  period: ['期间', '所属期', '账期月份', '月份'],
  project: ['项目名称', '项目', '工程名称', '合同名称'],
  contract: ['合同额', '合同金额', '合同总额', '合同价'],
  accepted: ['已验收金额', '已验收', '验收金额', '已确认收入'],
  unbilled: ['未开票余额', '未开票金额', '待开票金额', '未开票'],
  unpaid: ['未回款金额', '回款差额', '未回款', '欠款金额'],
  invoiced: ['已开票金额', '开票金额', '已开票', '累计开票'],
  invoiceDate: ['开票日期', '开票日', '发票日期'],
  collected: ['已回款金额', '回款金额', '已回款', '累计回款'],
  days: ['账期天数', '账期', '信用期', '回款天数'],
};

const LABELS = {
  period: '期间', project: '项目名称', contract: '合同额', accepted: '已验收金额',
  unbilled: '未开票余额', invoiced: '已开票金额', collected: '已回款金额',
  unpaid: '未回款金额', days: '账期天数', invoiceDate: '开票日期',
};

const REQUIRED = ['period', 'project', 'contract', 'accepted', 'invoiced', 'collected', 'unbilled'];
const NUM_ROLES = ['contract', 'accepted', 'invoiced', 'collected', 'unbilled', 'unpaid'];
const SUM_ROLES = ['contract', 'accepted', 'invoiced', 'collected', 'unbilled', 'unpaid'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|全年合计)$/;
const PLACEHOLDER = /^(n\/?a|无|待填|待补|待定|--|-—–|\/)$/i;

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
  return s === '' || /^[-—–]+$/.test(s) || PLACEHOLDER.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  if (!h) return null;
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

const money = (n) => (n < 0 ? '-' : '') + Math.abs(round2(n)).toFixed(2);

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
      // 合计行判定：只要「期间」或「项目名称」列写着合计/总计就算
      if ((role === 'period' || role === 'project') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && it.project ? String(it.project).trim() : '';
  const d = it && it.period ? String(it.period).trim() : '';
  if (p && d) return `${p} ${d} 期`;
  if (d) return `${d} 期`;
  if (p) return `${p}（第 ${it && it.line} 行）`;
  return `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

/** 已开票 + 未开票余额 = 已验收金额（等价于 未开票余额 = 已验收 − 已开票） */
function checkUnbilledClosure(it) {
  const acc = normNumber(it.accepted);
  const inv = normNumber(it.invoiced);
  const unb = normNumber(it.unbilled);
  if (acc === null || inv === null || unb === null) return null;
  const expect = round2(acc - inv);
  if (Math.abs(expect - unb) <= TOL) return null;
  return {
    level: 'P0', category: '未开票余额与合同已验收金额不符', line: it.line,
    message: `${who(it)}：已验收 ${money(acc)} − 已开票 ${money(inv)} = ${money(expect)}，`
      + `但表里未开票余额是 ${money(unb)}，相差 ${money(unb - expect)}`
      + '（未开票余额就是已验收但还没开票的部分，两者必须相等）。',
  };
}

/** 未回款 = 已开票 − 已回款 */
function checkUnpaidClosure(it) {
  const inv = normNumber(it.invoiced);
  const got = normNumber(it.collected);
  const unpaid = normNumber(it.unpaid);
  if (inv === null || got === null || unpaid === null) return null;
  const expect = round2(inv - got);
  if (Math.abs(expect - unpaid) <= TOL) return null;
  return {
    level: 'P0', category: '未回款与已开票金额不符', line: it.line,
    message: `${who(it)}：已开票 ${money(inv)} − 已回款 ${money(got)} = ${money(expect)}，`
      + `但表里未回款是 ${money(unpaid)}，相差 ${money(unpaid - expect)}。`,
  };
}

/** 合计行逐列复核（一列一条发现，返回数组，调用处用 for...of 展开）
 *
 * ⚠️ 「合同额」是**项目级常量**：同一项目的每一期都会重复写同一个合同额，
 *    按行直接相加会重复计算（2 个项目 6 行 ⇒ 虚增 3 倍，本轮实测就是这条假报）。
 *    所以合同额按**项目去重后**相加，其余各列按行相加。
 */
function totalRowFindings(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  if (role === 'contract') {
    const byProject = new Map();
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v === null) continue;
      const p = String(it.project === undefined ? '' : it.project).trim() || `__line${it.line}`;
      if (!byProject.has(p)) byProject.set(p, v);      // 同一项目只取一次
    }
    for (const v of byProject.values()) sum += v;
    n = byProject.size;
  } else {
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${money(stated)}，`
      + (role === 'contract' ? '各项目合同额相加' : '各行相加')
      + `是 ${money(sum)}，相差 ${money(stated - sum)}。`,
  });
  return out;
}

/** 同一项目同一期重复行检测 */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = String(it.project === undefined ? '' : it.project).trim();
    const d = String(it.period === undefined ? '' : it.period).trim();
    if (!p || !d) continue;
    const key = `${p}|${d}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一项目同一期重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行又出现一次`
          + '（同一项目同一期的开票与回款会被重复统计）。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 空白与占位符检测（必需列） */
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

/** 金额为负检测 */
function checkNegatives(it) {
  const out = [];
  for (const role of NUM_ROLES) {
    if (isBlank(it[role])) continue;
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${money(v)}（负数）—— 冲回或红字建议单独列示，`
          + '直接填负数会让合计与进度全部被拉偏。',
      });
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 已开票超过已验收金额提示（开票进度快于验收进度，收入确认可能站不住） */
/** 回款超过开票金额检测（回款多于已开票，必是串期或串项目） */
/** 未回款超过参考账期（如 90 天）提示 */
/** 验收进度与开票进度严重不匹配（差超 30 个百分点）提示 */
/** 合同额为零却有开票检测 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到台账正文（text）—— 请把「项目名称 / 期间 / 合同额 / 已验收 / 已开票 / 已回款 / 未开票余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何项目期间明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkUnbilledClosure(it); if (a) findings.push(a);
    const b = checkUnpaidClosure(it); if (b) findings.push(b);
    for (const x of checkNegatives(it)) findings.push(x);

  }
  for (const role of SUM_ROLES) {
    for (const f of totalRowFindings(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const colTotals = {};
  for (const role of SUM_ROLES) {
    // 合同额按项目去重（项目级常量，逐行相加会重复计算）；其余各列按行相加
    const byProject = role === 'contract' ? new Map() : null;
    let sum = 0;
    for (const it of t.items) {
      const v = normNumber(it[role]);
      if (v === null) continue;
      if (byProject) {
        const p = String(it.project === undefined ? '' : it.project).trim() || `__line${it.line}`;
        if (!byProject.has(p)) byProject.set(p, v);
      } else sum += v;
    }
    if (byProject) for (const v of byProject.values()) sum += v;
    colTotals[role] = round2(sum);
  }
  const periods = new Set();
  for (const it of t.items) {
    const d = String(it.period === undefined ? '' : it.period).trim();
    if (d) periods.add(d);
  }

  const result = {
    status: 'success',
    service_type: 'PROJECT_BILLING_COLLECTION_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      totals: colTotals,
      credit_days_ref: CREDIT_DAYS_REF,
      progress_gap_ref: PROGRESS_GAP_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核「未开票余额 = 已验收 − 已开票」「未回款 = 已开票 − 已回款」这类内部勾稽与合计复算，'
      + '**不判断**发票真伪、收入确认时点与账期合理性（以合同付款条款与会计准则为准）；'
      + '账期超期与进度差异均为**参考提示**；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
