/**
 * engine/light/distill.mjs — 轻量后端的蒸馏器
 *
 * 从 evolver generic-chat 格式的 transcript 起草 Gene（schema 1.13.0 对齐）。
 * 与 evolver `ingest --distill` 的关键差异（本项目方法论）：
 *   **信号提取只用 `is_error === true` 的 tool 消息内容**（精确口径），
 *   而非全文关键词匹配——避免把正文中"提及"的错误计为真实错误。
 *
 * 产出与 evolver 后端可互操作（同 schema、同 id 命名、同 asset_id 约定）。
 */
import fs from 'node:fs';
import crypto from 'node:crypto';

/** transcript 读取（role: system/user/assistant/tool；坏行跳过） */
export function readTranscript(p) {
  const msgs = [];
  let raw = '';
  try { raw = fs.readFileSync(p, 'utf8'); } catch { return msgs; }
  for (const line of raw.split('\n')) {
    const s = line.trim();
    if (!s) continue;
    try { msgs.push(JSON.parse(s)); } catch { /* 跳过 */ }
  }
  return msgs;
}

const textOf = (m) => {
  const c = m?.content;
  if (typeof c === 'string') return c;
  if (Array.isArray(c)) return c.map((x) => (typeof x === 'string' ? x : x?.text ?? x?.content ?? '')).join(' ');
  return c == null ? '' : JSON.stringify(c);
};

export const SIGNAL_RULES = [
  [/\bUnicodeDecodeError|invalid start byte|codec can't decode|invalid continuation byte/i, 'encoding-error'],
  [/\bPermissionError|EPERM|EACCES|Permission denied|operation not permitted/i, 'permission-denied'],
  [/\bFileNotFoundError|ENOENT|No such file or directory/i, 'file-not-found'],
  [/\bJSONDecodeError|Expecting value|Expecting property name|malformed JSON/i, 'invalid-json'],
  [/\bECONNREFUSED|ETIMEDOUT|ENOTFOUND|socket hang up/i, 'network-error'],
  [/\bAssertionError|assertion failed/i, 'assertion-failed'],
  [/\bSyntaxError|IndentationError/i, 'syntax-error'],
  [/\bTypeError|ValueError|KeyError|IndexError/i, 'type-or-value-error'],
];

/**
 * 信号提取（精确口径）：
 * - 错误家族：仅从 is_error=true 的 tool 消息提取；
 * - 工具名：从 assistant.tool_calls[].function.name 提取（仅统计实际出错的调用）。
 */
export function extractSignals(msgs) {
  const errTexts = [];
  const callNameById = new Map();
  for (const m of msgs) {
    if (m?.role === 'assistant' && Array.isArray(m.tool_calls)) {
      for (const tc of m.tool_calls) if (tc?.id && tc?.function?.name) callNameById.set(tc.id, tc.function.name);
    }
  }
  const tools = new Set();
  for (const m of msgs) {
    if (m?.role !== 'tool' || m?.is_error !== true) continue;
    errTexts.push(textOf(m));
    const name = callNameById.get(m.tool_call_id);
    if (name) tools.add(name);
  }
  const families = new Set();
  for (const [re, name] of SIGNAL_RULES) if (errTexts.some((t) => re.test(t))) families.add(name);
  const signals = [...tools, ...families];
  return { signals: signals.length ? signals : ['unknown'], hadErrors: errTexts.length > 0, errorCount: errTexts.length };
}

/** 修法抽取：从 assistant 的"修复叙述"中取最具体的一句（含技术手段者优先、靠后者优先） */
export function extractStrategy(msgs, limit = 3) {
  const FIX_CUE = /\b(let me|i'll|i will|fixed|fix|use|using|instead|switch|set|convert|change|handle|read with|open with|specify|rerun|verify|should)\b/i;
  const TECH = /encoding\s*=|utf-?8|gbk|chmod|re-?read|bytes|open\(|json\.loads|loads\(|--|retry|normalize|decode/i;
  const cands = [];
  for (const m of msgs) {
    if (m?.role !== 'assistant') continue;
    for (const sentence of textOf(m).split(/(?<=[.!?])\s+|\n+/)) {
      const s = sentence.trim().replace(/\s+/g, ' ');
      if (s.length < 25 || s.length > 300) continue;
      if (FIX_CUE.test(s)) cands.push(s);
    }
  }
  return cands
    .map((s, i) => ({ s, score: (TECH.test(s) ? 2 : 0) + i / Math.max(cands.length, 1) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map((x) => x.s.replace(/["'`]/g, "'"));
}

/**
 * AVOID/FIX 双段式（0.13.0）：对齐论文《From Procedural Skills to Strategy Genes》
 * (arXiv:2604.15097)——最优控制形态是「极度蒸馏后的独立 AVOID 警告」，而非叙述型修法。
 * 目标：信号密度更高（≤60 词）、可直接约束行为。
 */
export const AVOID_TEMPLATES = {
  'encoding-error': "reading a non-UTF-8 (GBK/GB18030) file with the default utf-8 codec",
  'permission-denied': "writing to a read-only path without restoring write permission first",
  'file-not-found': "assuming a path exists before listing/verifying the directory",
  'invalid-json': "parsing malformed JSON with a strict loader and no fallback",
  'network-error': "calling an endpoint with no timeout/retry handling",
  'syntax-error': "running a script without a syntax check right after editing it",
  'type-or-value-error': "assuming a value's type instead of coercing/validating it",
  'assertion-failed': "trusting unverified intermediate output",
  unknown: 'repeating the first approach after it failed, instead of inspecting the error',
};

/** 从错误文本里抽取"具体对象"，**按信号族选择提取类型**（避免错位，如把修法里的 utf-8-sig 当成编码对象） */
function concreteObject(errTexts, signals = []) {
  const all = errTexts.join('\n');
  const findFile = () => {
    const m = all.match(/File "([^"]{3,60})"/) || all.match(/([\w.-]+\.(?:py|json|jsonl|txt|md|cfg|ini|yaml|yml|toml|sh|js|ts))/);
    return m ? m[1].split(/[\\/]/).pop() : '';
  };
  const findEnc = () => {
    // 只认"导致解码失败"的编码名：优先错误行里的编码，排除 utf-8-sig（那是解法）
    const m = all.match(/\b(gbk|gb18030|gb2312|latin-?1)\b/i) || all.match(/\b(utf-?8-?sig)\b/i);
    return m ? m[1] : '';
  };
  const findCmd = () => {
    const m = all.match(/\b(nul|python3?|bash|curl|node)\b/);
    return m ? m[1] : '';
  };
  let obj = '';
  if (signals.includes('encoding-error')) obj = findEnc() || findFile();
  else if (signals.includes('file-not-found')) obj = findFile();
  else obj = findFile() || findCmd();
  return obj ? ` (${obj})` : '';
}

/** 把修法句压成可执行 FIX 片段：优先抽"动作子句"，退化为精简整句（≤40 词） */
function condenseFix(sentence) {
  let raw = String(sentence || '').replace(/\s+/g, ' ').trim();
  if (!raw) return '';
  // 1) 显式修法标记之后的内容（"fixed by …" / "fix: …" / "solution: …"）
  const marker = raw.match(/(?:fixed by|resolved by|fix(?:ed)?[:—–-]|solution:|the fix(?: is| was)?[:]?)\s*(.{8,})$/i);
  if (marker) raw = marker[1];
  else {
    // 2) 抽取含技术动作的片段（use/read with/open with/switch to/pass/set/chmod + 参数）
    const act = raw.match(/(?:^|[,;—–-]\s*)((?:use|read|open|switch|pass|set|specify|convert|chmod|decode|parse|re-?run)[^.;]{8,140})/i);
    if (act) raw = act[1];
    else {
      // 3) 去噪声开头（Let me / Done / The file uses X rather than Y，which caused…）
      raw = raw
        .replace(/^(let me|i'?ll|i will|done\.?|here(?:'s| is)[^:]*:)\s*/i, '')
        .replace(/^the (?:file|script|issue|problem|key fix)[^—–]*?(?:caused|because|since)[^—–]*?[—–]\s*/i, '')
        .replace(/^[,;:\s]+/, '');
    }
  }
  const words = raw.split(' ').filter(Boolean);
  return words.length > 40 ? words.slice(0, 40).join(' ') + '…' : words.join(' ');
}

/** 产出 AVOID/FIX 双段式 strategy（信号密度优先） */
export function formatAvoidFix(errTexts, fixSentence, signals = []) {
  const fam = signals.find((s) => AVOID_TEMPLATES[s]) ?? 'unknown';
  const avoid = `AVOID: ${AVOID_TEMPLATES[fam]}${concreteObject(errTexts, signals)}.`;
  const fix = `FIX: ${condenseFix(fixSentence) || 'curate a concrete fix (params/command/encoding).'}`;
  return `${avoid} ${fix}`;
}

/** 组装 Gene（schema 1.13.0） */
export function buildGene({ msgs, category = 'repair', strategy, summary, source, strategyFormat = 'narrative', antiPatterns = [] }) {
  const digest = crypto.createHash('sha256').update(JSON.stringify(msgs)).digest('hex');
  const { signals } = extractSignals(msgs);
  let strat = (strategy ?? extractStrategy(msgs)).slice(0, 3);
  // 0.13.0：可选输出 AVOID/FIX 双段式（对齐论文 arXiv:2604.15097 的控制形态）。
  // **默认仍为 narrative**——本地 A/B 未显示效应优势，且 AVOID 文本更长（实测 106 vs 61 字符），故不作为默认。
  if (strategyFormat === 'avoid' && strat.length) {
    const errTexts = msgs.filter((m) => m?.role === 'tool' && m?.is_error === true).map(textOf);
    strat = [formatAvoidFix(errTexts, strat[0], signals), ...strat.slice(1)];
  }
  return {
    type: 'Gene',
    schema_version: '1.13.0',
    id: `gene_distilled_${digest.slice(0, 8)}`,
    category,
    signals_match: signals,
    strategy: strat.length ? strat : ['(no concrete fix sentence extracted — needs curation)'],
    anti_patterns: Array.isArray(antiPatterns) ? antiPatterns : [],
    constraints: { max_files: 12, forbidden_paths: ['.git', 'node_modules'] },
    validation: [],
    summary: summary ?? `Light-distilled from session (UNPROVEN — curate via review): ${signals.join(', ')}`,
    generation_meta: { source: source ?? 'light-distill' },
    claims: [{ predicate: 'output_contract', kind: 'behavioral' }],
    scope: { signals: signals.map((s) => `capability:${s}`) },
    asset_id: `sha256:${digest}`,
  };
}

/** 主入口：transcript 路径 → { gene, raw } */
export function distillFromTranscript(transcriptPath, opts = {}) {
  const msgs = readTranscript(transcriptPath);
  if (!msgs.length) throw new Error(`transcript 为空或不可读: ${transcriptPath}`);
  const st = extractSignals(msgs);
  // 行为对齐 evolver：无真实错误（is_error 计数为 0）时不起草 —— "not enough to distill, Nothing stored"
  if (st.errorCount === 0) {
    return { gene: null, raw: '[pi-evox] no error signals in session (is_error count = 0) — Nothing stored' };
  }
  const gene = buildGene({ msgs, category: opts.category ?? 'repair', source: 'light-distill', strategyFormat: opts.strategyFormat ?? 'narrative' });
  const raw = `[pi-evox] drafted UNPROVEN gene ${gene.id} (${gene.asset_id.slice(0, 14)}…) — quarantined\n            signals_match: ${gene.signals_match.join(', ')}\n            errors seen: ${st.errorCount}`;
  return { gene, raw };
}

/** manual 蒸馏（LLM 精修路径使用）：直接给 strategy/summary 入库 */
export function distillManual({ category = 'repair', signals = [], strategy, summary, antiPatterns = [], source = 'light-manual', shareable = false }) {
  // 占位符守卫：引导草稿未补全 FIX 时拒绝落库（避免产出低质量基因）。
  if (/<在此填写|<\s*在此/.test(String(strategy || ''))) {
    return { gene: null, raw: '[pi-evox] 拒绝：strategy 仍是占位符，请补全 FIX（具体参数/命令/编码）后再提交' };
  }
  const payload = { strategy, signals, at: Date.now() };
  const digest = crypto.createHash('sha256').update(JSON.stringify(payload)).digest('hex');
  const sig = signals.length ? signals : ['manual'];
  const gene = {
    type: 'Gene',
    schema_version: '1.13.0',
    id: `gene_manual_${digest.slice(0, 8)}`,
    category,
    signals_match: sig,
    strategy: [strategy],
    anti_patterns: Array.isArray(antiPatterns) ? antiPatterns : [],
    constraints: { max_files: 12, forbidden_paths: ['.git', 'node_modules'] },
    validation: [],
    summary: summary ?? `Manually distilled: ${sig.join(', ')}`,
    generation_meta: { source },
    // 共享基因库（0.14.9）：显式 opt-in 才可导出/入池；默认 false（不外发）。
    shareable: shareable === true,
    claims: [{ predicate: 'output_contract', kind: 'behavioral' }],
    scope: { signals: sig.map((s) => `capability:${s}`) },
    asset_id: `sha256:${digest}`,
  };
  return { gene, raw: `[pi-evox] drafted UNPROVEN gene ${gene.id} (${gene.asset_id.slice(0, 14)}…) — quarantined${gene.shareable ? ' [shareable]' : ''}` };
}


/**
 * 从错误文本抽取「错误家族 + 信号 + 预填 AVOID 模板」（0.16.0 提到共享模块）。
 * 原先只定义在 light-cli 里，召回侧拿不到；现在 light-cli（沉淀）与
 * evolver-recall（`--error` 报错即召回）共用同一套抽取逻辑，保证口径一致。
 */
const ANTI_TAGS = {
  'encoding-error': 'assume-default-utf8',
  'permission-denied': 'write-without-restore-perm',
  'file-not-found': 'assume-path-exists',
  'invalid-json': 'strict-parse-no-fallback',
  'network-error': 'call-without-timeout-retry',
  'syntax-error': 'run-without-syntax-check',
  'type-or-value-error': 'assume-value-type',
  'assertion-failed': 'trust-unverified-output',
  unknown: 'repeat-failed-approach',
};
const ANTI_TOKENS = {
  // 仅"能用无歧义单 token 表达被禁止主张"的家族才有值；其余刻意留空。
  // 'utf-8'：对方若主张"直接用 utf-8 读（默认编码）"，即与本基因的"按真实编码读取"冲突。
  // 注意不要放 'json.loads' 这类**双方都会出现**的 token（合规方也写它 → 误删）。
  'encoding-error': ['utf-8'],
};

export function proposeFromError(error, { tool = '', context = '' } = {}) {
  const text = String(error || '');
  const families = new Set();
  for (const [re, name] of SIGNAL_RULES) if (re.test(text)) families.add(name);
  const signals = [...new Set([...(tool ? [tool] : []), ...families])];
  const fam = signals.find((s) => AVOID_TEMPLATES[s]) ?? 'unknown';
  const object = (text.match(/([\w.-]+\.(?:py|json|jsonl|txt|md|cfg|ini|yaml|yml|toml|sh|js|ts))/) || [])[1] || '';
  const objStr = object ? ` (${object})` : '';
  const avoid = `AVOID: ${AVOID_TEMPLATES[fam]}${objStr}.`;
  const strategy = `${avoid} FIX: <在此填写可执行修法，例如 use encoding='gbk' / 先 chmod u+w 再写 / 先 ls 确认路径>`;
  const head = text.replace(/\s+/g, ' ').trim().slice(0, 80);
  const antiTag = ANTI_TAGS[fam] || ANTI_TAGS.unknown;
  const summary = `${fam} 失败${context ? `（${context}）` : ''} [AVOID ${antiTag}]: ${head}`;
  return {
    signals: signals.length ? signals : ['manual'],
    strategy,
    summary,
    antiTag,
    antiPatterns: [...(ANTI_TOKENS[fam] || [])],
    family: fam,
  };
}
