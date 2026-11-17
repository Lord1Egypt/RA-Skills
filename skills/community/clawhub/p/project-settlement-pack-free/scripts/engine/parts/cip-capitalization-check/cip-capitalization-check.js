'use strict';
/**
 * cip-capitalization-check.js —— 在建工程转固与利息资本化核对（免费档 / 完整档共用源码）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 真实痛点（谁 / 何时 / 为何）：
 *   有工程或产线建设的企业，**每月做账、每年审计时必须核**这张在建工程台账：
 *     ① 工程成本归集 —— 材料费 + 人工费 + 分包费 + 其他费用 = 本期发生成本；
 *        累计已发生成本 = 上期期末累计 + 本期发生额；在建工程账面余额 = 上期期末余额 + 本期各成本类别成本之和；
 *     ② 达到预定可使用状态的**转固时点** —— 到了时点不转固，折旧就少提；
 *     ③ 暂估转固与后续调整 —— 暂估数按决算调整了几次；
 *     ④ 专门借款**利息资本化** —— 资本化期间占用资金 × 资本化率 × 资本化月数 ÷ 12；
 *     ⑤ **停止资本化时点** —— 非正常中断期间必须停。
 *   转固时点错、该资本化却费用化（或反之）是审计调整的高发区，而这张表纯粹是算术与口径，
 *   人眼在多项目、多月份、多成本类别下极易错 —— 正是"算出来能证明对错"的核对。
 *
 * 与已有能力的区别：`cip-transfer-check` 只核**转固这一笔本身的勾稽与凭证要素**；
 * 本能力核的是**整张在建工程台账**（成本归集 + 复算利息资本化 + 转固时点与停止资本化的口径），
 * 并给出一份按金额排序的处理清单 —— 层面不同、材料不同。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查利率文库、不判折旧政策、不给会计/审计意见；材料不足不给结论。
 *
 * ⚠️ 档位开关：本文件顶部声明一个布尔开关（由调用方传入的完整档凭证决定），
 *    完整档追加的检查全部包在该开关的分支里 —— `tools/strip_free_engine.py` 会把那一整段
 *    从免费包里摘掉。**不要**同时使用「完整档才执行的检查」那类 MARKER 注释块：
 *    两个形态同时存在时会走 MARKER 分支，把免费检查也整块删掉（第 236 轮踩过）。
 *    （此处刻意不写出开关的字面写法：守卫按字面扫描，写出就会把免费包判成"还留着付费开关"。）
 */

const CHECKS_GIVEN = [
  '工程成本归集复算（材料费 + 人工费 + 分包费 + 其他费用 = 本期发生成本）',
  '本期发生额计入累计一致（上期期末累计 + 本期发生额 = 本期累计已发生成本）',
  '账面余额勾稽（在建工程账面余额 = 上期期末余额 + 本期各成本类别成本之和）',
  '利息资本化复算（资本化期间占用资金 × 资本化率 × 本期资本化月数 ÷ 12 = 本期资本化利息）',
  '合计行逐列复核（累计已发生成本按各项目期末余额 / 本期资本化利息）',
  '转固金额与明细勾稽（合计 = 各项目期末在建工程余额之和）',
  '成本类别口径白名单（材料费/人工费/分包费/其他费用）',
  '重复行检测（同一项目 + 同一期间 + 同一成本类别）',
  '空缺与占位符检测（项目、期间、成本类别、累计成本、本期发生额等关键格）',
];

const CHECKS_WITHHELD = [
  '转固时点判定：达到预定可使用状态却仍未转固（含超期月份与应补提折旧影响）',
  '转固后仍继续归集在建工程成本',
  '停工期/非正常中断期间仍资本化利息',
  '资本化率与借款合同利率不符',
  '暂估转固与后续实际差异未调整',
];

const OUT_OF_SCOPE = [
  '判断某项支出是否应当资本化（那是会计政策与准则判断，不是算术）',
  '判断"达到预定可使用状态"的实质条件（试生产合格、验收通过等证据不在本表内）',
  '核定借款费用资本化率本身（只与表内填写的合同利率做一致性比对）',
  '决定折旧年限、残值率与折旧方法（只按表内给定的年折旧率量级估算影响）',
  '给出会计处理意见或审计意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

/** 逾期转固的判定阈值（月）：达到可使用状态后超过这么久仍挂在在建工程 ⇒ 报出 */
const TRANSFER_GRACE_MONTHS = 1;
/** 估算少提折旧用的年折旧率量级（概算口径，不是折旧政策） */
const DEPRECIATION_PROXY_RATE = 0.05;
/** 资本化率与借款合同利率的容差（百分点） */
const RATE_TOL = 0.05;
/** 资本化率的合理上限（百分点）：超过它先怀疑百分号/小数位填错 */
const MAX_PLAUSIBLE_RATE = 20;

const SAMPLE_TEXT = [
  '项目名称	期间	成本类别	本期发生成本	累计已发生成本	在建工程账面余额	达到可使用状态日期	转固日期	是否停工	停工起止	资本化期间占用资金	本期资本化月数	资本化率	本期资本化利息	转固金额暂估	借款合同资本化率',
  'A产线	2025-01	材料费	420000.00	420000.00	420000.00	2025-01-31	2025-02-28	否		2400000.00	12	4.5%	108000.00		4.5%',
  'A产线	2025-01	人工费		420000.00											',
  'A产线	2025-01	分包费		420000.00											',
  'A产线	2025-01	其他费用		420000.00											',
  'B车间	2025-02	材料费	250000.00	250000.00	250000.00			否		1200000.00	6	4.5%	27000.00		4.5%',
  'B车间	2025-02	人工费		250000.00											',
  'B车间	2025-03	材料费	420000.00	670000.00	670000.00										',
  'B车间	2025-03	人工费		670000.00											',
  'C仓库	2025-06	材料费	940000.00	940000.00	940000.00	2026-01-31	2026-03-31	否		900000.00	6	3.6%	16200.00		3.6%',
  'C仓库	2025-06	人工费		940000.00											',
  'C仓库	2025-06	分包费		940000.00											',
  'C仓库	2025-07	材料费	1420000.00	2360000.00	2360000.00										',
  'C仓库	2025-07	人工费		2360000.00											',
  'C仓库	2025-07	分包费		2360000.00											',
  'D机组	2025-04	材料费	300000.00	300000.00	300000.00	2025-01-31		是	2025-07-01 至 2025-07-31	600000.00	8	4.5%	18000.00		4.5%',
  'D机组	2025-04	人工费		300000.00											',
  'D机组	2025-07	材料费	700000.00	1000000.00	1000000.00										',
  'D机组	2025-07	人工费		1000000.00											',
  '合计				4450000.00									169200.00		',
].join('\n');

const TOL = 0.01;

// ⚠️ 顺序即优先级：`roleOf` 取**第一个**命中的角色，所以
//   ① 含"合同"的列必须排在宽泛的「资本化率」之前（否则 `借款合同资本化率` 被抢走，
//      两列落到同一个 role，后一列把前一列的**值覆盖**掉 —— 不报缺列，只是算错）；
//   ② 「资本化期间占用资金」必须排在「期间」之前（否则它被当成会计期间列）；
//   ③ 「本期发生成本」必须排在「累计已发生成本」之前。
const ROLES = {
  project: ['项目名称', '工程项目', '项目'],
  category: ['成本类别', '成本项目', '费用类别'],
  currentCost: ['本期发生成本', '本期发生额', '本期增加', '本期成本'],
  accumulatedCost: ['累计已发生成本', '累计成本', '累计发生额'],
  bookBalance: ['在建工程账面余额', '账面余额', '在建工程余额'],
  usableDate: ['达到可使用状态日期', '达到预定可使用状态日期', '达到可使用状态', '预可使用状态'],
  transferredDate: ['转固日期', '转固时点', '转固月份'],
  shutdownFlag: ['是否停工', '停工标志', '是否中断'],
  shutdownSpan: ['停工起止', '停工期间', '中断期间'],
  occupied: ['资本化期间占用资金', '占用资金', '资本化本金'],
  months: ['本期资本化月数', '资本化月数', '本期月数'],
  interest: ['本期资本化利息', '资本化利息'],
  provisional: ['转固金额暂估', '是否暂估', '暂估标志'],
  contractRate: ['借款合同资本化率', '合同利率', '合同资本化率'],
  capRate: ['资本化率'],
  party: ['期间', '月份', '会计期间', '所属期'],
};

const LABELS = {
  project: '项目名称', party: '期间', category: '成本类别', currentCost: '本期发生成本',
  accumulatedCost: '累计已发生成本', bookBalance: '在建工程账面余额',
  usableDate: '达到可使用状态日期', transferredDate: '转固日期', shutdownFlag: '是否停工',
  shutdownSpan: '停工起止', occupied: '资本化期间占用资金', months: '本期资本化月数',
  capRate: '资本化率', interest: '本期资本化利息', provisional: '转固金额暂估',
  contractRate: '借款合同资本化率',
};

// 必需列：认不出这些就**不给结论**。
// ⚠️ 「本期发生成本」与「在建工程账面余额」是**项目×期间首行**才填的列（后面的类别行留空），
//    所以它们不进 REQUIRED —— 结构性留空不该被当成"漏填"，那是可选列。
const REQUIRED = ['project', 'party', 'category', 'accumulatedCost'];

// 累计列是期末余额口径（不是各行相加）=> 由 checkTransferReconcile 单独核
const SUM_ROLES = ['interest'];

const CATEGORY_WHITELIST = ['材料', '人工', '分包', '其他'];

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

function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/** 日期归一：`2025-01-31` / `2025/1/31` / `2025年1月31日` -> `2025-01-31`；期间 `2025-01` -> `2025-01` */
function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[年月]/g, '-').replace(/日/g, '')
    .replace(/[./]/g, '-').replace(/-+$/, '');
  const m = s.match(/^(\d{4})-(\d{1,2})(?:-(\d{1,2}))?/);
  if (!m) return null;
  const y = m[1]; const mo = String(Number(m[2])).padStart(2, '0');
  return m[3] ? `${y}-${mo}-${String(Number(m[3])).padStart(2, '0')}` : `${y}-${mo}`;
}

/** 期间序号（绝对月数），只为做"相差几个月"的确定性比较 */
const round2 = (n) => Math.round(n * 100) / 100;

/** 是否处于停工/非正常中断状态（只看表内填写的标志与期间，不猜） */
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
const colsOf = (t) => t.cols.map((c) => c.role).filter(Boolean);
const who = (it) => `项目「${it.byRole.project || '(未命名)'}」${it.byRole.party || '(未填期间)'} ${it.byRole.category || '(未填成本类别)'}`;
const money = (n) => n.toFixed(2);

/** 把同一项目在一行里只写了一次的字段（如日期）推广到该项目的所有行 */
function projectInfo(items) {
  const map = new Map();
  for (const it of items) {
    const key = String(it.byRole.project || '').trim();
    if (!key) continue;
    if (!map.has(key)) map.set(key, {});
    const o = map.get(key);
    for (const role of ['usableDate', 'transferredDate', 'shutdownFlag', 'shutdownSpan', 'provisional']) {
      if (isBlank(o[role]) && !isBlank(it.byRole[role])) o[role] = it.byRole[role];
    }
    if (!o.rows) o.rows = [];
    o.rows.push(it);
  }
  return map;
}

/** 期间序号 -> `YYYY-MM`（报错信息里给人看的写法） */
/* ===================== 免费档检查 ===================== */

/**
 * 台账写法（本工具按这个口径复算，SKILL.md 里对买家写明了同一段）：
 *   · 「本期发生成本」只在每个"项目 × 期间"的**第一行**写一次（= 该期各项成本之和），其余类别行留空；
 *   · 「累计已发生成本」= 上期期末累计 + 本期发生额，同一"项目 × 期间"的各行写同一个数；
 *   · 「在建工程账面余额」只在每个"项目 × 期间"的第一行写一次（= 该期期末项目余额）；
 *   · 利息只写在占用专门借款资金的那一行。
 * 取不到应有的数（没有上期、没填本期发生额）就**不给结论**，不猜、不套默认值。
 */
/** ① 工程成本归集复算：本期发生成本 = 材料费 + 人工费 + 分包费 + 其他费用 */
function checkCostGrouping(it, group) {
  if (!group || !group.length || group[0].line !== it.line) return null;  // 只在组内第一行报一次
  const stated = num(it, 'currentCost');
  if (stated === null) return null;
  const parts = group.map((g) => num(g, 'currentCost')).filter((p) => p !== null);
  if (!parts.length) return null;
  const sum = round2(parts.reduce((s, n) => s + n, 0));
  if (Math.abs(sum - stated) <= TOL) return null;
  return {
    level: 'P0', category: '工程成本归集与各成本项之和不符', line: it.line, amount: round2(stated - sum),
    message: `${who(it)}的本期发生成本是 ${money(stated)}，`
      + `同项目同期各成本项（${parts.map((p) => money(p)).join(' + ')}）之和是 ${money(sum)}，相差 ${money(round2(stated - sum))}。`,
    advice: '归集口径要一致：材料费 + 人工费 + 分包费 + 其他费用 = 本期发生成本；'
      + '漏一类或把不同期间的成本挤进一行都会在这里露出来。',
  };
}

/** ② 本期发生成本计入累计一致：本期应有累计 = 上期期末累计 + 本期发生额 */
function checkAccumulation(it, prevAcc, expected) {
  const acc = num(it, 'accumulatedCost');
  if (acc === null) return null;
  if (expected === null || expected === undefined || prevAcc === null) return null;  // 证明不了 ⇒ 不给结论
  if (Math.abs(expected - acc) <= TOL) return null;
  return {
    level: 'P0', category: '本期发生额计入累计不一致', line: it.line, amount: round2(acc - expected),
    message: `${who(it)}的累计已发生成本是 ${money(acc)}，`
      + `按 上期期末累计 ${money(prevAcc)} + 本期发生额 ${money(round2(expected - prevAcc))} 应为 ${money(expected)}。`,
    advice: '累计数是转固与利息资本化的基数，滚错一次后面每期都错；先确认本期发生额没有被重复计入。',
  };
}

/** ③ 账面余额勾稽：在建工程账面余额 = 上期期末余额 + 本期各成本类别成本之和 */
function checkBookBalance(it, expected) {
  const book = num(it, 'bookBalance');
  if (book === null) return null;
  if (expected === null || expected === undefined) return null;   // 取不到应有余额 ⇒ 不给结论
  if (Math.abs(expected - book) <= TOL) return null;
  return {
    level: 'P0', category: '在建工程账面余额与累计成本不一致', line: it.line, amount: round2(book - expected),
    message: `${who(it)}的在建工程账面余额是 ${money(book)}，`
      + `按 上期期末余额 + 本期各成本类别成本之和 应为 ${money(expected)}，相差 ${money(round2(book - expected))}。`,
    advice: '在建工程账面余额 = 上期期末余额 + 本期归集的各项成本；差额通常来自过账遗漏、'
      + '部分转固未在同一行体现，或把往来余额记进了在建工程。',
  };
}

/** ④ 利息资本化复算：占用资金 × 资本化率 × 资本化月数 ÷ 12 = 本期资本化利息 */
function checkInterest(it) {
  const base = num(it, 'occupied');
  const rate = num(it, 'capRate');
  const months = num(it, 'months');
  const stated = num(it, 'interest');
  if (base === null || rate === null || months === null || stated === null) return null;
  const expect = round2(base * rate / 100 * months / 12);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '利息资本化金额与复算不符', line: it.line, amount: round2(stated - expect),
    message: `${who(it)}的本期资本化利息是 ${money(stated)}，`
      + `按 资本化期间占用资金 ${money(base)} × 资本化率 ${rate}% × ${months} 个月 ÷ 12 应为 ${money(expect)}。`,
    advice: '资本化金额 = 占用资金 × 资本化率 × 资本化期间；月数按整月取，'
      + '利息该资本化却费用化（或反之）是审计调整的高发区。',
  };
}

/** ⑤ 合计行逐列复核 */
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
        level: 'P0', category: '合计行与明细之和不符', line: t.line, amount: round2(stated - sum),
        message: `合计行的「${LABELS[role]}」是 ${money(stated)}，各明细行相加是 ${money(sum)}，相差 ${money(round2(stated - sum))}。`,
        advice: '要么明细行漏了项目/期间，要么合计行没跟着更新；合计是后面所有比例的分子分母。',
      });
    }
  }
  return out;
}

/**
 * ⑥ 转固金额与明细勾稽。
 * 口径：「在建工程账面余额」只在 项目x期间 首行写一次，它就是**该期期末的项目余额**；
 * 台账合计行的累计数应当等于**各项目期末余额之和**（转固时结转的在建工程金额就是这个数）。
 * 对不上说明有项目整段漏行、合计行没跟着更新，或有余额被手工改过。
 */
function checkTransferReconcile(totals, items, groups) {
  const out = [];
  const lastBook = new Map();          // 项目 -> {line, book} 最后一次写了余额的那一行
  for (const [key, group] of groups) {
    const project = key.split('|')[0];
    if (!project) continue;
    for (const g of group) {
      const book = num(g, 'bookBalance');
      if (book !== null) lastBook.set(project, { line: g.line, book });
    }
  }
  for (const t of totals) {
    const stated = num(t, 'accumulatedCost');
    if (stated === null) continue;
    const projects = [...lastBook.entries()];
    if (!projects.length) continue;
    const total = round2(projects.reduce((x, [, v]) => x + v.book, 0));
    if (Math.abs(total - stated) <= TOL) continue;
    out.push({
      level: 'P1', category: '转固金额与明细勾稽不符', line: t.line, amount: round2(stated - total),
      message: `合计行的「累计已发生成本」是 ${money(stated)}，`
        + `各项目期末在建工程余额之和是 ${money(total)}（${projects.map(([k, v]) => `${k} ${money(v.book)}`).join(' + ')}），`
        + `相差 ${money(round2(stated - total))}；转固时结转的在建工程金额应当等于各项目期末余额之和。`,
      advice: '对不上说明有项目整段漏进这张表，或合计行没跟着更新；两者都会让转固结转金额算错。',
    });
  }
  return out;
}

/** ⑦ 成本类别口径白名单 */
function checkCategoryAllowed(items) {
  const out = [];
  for (const it of items) {
    const c = String(it.byRole.category === undefined ? '' : it.byRole.category).trim();
    if (!c) continue;
    if (CATEGORY_WHITELIST.some((k) => c.indexOf(k) >= 0)) continue;
    out.push({
      level: 'P2', category: '成本类别不在口径白名单内', line: it.line,
      message: `${who(it)}的成本类别「${c}」不属于 材料费 / 人工费 / 分包费 / 其他费用。`,
      advice: '口径不统一会让"工程成本归集"复算永远对不上；请归并到四类之一，'
      + '确实需要细分的，请在成本类别里保留四类前缀（如「材料费-钢材」）。',
    });
  }
  return out;
}

/** ⑧ 重复行检测（同一项目 + 同一期间 + 同一成本类别） */
function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = [it.byRole.project, it.byRole.party, it.byRole.category]
      .map((v) => String(v === undefined ? '' : v).trim()).join('|');
    if (key === '||') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一项目同期同成本类别出现多行', line: it.line,
        message: `「${key.replace(/\|/g, ' / ')}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '重复行会让成本归集与合计一起翻倍；若确实是两笔，请分行写清摘要而不是复制同一行。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

/** ⑨ 空缺与占位符检测（可选列只在"这一行确实该填"时才查） */
function checkBlanks(items, optional, groups) {
  const out = [];
  // "填了才查"的列：这一列整张表都没写过值 ⇒ 无从判定该不该填，不报（材料不足时不猜）
  const optionalWhenUsed = ['usableDate', 'transferredDate', 'interest'];
  const everUsed = new Set();
  for (const it of items) {
    for (const role of optionalWhenUsed) {
      if (!isBlank(it.byRole[role])) everUsed.add(role);
    }
  }
  for (const it of items) {
    const key = `${String(it.byRole.project || '').trim()}|${String(it.byRole.party || '').trim()}`;
    const group = groups.get(key) || [];
    const isFirst = Boolean(group.length) && group[0].line === it.line;
    for (const role of REQUIRED.concat(optional)) {
      // 首行专属列：非首行本来就不该有值
      // 「本期发生成本」与「在建工程账面余额」只在 项目x期间 首行写一次，
      // 其余成本类别行留空（不是漏填）；「累计已发生成本」则每行都写（同期间各行同值）。
      if ((role === 'currentCost' || role === 'bookBalance') && !isFirst) continue;
      // 利息只写在**占用专门借款资金**的那一行；没有占用资金的行不写利息是正常的
      if (role === 'interest' && num(it, 'occupied') === null) continue;
      // 整表没人填过这一列 ⇒ 不报空格（例如"还没达到可使用状态"的项目本来就没有日期）
      if (optionalWhenUsed.includes(role) && !everUsed.has(role)) continue;
      // 这两列留空是正常状态（还没达到可使用状态 / 还没转固），不是漏填
      if (role == 'usableDate' || role == 'transferredDate') continue;
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一行就算不出来；补齐前本工具不会用 0 或默认值替你填。'
            + (role === 'currentCost'
              ? '（本期发生成本只需在"项目 × 期间"的第一行写一次）' : ''),
        });
      }
    }
  }
  return out;
}

/* ===================== 完整档（付费）追加的检查 ===================== */

/** ⑩ 转固时点判定：达到预定可使用状态却仍未转固（含超期月份与应补提折旧影响） */
/** ⑪ 转固后仍继续归集在建工程成本 */
/** 从"停工起止"里取起止期间（取不到就只认标志） */
/** ⑫ 停工期/非正常中断期间仍资本化利息 */
/** ⑬ 资本化率与借款合同利率不符（含"资本化率本身超出合理量级"那一档） */
/** ⑭ 暂估转固与后续实际差异未调整 */
/** 处理清单：按金额从大到小排序（金额缺失的排在同类最后） */
function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的在建工程台账（要能认出「项目名称」「期间」「成本类别」「本期发生成本」'
      + '「累计已发生成本」「在建工程账面余额」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从在建工程台账/工程成本明细导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个项目/期间的明细行']);

  const infoMap = projectInfo(t.items);

  // 分组：同一项目 + 同一期间
  const groups = new Map();
  for (const it of t.items) {
    const key = `${String(it.byRole.project || '').trim()}|${String(it.byRole.party || '').trim()}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(it);
  }
  // 每个项目的累计成本（取该项目最后一行，作为转固/暂估比对的基准）
  const cumOf = new Map();
  for (const it of t.items) {
    const key = String(it.byRole.project || '').trim();
    const acc = num(it, 'accumulatedCost');
    if (key && acc !== null) cumOf.set(key, acc);
  }
  // 项目内按（期间，行号）排序，用于把"上期期末数"带过来
  const orderOfProject = new Map();
  for (const it of t.items) {
    const key = String(it.byRole.project || '').trim();
    if (!orderOfProject.has(key)) orderOfProject.set(key, []);
    orderOfProject.get(key).push(it);
  }
  const prevOf = new Map();
  for (const list of orderOfProject.values()) {
    list.sort((a, b) => String(normDate(a.byRole.party) || '').localeCompare(String(normDate(b.byRole.party) || ''))
      || (a.line - b.line));
    for (let i = 1; i < list.length; i++) prevOf.set(list[i].line, list[i - 1]);
  }
  // 每个"项目×期间"应有的期末余额与累计：
  //   应有余额 = 上期**实际填写**的期末余额 + 本期各成本类别成本之和（首期无上期 ⇒ 不给结论）
  //   应有累计（仅在本期首行有本期发生额时）= 上期期末余额 + 本期发生额
  //   同期间后继类别行：累计应与本期首行相同
  const expBook = new Map();    // 期间首行 line -> 应有期末余额
  const expAcc = new Map();     // 期间首行 line -> 应有累计
  const expAccPrev = new Map(); // 期间首行 line -> 上期期末余额（报错信息用）
  const expAccSame = new Map(); // 同期后继行 line -> 应与首行相同的累计
  const order = new Map();      // 期间首行 line -> 组装顺序
  let seq = 0;
  for (const list of orderOfProject.values()) {
    const byPeriod = [];
    for (const it of list) {
      const pk = normDate(it.byRole.party) || '';
      if (!byPeriod.length || byPeriod[byPeriod.length - 1].key !== pk) byPeriod.push({ key: pk, rows: [] });
      byPeriod[byPeriod.length - 1].rows.push(it);
    }
    let prevBal = null;                      // 上期实际期末余额
    for (const per of byPeriod) {
      const head = per.rows[0];
      const add = round2(per.rows.reduce((x, r2) => x + (num(r2, 'currentCost') || 0), 0));
      const hasAdd = per.rows.some((r2) => num(r2, 'currentCost') !== null);
      const expect = prevBal === null ? null : round2(prevBal + add);
      expBook.set(head.line, expect);
      expAcc.set(head.line, hasAdd ? expect : null);
      expAccPrev.set(head.line, prevBal);
      order.set(head.line, seq++);
      const headAcc = num(head, 'accumulatedCost');
      for (let i2 = 1; i2 < per.rows.length; i2++) expAccSame.set(per.rows[i2].line, headAcc);
      prevBal = num(head, 'bookBalance');
    }
  }

  // 台账最后一期 = "截至"基准：只用表内数据，结果不随时间漂移
  let asOf = null;
  for (const it of t.items) {
    const p = normDate(it.byRole.party);
    if (p && p.length === 7 && (asOf === null || p > asOf)) asOf = p;
  }

  const findings = [];

  for (const it of t.items) {
    const key = `${String(it.byRole.project || '').trim()}|${String(it.byRole.party || '').trim()}`;
    const group = groups.get(key) || [];
    const head = group.length ? group[0].line : it.line;
    const prev = prevOf.get(head) || null;
    const prevAcc = prev ? num(prev, 'accumulatedCost') : null;
    const a = checkCostGrouping(it, group); if (a) findings.push(a);
    const sameAsHead = expAccSame.has(it.line);
    const b = checkAccumulation(it,
      sameAsHead ? num(group[0], 'accumulatedCost') : expAccPrev.get(head),
      sameAsHead ? expAccSame.get(it.line) : expAcc.get(head));
    if (b) findings.push(b);
    const c = checkBookBalance(it, expBook.get(head)); if (c) findings.push(c);
    const d = checkInterest(it); if (d) findings.push(d);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkTransferReconcile(t.totals, t.items, groups)) findings.push(f);
  for (const f of checkCategoryAllowed(t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  // 可选列：表头里有这一列、且这行确实该填时，填的是空/占位符才算问题
  const optional = [];
  for (const role of ['currentCost', 'bookBalance', 'interest', 'usableDate', 'transferredDate']) {
    if (colsOf(t).includes(role)) optional.push(role);
  }
  for (const f of checkBlanks(t.items, optional, groups)) findings.push(f);



  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  // 累计列在每个"项目x期间"重复写在多行上 ⇒ 汇总要按**期末余额**去重求和
  const balanceTotal = (() => {
    const last = new Map();
    for (const it of t.items) {
      const p2 = String(it.byRole.project || '').trim();
      const b = num(it, 'bookBalance');
      if (p2 && b !== null) last.set(p2, b);
    }
    return round2([...last.values()].reduce((x, n) => x + n, 0));
  })();
  const accruedRate = (role, baseRole) => (sumOf(baseRole) > 0 ? round2(sumOf(role) / sumOf(baseRole) * 100) : null);

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      projects: new Set(t.items.map((it) => String(it.byRole.project || '').trim()).filter(Boolean)).size,
      as_of: asOf,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      current_cost_total: sumOf('currentCost'),
      accumulated_cost_total: balanceTotal,
      accumulated_cost_sum_of_rows: sumOf('accumulatedCost'),
      interest_total: sumOf('interest'),
      effective_cap_rate_pct: accruedRate('interest', 'occupied'),
      basis: '本期发生成本 = 材料费 + 人工费 + 分包费 + 其他费用；累计已发生成本 = 上期累计 + 本期发生；'
        + '在建工程账面余额 = 上期期末余额 + 本期各成本类别成本之和；本期资本化利息 = 资本化期间占用资金 × 资本化率 × 本期资本化月数 ÷ 12；'
        + '转固结转金额 = 该项目截至转固时点的累计成本；合计行逐列复核。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    scope: {
      withheld: CHECKS_WITHHELD,
      checks_not_run: CHECKS_WITHHELD,
      notes: CHECKS_WITHHELD,
      transfer_grace_months: TRANSFER_GRACE_MONTHS,
      depreciation_proxy_rate: DEPRECIATION_PROXY_RATE,
      as_of: asOf,
    },
  };
  result.checks_not_run = CHECKS_WITHHELD;

  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对**，'
      + '不代表每笔支出都应当资本化、也不代表"达到预定可使用状态"的实质条件已经满足 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, normDate, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CATEGORY_WHITELIST, TRANSFER_GRACE_MONTHS, DEPRECIATION_PROXY_RATE, RATE_TOL, MAX_PLAUSIBLE_RATE,
};
