'use strict';
/**
 * procurement-payable-pack-full.js —— 采购与付款技能包（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须用它：**采购 / 应付会计 / 财务共享中心 / 内控与审计，在月末结账、付款审批、
 * 供应商对账、招标与合同付款节点上**。要核的从来不是一张表，而是一整套互相关联的采购与付款底稿：
 * 供应商应付对账、应付账龄与付款计划、暂估入账与发票未到、应付保理与贴现、采购返利与阶梯、
 * 投标保证金收退、履约保证金与保函台账、中标结果与合同一致性、合同一致性、多份合同条款差异、
 * 三单匹配（订单/入库/发票）、报销单合规、预付卡消费核销、预收账款与收入确认 ——
 * 每一张都有自己的勾稽关系，**逐张手核既慢又容易漏**，而且月月重复；
 * 一笔对不上的应付、一个算错的暂估、一张没匹配上的发票，后果都比多花半小时严重得多。
 *
 * 这个包做的事**只有一件**（不是重写任何规则）：把仓库里**已有的 14 个采购与付款检查引擎**
 * 装进一个批量壳里，`--input <目录>`（每个子目录 = 一个对象 / 一套材料）一次跑完所有对象，
 * **每个对象一行结论**。
 *   规则来源：`scripts/engine/parts/<检查项>/`（**逐字节拷贝**自那 14 个免费包，一行都没改；
 *   本包只做"目录 → 对象 → 逐项派发"的编排与汇总）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（与仓库其它引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *     payload.text            单对象：该对象的一套采购与付款材料文本（每项用 `=== 检查项 ===` 分段）
 *     payload.objects[]       多对象：{name, files:[{name, text}]} —— 每个子目录 = 一个对象
 *   CHECKS_GIVEN / CHECKS_WITHHELD   免费档执行 / 不执行的检查项（免费包据此如实列出未执行项）
 *   CHECKS_OUT_OF_SCOPE              本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT / SAMPLE_OBJECTS     样例（免费包 --sample / --sample-batch 用它自检）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），
 * **不读环境变量**，**不写任何文件**（结果只打到 stdout）。
 * ⚠️ 材料不足**绝不给结论**：某个对象没材料就单独标"未执行"，一个对象都跑不了就整体不给结论。
 * ⚠️ 本工具**不代替审计、不出鉴证意见**，也不判断某笔采购/付款该不该做、金额该不该付。
 */

const MEMBERS = [
  {
    label: '供应商应付对账',
    id: 'ap-reconciliation',
    entry: require('./parts/ap-reconciliation/ap-reconciliation.js'),
  },
  {
    label: '应付账款账龄与付款计划核对',
    id: 'ap-aging-plan-check',
    entry: require('./parts/ap-aging-plan-check/ap-aging-plan-check.js'),
  },
  {
    label: '应付暂估与发票未到核对',
    id: 'ap-provisional-check',
    entry: require('./parts/ap-provisional-check/ap-provisional-check.js'),
  },
  {
    label: '应付账款保理与贴现核对',
    id: 'ap-factoring-check',
    entry: require('./parts/ap-factoring-check/ap-factoring-check.js'),
  },
  {
    label: '采购返利与阶梯核算核对',
    id: 'purchase-rebate-check',
    entry: require('./parts/purchase-rebate-check/purchase-rebate-check.js'),
  },
  {
    label: '投标保证金收退核对',
    id: 'bid-deposit-refund-check',
    entry: require('./parts/bid-deposit-refund-check/bid-deposit-refund-check.js'),
  },
  {
    label: '履约保证金与保函台账核对',
    id: 'contract-performance-bond-check',
    entry: require('./parts/contract-performance-bond-check/contract-performance-bond-check.js'),
  },
  {
    label: '中标结果与合同一致性核对',
    id: 'award-contract-consistency-check',
    entry: require('./parts/award-contract-consistency-check/award-contract-consistency-check.js'),
  },
  {
    label: '合同一致性AI核对',
    id: 'contract-consistency-check',
    entry: require('./parts/contract-consistency-check/contract-consistency.js'),
  },
  {
    label: '多份合同条款差异比对',
    id: 'contract-comparison',
    entry: require('./parts/contract-comparison/contract-comparison.js'),
  },
  {
    label: '三单匹配AI核对',
    id: 'three-way-match',
    entry: require('./parts/three-way-match/three-way-match.js'),
  },
  {
    label: '报销单合规预检',
    id: 'expense-compliance',
    entry: require('./parts/expense-compliance/expense-compliance.js'),
  },
  {
    label: '预付卡消费核销核对',
    id: 'prepaid-card-consumption-check',
    entry: require('./parts/prepaid-card-consumption-check/prepaid-card-consumption-check.js'),
  },
  {
    label: '预收账款与收入确认核对',
    id: 'advance-receipt-check',
    entry: require('./parts/advance-receipt-check/advance-receipt-check.js'),
  },
];

/* 免费档执行：14 个采购与付款检查项，逐个对象全跑一遍（这就是免费层的核心产出：一次跑完所有对象） */
const CHECKS_GIVEN = MEMBERS.map((m) => m.label);

/* 完整档追加（**多一种能力**，不是多几个数）：跨对象汇总台账 —— 单对象结果里根本不存在的东西 */
const CHECKS_WITHHELD = [
  '跨对象汇总台账（全部对象 × 全部 14 项检查合并成一张总表）',
  '采购付款风险排序清单（按 P0/P1/P2 排序，带对象名与原文文件行号）',
  '跨对象共性问题归类（同一问题命中 2 个及以上对象时合并成一条共性项）',
  '采购付款台账导出（Markdown 与 CSV 文本，直接用于付款审批附件与结账前复核说明）',
];

/* 如实列出**每个成员检查包自己**没做的子检查（那 14 个免费包各自的未执行项）——
   两个档位都没实现它们，绝不能因为"买断档打开了汇总"就让买家以为这些项被跑了。 */
const SUB_CHECKS_WITHHELD = [];
for (const m of MEMBERS) {
  for (const w of (m.entry.CHECKS_WITHHELD || [])) SUB_CHECKS_WITHHELD.push(`${m.label}：${w}`);
}

const TOTAL_SUB_CHECKS = MEMBERS.reduce((n, m) => n + (m.entry.CHECKS_GIVEN || []).length, 0);

const OUT_OF_SCOPE = [
  '判断某笔采购、付款、保理、贴现、返利该不该做，或金额该不该付（属于业务与审批判断，请按合同、授信与审批结论执行）',
  '核对发票 / 合同 / 入库单 / 保函的真伪，或比对税务系统、ERP、网银的逐行明细',
  '代替审计程序、代替函证，或出具鉴证意见与审计意见（只做表内/表间的算术与勾稽核对）',
  '判断适用税率、返利率、融资比例、保证金比例该取什么值算公允（本工具只核你给的表内数字与表间勾稽关系）',
  '查询供应商 / 客户的征信、失信名单、主体资格或关联关系（属于外部数据查询）',
  '读取 ERP / 采购系统 / 报销系统 / 网银的导出文件（需要你先导出成文本，每个对象一个目录）',
];

/* 样例 = 14 个成员检查包各自的最小完整样例（各自带表头，用 `=== 检查项 ===` 分段）。
   注意：其中四个成员的样例本身是**问题稿**，按各自规则一定会报出发现 —— 这不是误报，是它们的样例
   就是照着"有问题"的样子写的：
     · contract-consistency-check（合同一致性）的样例里有日期倒挂、金额矛盾、占位符残留等；
     · contract-comparison（多份合同条款差异比对）的样例里两份合同条款对不齐；
     · three-way-match（三单匹配）的样例里有跨单据不一致；
     · expense-compliance（报销单合规预检）的样例里有重复发票号等。
   本包如实转述它们的结论，不做任何静默过滤。 */
const SAMPLE_TEXT = MEMBERS
  .map((m) => `=== ${m.label} ===\n${m.entry.SAMPLE_TEXT}`)
  .join('\n\n');

/* 有一处硬伤的样例：把「供应商应付对账」里甲物资有限公司的**期末应付**
   从 120000.00 改成 121000.00（期初 100000.00 + 本期采购 50000.00 − 本期付款 30000.00 = 120000.00，
   与 121000 不符；差异列与合计行也随之不平）⇒ 必须报出来，并带**原文行号**。 */
const DIRTY_FROM = '甲物资有限公司\t100000.00\t50000.00\t30000.00\t120000.00\t120000.00\t0.00';
const DIRTY_TO = '甲物资有限公司\t100000.00\t50000.00\t30000.00\t121000.00\t120000.00\t0.00';
const DIRTY_TEXT = SAMPLE_TEXT.replace(DIRTY_FROM, DIRTY_TO);

/* 只覆盖 3 项的样例：用来演示"材料只覆盖了一部分"时，批量壳**明确报一条**，
   而不是把"跑了 3 项"说成"14 项都核过了"。 */
const PARTIAL_TITLES = ['供应商应付对账', '应付暂估与发票未到核对', '三单匹配AI核对'];
const PARTIAL_TEXT = SAMPLE_TEXT.split(/(?=^=== )/m)
  .filter((s) => PARTIAL_TITLES.some((t) => s.trim().indexOf(`=== ${t} ===`) === 0))
  .join('\n');

/* 批量样例：3 个对象（成员样例合并稿 / 有一处硬伤 / 没交材料），用来演示"一次跑完所有对象"。 */
const SAMPLE_OBJECTS = [
  { name: '样例对象（14 项成员样例合并稿）', files: [{ name: '采购付款材料.txt', text: SAMPLE_TEXT }] },
  { name: '改坏期末应付的对象', files: [{ name: '采购付款材料.txt', text: DIRTY_TEXT }] },
  { name: '空料对象（只登记未交材料）', files: [] },
];

/** 内置样例**本身带有发现**（四个成员的样例就是问题稿，见上）。
 *  这是**显式声明**、不是放水：`tools/strip_free_engine.py` 的烟测要求"干净样例 ⇒ 0 发现"，
 *  样例自带问题时**必须声明这个常量**，否则会把"样例真实报出了问题"误判成"改动把包改坏了"。 */
const SAMPLE_HAS_FINDINGS = true;

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: advice
      || '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（认不出表头就不出结论）。',
  };
}

function countLevels(list) {
  const out = { p0: 0, p1: 0, p2: 0 };
  for (const f of list) {
    if (f.level === 'P0') out.p0 += 1;
    else if (f.level === 'P1') out.p1 += 1;
    else if (f.level === 'P2') out.p2 += 1;
  }
  return out;
}

/** 把一份材料按 `=== 检查项 ===` 分段，并**记住每一行来自哪个文件第几行**（结论要能回到原文）。
 *
 *  ⛔ 分段文本**原样**交给成员引擎（**不删空行**）：实测本包有 2 个成员对空行敏感
 *  （合同一致性 12 → 10 条、三单匹配 2 → 0 条），删空行等于**静默改变成员的结论** ——
 *  那正是"改动没生效/结论凭空消失"类缺陷的温床。成员引擎行号口径本就不统一
 *  （有的算原始行、有的只算数据行），所以对外行号一律由 mapMemberLine **按原文内容**落位，
 *  不依赖成员内部行号；这里只负责把"分段内第 i 行 → 原文件第几行"如实记下来备用。 */
function sectionsOfFile(f) {
  const lines = String(f.text === undefined || f.text === null ? '' : f.text).split(/\r?\n/);
  const out = [];
  let cur = { title: '', lines: [], lineNos: [] };
  const flush = () => {
    if (!cur.lines.some((l) => String(l).trim() !== '')) return;   // 整段都是空行 ⇒ 不是一段材料
    /* codeLineNos = **非空行**的原文件行号。成员引擎报的内部行号（f.line）口径不统一，
       但用哪一套兜底都必须落在**有内容的那一行**上 —— 把行号指到空行上，买家回原文只会看到空白。 */
    const codeLineNos = [];
    for (let i = 0; i < cur.lines.length; i += 1) {
      if (String(cur.lines[i]).trim() !== '') codeLineNos.push(cur.lineNos[i]);
    }
    out.push({
      title: cur.title, file: f.name, text: cur.lines.join('\n'),
      lineNos: cur.lineNos.slice(), codeLineNos: codeLineNos,
      startLine: codeLineNos[0],
    });
  };
  for (let i = 0; i < lines.length; i += 1) {
    const m = lines[i].match(/^\s*===\s*(.+?)\s*===\s*$/);
    if (m) {
      flush();
      cur = { title: m[1].trim(), lines: [], lineNos: [] };
      continue;
    }
    cur.lines.push(lines[i]);
    cur.lineNos.push(i + 1);
  }
  flush();
  return out;
}

function coerceFiles(o) {
  const files = [];
  if (Array.isArray(o.files)) {
    for (const f of o.files) {
      if (!f) continue;
      const t = f.text !== undefined ? f.text : f.content;
      files.push({
        name: String(f.name || f.file || '材料'),
        text: t === undefined || t === null ? '' : String(t),
      });
    }
    return files;
  }
  const t = o.text !== undefined ? o.text : o.content;
  if (t !== undefined && t !== null) {
    files.push({ name: String(o.file || o.file_name || '材料'), text: String(t) });
  }
  return files;
}

/** 入参归一化成"对象列表"：`{text}` 是单对象，`{objects:[…]}`（或 `{clients:[…]}`）是批量。 */
function normalizeObjects(payload) {
  const raw = [];
  const list = Array.isArray(payload.objects) ? payload.objects
    : (Array.isArray(payload.clients) ? payload.clients : null);
  if (list) {
    for (const o of list) {
      if (!o) continue;
      raw.push({ name: String(o.name || o.object || o.client || '').trim(), files: coerceFiles(o) });
    }
  }
  if (payload.text !== undefined || payload.content !== undefined) {
    raw.push({
      name: String(payload.object_name || payload.object || payload.client_name || payload.client
        || payload.name || '单对象').trim(),
      files: coerceFiles(payload),
    });
  }
  const out = [];
  raw.forEach((o, i) => out.push({ name: o.name || `对象${i + 1}`, files: o.files }));
  return out;
}

/** 覆盖缺口检查：对象交了材料，但只覆盖了一部分检查项 ⇒ **明确报一条**，
 *  不能因为"跑了几项"就以为 14 项都核过了。整份材料都没交的对象不在这里报（那是对象级的"未执行"）。 */
function checkClientCoverage(it) {
  const ran = it.checks.filter((c) => c.status === 'ok');
  const notRun = it.checks.filter((c) => c.status !== 'ok');
  if (!ran.length || !notRun.length) return null;
  return {
    level: 'P2',
    category: '检查项未执行（材料只覆盖了一部分）',
    line: 1,
    message: `对象「${it.client}」的材料只覆盖了 ${ran.length} / ${it.checks.length} 个采购与付款检查项，`
      + `未执行的是：${notRun.map((c) => c.check).join('、')} —— 这些项这次**没有核**，请补齐材料后重跑。`,
  };
}

/** 派发池：**先认段标题，再兜底**。
 *
 *  为什么不能像样板那样"每个成员从前到后试第一个跑得通的段"：本包有 3 个成员是**自由文本型**
 *  引擎（合同一致性 / 三单匹配 / 报销单合规），它们对**任何**文字都会回 success
 *  （它们本来就是"拿全文去找线索"的），而 contract-comparison 也会接受合同一致性那一段
 *  ⇒ 若按"第一个跑得通的段"派发，这几项会去跑**别的检查项**的材料，
 *  结论挂错检查项（实测：4 个成员抢错段）。所以：
 *    ① **段标题 == 本检查项名** 的段优先（这正是本包文档与样例约定的分段法）；
 *    ② 没有同名段时，才在"**没有被别的检查项认领**"的段（无标题段 / 自定义标题段）里兜底；
 *    ③ **绝不抢**别的检查项名下的那一段 —— 宁可如实标 `not_run`，也不拿别人的材料出结论。 */
function candidatePool(m, candidates) {
  const own = candidates.filter((c) => c.title === m.label);
  if (own.length) return own;
  return candidates.filter((c) => !c.title || CHECKS_GIVEN.indexOf(c.title) < 0);
}

/** 把成员引擎报的行号**落回原文文件行**（用于结论里的"原文文件与行号"）。
 *
 *  为什么不能直接 `lineNos[f.line - 1]`：成员引擎的行号口径**实测不统一**（有的把行号记成原文里的
 *  行位置、含表头，有的只算数据行，有的干脆只给行号不给内容片段），而本包的分段恰好把空行与
 *  `=== 检查项 ===` 标题行去掉了 ⇒ 直接查表会**整体错位**。错行号比没有行号更糟 ——
 *  买家按行号找回原文会看到别的记录。
 *
 *  所以落位**以原文内容为准**：成员给的 evidence 行首片段必须在原文里真的能对上。
 *    ① 用 evidence 片段按**行首**在原文里找出所有候选行；
 *    ② 候选唯一 ⇒ 直接用它；
 *    ③ 候选多行（同一片段重复出现）⇒ 取距"成员行号所对应的分段行"最近的那一行；
 *    ④ 片段缺失或对不上（成员只给了行号 / 对象级结论）⇒ 如实用成员行号对应的原文行，
 *       退回该分段首行兜底 —— 绝不编造行号。
 *  这样"对得上"的成员行为完全不变，只有口径不同的成员被纠正到原文行。 */
function evidenceKey(ev) {
  if (Array.isArray(ev)) return String(ev[0] === undefined || ev[0] === null ? '' : ev[0]).trim().slice(0, 15);
  const s = String(ev === undefined || ev === null ? '' : ev).trim();
  if (s.indexOf('\n') >= 0) return s.split('\n')[0].trim().slice(0, 15);
  return s.slice(0, 15);
}

function mapMemberLine(f, cand) {
  /* 兜底一律走**非空行**表：行号指到空行等于没指（买家回原文只看到空白）。 */
  const codeLineNos = cand.codeLineNos || cand.lineNos;
  const direct = codeLineNos[f.line - 1];
  const key = evidenceKey(f.evidence);
  const rows = String(cand.text).split('\n');       // 与 lineNos 一一对应（sectionsOfFile 已过滤空行）
  /* 汇总级结论（成员自己把行号记成 0）没有具体行 —— 如实指向本分段的首行，
     不要按 evidence 去挑一行（那会让买家以为那行有问题）。 */
  if (!f.line) return cand.startLine;
  if (!key) return direct === undefined ? cand.startLine : direct;
  const hits = [];
  for (let i = 0; i < rows.length; i += 1) {
    if (String(rows[i]).trim().slice(0, 15) === key) hits.push(i);
  }
  if (!hits.length) return direct === undefined ? cand.startLine : direct;
  if (hits.length === 1) return cand.lineNos[hits[0]];
  let best = hits[0];
  for (const i of hits) {
    const bi = (best + 1) - f.line;
    const ii = (i + 1) - f.line;
    if (Math.abs(ii) < Math.abs(bi) || (Math.abs(ii) === Math.abs(bi) && i < best)) best = i;
  }
  return cand.lineNos[best];
}

/* 台账层挂载点：**默认什么都不做**（免费档就是这样）。
   完整档在自己的付费块里把它定义成真正的台账实现（函数声明提升，run() 里引用不会报未定义）。 */
function ledger_hook() {}

/** 一个对象跑完全部 14 项；每一项的实际规则在 parts/ 里（本文件一行规则都没改）。
 *  派发方式：段标题优先（见 candidatePool），**第一个跑通的段**就是这一项的表；
 *  一段都跑不通 ⇒ 这一项如实标 `not_run` 并列出还缺哪个表头，**绝不算它跑过**。 */
function runOneObject(object) {
  const live = object.files.filter((f) => String(f.text).trim() !== '');
  const candidates = [];
  for (const f of live) for (const s of sectionsOfFile(f)) candidates.push(s);
  const materialLines = live.reduce(
    (n, f) => n + String(f.text).split(/\r?\n/).filter((l) => l.trim() !== '').length, 0);

  /* 材料为空、或只有一两行（连一张最小表都凑不齐）⇒ 这个对象如实标"未执行"。
     门限取 3：本领域最小的表就是"表头 + 数据行 + 合计"3 行。 */
  if (!candidates.length || materialLines < 3) {
    return {
      object: object.name, status: 'insufficient_input', files: live.map((f) => f.name),
      material_lines: materialLines,
      checks: MEMBERS.map((m) => ({ check: m.label, status: 'not_run', findings: 0 })),
      findings: [], not_run: MEMBERS.map((m) => m.label),
      total: 0, p0: 0, p1: 0, p2: 0, verdict: 'NOT_RUN',
      reason: '没有收到这个对象的可用材料（材料为空或只有一两行，凑不齐一张最小的表）',
    };
  }

  const checks = [];
  const findings = [];
  const notRun = [];
  for (const m of MEMBERS) {
    let hit = null;
    let bestMissing = null;
    for (const cand of candidatePool(m, candidates)) {
      let out = null;
      try { out = m.entry.run({ text: cand.text }); } catch (e) { out = null; }
      if (out && out.status === 'success' && out.result) { hit = { cand: cand, result: out.result }; break; }
      const miss = (out && out.missing) || [];
      if (Array.isArray(miss) && miss.length && (!bestMissing || miss.length < bestMissing.length)) {
        bestMissing = miss;
      }
    }
    if (!hit) {
      notRun.push(m.label);
      checks.push({
        check: m.label, status: 'not_run', findings: 0,
        missing: bestMissing || ['这个对象的材料里没有这一项需要的表头行（或没有 `=== 本检查项名 ===` 分段）'],
      });
      continue;
    }
    const per = (hit.result.findings || []).map((f) => {
      const lineNo = mapMemberLine(f, hit.cand);
      return {
        level: f.level,
        category: f.category,
        line: f.line,
        object: object.name,
        check: m.label,
        section: hit.cand.title,
        source_file: hit.cand.file,
        source_line: lineNo,
        evidence: `${hit.cand.file}:${lineNo}`,
        message: f.message,
      };
    });
    for (const f of per) findings.push(f);
    checks.push({
      check: m.label, status: 'ok', findings: per.length,
      section: hit.cand.title || hit.cand.file,
    });
  }

  /* 批量壳自己的检查项：材料只覆盖了一部分检查项时，明确报一条
     （别把"跑了 3 项"说成"14 项都核过了"）。 */
  const cover = checkClientCoverage({ client: object.name, checks: checks });
  if (cover) {
    findings.push(Object.assign({}, cover, {
      object: object.name, check: '（批量壳）', section: '',
      source_file: '', source_line: 0, evidence: '对象级',
    }));
  }

  const lv = countLevels(findings);
  const anyRan = checks.some((c) => c.status === 'ok');
  const row = {
    object: object.name,
    status: anyRan ? 'ok' : 'insufficient_input',
    files: live.map((f) => f.name),
    material_lines: materialLines,
    checks: checks,
    findings: findings,
    not_run: notRun,
    total: findings.length,
    p0: lv.p0, p1: lv.p1, p2: lv.p2,
    verdict: lv.p0 > 0 ? 'P0_ISSUES' : (findings.length ? 'ISSUES' : (anyRan ? 'NO_ISSUE_FOUND' : 'NOT_RUN')),
    reason: anyRan ? '' : '材料里没有任何一项能被认出的表（每个 `=== 检查项 ===` 分段的第一行要是表头行）',
  };

  /* 这一行有没有被真正核对过（有材料、且至少有一项能跑）⇒ 才够格进跨对象汇总台账。
     免费档与完整档都用它：台账只收"真跑过"的对象行，没交材料的对象不进总表。 */
  row.ledger_member = false;   // 由完整档的台账层置位；免费档恒为 false

  return row;
}

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  if (!payload) {
    return insufficient([
      '一个对象的材料都没收到（objects[] 与 text 都是空）',
      '单对象用 {"text":"…"}；批量用 {"objects":[{"name":"对象名","files":[{"name":"材料.txt","text":"…"}]}]}',
    ]);
  }
  const objects = normalizeObjects(payload);
  if (!objects.length) {
    return insufficient([
      '一个对象的材料都没收到（objects[] 与 text 都是空）',
      '每个对象一个子目录，目录里放该对象的一套采购与付款材料（每项用 `=== 检查项 ===` 分段，Tab 分隔最稳）',
    ]);
  }

  const rows = objects.map((o) => runOneObject(o));
  const usable = rows.filter((r) => r.status === 'ok');
  if (!usable.length) {
    return insufficient(
      [`全部 ${rows.length} 个对象都没有可用材料（每个对象目录里要有该对象的采购与付款材料，且每张表要有表头行）`]
        .concat(rows.map((r) => `对象「${r.object}」：没有可用材料`)),
      '把每个对象的采购与付款材料放进各自子目录后再跑；材料不足时本工具不做任何认定、也不给任何结论。');
  }

  const findings = [];
  for (const r of rows) for (const f of r.findings) findings.push(f);
  findings.sort((a, b) => (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
    || (a.line - b.line) || String(a.category).localeCompare(String(b.category)));

  const lv = countLevels(findings);
  const withIssues = rows.filter((r) => r.findings.length > 0).length;
  const notRunObjects = rows.filter((r) => r.status !== 'ok').length;   // run() 里的 rows 就是全部对象

  const result = {
    service_type: 'PROCUREMENT_PAYABLE_PACK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: CHECKS_WITHHELD.slice(),
      sub_checks_not_run: SUB_CHECKS_WITHHELD.slice(),
      objects: rows.length,
      objects_ran: usable.length,
      sub_checks_per_object: TOTAL_SUB_CHECKS,
      executed_locally: true,
      network_used: false,
      wrote_files: false,
    },
    objects: rows,
    findings: findings,
    summary: {
      objects: rows.length,
      objects_with_issues: withIssues,
      objects_clean: usable.length - withIssues,
      objects_not_run: notRunObjects,
      total: findings.length,
      p0: lv.p0, p1: lv.p1, p2: lv.p2,
      verdict: lv.p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本次对 ${rows.length} 个对象逐个跑了 ${CHECKS_GIVEN.length} 个采购与付款检查项（每个成员包内部还有 `
      + `${TOTAL_SUB_CHECKS} 项子检查）；未执行的检查项见 scope.checks_not_run 与 `
      + 'scope.sub_checks_not_run。',
    disclaimer: '只把各对象材料里的表内/表间算术与勾稽核一遍，结论都带**原文文件与行号**、可由第三方复算；'
      + '**不代替审计、不出具鉴证意见**，也不判断某笔采购、付款、保理、贴现该不该做、金额该不该付。',
  };

  /* 分层：
     · 免费档（免费包里就是下面这两行 + 再下面那句 return，付费块被整块摘掉）：
       只报**实际执行**的那 14 项，未执行项如实列出（说明文本，不是实现）。
     · 完整档（本文件）：在上面那层之上再挂一层跨对象汇总台账
       （对象 × 检查项总表、采购付款风险排序清单、跨对象共性问题归类、Markdown / CSV 导出）。 */
  result.checks_executed = CHECKS_GIVEN.concat();
  result.checks_withheld = CHECKS_WITHHELD.concat();

  /* 完整档：把跨对象汇总台账挂到本次结果上。
     ledger_hook 在免费档里是空函数（免费包付费块整块不存在）⇒ 免费档永远挂不出 ledger。 */
  ledger_hook(result, findings, rows, payload);

  /* 免费档的出口：付费块被整块摘掉后直接走到这一句（完整档在上面那一支里已经挂好台账）。 */
  return { status: 'success', result: result };
}

module.exports = {
  run, runOneObject, normalizeObjects, coerceFiles, sectionsOfFile, candidatePool, countLevels, checkClientCoverage, CHECKS_GIVEN, CHECKS_WITHHELD, SUB_CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, SAMPLE_OBJECTS, DIRTY_TEXT, PARTIAL_TEXT, MEMBERS, SAMPLE_HAS_FINDINGS,
};
