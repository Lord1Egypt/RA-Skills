/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * group-intercompany-reconciliation-check.js —— 集团内部往来对账与抵消核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月合并报表之前**。集团内各子公司之间的往来与交易，
 * 两边必须对得上、并且抵消干净：
 *
 *   双方差额   = 本方余额 − 对方余额              （对得上才是 0；不为 0 就得挂账查原因）
 *   抵消金额   = min(往来余额, 本期内部交易额)     （抵消不能超过账上往来余额，也不能超过本期交易额）
 *   合计行各列 = 明细行相加
 *
 * 这三条都是**表内勾稽**：每一格都能手算复现，所以"对不对"完全可以机械核出来 ——
 * 而对不上的后果很硬：一处挂账、一行抵消错，整个合并报表就是错的。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某笔内部往来该不该抵消、抵消后还有没有未实现内部利润（那属于合并会计判断）：
 *    表里给的余额、交易额、抵消额一律**以你填的为准**，本工具只核表内勾稽与档位提示。
 *
 * 档位分工（刻意如此，两档不是同一件事的粗细两版）：
 *   · 免费档核**表内算术**：差额列必须等于两余额之差、抵消金额必须等于孰低、合计勾稽、重复与空缺；
 *   · 完整档核**业务实质**：双方余额到底对不对得上（差额超容差的挂账风险）、应收应付有没有抵干净、
 *     有没有超抵消、内部交易有没有配比、同一个主体是不是被写成了两个名字。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚。
 */

const CHECKS_GIVEN = [
  '双方差额 = 本方余额 − 对方余额 复算（差额列必须等于两余额之差；对得上的表必须为 0）',
  '抵消金额 = 往来余额与内部交易额孰低 复算',
  '合计行逐列复核',
  '同一往来单位重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '双方差额超过容差提示（双方账面没对上的挂账风险）',
  '同一对往来主体方向相反（一方应收一方应付）未抵消干净提示',
  '抵消金额超过往来余额提示（超抵消）',
  '内部交易未配比（有销售无采购）提示',
  '往来单位名称疑似同一主体多写法提示（名称包含关系）',
];

const OUT_OF_SCOPE = [
  '判断某笔内部往来到底该不该抵消、按什么口径抵消（权益法/成本法、未实现内部利润、递延所得税，属于合并会计判断，请咨询会计师）',
  '核对内部交易定价是否公允、是否属于需要披露的关联交易（那属于转让定价与披露事项）',
  '处理外币内部往来的折算差额、内部往来的减值与核销（表里必须你自己给成同一币种口径）',
  '读取 ERP / 财务系统或合并报表软件导出的文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t本方公司\t往来单位\t科目方向\t交易类型\t本方余额\t对方余额\t双方差额\t内部交易额\t抵消金额',
  '2026-01\t甲集团\t乙公司\t应收\t销售\t1000.00\t1000.00\t0.00\t1000.00\t1000.00',
  '2026-01\t乙公司\t甲集团\t应付\t采购\t1000.00\t1000.00\t0.00\t1000.00\t1000.00',
  '2026-02\t甲集团\t乙公司\t应收\t销售\t1000.00\t1000.00\t0.00\t1000.00\t1000.00',
  '2026-02\t乙公司\t甲集团\t应付\t采购\t1000.00\t1000.00\t0.00\t1000.00\t1000.00',
  '合计\t\t\t\t\t4000.00\t4000.00\t0.00\t4000.00\t4000.00',
].join('\n');

const TOL = 0.01;                 // 金额容差：分
const ELIM_TOL = 1.00;            // 抵消金额常按元取整 ⇒ 孰低复算允许 1 元以内的取整差
const NAME_MIN = 2;               // 名称包含关系只在"短名至少 2 个字"时才提示（1 个字会满屏误报）

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「本方余额」不能被「本方公司」抢走、「内部交易额」不能被「交易类型」抢走）
  period: ['会计期间', '所属期间', '所属期', '期间', '月份', '月度'],
  selfEntity: ['本方公司', '本方主体', '本方单位', '编制单位', '本公司', '本企业'],
  counterparty: ['内部往来单位', '往来单位', '对方单位', '对方公司', '对方主体', '交易对方', '往来客户', '往来供应商'],
  direction: ['科目方向', '往来方向', '核算方向', '余额方向', '方向'],
  txnType: ['内部交易类型', '交易类型', '业务类型', '交易性质', '往来类型', '类型'],
  selfBalance: ['本方账面余额', '本方挂账余额', '本方余额', '本单位余额'],
  cpBalance: ['对方账面余额', '对方挂账余额', '对方单位余额', '对方余额'],
  difference: ['双方差额', '对账差额', '余额差额', '往来差额', '差额', '差异'],
  txnAmount: ['本期内部交易额', '内部交易金额', '内部交易额', '交易金额', '交易额', '发生额'],
  elimination: ['内部抵消金额', '合并抵消金额', '抵消金额', '抵销金额', '抵消额', '抵销额'],
};

const LABELS = {
  period: '期间', selfEntity: '本方公司', counterparty: '往来单位', direction: '科目方向',
  txnType: '交易类型', selfBalance: '本方余额', cpBalance: '对方余额',
  difference: '双方差额', txnAmount: '内部交易额', elimination: '抵消金额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'selfEntity', 'counterparty', 'direction', 'txnType',
  'selfBalance', 'cpBalance', 'difference', 'txnAmount', 'elimination'];
/** 合计行逐列复核的列（这 5 列都是明细行的直接加总，没有去重口径） */
const SUM_ROLES = ['selfBalance', 'cpBalance', 'difference', 'txnAmount', 'elimination'];
/**
 * 免费档负值检测覆盖的列。
 * ⚠️ 刻意**不含**「双方差额」：差额为负只表示本方余额小于对方余额，是**正常方向**，不是错误
 *    （真正的问题"差额不为 0"由完整档的容差提示项管）。
 */
const NEGATIVE_ROLES = ['selfBalance', 'cpBalance', 'txnAmount', 'elimination'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|合计:)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|不详)$/i.test(s);
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
  const n = [it && it.selfEntity, it && it.counterparty]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' → ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const counterpartyKeyOf = (it) => {
  const c = it && it.counterparty !== undefined ? String(it.counterparty).trim() : '';
  return c || `第 ${it && it.line} 行`;
};

const directionKeyOf = (it) => {
  const d = it && it.direction !== undefined ? String(it.direction).trim() : '';
  return d || '(未填方向)';
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

/**
 * 双方差额 = 本方余额 − 对方余额（复算）。
 * 这里核的是**差额列本身**：它必须等于两余额之差；对得上的表这一列就是 0。
 * 「差额本身超过容差（双方没对上）」由完整档的提示项给出 —— 免费档先把表内算术钉死。
 */
function checkDifferenceRecompute(it) {
  const out = [];
  const self = normNumber(it.selfBalance);
  const cp = normNumber(it.cpBalance);
  const stated = normNumber(it.difference);
  if (self === null || cp === null || stated === null) return out;
  const expect = round2(self - cp);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '双方差额与复算不符', line: it.line,
    message: `${who(it)}：本方余额 ${self.toFixed(2)} − 对方余额 ${cp.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「双方差额」填的是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '双方差额必须等于两余额之差 —— 对得上的内部往来，这一列必须为 0。',
  });
  return out;
}

/**
 * 抵消金额 = min(往来余额, 本期内部交易额)（复算）。
 * 往来余额取**本方账上**的往来余额（编制抵消分录时以本方的内部往来余额为上限）。
 * 抵消金额常按元取整，所以这里允许 ELIM_TOL（1 元）以内的取整差；
 * 「抵消金额超过往来余额」另有完整档的硬约束提示（容差 TOL）。
 */
function checkEliminationRecompute(it) {
  const out = [];
  const base = normNumber(it.selfBalance);
  const txn = normNumber(it.txnAmount);
  const stated = normNumber(it.elimination);
  if (base === null || txn === null || stated === null) return out;
  const expect = round2(Math.min(base, txn));
  if (Math.abs(stated - expect) <= ELIM_TOL) return out;
  out.push({
    level: 'P0', category: '抵消金额与孰低复算不符', line: it.line,
    message: `${who(it)}：往来余额 ${base.toFixed(2)} 与本期内部交易额 ${txn.toFixed(2)} 孰低是 ${expect.toFixed(2)}，`
      + `表里「抵消金额」填的是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '抵消金额就是这两个数的较小者：既不能超过账上的往来余额，也不能超过本期真的发生了的内部交易额。',
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
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是整张表的控制数，它错了后面每一步都错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const s = it.selfEntity !== undefined ? String(it.selfEntity).trim() : '';
    const c = it.counterparty !== undefined ? String(it.counterparty).trim() : '';
    const d = directionKeyOf(it);
    if (!p || !c) continue;
    const key = `${p}|${s}|${c}|${d}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一往来单位重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过（期间 / 本方公司 / 往来单位 / 科目方向 完全相同），`
          + `第 ${it.line} 行又出现一次 —— 要么是重复粘贴了一行，要么是同一笔往来被拆成了两行，`
          + '多出来的那一行会把余额、交易额与抵消额都重复计一遍。',
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

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— `
        + '本方余额、对方余额、内部交易额与抵消金额都不该为负；'
        + '红字冲回、超付或方向记反应当单独列示并在备注里说明。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 双方余额本身对不上（超过容差）⇒ 这一对往来就是挂账的 */
/** 抵消金额超过本方账上的往来余额 ⇒ 超抵消 */
/** 方向归类：先认「应付」再认「应收」（"其他应收款"里没有"应付"，反过来也成立） */
/** 交易类型归类：一方销售 ⇄ 另一方采购 */
/** 同一对往来主体（无序）在同一期间归为一组：一对主体的两边必须成对出现 */
/** 同一对主体：一方记应收、另一方记应付 —— 这是同一笔往来的两边，净额必须为 0 才算抵干净 */
/** 同一对主体的内部交易必须成对：一方销售 ⇄ 另一方采购，且金额一致 */
/** 往来单位名称疑似同一主体多写法：短名是长名的子串 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到集团内部往来对账与抵消核对表正文（text）—— 请把「期间 / 本方公司 / 往来单位 / 科目方向 / 交易类型 / 本方余额 / 对方余额 / 双方差额 / 内部交易额 / 抵消金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `集团内部往来对账与抵消核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何内部往来明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkDifferenceRecompute(it));
    findings.push(...checkEliminationRecompute(it));
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

  let eliminationTotal = 0;
  for (const it of t.items) {
    const v = normNumber(it.elimination);
    if (v !== null) eliminationTotal += v;
  }

  const result = {
    status: 'success',
    service_type: 'GROUP_INTERCOMPANY_RECONCILIATION_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      elimination_total: round2(eliminationTotal),
      tolerance: TOL,
      elimination_tolerance: ELIM_TOL,
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
    disclaimer: '只核"双方差额 = 本方余额 − 对方余额"、"抵消金额 = 往来余额与交易额孰低"这类**表内勾稽**与档位提示，'
      + '**不判断某笔内部往来该不该抵消、按什么口径抵消**（以合并会计准则与会计师口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
