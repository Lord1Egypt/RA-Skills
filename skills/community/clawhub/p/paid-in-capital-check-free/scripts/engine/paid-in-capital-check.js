/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * paid-in-capital-check.js —— 实收资本与股东出资核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**增资 / 股改 / 引入新股东、月度或年度结账、审计与验资要出资底稿之前**。
 * 会计手里的是一张「股东出资明细表」：每位股东认缴多少、累计实缴多少、本期实缴多少、还欠多少、
 * 持股比例多少，以及银行进账、实收资本、资本公积。这几列之间全是加减法，但股东一多、金额一长，
 * 人眼极易漏 —— **一笔"认缴 ≠ 实缴 + 未缴"会带着错一路进报表、进工商公示**，
 * 所以它是"必须做、且完全能算出来对错"的典型。
 *
 * 核心可算关系（都能手算复现）：
 *   未缴出资额        = 认缴出资额 − 累计实缴出资额
 *   累计实缴出资额    ≤ 认缴出资额
 *   该股东持股比例    = 该股东认缴出资额 ÷ 各股东认缴出资额合计
 *   实收资本 + 资本公积 = 认缴合计 − 未缴合计（所有者投入勾稽）
 *   明细逐行相加      = 合计行（认缴 / 累计实缴 / 本期实缴 / 未缴 / 实收资本 / 资本公积 / 银行进账）
 *
 * 输入是一张 Tab 分隔的表（第一行表头）：
 *   股东名称 认缴出资额 累计实缴出资额 本期实缴出资额 未缴出资额 持股比例 银行进账金额 实收资本 资本公积
 * `持股比例` 既接受 `60%`，也接受 `0.6`（小数比例）；合计行（第一列写「合计」）可有可无。
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**出资行为是否合法合规、出资期限是否已过、是否需要催缴，
 *    也不核验银行回单与验资报告的真伪（那属于法律、公司治理与审计程序）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不读环境变量、不写文件**。
 */

/* ⛔ 顺序即优先级：**更具体（带前缀/限定语）的列必须排在裸词前面**（本仓库踩过 4 次的坑，
   `tools/header_map_check.py` 会拦）。
   `认缴出资额` / `累计实缴出资额` / `本期实缴出资额` / `未缴出资额` 四列都含「出资额／实缴」，
   只要出现一个宽泛的 `出资额` 或 `实缴出资额` 键，它就会把这四列**全部抢走**
   （识别出的表头数 > 解析出的列数 ⇒ 后一列把前一列的值盖掉，算错却不报缺列）。 */
const ROLES = {
  shareholder: ['股东名称', '出资人名称', '股东', '出资人'],
  /* 「认缴」三兄弟：先长的、后短的；`累计实缴` / `本期实缴` 都含「实缴」，必须各自成键。 */
  subscribedAmount: ['认缴出资额', '认缴出资', '认缴额', '认缴'],
  cumPaidAmount: ['累计实缴出资额', '累计实缴出资', '累计实缴额', '累计实缴'],
  curPaidAmount: ['本期实缴出资额', '本期实缴出资', '本期实缴额', '本期实缴'],
  unpaidAmount: ['未缴出资额', '未缴出资', '未缴额', '未缴'],
  /* 「持股比例」排在「比例」类键之前；`控股比例` / `股权比例` 都收敛到同一个角色。 */
  ratio: ['持股比例', '出资比例', '股权比例', '股份比例', '控股比例', '比例'],
  bankInAmount: ['银行进账金额', '银行进账额', '银行进账', '进账金额'],
  /* ⛔ `实收资本` 与 `资本公积` 都含「资本」，所以**不许**出现裸词 `资本`；两者互不包含，安全。 */
  paidInCapital: ['实收资本', '实收股本'],
  capitalReserve: ['资本公积', '资本溢价'],
};

const LABELS = {
  shareholder: '股东名称',
  subscribedAmount: '认缴出资额',
  cumPaidAmount: '累计实缴出资额',
  curPaidAmount: '本期实缴出资额',
  unpaidAmount: '未缴出资额',
  ratio: '持股比例',
  bankInAmount: '银行进账金额',
  paidInCapital: '实收资本',
  capitalReserve: '资本公积',
};

/* 必需列：这 9 列任一列认不出来，对应检查就**只能不执行**，所以要如实报「列缺失」而不是硬跑。 */
const REQUIRED = [
  'shareholder', 'subscribedAmount', 'cumPaidAmount', 'curPaidAmount', 'unpaidAmount',
  'ratio', 'bankInAmount', 'paidInCapital', 'capitalReserve',
];

/* 合计行逐列复核的列（顺序 = 结果里的叙述顺序）。 */
const SUM_ROLES = [
  'subscribedAmount', 'cumPaidAmount', 'curPaidAmount', 'unpaidAmount',
  'paidInCapital', 'capitalReserve', 'bankInAmount',
];

const TOTAL_WORDS = /^(合计|总计|小计|合计数?|总额)$/;
const TOL = 0.01;              // 金额容差（元）
const RATIO_TOL_PP = 0.02;     // 持股比例容差（**百分点**：0.02 个百分点）

/* ⚠️ 付费开关只声明一次：形如 `Boolean(p && (p.full || p.credit || p.token))`，
   付费检查整块包在它的 if 块里。`tools/strip_free_engine.py` 会把开关、付费分支
   与"因此没人引用"的付费函数一起摘掉；写成别的形态（例：数组的 `.some()`）会留下开关不删
   ⇒ 泄漏守卫报"免费引擎里仍留着付费开关"。
   ⛔ 注释里也**不要**写出那一行的字面量：strip 的残渣断言是**纯字符串包含**判断。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（认缴 / 累计实缴 / 本期实缴 / 未缴 / 实收资本 / 资本公积 / 银行进账 —— 明细逐行相加 = 合计）',
  '同一股东重复行检测',
  '未缴出资额 = 认缴出资额 − 累计实缴出资额',
  '累计实缴出资额 ≤ 认缴出资额（超额实缴）',
  '持股比例与认缴出资额匹配（该股东认缴 ÷ 各股东认缴合计 = 填报比例，误差 > 0.02 个百分点）',
  '所有者投入勾稽（实收资本 + 资本公积 = 认缴合计 − 未缴合计）',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '本期实缴出资额 ≠ 银行进账金额（本期出资没有对应进账 / 进账被记到别的期间）',
  '未缴出资额为负（实缴超过认缴，通常伴随认缴或累计实缴填错）',
  '各股东持股比例合计 ≠ 100%（比例与认缴口径至少有一处错）',
  '单一股东持股 > 50% 提示（> 67% 时注明"绝对控股"，需确认章程/协议里的表决权安排）',
  '累计实缴出资额为 0 的股东提示（认而未缴，需核对出资期限）',
];

const OUT_OF_SCOPE = [
  '判断出资行为是否合法合规、出资期限是否已过、是否需要催缴（属于法律与公司治理判断）',
  '核验银行回单、验资报告、评估报告的真伪，也不代替验资或审计程序',
  '判断股权比例应当如何设计、是否需要减资或调整章程（属于股东会决议事项）',
  '读取 Excel / 工商登记 / 银行流水文件（需要你先导出成文本贴进来）',
  '判断认缴出资额本身是否与章程、股东协议一致（本工具只核表内自洽）',
];

/* 样例是**干净稿**：两档跑出来都必须 0 条发现。
   ⚠️ 注意单一股东持股这里刻意填 **50%**（不是 60%）：完整档第 4 项在 > 50% 时会出提示，
   样例若有人过半就会在完整档出现 1 条 P2 ⇒ 不再是"干净稿"。
   过半控股的提示能力由对照测试用专门的坏样例钉住。 */
const SAMPLE_TEXT = [
  '股东名称\t认缴出资额\t累计实缴出资额\t本期实缴出资额\t未缴出资额\t持股比例\t银行进账金额\t实收资本\t资本公积',
  '豫州控股集团有限公司\t5000000.00\t5000000.00\t0.00\t0.00\t50%\t0.00\t5000000.00\t0.00',
  '中岳创业投资合伙企业\t3000000.00\t2000000.00\t1000000.00\t1000000.00\t30%\t1000000.00\t2000000.00\t0.00',
  '员工持股平台\t2000000.00\t1000000.00\t0.00\t1000000.00\t20%\t0.00\t1000000.00\t0.00',
  '合计\t10000000.00\t8000000.00\t1000000.00\t2000000.00\t100%\t1000000.00\t8000000.00\t0.00',
].join('\n');

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|未知)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()【】\[\]]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim().replace(/[¥￥$，,\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  if (s.endsWith('%')) s = s.slice(0, -1);
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

/* 持股比例统一折算成**百分点**：`60%` -> 60；`0.6` -> 60；`60` -> 60（已按百分点填）。 */
function ratioPoints(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim();
  if (s === '') return null;
  const v = normNumber(s);
  if (v === null) return null;
  if (s.indexOf('%') >= 0) return round2(v);
  if (v > 0 && v <= 1) return round2(v * 100);
  return round2(v);
}

const who = (it) => {
  const n = String(it.shareholder || '').trim();
  return n ? `${n}（第 ${it.line} 行）` : `第 ${it.line} 行`;
};

/** 某一列在明细行上的合计（只累加能解析成数字的单元格，并回传参与行数）。 */
function columnSum(items, role) {
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    sum += v;
    n += 1;
  }
  return { sum: round2(sum), n };
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [], header: [] };
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const missingColumns = REQUIRED.filter((r) => !cols.some((c) => c.role === r));
  const items = [];
  const totals = {};
  for (let li = 1; li < lines.length; li += 1) {
    const cells = splitRow(lines[li]);
    const row = { line: li + 1 };
    cols.forEach((c) => { if (c.role) row[c.role] = cells[c.i] === undefined ? '' : cells[c.i]; });
    const label = (cells[0] || '').replace(/\s/g, '');
    if (TOTAL_WORDS.test(label)) { totals.line = li + 1; totals.row = row; continue; }
    items.push(row);
  }
  return { items, totals, missingColumns, header };
}

/* ================================ 免费档检查项 ================================ */

function checkTotalRow(items, totals) {
  if (!totals.row) return [];
  const out = [];
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    const { sum, n } = columnSum(items, role);
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        line: totals.line, level: 'P1', category: '合计复核',
        message: `合计行「${LABELS[role]}」填 ${stated}，但明细逐行相加是 ${sum}（相差 ${round2(stated - sum)}）`,
        evidence: `合计行=${stated}；明细合计=${sum}（${n} 行）；差额=${round2(stated - sum)}`,
      });
    }
  }
  return out;
}

function checkDuplicateShareholder(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.shareholder || '').replace(/\s/g, '');
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '股东重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「股东名称」完全相同 —— 同一股东可能被重复计入`,
        evidence: `股东名称=${key}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkUnpaidFormula(it) {
  const sub = normNumber(it.subscribedAmount);
  const cum = normNumber(it.cumPaidAmount);
  const un = normNumber(it.unpaidAmount);
  if (sub === null || cum === null || un === null) return null;
  const expect = round2(sub - cum);
  if (Math.abs(un - expect) > TOL) {
    return {
      line: it.line, level: 'P0', category: '未缴出资额不符',
      message: `${who(it)} 未缴出资额填 ${un}，但 认缴出资额 ${sub} − 累计实缴出资额 ${cum} = ${expect}`,
      evidence: `认缴出资额=${sub}；累计实缴出资额=${cum}；未缴出资额=${un}；应为=${expect}；差额=${round2(un - expect)}`,
    };
  }
  return null;
}

function checkPaidLeSubscribed(it) {
  const sub = normNumber(it.subscribedAmount);
  const cum = normNumber(it.cumPaidAmount);
  if (sub === null || cum === null) return null;
  if (cum - sub > TOL) {
    return {
      line: it.line, level: 'P0', category: '实缴超过认缴',
      message: `${who(it)} 累计实缴出资额 ${cum} 超过认缴出资额 ${sub}（超出 ${round2(cum - sub)}）`,
      evidence: `认缴出资额=${sub}；累计实缴出资额=${cum}；超出=${round2(cum - sub)}`,
    };
  }
  return null;
}

function checkRatioVsSubscribed(it, totalSubscribed) {
  const sub = normNumber(it.subscribedAmount);
  const reported = ratioPoints(it.ratio);
  if (sub === null || reported === null || !totalSubscribed) return null;
  const computed = round2((sub / totalSubscribed) * 100);
  const diff = Math.abs(computed - reported);
  if (diff > RATIO_TOL_PP) {
    return {
      line: it.line, level: 'P1', category: '持股比例与认缴不匹配',
      message: `${who(it)} 认缴出资额 ${sub} ÷ 认缴合计 ${round2(totalSubscribed)} = ${computed}%，但「持股比例」填的是 ${reported}%`,
      evidence: `认缴出资额=${sub}；认缴合计=${round2(totalSubscribed)}；应为=${computed}%；填报=${reported}%；相差=${round2(diff)} 个百分点`,
    };
  }
  return null;
}

function checkOwnerContribution(items, totals) {
  const pic = columnSum(items, 'paidInCapital');
  const res = columnSum(items, 'capitalReserve');
  const sub = columnSum(items, 'subscribedAmount');
  const un = columnSum(items, 'unpaidAmount');
  if (!pic.n || !sub.n) return [];
  const invest = round2(pic.sum + res.sum);
  const expect = round2(sub.sum - un.sum);
  if (Math.abs(invest - expect) > TOL) {
    return [{
      line: totals && totals.line ? totals.line : 1, level: 'P0', category: '所有者投入勾稽不符',
      message: `实收资本合计 ${pic.sum} + 资本公积合计 ${res.sum} = ${invest}，但 认缴合计 ${sub.sum} − 未缴合计 ${un.sum} = ${expect}`,
      evidence: `实收资本合计=${pic.sum}；资本公积合计=${res.sum}；所有者投入=${invest}；认缴合计=${sub.sum}；未缴合计=${un.sum}；应为=${expect}；差额=${round2(invest - expect)}`,
    }];
  }
  return [];
}

function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')} —— 相关检查本次无法执行`,
      evidence: `表头=${header.join('|')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (missingColumns.indexOf(role) >= 0) continue;
      if (isBlank(it[role])) {
        out.push({
          line: it.line, level: 'P1', category: '空白或占位符',
          message: `${who(it)} 的「${LABELS[role]}」是空白或占位符 —— 这一行无法参与核对`,
          evidence: `${LABELS[role]}=${it[role] === undefined ? '(空)' : it[role]}`,
        });
      }
    }
  }
  return out;
}

/* ============================== 完整档（付费）检查项 ============================== */

/* ================================== 主流程 ================================== */

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') return insufficient(['材料文本为空：请把股东出资明细表（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  const recognized = header.filter((h) => roleOf(h) !== null);
  if (!recognized.length) {
    return insufficient([`认不出表头：第一行必须是表头，且至少有「${LABELS.shareholder}」「${LABELS.subscribedAmount}」这类可识别的列名`]);
  }
  if (!items.length) {
    return insufficient(['没有任何数据行：表头下面至少要有 1 行股东明细（合计行可留）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  const totalSubscribed = columnSum(items, 'subscribedAmount').sum;
  for (const it of items) {
    const one = [
      checkUnpaidFormula(it),
      checkPaidLeSubscribed(it),
      checkRatioVsSubscribed(it, totalSubscribed),
    ];
    for (const f of one) if (f) findings.push(f);
  }
  for (const f of checkDuplicateShareholder(items)) findings.push(f);
  for (const f of checkOwnerContribution(items, totals)) findings.push(f);
  for (const f of checkBlanks(header, items, missingColumns)) findings.push(f);



  findings.sort((a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const checkList = CHECKS_GIVEN;
  const notRun = CHECKS_WITHHELD;

  return {
    status: 'success',
    result: {
      findings,
      summary: {
        rows: items.length,
        total: findings.length,
        p0, p1, p2,
        verdict: findings.length === 0 ? 'NO_ISSUE_FOUND' : (p0 > 0 ? 'P0_ISSUES' : 'ISSUES'),
        omitted: 0,
      },
      scope: {
        checks: checkList,
        checks_not_run: notRun,
        rows: items.length,
        subscribed_total: totalSubscribed,
        cum_paid_total: columnSum(items, 'cumPaidAmount').sum,
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
