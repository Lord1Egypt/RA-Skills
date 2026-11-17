#!/usr/bin/env node
/**
 * evolver-recall.mjs — 智能体经验库「召回 + 命中登记」（Pi × EvoX Lab 运行时）
 *
 * 任务开始时调用（无参数）：
 *   输出已审核（approved）且通过修法守卫的编号经验列表，供智能体读入上下文。
 * 任务结束调用（登记命中）：
 *   node evolver-recall.mjs --register-hit --gene <asset_id或gene_id> --note "<任务一句话>"
 *   （N = 召回输出中的编号；内部解析为 gene_id 落 experiments/hits.jsonl）
 *
 * 设计纪律：
 *   - 只输出 approved 且命中修法信号词（REPAIR_SIGNAL_RE）的 strategy——宁缺毋滥（报告 §21）
 *   - 审核状态以台账「最后一条」为准（last-write-wins）——quarantine 必须能撤销 approved
 *   - 首段若是会话旁白（NARRATION_RE）→ 跳过（不可执行，且 P0 自动召回会放大噪声）
 *   - 命中登记落在 EVOX_HITS_DIR（默认 <cwd>/experiments/hits.jsonl），用于月度命中率盘点
 *   - 纯 Node 标准库，无第三方依赖
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { withLock, isApprovedState } from './engine/light/store.mjs';
import { proposeFromError } from './engine/light/distill.mjs';
import { REPAIR_SIGNAL_RE, NARRATION_RE, RETRY_LOG_RE } from './engine/light/guards.mjs';

// 0.16.0 Q3-1：注入守卫。静态导入（同目录，无网络）；外层 try 保证**模块缺失也不能让召回崩掉**
// ——宁可降级为「不加这道守卫」，也绝不能因守卫失败导致宿主 bootstrap 失败。
// 0.36 B-2（aig 0.35 加固建议①落地）：降级不再静默——显式一次性中文告警到 stderr，
// 与安全声明「召回侧跳过注入门」的语义对齐，doctor 可据此汇总守卫降级状态。
let injectionScan = null;
try {
  ({ injectionScan } = await import(new URL('./injection_scan.mjs', import.meta.url).href));
} catch (e) {
  injectionScan = null;
  console.error('[pi-evox] ⚠ 注入守卫降级：injection_scan.mjs 缺失或加载失败（' + (e?.code || e?.message || e) + '）');
  console.error('         → 本次召回**不经过注入守卫**（修法/叙述/脱敏三门照常；导出/导入仍 fail-closed）。');
  console.error('         → 修正：恢复 code/injection_scan.mjs 后重跑，或用 `node code/tests/injection-regression.mjs` 自检。');
}

// ── 统一错误输出（0.14.7，回应 skillhub errorHandling 4.3「缺统一错误码 / 中英文混杂 / 生硬退出」）──
// 退出码约定：0=成功；1=运行期失败；2=用法错误（缺参数 / 用法错误）。统一前缀 [pi-evox]，
// 需要时附「→ 修正：」一行可执行指引，避免只丢退出码。本文件全程 fail-closed / 守卫不变。
function fail(msg, { hint, code = 2 } = {}) {
	console.error(`[pi-evox] ✗ ${msg}`);
	if (hint) console.error(`         → 修正：${hint}`);
	process.exit(code);
}

const EVO_STORE = process.env.EVO_STORE_DIR || path.join(os.homedir(), '.evomap', 'assets');
const EVO_GENES = path.join(EVO_STORE, 'genes.jsonl');
const EVO_REVIEW = path.join(EVO_STORE, 'review.jsonl');
// 0.17.0：默认落点 = **技能根/experiments**（脱离 cwd——此前在别的目录跑会让埋点散落、info 误报「从未召回」；
// 既有部署（显式配置的钩子）传 EVOX_HITS_DIR，不受影响）
const HITS_DIR = process.env.EVOX_HITS_DIR || path.join(path.dirname(path.dirname(fileURLToPath(import.meta.url))), 'experiments');
const HITS_FILE = path.join(HITS_DIR, 'hits.jsonl');
const RECALL_CALLS_FILE = path.join(HITS_DIR, 'recall_calls.jsonl');
/** 0.15.0 P0-3：注入即登记（pending → 命中/未命中），闭合「召回→注入→效果」漏斗。
 *  私有节点实测：hits.jsonl 仅 1 条（部署自检），说明"注入后是否真避免"从未被记录。 */
const PENDING_FILE = path.join(HITS_DIR, 'pending_injections.jsonl');

/**
 * 埋点：记录一次 recall 调用（仅 recall 模式，不含 register-hit）。
 * P3（2026-09-23）扩为**按调用方**记录：agent + 是否对靶 + 实际注入条数 + 查询摘要。
 * 动机：旧埋点只有 {ts,mode}，无法回答"哪个宿主注入了几条、是否多为空注入"——
 * 多个智能体宿主共享本实现，需按 agent 分离观测。
 * 向后兼容：未传 --agent 时记为 'unknown'；写失败不影响 recall 主流程。
 * 0.15.0：新增 taskText（清洗后意图）与 noise（原始 query 清洗后是否变空）两个字段。
 */
function recordRecallCall(extra = {}) {
	try {
		withLock(HITS_DIR, () => {
			fs.mkdirSync(HITS_DIR, { recursive: true });
			fs.appendFileSync(RECALL_CALLS_FILE, JSON.stringify({
				ts: new Date().toISOString(), mode: 'recall', agent: AGENT,
				targeted: !!extra.targeted, injected: Number.isFinite(extra.injected) ? extra.injected : 0,
				query: String(extra.query ?? '').slice(0, 200),
				taskText: String(extra.taskText ?? '').slice(0, 200),
				noise: !!extra.noise,
			}) + '\n');
		});
	} catch { /* 写失败不影响 recall 主流程 */ }
}

/** 0.15.0 P0-3：把本次注入的 gene_id 落 pending，供 --register-hit / --negate 回填。 */
function recordPending(picked) {
	try {
		const ts = new Date().toISOString();
		withLock(HITS_DIR, () => {
			fs.mkdirSync(HITS_DIR, { recursive: true });
			for (const it of picked) {
				fs.appendFileSync(PENDING_FILE, JSON.stringify({
					ts, agent: AGENT, gene_id: it.id, asset_id: it.assetId,
					category: it.category, taskText: String(TASK_TEXT || '').slice(0, 200),
				}) + '\n');
			}
		});
	} catch { /* 留痕失败不影响召回 */ }
}


// REPAIR_SIGNAL_RE / NARRATION_RE 已抽到 engine/light/guards.mjs 共享（0.17.0，沉淀与召回同口径）

/* 叙述检测（NARRATION_RE）已抽到 engine/light/guards.mjs 共享——0.17.0，沉淀与召回同口径 */

function readJsonl(p) {
	const out = [];
	try {
		for (const [idx, line] of fs.readFileSync(p, 'utf8').split('\n').entries()) {
			const s = line.trim();
			if (!s) continue;
			try {
				out.push(JSON.parse(s));
			} catch (err) {
				const preview = s.length > 140 ? s.slice(0, 140) + '…' : s;
				console.error(`[pi-evox] ⚠ ${p} 第 ${idx + 1} 行不是合法 JSON，已跳过（原因：${err.message}）`);
				console.error(`         该行内容：${preview}`);
				console.error(`         → 修正：检查该行是否缺引号/逗号/括号；或用 light-cli 重新沉淀该条；不影响其他基因流转。`);
			}
		}
	} catch { /* 文件不存在 → 空 */ }
	return out;
}

/**
 * 聚合 experiments/hits.jsonl 得 per-gene 命中计数（按 gene_id）。
 * P1④ 负载均衡偏置的数据基础（FlyLoRA / Switch Transformer 的 c_i）。
 */
// 0.32 B-6：本机压缩方案族（未知则空串 ⇒ scoreGene 完全不加权，行为与 0.31 一致）。
// ⚠️ 必须用动态 import：本文件是 ESM（.mjs），require 未定义（实测踩过：用 require 会被
//    try/catch 吞掉、localKv 恒空、加权静默失效）。
async function localKvFamily() {
	const explicit = (process.env.EVOX_KV_COMPRESSION || '').slice(0, 40);
	if (explicit) return explicit === 'unknown' ? '' : explicit;
	try {
		const { kvCompressionOf } = await import('./engine/light/store.mjs');
		const fam = kvCompressionOf(process.env.EVOX_SOURCE_MODEL || '');
		return fam === 'unknown' ? '' : fam;
	} catch { return ''; }
}

async function aggregateHits() {
	const counts = new Map();
	let total = 0;
	for (const h of readJsonl(HITS_FILE)) {
		const id = h && h.gene_id;
		if (!id) continue;
		counts.set(id, (counts.get(id) || 0) + 1);
		total++;
	}
	const mean = counts.size ? total / counts.size : 0;
	return { counts, mean, localKv: await localKvFamily(), decay: geneDecay() };
}

/**
 * 0.33 C-7：基因有效性衰减——skillhub 0.31 评测建议③的落地（"基因有效性衰减机制"）。
 * 对每个**有反馈**（hit/negate 至少一条）的基因算一个 [0.25, 1] 的乘性衰减因子：
 *   · 时间半衰期：0.5^(距上次反馈天数 / 半衰期)，半衰期默认 90 天（EVOX_GENE_DECAY_DAYS）
 *   · 否定压力：negate ≥ 2 且否定率 ≥ 0.5 ⇒ 再乘 0.5（"该修法已多次未奏效"）
 *   · 地板 0.25：衰减永不单独杀死基因（硬过滤仍是审核门控 + 守卫，职责不混）
 * 设计纪律（宁缺毋滥，三条都不破）：
 *   · **无反馈的基因不衰减**——unproven 由审核门控管，不双重惩罚（否则新基因永无出头日）
 *   · 只做排序偏置：与 kv 同族加权同性质，阈值（MIN_MATCH_SCORE）与语义匹配分保持主导
 *   · 默认开但可一键关：EVOX_GENE_DECAY=0 ⇒ 返回空 Map，行为与 0.32 完全一致
 */
function geneDecay() {
	if (process.env.EVOX_GENE_DECAY === '0') return new Map();
	const halfLife = Number(process.env.EVOX_GENE_DECAY_DAYS || 90);
	if (!Number.isFinite(halfLife) || halfLife <= 0) {
		console.error(`[pi-evox] ⚠ EVOX_GENE_DECAY_DAYS=${process.env.EVOX_GENE_DECAY_DAYS} 非法，本次不衰减（需正数）`);
		return new Map();
	}
	const agg = new Map();	// id -> { hit, neg, lastTs }
	for (const h of readJsonl(HITS_FILE)) {
		const id = h && h.gene_id;
		if (!id) continue;
		const ts = typeof h.ts === 'string' ? Date.parse(h.ts) : NaN;
		const cur = agg.get(id) || { hit: 0, neg: 0, lastTs: 0 };
		if (h.outcome === 'negated') cur.neg++; else cur.hit++;
		if (Number.isFinite(ts) && ts > cur.lastTs) cur.lastTs = ts;
		agg.set(id, cur);
	}
	const now = Date.now();
	const out = new Map();
	for (const [id, a] of agg) {
		if (a.hit + a.neg === 0) continue;	// 无反馈不衰减
		let factor = 1;
		let days = 0;
		if (a.lastTs > 0) {
			days = Math.max(0, (now - a.lastTs) / 86400000);
			factor *= Math.pow(0.5, days / halfLife);
		}
		const negPress = a.neg >= 2 && a.neg / (a.hit + a.neg) >= 0.5;
		if (negPress) factor *= 0.5;
		out.set(id, { factor: Math.max(0.25, factor), days: Math.round(days), negPress });
	}
	return out;
}

function approvedAssetIds() {
	// 追加式台账 ⇒ 以「每个 assetId 的最后一条状态」为准（last-write-wins）。
	// 修复（2026-09-17 实测）：旧实现只要历史上出现过 approved 就计入，
	// 导致 quarantine 无法撤销已批准 —— 被隔离的基因仍会被召回并注入。
	const latestState = new Map();
	for (const r of readJsonl(EVO_REVIEW)) {
		if (r && typeof r.assetId === 'string' && r.assetId) latestState.set(r.assetId, r.state);
	}
	const set = new Set();
	for (const [assetId, state] of latestState) {
		// 0.31 安全修复：精确比对（旧写法 `includes('approv')` 会放行 unapproved/disapproved）。
		if (isApprovedState(state)) set.add(assetId);
	}
	return set;
}

/** 与 evolver-bridge 同源：approved + 修法守卫，输出 [{id, assetId, category, text, signals}] */
function recallList() {
	const approved = approvedAssetIds();
	const out = [];
	for (const g of readJsonl(EVO_GENES)) {
		const st = g && Array.isArray(g.strategy) ? g.strategy : null;
		if (!st || st.length === 0) continue;
		const aid = g.asset_id;
		// fail-closed（安全修复，2026-09-10）：台账不可用或未 approved → 跳过（旧逻辑在台账缺失时 fail-open）
		if (!aid || !approved.has(aid)) continue;
		const text = st.join(' ').replace(/\s+/g, ' ').trim();
		if (!REPAIR_SIGNAL_RE.test(text)) continue; // 修法守卫：宁缺毋滥
		if (NARRATION_RE.test(String(st[0] ?? '').trim())) continue; // 叙述守卫：旁白开场 → 不可执行，跳过
		if (RETRY_LOG_RE.test(text)) continue; // 0.17.0 重试日志守卫：与沉淀质检同口径——「重试后成功」的复述不是修法（纵深：拦已入库的历史噪音）
		// 0.16.0 Q3-1 注入守卫（第三道）：恶意基因即便已入库（共享导入/误审），
		// 也**绝不允许注入到 system prompt**——这是纵深防御的最后一道。
		// 前两道管「质量」（有没有真修法 / 是不是旁白），这道管「恶意」（是不是提示词注入）。
		if (injectionScan && !injectionScan(g).ok) continue;
		out.push({
			id: g.id,
			assetId: aid || '',
			category: g.category || 'repair',
			text: text.slice(0, 600),
			signals: Array.isArray(g.signals_match) ? g.signals_match : [],
			antiPatterns: Array.isArray(g.anti_patterns) ? g.anti_patterns : [],
			scope: g.scope || null,
			// 0.32 B-5/B-6：压缩方案族（来自 generation_meta.source_kv；0.31 及以前入库的没有此字段 ⇒ undefined）
			sourceKv: (g.generation_meta && g.generation_meta.source_kv) || '',
		});
	}
	return out;
}

// ──────────────────────── P2 对靶匹配 + top-N（2026-09-17）────────────────────────
// 动机（实测）：approved 涨到 20 条后，全量注入 7,128 字符 > 注入上限 3,000 ⇒
// 只注入前 9 条且顺序=文件顺序（等于随机）。对靶 + top-N 才是正解。
//   · 有 --query / EVOX_QUERY：按「signals_match 命中 + 与查询词的 token 交集」打分，
//     **只保留 score>0**（不对靶就不注入——避免不对靶注入的净开销），按分排序取前 N。
//   · 无 query：退化为按入库顺序（追加式 → 靠后更新）取前 N，仅做**数量封顶**，不再任意截断。
/**
 * `--error`：拿**刚弹出的报错原文**直接问「这个错我踩过吗」（0.16.0 T3 触发点）。
 *
 * 为什么这是最自然的触发点：报错是**唯一一个用户/智能体 100% 会注意到、且立刻需要答案**的时刻，
 * 不需要它"记得"先来查——错误本身就来提醒了。价值也最直观：本来要盲目重试，现在先拿到修法。
 *
 * 实现：复用 distill 的 proposeFromError 抽错误家族 → 拼成信号串 → 走同一套打分，口径与沉淀一致。
 */
const ERROR_TEXT = (() => {
	const i = process.argv.indexOf('--error');
	const e = i >= 0 ? (process.argv[i + 1] ?? '') : (process.env.EVOX_ERROR ?? '');
	return String(e || '');
})();

const QUERY = (() => {
	const argv = process.argv.slice(2);
	// 位置参数护栏（0.14.8）：query 必须用 --query "<文本>" 或 EVOX_QUERY。
	// 旧版把裸位置参数（如 `evolver-recall.mjs "处理 GBK 报错"`）静默忽略，回落成
	// 「按入库顺序注入尾部 N 条」——看似有结果实则与当前任务无关，非开发者极难察觉。
	// 现把首个裸位置参数提升为 query 并提示规范写法，消除该静默 footgun。
	const VALUED = ['--query', '--top', '--agent', '--register-hit', '--note', '--error', '--gene', '--record', '--because'];
	const consumed = new Set();
	for (const f of VALUED) {
		const i = argv.indexOf(f);
		if (i >= 0) { consumed.add(i); if (i + 1 < argv.length) consumed.add(i + 1); }
	}
	const stray = argv.filter((a, i) => !consumed.has(i) && !String(a).startsWith('--'));
	const i = process.argv.indexOf('--query');
	let q = i >= 0 ? (process.argv[i + 1] ?? '') : (process.env.EVOX_QUERY ?? '');
	if (stray.length) {
		const head = String(stray[0]).replace(/\s+/g, ' ').trim().slice(0, 60);
		if (!q) {
			q = String(stray[0]);
			console.error(`[pi-evox] ⚠ 检测到位置参数，已按 query 处理：「${head}」`);
			console.error('         → 修正：query 请用 --query "' + head.slice(0, 40) + '" 显式传参（位置参数写法不推荐）');
		} else {
			console.error(`[pi-evox] ⚠ 位置参数「${head}」已被忽略（当前 query 由 --query / EVOX_QUERY 提供）`);
		}
	}
	// T3：给了 --error 就把错误家族信号并入查询，让召回能命中「同类报错的修法」
	if (ERROR_TEXT) {
		try {
			const fam = proposeFromError(ERROR_TEXT, { tool: '', context: '' });
			const sig = (fam && Array.isArray(fam.signals) ? fam.signals : []).join(' ');
			if (sig) q = (q ? q + ' ' : '') + sig + ' ' + ERROR_TEXT.slice(0, 200);
		} catch { /* 抽取失败不影响召回 */ }
	}
	return q;
})();

/**
 * 任务文本清洗（0.15.0 P0-1，治「63% 打分落空」）。
 *
 * 私有节点实测：宿主钩子喂进来的原始消息带大量**与任务无关的注入前缀/样板**，
 * 与基因 signals_match 零交集 ⇒ score<MIN_MATCH_SCORE ⇒ 宁缺毋滥不注入。
 * 实测噪声样本（recall_calls.jsonl 实拉）：
 *   「[企业IM 群消息前缀] 看看这是个什么技术」
 *   「[企业IM 私聊前缀] …」「[OpenClaw heartbeat poll]」
 *   纯 URL「https://mp.weixin.qq.com/s/olTmQF1rBWI…」
 *   「What is the weather?」「reply with the single word OK」（无任务意图的探针）
 *
 * 这里**只剥壳、不改写语义**：去掉信封前缀/纯 URL/心跳样板，保留用户真实诉求。
 * 剥完若为空 ⇒ 视为「无任务意图」（交由 selectList 走不注入路径，见 P0-2）。
 */
const HOST_PREFIX_RE = /^\s*\[(?:[^\]]{0,80})\]\s*/;
const PURE_URL_RE = /^\s*(?:https?:\/\/|www\.)\S+\s*$/i;
const HEARTBEAT_RE = /^\s*\[?\s*(?:openclaw\s+)?(?:heartbeat|heartbeat poll|ping|pong|cron)[^\]]{0,40}\]?\s*$/i;
const PROBE_RE = /^\s*(?:what is the weather[?]?|reply with the single word ok|ping|pong|ok|test|hello|hi)[.?! ]*$/i;

function sanitizeTaskText(raw) {
	let t = String(raw || '').trim();
	if (!t) return '';
	// 反复剥信封前缀（部分宿主会叠多层，如 "[A][B] 正文"）
	for (let i = 0; i < 4; i++) {
		const m = t.match(HOST_PREFIX_RE);
		if (!m || !m[0].trim()) break;
		t = t.slice(m[0].length).trim();
	}
	if (!t) return '';
	if (PURE_URL_RE.test(t) || HEARTBEAT_RE.test(t) || PROBE_RE.test(t)) return '';
	return t.slice(0, 500);
}
/** 清洗后的任务意图（空串 = 无可对靶意图）。埋点与打分共用此值。 */
const TASK_TEXT = sanitizeTaskText(QUERY);

const TOPN = (() => {
	const i = process.argv.indexOf('--top');
	const n = i >= 0 ? Number(process.argv[i + 1]) : Number(process.env.EVOX_TOPN ?? 5);
	return Number.isFinite(n) && n > 0 ? n : 5;
})();
const SELECTION_FILE = path.join(HITS_DIR, '.evox-last-selection.json');
/** P3 溯源（2026-09-23）：调用方身份（宿主）——由钩子以 `--agent <name>` 或 EVOX_AGENT 传入。
 *  仅允许安全字符集；未传/非法 → 'unknown'（向后兼容，不影响既有调用方）。 */
const AGENT = (() => {
	const i = process.argv.indexOf('--agent');
	const v = i >= 0 ? process.argv[i + 1] : process.env.EVOX_AGENT;
	return /^[a-z0-9_.-]{1,32}$/i.test(String(v || '')) ? String(v) : 'unknown';
})();

/**
 * 停用词表：常见英文虚词/泛化词不应制造「假对靶」。
 * 实测教训（2026-09-17）：查询 "what is the capital of France?" 曾误命中 3 条——
 * 因为 "the/what" 这类词与长句 strategy 里的同词重叠而计分。故须过滤 + 设最低分。
 */
const STOP_WORDS = new Set([
	"the", "and", "for", "with", "that", "this", "from", "not", "are", "was", "were", "has", "have", "had", "been",
	"you", "your", "yours", "can", "could", "will", "would", "should", "shall", "may", "might", "must", "its", "our",
	"about", "when", "what", "which", "where", "why", "who", "whom", "how", "there", "here", "then", "than", "them",
	"they", "their", "into", "onto", "out", "over", "under", "again", "once", "only", "just", "also", "very", "more",
	"most", "much", "many", "please", "help", "need", "want", "make", "makes", "made", "get", "gets", "got", "give",
	"take", "takes", "use", "used", "uses", "using", "run", "runs", "ran", "running", "see", "say", "said", "tell",
	"new", "old", "first", "last", "next", "one", "two", "three", "file", "files", "data", "error", "errors", "issue",
	"issues", "problem", "problems", "command", "commands", "fix", "fixes", "failed", "fails", "failure", "true",
	"false", "null", "none", "thing", "things", "way", "ways", "time", "does", "did", "doing", "why", "let", "lets",
]);
/** 最低匹配分：低于此分视为「不对靶」（宁可少注入，避免 §11 的不对靶净开销） */
const MIN_MATCH_SCORE = 2;

function queryTokens(s) {
	const raw = String(s || '').toLowerCase().match(/[a-z0-9_\-./]{3,}|[\u4e00-\u9fa5]{2,}/g) || [];
	const out = new Set();
	for (const t of raw) {
		if (STOP_WORDS.has(t)) continue;
		// 0.15.0 P0-1b：**CJK 段切二元（bigram）**。
		// 根因（私有节点实测 63% 打分落空）：原实现把整段中文当**一个** token，
		// 于是「帮我抓取这个公众号文章」与基因正文「公众号抓取一次成功」永不相交，
		// signals 里的中文词也命中不了 ⇒ score<2 ⇒ 中文任务几乎永远召回不到修法。
		// bigram 无需分词器、零依赖，对中文检索是标准做法（召回率显著提升）。
		if (/[\u4e00-\u9fa5]/.test(t)) {
			const cs = [...t];
			if (cs.length === 1) { out.add(t); continue; }
			for (let i = 0; i + 1 < cs.length; i++) out.add(cs[i] + cs[i + 1]);
		} else {
			out.add(t);
		}
	}
	return out;
}

function scoreGene(item, qTokens, hitInfo) {
	let score = 0;
	for (const sig of item.signals) {
		if (sig && qTokens.has(String(sig).toLowerCase())) score += 3;
	}
	const st = queryTokens(item.text);
	for (const t of qTokens) if (st.has(t)) score += 1;
	// P1④ 负载均衡偏置（FlyLoRA / Switch Transformer 转移）：d_i = -u·sign(c_i − c̄)，
	// 冷门基因（c_i < c̄）上抬、热门（c_i > c̄）下压，缓解"高信号重叠热门基因恒霸榜"；
	// 温和封顶（u=0.4，最大 ±2.0），规模未到（命中全 0 → c_i=c̄=0）时无作用。
	if (hitInfo) {
		const c = hitInfo.counts.get(item.id) || 0;
		const d = c - hitInfo.mean;
		score += -0.4 * Math.sign(d) * Math.min(Math.abs(d), 5);
	}
	// 0.32 B-6：**压缩方案族同族加权**（arXiv:2609.36322 的工程落地）。
	// 论文因果证据：相位敏感性由压缩核决定（CSA 核移植到 Qwen 骨架仍复现），与厂商血统无关
	// ⇒ 同一压缩方案族的模型，位置相关的失败模式可迁移；异族不可直接移植。
	// 做法：仅对**已知同族**加分（未知族一律不奖不罚，宁缺毋滥）。
	//   · 本机族未知（EVOX_KV_COMPRESSION 未设且 source_model 映射不出）⇒ 完全不加，行为与 0.31 一致
	//   · 基因未记录 source_kv ⇒ 不加（不惩罚未知）
	//   · 同族 ⇒ +w（默认 1.5，EVOX_SAME_KV_WEIGHT 可调；设为 0 则关闭）
	// 阈值与语义匹配分（3/1）保持主导：加权只做**同分时的排序偏置**，不制造"低相关但同族"的注入。
	if (hitInfo && hitInfo.localKv && item.sourceKv && item.sourceKv === hitInfo.localKv) {
		const w = Number(process.env.EVOX_SAME_KV_WEIGHT ?? 1.5);
		if (w > 0) score += w;
	}
	// 0.33 C-7：基因有效性衰减（乘性，地板 0.25；无反馈基因不衰减）。
	// 与 kv 加权同性质：只做同分段排序偏置；阈值与语义匹配分保持主导。
	// 衰减后低于 MIN_MATCH_SCORE 的自然落选——这正是"久未验证的修法不再优先注入"的语义。
	if (hitInfo && hitInfo.decay) {
		const d = hitInfo.decay.get(item.id);
		if (d && d.factor < 1) score *= d.factor;
	}
	return score;
}

/**
 * 注入冲突守卫（anti_patterns 与对方 token 集互斥即拦，免训练合并不干扰）：
 * 选中的 top-N 中，若两条基因相互矛盾，剔除低分者（保高分的）。
 * 判定极保守——仅在「一方 anti_patterns 字面命中另一方 strategy 文本」时冲突，
 * 即一方明令禁止的动作被另一方倡导。不引入编码重叠等脆弱启发式（易误删正确基因，违背宁缺毋滥）。
 * 预埋无害：基因普遍无 anti_patterns 或策略不重叠时，守卫不触发。
 */
function tokenSet(str) {
	// 0.15.0：与 queryTokens 同口径——CJK 也走 bigram，避免"召回用 bigram、
	// 冲突守卫用整段"导致判据不一致（两处口径必须一致）。
	const out = new Set();
	for (const t of String(str || '').toLowerCase().match(/[a-z0-9_.-]+|[\u4e00-\u9fa5]{2,}/g) || []) {
		if (/[\u4e00-\u9fa5]/.test(t)) {
			const cs = [...t];
			if (cs.length === 1) { out.add(t); continue; }
			for (let i = 0; i + 1 < cs.length; i++) out.add(cs[i] + cs[i + 1]);
		} else {
			out.add(t);
		}
	}
	return out;
}
function geneConflicts(a, b) {
	const aAnti = new Set((a.antiPatterns || []).map((s) => String(s).toLowerCase()));
	const bAnti = new Set((b.antiPatterns || []).map((s) => String(s).toLowerCase()));
	const aTok = tokenSet(a.text), bTok = tokenSet(b.text);
	for (const ap of aAnti) if (bTok.has(ap)) return true;
	for (const bp of bAnti) if (aTok.has(bp)) return true;
	return false;
}
/** 贪心冲突消解：保留高分项，剔除与已保留项冲突的低分项（若新项更强则替换旧项） */
function resolveConflicts(items, scored) {
	const kept = [];
	for (const it of items) {
		const conflict = kept.find((k) => geneConflicts(k, it));
		if (!conflict) { kept.push(it); continue; }
		if ((scored.get(it.id) || 0) > (scored.get(conflict.id) || 0)) {
			kept.splice(kept.indexOf(conflict), 1);
			kept.push(it);
		}
	}
	return kept;
}

/**
 * 0.18：按 **asset_id 或 gene_id** 解析回填目标——多会话并行下位置编号会漂移
 * （.evox-last-selection.json 是共享单文件，另一会话的 recall 会覆盖它，2026-10-09 实测错记）。
 * 解析顺序：①选择快照内匹配 ②全量召回列表匹配 ③基因库直查。
 */
function resolveRef(ref) {
	if (!ref) return null;
	try {
		const sel = JSON.parse(fs.readFileSync(SELECTION_FILE, 'utf8'));
		if (sel && Array.isArray(sel.ids) && sel.ids.length) {
			const byId = new Map(recallList().map((x) => [x.id, x]));
			if (byId.has(ref)) return byId.get(ref);
			const hit = sel.ids.map((id) => byId.get(id)).filter(Boolean).find((x) => x.assetId === ref || x.id === ref);
			if (hit) return hit;
		}
	} catch { /* 无留痕 → 走全量 */ }
	const all = recallList();
	const hit2 = all.find((x) => x.assetId === ref || x.id === ref);
	if (hit2) return hit2;
	try {
		const storeDir = process.env.EVO_STORE_DIR || path.join(os.homedir(), '.evomap', 'assets');
		for (const line of fs.readFileSync(path.join(storeDir, 'genes.jsonl'), 'utf8').split('\n')) {
			const t = line.trim(); if (!t) continue;
			let g; try { g = JSON.parse(t); } catch { continue; }
			if (g && (g.asset_id === ref || g.id === ref)) {
				return { id: g.id, assetId: g.asset_id, category: g.category || 'repair', text: (g.summary || '') + ' ' + (g.strategy || []).join(' ') };
			}
		}
	} catch { /* 库不可读 */ }
	return null;
}

/** 对靶 + top-N 选取；并落一份「本次选中」sidecar，供 --register-hit 正确解析编号 */
async function selectList(all) {
	// 0.15.0：用**清洗后**的任务意图打分（治 私有节点实测 63% 打分落空）。
	// 注：QUERY 原值仍用于埋点留痕/诊断，TASK_TEXT 才是"用户真实诉求"。
	let qTokens = queryTokens(TASK_TEXT);
	// 0.28 S-3：query 侧概念别名展开——中文 query 命中概念别名时，把该概念的英文 canonical
	// 加入 token 集合（于是中文措辞能命中英文 canonical signals）。**不改打分公式与阈值**。
	// EVOX_ALIAS=off：关闭别名展开（基线对照开关——门禁用它测本次改动新增的误选；非错误，不告警）
	if (process.env.EVOX_ALIAS !== 'off') try {
		const { expandQueryTokens } = await import('./engine/light/aliases.mjs');
		qTokens = expandQueryTokens(qTokens, TASK_TEXT);
	} catch (e) {
		// 不静默：别名展开失败会让"中文措辞命中英文 signals"失效（静默退化为字面匹配）
		console.error('[pi-evox] ⚠ 召回别名展开不可用（退化为纯字面匹配）：' + String((e && e.message) || e));
	}
	const hitInfo = await aggregateHits();
	let picked;
	if (qTokens.size > 0) {
		const scoredArr = all
			.map((it) => ({ it, s: scoreGene(it, qTokens, hitInfo) }))
			.filter((x) => x.s >= MIN_MATCH_SCORE)
			.sort((a, b) => b.s - a.s)
			.slice(0, TOPN);
		const scored = new Map(scoredArr.map((x) => [x.it.id, x.s]));
		picked = resolveConflicts(scoredArr.map((x) => x.it), scored);
	} else {
		// 0.15.0 P0-2：**无任务意图 → 一律不注入**（不再"取最近 N 条"）。
		// 依据：私有节点实测该回落路径产生 30 次"与任务无关的注入"，而本项目实验已证
		// 只注入不对靶内容比不注入**更差**（+36pp）——无任务文本时本就不该灌库。
		picked = [];
	}
	try {
		fs.mkdirSync(HITS_DIR, { recursive: true });
		fs.writeFileSync(SELECTION_FILE, JSON.stringify({ ts: new Date().toISOString(), query: QUERY, taskText: TASK_TEXT, ids: picked.map((p) => p.id) }));
	} catch { /* 留痕失败不影响召回 */ }
	// targeted 现在等价于"有任务意图"（即使未命中基因，语义上仍是对靶查询）
	return { picked, total: all.length, targeted: qTokens.size > 0, hitInfo };
}

/** 0.29 B-1 溯源：命中/否定登记时带上「是谁在什么模型上得出的结论」——同源沉积是单作危机的根因 */
async function sourceOf() {
	// 0.30 B-2：优先读 ~/.evomap/source.json（sourceInfo），env 仍可覆盖
	// 0.32 D-2：中间加一层 last_source.json（最近一次实测服务模型），见 store.mjs sourceInfo 注释
	// 0.32 B-5：sourceInfo 现额外返回 kv_compression（压缩方案族）
	try {
		const { sourceInfo } = await import('./engine/light/store.mjs');
		const si = sourceInfo();
		if (si.model || si.host) return { source_model: si.model, source_host: si.host, source_kv: si.kv_compression || '' };
	} catch { /* 回落 */ }
	return {
		source_model: (process.env.EVOX_SOURCE_MODEL || '').slice(0, 80),
		source_host: os.hostname().slice(0, 80),
		source_kv: '',
	};
}

/** 0.32 D-2：把钩子透传进来的「本轮实际服务模型」落盘成 last_source.json。
 *  为什么需要：deposit / register-hit 是 **agent 自己调**的，钩子子进程的 env 到不了那些调用；
 *  而召回（本脚本）是钩子调的 ⇒ 在这里当中转站，让后续 deposit/hit 也能拿到实测模型。
 *  host 传空串，由 recordActualSource 走 EVOX_SOURCE_HOST > source.json > hostname 的兜底链。
 *  无 env（直接手跑）时不做任何事，静默保持既有行为。 */
async function persistActualSource() {
	const m = (process.env.EVOX_SOURCE_MODEL || '').slice(0, 80);
	if (!m) return;
	try {
		const { recordActualSource } = await import('./engine/light/store.mjs');
		recordActualSource(m, (process.env.EVOX_SOURCE_HOST || '').slice(0, 80));
	} catch { /* 落盘失败不影响主流程 */ }
}
/** 0.29 B-4：否定原因受控词表（让"A 沉积 B 失效"可归类、可统计） */
const NEGATE_CAUSES = ['model-diff', 'env-diff', 'scene-mismatch', 'fix-wrong', 'unknown'];

async function registerHit(n, note, geneRef) {
	// 0.18：--gene <asset_id|gene_id> 寻址优先（并发安全）；位置 N 为兼容路径
	let item;
	if (geneRef) {
		item = resolveRef(geneRef);
		if (!item) fail(`登记失败：基因「${geneRef}」未找到（检查 asset_id/gene_id 拼写，或先跑 recall 确认）`, { code: 1 });
	} else {
		let list = null;
		try {
			const sel = JSON.parse(fs.readFileSync(SELECTION_FILE, 'utf8'));
			if (sel && Array.isArray(sel.ids) && sel.ids.length) {
				const byId = new Map(recallList().map((x) => [x.id, x]));
				list = sel.ids.map((id) => byId.get(id)).filter(Boolean);
			}
		} catch { /* 无留痕 → 退化为全量列表 */ }
		if (!list) list = recallList();
		item = list[n - 1];
		if (!item) fail(`登记失败：编号 #${n} 不存在（当前召回共 ${list.length} 条）`, { code: 1, hint: '多会话并发环境建议改用 --gene <asset_id>（位置编号可能漂移）' });
	}
	fs.mkdirSync(HITS_DIR, { recursive: true });
	await persistActualSource();   // 0.32 D-2：钩子透传的实测模型 → last_source.json
	const srcInfo = await sourceOf();
	const rec = {
		ts: new Date().toISOString(),
		gene_id: item.id,
		asset_id: item.assetId,
		category: item.category,
		note: String(note).slice(0, 300),
		...srcInfo,
	};
	withLock(HITS_DIR, () => { fs.appendFileSync(HITS_FILE, JSON.stringify(rec) + '\n'); });
	console.log(`[pi-evox] 命中已登记 ${geneRef ? `(${item.id})` : `#${n} (${item.id})`} → ${HITS_FILE}`);
	console.log(`[pi-evox] 当前命中总数: ${readJsonl(HITS_FILE).length}`);
}

async function recall() {
	await persistActualSource();   // 0.32 D-2：钩子透传的实测模型 → last_source.json
	const all = readJsonl(EVO_GENES);
	const approved = approvedAssetIds();
	const full = recallList();
	const { picked, total, targeted, hitInfo } = await selectList(full);
	recordRecallCall({ targeted, injected: picked.length, query: QUERY, taskText: TASK_TEXT, noise: !TASK_TEXT });
	recordPending(picked);
	console.log(
		`[pi-evox] 基因总数=${all.length} | 已审核=${approved.size} | 守卫通过=${full.length} | ` +
		`${targeted ? '对靶' : '无任务意图'}选中=${picked.length}/${total}` +
		(targeted ? '' : '（0.15.0：查无任务意图 → 不注入）'),
	);
	if (picked.length === 0) {
		if (!TASK_TEXT) {
			// 0.15.0：区分「无任务意图」与「有意图但无对靶项」——前者是宿主没喂干净 query。
			console.log('未拿到任务意图（query 清洗后为空）→ 不注入。');
			console.log('  → 修正：宿主钩子请传**用户消息正文**到 EVOX_QUERY（勿带企业IM/心跳等信封前缀、勿只传 URL）。');
			console.log('  本项目原则：查无任务意图时宁可不注入，也不用无关基因凑数（实测不对靶注入净开销为正）。');
			return;
		}
		if (targeted) {
			console.log('本任务与经验库无对靶项 → 不注入（宁缺毋滥，避免不对靶注入的净开销）。');
			return;
		}
		console.log('经验库当前无可召回修法（首次运行属正常——价值随使用复利增长）。点亮方法：');
		console.log('  1) 完成一个非平凡任务，遇到并修复了不显而易见的坑（见 SKILL.md 流程 B 判定标准）；');
		console.log('  2) 沉淀（内置后端）：node code/light-cli.mjs distill --signals <信号> \\');
		console.log('             --strategy "<可执行修法：参数/命令/编码>" --summary "<坑的一句话>"');
		console.log('  3) 审核（内置后端）：node code/light-cli.mjs approve <gene_id>');
		console.log('   （如已安装可选集成 evolver，也可用：evolver distill / evolver review --approve）');
		console.log('  之后本命令即可召回。完整说明见 SKILL.md 流程 B。');
		return;
	}
	console.log('以下为已验证修法，与本任务相关时优先采用；任务结束时请回填效果：');
	console.log(`  采用了 → node ${path.basename(process.argv[1])} --register-hit --gene <asset_id或gene_id> --note "<任务一句话>"（0.18 起推荐：按 id 寻址，多会话并发不漂移）`);
	console.log(`  没采用/仍踩坑 → node ${path.basename(process.argv[1])} --negate --gene <asset_id或gene_id> --note "<为什么没起作用>"`);
	console.log('  （位置写法 --register-hit <N> 仍兼容，但多会话并行时 N 可能漂移——见 0.18 变更说明）');
	console.log('  （回填才能量化"注入→有效"转化率；不回的注入不计入效果统计）');
	console.log('');
	picked.forEach((it, i) => {
		// 0.33 C-7：衰减标记——因子 <0.7 或踩过否定压力的基因，在注入行内带一眼可辨的记号。
		// 位置在 [#N|id] 行内（钩子 extractFixes 只认 [#\d+| 前缀，标记不破坏解析），
		// 且不写进 strategy 正文（守卫与注入扫描只审策略文本，记号不进策略）。
		let mark = '';
		if (hitInfo && hitInfo.decay) {
			const d = hitInfo.decay.get(it.id);
			if (d && (d.factor < 0.7 || d.negPress)) {
				mark = ` ⚠[衰减:${Math.round(d.factor * 100)}%${d.negPress ? '·多次未奏效' : ''}·${d.days}天前反馈]`;
			}
		}
		console.log(`[#${i + 1}|${it.id}] [${it.category}]${mark} ${it.text}`);
	});
	// 0.25：--record "<结论>" —— 把隔离测试/验证结论回填生产账本（A5：狗粮证据落隔离目录即丢失）。
	 const ri = process.argv.indexOf('--record');
	if (ri >= 0) {
		const note = process.argv[ri + 1] ?? '';
		try {
			fs.mkdirSync(HITS_DIR, { recursive: true });
			fs.appendFileSync(path.join(HITS_DIR, 'verifications.jsonl'), JSON.stringify({
				ts: new Date().toISOString(), kind: 'verification', note,
			 query: QUERY, top: picked.slice(0, 3).map((x) => x.id), injected: picked.length,
			}) + '\n');
			console.log(`[pi-evox] 验证结论已回填生产账本（verifications.jsonl）：${note}`);
		} catch (e) { console.error('[pi-evox] 验证结论回填失败：' + String(e.message || e)); }
	}
}

/** 0.15.0 P0-3：--negate 回填「注入了但没起作用」——与 --register-hit 对称，闭合漏斗。 */
async function registerNegated(n, note, geneRef, because = '') {
	let item;
	if (geneRef) {
		item = resolveRef(geneRef);
		if (!item) fail(`回填失败：基因「${geneRef}」未找到`, { code: 1 });
	} else {
		let list = null;
		try {
			const sel = JSON.parse(fs.readFileSync(SELECTION_FILE, 'utf8'));
			if (sel && Array.isArray(sel.ids) && sel.ids.length) {
				const byId = new Map(recallList().map((x) => [x.id, x]));
				list = sel.ids.map((id) => byId.get(id)).filter(Boolean);
			}
		} catch { /* 无留痕 → 退化为全量列表 */ }
		if (!list) list = recallList();
		item = list[n - 1];
		if (!item) fail(`回填失败：编号 #${n} 不存在（当前召回共 ${list.length} 条）`, { code: 1, hint: '多会话并发环境建议改用 --gene <asset_id>' });
	}
	const srcInfo = await sourceOf();
	withLock(HITS_DIR, () => {
		fs.mkdirSync(HITS_DIR, { recursive: true });
		fs.appendFileSync(PENDING_FILE, JSON.stringify({
			ts: new Date().toISOString(), agent: AGENT, gene_id: item.id, asset_id: item.assetId,
			category: item.category, outcome: 'negated', note: String(note).slice(0, 300),
			because: because || 'unknown',
			taskText: String(TASK_TEXT || '').slice(0, 200),
			...srcInfo,
		}) + '\n');
	});
	console.log(`[pi-evox] 已回填未采用 ${geneRef ? `(${item.id})` : `#${n} (${item.id})`} → ${PENDING_FILE}`);
	console.log('  → 该条会进入"注入→有效"转化率的分母，用于识别**该修法是否已失效**。');
}

const argv = process.argv.slice(2);
const gi = argv.indexOf('--gene');
if (argv[0] === '--register-hit') {
	const ni = argv.indexOf('--note');
	if (gi >= 0) {
		await registerHit(null, ni >= 0 ? argv[ni + 1] ?? '' : '', argv[gi + 1]);
	} else {
		const n = parseInt(argv[1], 10);
		if (!Number.isInteger(n) || n < 1) {
			fail('用法: evolver-recall.mjs --register-hit [--gene <asset_id|gene_id>] --note "<任务一句话>"（0.18 推荐按 --gene 寻址）');
		}
		await registerHit(n, ni >= 0 ? argv[ni + 1] ?? '' : '');
	}
} else if (argv[0] === '--negate') {
	const ni = argv.indexOf('--note');
	const bi = argv.indexOf('--because');
	if (bi >= 0 && argv[bi + 1] && !NEGATE_CAUSES.includes(argv[bi + 1])) {
		fail(`--because 必须是受控词表之一: ${NEGATE_CAUSES.join(' / ')}`, { code: 1, hint: 'model-diff=模型差异 / env-diff=环境差异 / scene-mismatch=场景不匹配 / fix-wrong=修法本身错' });
	}
	const because = bi >= 0 ? argv[bi + 1] ?? '' : '';
	if (gi >= 0) {
		await registerNegated(null, ni >= 0 ? argv[ni + 1] ?? '' : '', argv[gi + 1], because);
	} else {
		const n = parseInt(argv[1], 10);
		if (!Number.isInteger(n) || n < 1) {
			fail('用法: evolver-recall.mjs --negate [--gene <asset_id|gene_id>] --note "<为什么没起作用>" [--because <类别>]');
		}
		await registerNegated(n, ni >= 0 ? argv[ni + 1] ?? '' : '', null, because);
	}
} else {
	await recall();
}
