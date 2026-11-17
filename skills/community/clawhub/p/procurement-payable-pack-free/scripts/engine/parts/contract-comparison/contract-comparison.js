'use strict';
/**
 * contract-comparison.js —— 多份合同条款横向比对（免费版引擎）
 *
 * 为什么做这个：
 *   采购 / 法务 / 审计经常遇到同一件事：**按同一个模板签了几十份合同**，
 *   其中某一份被**悄悄改过一条**。手工逐份比对不现实，而内审 / 外审恰恰会拿这个说事。
 *   这件事**完全是确定性的**：把每份合同按「条」切开、对齐、找不同。
 *
 * 本文件是**免费版**：只实现下面 CHECKS_GIVEN 列出的四类检查。
 * 收费档的检查项（关键字段跨合同数值对比、日期逻辑、模板占位符残留、金额大小写）
 * **没有实现**，因此不可能被伪造出来 —— 它们只会如实地列为"未执行"。
 *
 * 设计原则（与本仓库其它引擎一致）：
 *   · 自包含：只用 Node.js 标准库，**不发起任何网络请求**；
 *   · 每条结论都引用原文与行号，第三方可用同一份输入复算；
 *   · 材料不足时返回 insufficient_input 并说明缺什么，**绝不输出"未发现问题"**；
 *   · 只做AI比对，**不判断哪一份条款更有利、也不给法律意见**。
 */

const CHECKS_GIVEN = [
  '条款切分与横向对齐（把每份合同按「第X条」切开，按条款标题对齐）',
  '缺条 / 多条（某份合同少了或多了哪一条）',
  '条款正文不一致（同一条的各版本摘要）',
  '条款对照表（每条被几份合同覆盖、有几份不同版本）',
];

const CHECKS_WITHHELD = [
  '关键字段跨合同对比（合同金额 / 违约金比例 / 预付款比例 / 争议解决 / 合同期限）',
  '日期逻辑（签订日 ≤ 生效日 ≤ 到期日）',
  '模板占位符残留（【填写…】/ XXX / TBD）',
  '合同金额大小写是否一致',
];

/* ---------------------------------------------------------------- 工具 */

function finding(level, category, line, message, advice, evidence) {
  return { level, category, line, message, advice, evidence };
}

/** 文本归一：去掉空白与常见标点，用于比较 */
function normText(s) {
  return String(s == null ? '' : s)
    .replace(/\s+/g, '')
    .replace(/[，。；：、（）()【】\[\]"'"'《》<>·—\-_,.;:]/g, '')
    .toLowerCase();
}

/* --------------------------------------------------- 1. 条款切分与对齐 */

const CLAUSE_RE = /^第\s*([一二三四五六七八九十百零〇\d]+)\s*条/;
const ARTICLE_RE = /^Article\s+(\d+)/i;
// 兜底口径：合同不用「第X条」时才启用，避免把条款内部的 1. 2. 3. 误切成新条款
const FALLBACK_RE = /^(第\s*[一二三四五六七八九十百零〇\d]+\s*章|[一二三四五六七八九十]+[、.．]|\d+[、.．]\s*\S)/;

/** 从标题行的剩余部分抽「条款标题」，遇到第一个标点就停 */
function titleOf(rest) {
  const t = String(rest || '').trim();
  if (!t) return '';
  const cut = t.split(/[：:。；;，,（(【\[]/)[0].trim();
  return (cut || t).slice(0, 16);
}

function segmentClauses(text) {
  const lines = String(text == null ? '' : text).split(/\r?\n/);
  const hasMain = lines.some((l) => CLAUSE_RE.test(l.trim()) || ARTICLE_RE.test(l.trim()));
  const head = hasMain ? null : FALLBACK_RE;

  const out = [];
  let cur = null;
  lines.forEach((raw, i) => {
    const line = raw.trim();
    const m = CLAUSE_RE.exec(line);
    let no = '';
    let rest = '';
    if (m) { no = m[1]; rest = line.slice(m[0].length); }
    else {
      const a = ARTICLE_RE.exec(line);
      if (a) { no = a[1]; rest = line.slice(a[0].length); }
      else if (head && head.test(line)) { no = ''; rest = line; }
    }
    if (no !== '' || (head && head.test(line))) {
      cur = { no, title: titleOf(rest), body: line, line: i + 1 };
      out.push(cur);
    } else if (cur) {
      cur.body += '\n' + raw;
    }
  });
  return out.filter((c) => c.body.trim().length > 0);
}

/** 条款的对齐键：优先用标题文本（编号会因增删条款而错位），没有标题才退回编号 */
function clauseKey(c) {
  const t = normText(c.title);
  if (t) return 'T:' + t;
  return 'N:' + normText(c.no);
}

function align(contracts) {
  const groups = new Map();
  contracts.forEach((c, ci) => {
    c.clauses.forEach((cl) => {
      const k = clauseKey(cl);
      if (!groups.has(k)) groups.set(k, { key: k, title: cl.title || ('第' + cl.no + '条'), byContract: new Map() });
      const g = groups.get(k);
      if (!g.byContract.has(ci)) g.byContract.set(ci, cl);
    });
  });
  return groups;
}

/**
 * 标题近似合并。
 * 真实场景：同一模板下有的写「第八条 违约责任」、有的写「第八条 违约责任与赔偿」。
 * 只按标题精确对齐会被误报成**两条缺条**（写测试时真的踩到）。
 * 规则：标题互为包含、且**覆盖的合同不重叠**时才合并 —— 重叠说明它们本就是各自的独立条款。
 */
function mergeSimilarTitles(groups) {
  const keys = [...groups.keys()];
  for (let i = 0; i < keys.length; i++) {
    for (let j = i + 1; j < keys.length; j++) {
      const a = groups.get(keys[i]), b = groups.get(keys[j]);
      if (!a || !b) continue;
      const ta = String(a.title).replace(/\s/g, ''), tb = String(b.title).replace(/\s/g, '');
      if (!ta || !tb) continue;
      if (!(ta === tb || ta.includes(tb) || tb.includes(ta))) continue;
      if ([...a.byContract.keys()].some((k) => b.byContract.has(k))) continue;
      const keep = a.byContract.size >= b.byContract.size ? a : b;
      const drop = keep === a ? b : a;
      drop.byContract.forEach((v, k) => keep.byContract.set(k, v));
      if (String(keep.title).length < String(drop.title).length) keep.title = drop.title;
      groups.delete(drop.key);
    }
  }
}

/* --------------------------------------------------------- 各项检查 */

function excerpt(s, n) {
  const t = String(s || '').replace(/\s+/g, ' ').trim();
  return t.length > (n || 40) ? t.slice(0, n || 40) + '…' : t;
}

/** 缺条 / 多条 */
function checkMissing(groups, contracts) {
  const out = [];
  groups.forEach((g) => {
    const missing = contracts.map((c, i) => ({ c, i })).filter((x) => !g.byContract.has(x.i));
    if (!missing.length) return;
    const first = g.byContract.values().next().value;
    out.push(finding('P1', '缺条', first ? first.line : 0,
      `条款「${g.title}」有 ${contracts.length - missing.length} 份合同写了、`
      + `${missing.length} 份没有：${missing.map((x) => x.c.name).join('、')}。`,
      '同一模板下的合同条款应当一致；请确认是遗漏、是被删掉，还是这一份本来就另用模板。',
      missing.map((x) => x.c.name)));
  });
  return out;
}

/** 条款正文差异 */
function checkClauseDiff(groups, contracts) {
  const out = [];
  groups.forEach((g) => {
    const versions = new Map();
    g.byContract.forEach((cl, ci) => {
      const key = normText(cl.body);
      if (!versions.has(key)) versions.set(key, { clause: cl, names: [] });
      versions.get(key).names.push(contracts[ci].name);
    });
    if (versions.size < 2) return;
    const list = [...versions.values()].sort((a, b) => b.names.length - a.names.length);
    out.push(finding('P1', '条款正文不一致', list[0].clause.line,
      `条款「${g.title}」在 ${contracts.length} 份合同里有 ${versions.size} 个不同版本：`
      + list.map((v) => `${v.names.length} 份写的是「${excerpt(v.clause.body)}」`).join('；') + '。',
      '同一条款出现多个版本，通常是某一两份被单独改过；请逐份确认是有意为之还是遗漏。',
      list.map((v) => `${v.names.join('、')}：${v.clause.body}`)));
  });
  return out;
}

/* -------------------------------------------------------------- 主流程 */

function analyze(contracts) {
  const groups = align(contracts);
  mergeSimilarTitles(groups);

  const findings = [
    ...checkMissing(groups, contracts),
    ...checkClauseDiff(groups, contracts),
  ];

  const comparison = [...groups.values()].map((g) => {
    const versions = new Set([...g.byContract.values()].map((cl) => normText(cl.body)));
    return {
      clause: g.title,
      covered: g.byContract.size,
      total: contracts.length,
      versions: versions.size,
      missing: contracts.filter((c, i) => !g.byContract.has(i)).map((c) => c.name),
    };
  }).sort((a, b) => (b.missing.length - a.missing.length) || (b.versions - a.versions));

  const summary = { p0: 0, p1: 0, p2: 0 };
  const byCategory = {};
  findings.forEach((f) => {
    const k = f.level === 'P0' ? 'p0' : (f.level === 'P1' ? 'p1' : 'p2');
    summary[k]++;
    byCategory[f.category] = (byCategory[f.category] || 0) + 1;
  });
  summary.total = findings.length;
  summary.by_category = byCategory;
  summary.verdict = summary.p0 > 0
    ? '发现必须处理的硬错误（P0）'
    : (summary.p1 > 0 ? '没有 P0，但有需要人工确认的条款偏离（P1）'
      : '在上述检查项范围内没有发现问题 —— 这不等于没有问题');

  return {
    findings, summary, comparison,
    contractCount: contracts.length,
    clauseCount: groups.size,
    contracts: contracts.map((c) => ({ name: c.name, clauseCount: c.clauses.length })),
  };
}

/* ------------------------------------------------------------ 材料收集 */

function normContract(x, i) {
  if (x && typeof x === 'object' && typeof x.text === 'string') {
    return { name: String(x.name || x.title || `合同${i + 1}`).slice(0, 40), text: x.text };
  }
  if (typeof x === 'string') return { name: `合同${i + 1}`, text: x };
  return null;
}

function splitContractsFromText(text) {
  const lines = String(text || '').split(/\r?\n/);
  const blocks = [];
  let cur = null;
  lines.forEach((l) => {
    const t = l.trim();
    const m = /^(?:#{1,3}\s*)?(?:【)?(合同\s*[一二三四五六七八九十A-Za-z\d]+|第\s*[一二三四五六七八九十\d]+\s*份(?:合同)?|===+\s*(.+?)\s*===+)(?:】)?\s*$/.exec(t);
    if (m) {
      cur = { name: (m[2] || m[1]).trim(), lines: [] };
      blocks.push(cur);
      return;
    }
    if (cur) cur.lines.push(l);
    else { cur = { name: '合同1', lines: [] }; blocks.push(cur); }
  });
  return blocks.map((b) => ({ name: b.name, text: b.lines.join('\n') }))
    .filter((b) => b.text.trim().length > 0);
}

function collectContracts(payload) {
  const p = payload && typeof payload === 'object' ? payload : {};
  if (Array.isArray(p.contracts) && p.contracts.length) {
    return p.contracts.map(normContract).filter(Boolean);
  }
  if (typeof p.text === 'string' && p.text.trim()) {
    const byMarker = splitContractsFromText(p.text);
    if (byMarker.length >= 2) return byMarker;
    const blocks = p.text.split(/\n[ \t]*\n+/).map((x) => x.trim()).filter(Boolean);
    if (blocks.length >= 2) return blocks.map((b, i) => ({ name: `合同${i + 1}`, text: b }));
  }
  return [];
}

/* ------------------------------------------------------------------ run */

function insufficient(missing, advice) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice };
}

function run(payload) {
  const raw = collectContracts(payload);
  if (raw.length === 0) {
    return insufficient(['没有收到任何合同正文'],
      '请提供至少两份合同：contracts 数组，每项形如 {"name":"合同A","text":"第三条 服务期限…"}；'
      + '也可以用一个 text，每份合同用单独一行「合同一」「合同二」这样的分节标题开头（或空行分隔）。');
  }
  const enabled = raw.filter((c) => c.text.trim().length >= 30);
  if (enabled.length < 2) {
    return insufficient([
      `收到 ${raw.length} 份，但其中正文足够长的只有 ${enabled.length} 份`,
    ], '横向比对至少需要**两份**都有实质正文的合同；请补齐后再跑。只有一份时无从比对，本工具不会硬给结论。');
  }
  const contracts = enabled.map((c) => ({ name: c.name, text: c.text, clauses: segmentClauses(c.text) }));
  if (contracts.every((c) => c.clauses.length === 0)) {
    return insufficient(['两份合同的正文里都没有识别出任何条款标题'],
      '本工具靠「第X条」这类条款标题来对齐。请确认正文里保留了条款标题；'
      + '如果合同确实没有分条，本工具无法做横向对齐（不会用猜测凑出结论）。');
  }
  const result = analyze(contracts);
  result.scope = { given: CHECKS_GIVEN.slice(), withheld: CHECKS_WITHHELD.slice() };
  return { status: 'success', result: result };
}

module.exports = {
  run,
  analyze,
  collectContracts,
  splitContractsFromText,
  segmentClauses,
  clauseKey,
  normText,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
  CHECKS_EXECUTED: CHECKS_GIVEN,
  CHECKS_OUT_OF_SCOPE: [
    '判断哪一份条款对甲方/乙方更有利（那是法务与商务的判断）',
    '给出法律意见、认定条款是否有效或是否违法',
    '核对签署人权限、印章真伪或签署流程是否合规',
    '把两份法律含义不同但用词相近的条款认定为"等价"（本工具只做文本的AI比对）',
    '连接合同管理系统或电子签平台取数（本工具只处理你贴进来的文本）',
  ],
  SAMPLE_TEXT: [
    '合同一',
    '技术服务合同',
    '甲方：北京星河科技有限公司',
    '乙方：上海云帆信息技术有限公司',
    '签订日期：2026-03-01',
    '',
    '第三条 服务期限',
    '本协议自 2026年3月1日 起生效，至 2027年2月28日 止。',
    '',
    '第五条 合同金额',
    '合同总金额：人民币壹拾万元整（小写 100,000.00）。',
    '',
    '第八条 违约责任',
    '任何一方违约，应向对方支付合同总金额 5% 的违约金。',
    '',
    '第十条 争议解决',
    '双方同意向北京市朝阳区人民法院提起诉讼。',
    '',
    '合同二',
    '技术服务合同',
    '甲方：北京星河科技有限公司',
    '乙方：上海云帆信息技术有限公司',
    '签订日期：2026-04-01',
    '开户银行：【填写：开户银行】',
    '',
    '第三条 服务期限',
    '本协议自 2026年3月1日 起生效，至 2027年2月28日 止。',
    '',
    '第五条 合同金额',
    '合同总金额：人民币壹拾万元整（小写 100,000.00）。',
    '',
    '第七条 保密义务',
    '双方对履约过程中知悉的商业秘密保密，保密期为五年。',
    '',
    '第八条 违约责任',
    '任何一方违约，应向对方支付合同总金额 2% 的违约金。',
    '',
    '第十条 争议解决',
    '双方同意向上海市浦东新区人民法院提起诉讼。',
  ].join('\n'),
};
