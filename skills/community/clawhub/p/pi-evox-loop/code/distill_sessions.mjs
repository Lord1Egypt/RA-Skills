#!/usr/bin/env node
/**
 * distill_sessions.mjs v3 — 生产会话蒸馏适配器（参数差异抽取版）
 *
 * ── 演进 ─────────────────────────────────────────────────────────────────
 * v1：扫错数据源（OpenClaw 只扫 2KB 的已删除会话 .zst；Hermes 只扫单条出站
 *     request_dump），且 distillablePairs 为**硬编码 0**（未实现）。
 * v2：改读真实存储（OC `openclaw-agent.sqlite.transcript_events` / Hermes
 *     `state.db.messages`），真实计数可用；但「修法」取自失败后的 assistant 旁白，
 *     实测样本是**健康检查日志 / 心跳报告 / 错误正文**——不可执行。
 * v3（本版）：**修法 = 失败调用与重试调用的「参数差异」**（"改了什么才成功"）。
 *     · 不再退化为「错误正文」或「旁白」，无参数差异一律拒（宁缺毋滥）。
 *
 * ── 数据契约（实测）──────────────────────────────────────────────────────
 * OpenClaw：`transcript_events(session_id, seq, event_json)`，event_json 为 session v3 形状
 *   {type,id,parentId,timestamp,message:{role,toolName,toolCallId,isError,content[]}}
 *   · assistant.content[] 里的 toolCall 块：{type:'toolCall', id:'call_…', name, arguments, partialArgs}
 *     —— `id` 与 toolResult.toolCallId 对应；`partialArgs` 是合法 JSON（优先用它）
 *   · `session_transcript_active_events` 给出活跃集与顺序
 * Hermes：`state.db.messages(id, session_id, role, content, tool_call_id, tool_calls, tool_name, timestamp)`
 *   · assistant.tool_calls = JSON 数组 [{id, function:{name, arguments(JSON 字符串)}}]
 *   · tool.content = JSON {"output":…, "exit_code":N, "error":…}；tool_call_id ↔ tool_calls[].id
 *
 * ── 纪律 ─────────────────────────────────────────────────────────────────
 *   · 默认 --dry-run：只报告，绝不写基因库；--commit 才落。
 *   · 落库前过守卫：REPAIR_SIGNAL_RE + NARRATION_RE + 最小长度 + 必须有参数差异。
 *   · 任何解析失败一律跳过，绝不中断周常；零依赖（node:sqlite），路径全 env 可覆盖。
 */
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { DatabaseSync } from "node:sqlite";

const HOME = process.env.EVOX_HOME || process.env.HOME || process.env.USERPROFILE || "/root";
const argIdx = (k) => process.argv.indexOf(k);
const DAYS = argIdx("--days") >= 0 ? Number(process.argv[argIdx("--days") + 1]) || 7 : 7;
const COMMIT = process.argv.includes("--commit");
const DRY = !COMMIT;

const OC_DB = process.env.EVOX_OC_DB || path.join(HOME, ".openclaw/agents/main/agent/openclaw-agent.sqlite");
const HM_DB = process.env.EVOX_HERMES_DB || path.join(HOME, ".hermes/state.db");
const LIGHT_CLI = process.env.EVOX_LIGHT_CLI || path.join(HOME, "pi-evox-lab/code/light-cli.mjs");

const REPAIR_SIGNAL_RE =
	/error|exception|traceback|failed|invalid|cannot|unable|missing|not found|wrong|instead|avoid|fix|encoding\s*[=:]|errors\s*=|utf-?8|gbk|gb18030|latin-1|\brb\b|except|skip/i;
const NARRATION_RE =
	/^\s*(now i (understand|see|have|know|remember|need|can)|let me\b|i'?(ll|ve|m)\b|i will\b|here'?s\b|done[.!\u2026]|confirmed[:.]|the output matches|to summarize|summarize\b|first,? i\b|next,? i\b|alright\b|okay\b)/i;

const MIN_STRATEGY = 40;
const MAX_STRATEGY = 600;
const MIN_ARG_LEN = 6;
/** 真重试必然是「紧接着」的：失败与重试之间跨越过多事件即视为无关步骤 */
const MAX_GAP = 6;

const flat = (s) => String(s || "").replace(/\s+/g, " ").trim();
const clip = (s, n = MAX_STRATEGY) => (s.length > n ? s.slice(0, n) + "\u2026" : s);

function openRO(p) {
	return new DatabaseSync(p, { readOnly: true });
}
function textOfContent(content) {
	if (typeof content === "string") return content;
	if (Array.isArray(content)) {
		return content.filter((b) => b && (b.type === "text" || b.type === undefined)).map((b) => b.text ?? "").join("\n");
	}
	return "";
}
function withinDays(ms, days) {
	if (!ms) return true;
	return Date.now() - Number(ms) <= days * 86400_000;
}

/** 解析参数串（JSON 优先；退化时保留原串） */
function parseArgs(raw) {
	const s = typeof raw === "string" ? raw.trim() : raw == null ? "" : String(raw);
	if (!s) return null;
	try {
		const o = JSON.parse(s);
		if (o && typeof o === "object") return o;
	} catch {
		/* 可能是 Python repr 风格（OC 的 arguments 字段） */
	}
	return null;
}

/** 参数差异：返回 [{key, before, after}]；无法结构化比较时退化为整体比较 */
function diffArgs(oldArgs, newArgs) {
	const o = parseArgs(oldArgs);
	const n = parseArgs(newArgs);
	if (o && n) {
		const keys = new Set([...Object.keys(o), ...Object.keys(n)]);
		const changed = [];
		for (const k of keys) {
			const a = JSON.stringify(o[k] ?? null);
			const b = JSON.stringify(n[k] ?? null);
			if (a !== b) changed.push({ key: k, before: a, after: b });
		}
		return changed;
	}
	const a = flat(oldArgs);
	const b = flat(newArgs);
	if (a && b && a !== b) return [{ key: "args", before: a, after: b }];
	return [];
}

/**
 * 「同一操作的小改动」判定。
 *
 * 为什么必须有它：实测发现这些智能体日常跑的是**例行运维/巡检**，同一工具（exec/terminal）
 * 被用于大量彼此无关的步骤；于是「同名工具下一次成功」往往只是**下一个任务**，不是重试。
 * 例：失败 = 健康巡检脚本，下一次同工具成功 = deliver-pending-report.sh —— 整体换命令 ≠ 修法。
 * 真正的修法是**同一操作的参数微调**（如加 encoding='gbk'、换 --flag、改路径），
 * 故要求 before/after 有实质相似度。
 */
function similarEnough(before, after) {
	const A = flat(before).replace(/^["']|["']$/g, "");
	const B = flat(after).replace(/^["']|["']$/g, "");
	if (!A || !B) return false;
	if (A.includes(B) || B.includes(A)) return true;
	let i = 0;
	const m = Math.min(A.length, B.length);
	while (i < m && A[i] === B[i]) i++;
	if (i / Math.max(A.length, B.length) >= 0.3) return true;
	const ta = new Set(A.split(/\s+/));
	const tb = new Set(B.split(/\s+/));
	let inter = 0;
	for (const t of ta) if (tb.has(t)) inter++;
	const uni = new Set([...ta, ...tb]).size;
	return uni === 0 ? false : inter / uni >= 0.6;
}

/**
 * 由「失败调用 + 重试调用」的参数差异构造可执行修法。
 * 门槛（宁缺毋滥）：①差异键数 1..3（整体替换不算）②至少一个差异键是「同一操作的小改动」
 * （similarEnough）③after 侧有实质内容。
 */
function buildStrategy(tool, oldArgs, newArgs, errHead) {
	const changedAll = diffArgs(oldArgs, newArgs);
	if (changedAll.length === 0 || changedAll.length > 3) return null;
	const tweaks = changedAll.filter((c) => similarEnough(c.before, c.after) && flat(c.after).replace(/^["']|["']$/g, "").length >= MIN_ARG_LEN);
	if (tweaks.length === 0) return null;
	const parts = tweaks.slice(0, 3).map((c) => `${c.key} -> ${clip(c.after, 260)} (was ${clip(c.before, 120)})`);
	return clip(`${tool}: retry with corrected args [after error: ${clip(errHead, 140)}] :: ${parts.join(" ;; ")}`);
}

// ────────────────────────────── OpenClaw ──────────────────────────────
function scanOpenClaw() {
	const res = { available: false, sessions: 0, toolResults: 0, failures: 0, pairs: 0, out: [], rejected: {} };
	let db;
	try {
		if (!fs.existsSync(OC_DB)) return res;
		db = openRO(OC_DB);
		db.prepare("select 1 from session_windows limit 1").get();
		res.available = true;
	} catch (e) {
		res.note = "oc db err: " + e.message;
		return res;
	}
	try {
		const wins = db.prepare(
			"select session_id, coalesce(started_at, updated_at, created_at) as ts from session_windows",
		).all();
		for (const w of wins) {
			if (!withinDays(w.ts, DAYS)) continue;
			res.sessions++;
			let rows;
			try {
				rows = db.prepare(
					"select t.seq, t.event_json from session_transcript_active_events a " +
					"join transcript_events t on t.session_id = a.session_id and t.seq = a.event_seq " +
					"where a.session_id = ? order by a.active_position",
				).all(w.session_id);
			} catch {
				rows = db.prepare("select seq, event_json from transcript_events where session_id = ? order by seq").all(w.session_id);
			}
			const turns = [];
			for (const r of rows) {
				try { turns.push(JSON.parse(r.event_json)); } catch { /* 跳过坏行 */ }
			}
			// pass 1：toolCallId -> {tool, args}
			const callMap = new Map();
			for (const t of turns) {
				const m = t && t.message;
				if (!m || m.role !== "assistant" || !Array.isArray(m.content)) continue;
				for (const b of m.content) {
					if (b && b.type === "toolCall" && b.id) {
						callMap.set(b.id, { tool: b.name, args: b.partialArgs || b.arguments || "" });
					}
				}
			}
			// pass 2：失败 → 重试
			for (let i = 0; i < turns.length; i++) {
				const m = turns[i] && turns[i].message;
				if (!m || m.role !== "toolResult") continue;
				res.toolResults++;
				const body = textOfContent(m.content);
			// 失败判定：以运行时显式 isError 为准。
			// 实测（2026-09-23）：OpenClaw 对 exec 命令失败**不置** isError，从输出正文做错误启发式
			// 不可靠——自审报告/file 命令/grep/侦察脚本源码里的 "error" 字样会被误判，且一旦附近出现
			// 同工具重试就会产出噪声基因。故只采纳 isError===true（宁漏真实命令失败，不引入噪声）。
			if (m.isError !== true) continue;
				res.failures++;
				const errHead = flat(body) || "tool reported isError=true";
				let retry = null;
				let retryIdx = -1;
				for (let j = i + 1; j < Math.min(turns.length, i + 20); j++) {
					const m2 = turns[j] && turns[j].message;
					if (!m2 || m2.role !== "toolResult" || m2.toolName !== m.toolName) continue;
				const b2 = textOfContent(m2.content);
				// 重试 = 同工具且未报错（isError 非 true）的结果
				if (m2.isError !== true) { retry = m2; retryIdx = j; }
					break;
				}
				if (!retry) { res.rejected.noRetry = (res.rejected.noRetry || 0) + 1; continue; }
				if (retryIdx - i > MAX_GAP) { res.rejected.farRetry = (res.rejected.farRetry || 0) + 1; continue; }
				const oldC = callMap.get(m.toolCallId);
				const newC = callMap.get(retry.toolCallId);
				if (!oldC || !newC) { res.rejected.noCallRecord = (res.rejected.noCallRecord || 0) + 1; continue; }
				const strategy = buildStrategy(retry.toolName || oldC.tool, oldC.args, newC.args, errHead);
				if (!strategy) { res.rejected.noArgDelta = (res.rejected.noArgDelta || 0) + 1; continue; }
				res.pairs++;
				res.out.push({ source: "openclaw", session: String(w.session_id).slice(0, 8), tool: retry.toolName || oldC.tool, error: clip(errHead, 200), strategy });
			}
		}
	} catch (e) {
		res.note = "oc scan err: " + e.message;
	} finally {
		try { db.close(); } catch { /* noop */ }
	}
	return res;
}

// ────────────────────────────── Hermes ──────────────────────────────
function scanHermes() {
	const res = { available: false, sessions: 0, tools: 0, failures: 0, pairs: 0, out: [], rejected: {} };
	let db;
	try {
		if (!fs.existsSync(HM_DB)) return res;
		db = openRO(HM_DB);
		db.prepare("select 1 from messages limit 1").get();
		res.available = true;
	} catch (e) {
		res.note = "hermes db err: " + e.message;
		return res;
	}
	try {
		const since = Math.floor((Date.now() - DAYS * 86400_000) / 1000);
		const sess = db.prepare("select id from sessions where coalesce(ended_at, started_at) >= ?").all(since);
		for (const s of sess) {
			res.sessions++;
			let msgs;
			try {
				msgs = db.prepare("select id, role, content, tool_name, tool_call_id, tool_calls from messages where session_id = ? order by id").all(s.id);
			} catch {
				continue;
			}
			// pass 1：toolCallId -> {tool, args}
			const callMap = new Map();
			for (const m of msgs) {
				if (m.role !== "assistant" || !m.tool_calls) continue;
				let arr = null;
				try { arr = JSON.parse(m.tool_calls); } catch { continue; }
				if (!Array.isArray(arr)) continue;
				for (const c of arr) {
					if (c && c.id) callMap.set(c.id, { tool: c.function && c.function.name, args: (c.function && c.function.arguments) || "" });
				}
			}
			// pass 2：失败 → 重试
			for (let i = 0; i < msgs.length; i++) {
				const m = msgs[i];
				if (m.role !== "tool") continue;
				res.tools++;
				let p = null;
				try { p = JSON.parse(m.content || ""); } catch { /* 非 JSON */ }
				const out = p && typeof p === "object" ? String(p.output ?? "") : String(m.content ?? "");
				const ec = p && typeof p === "object" ? p.exit_code : undefined;
				const er = p && typeof p === "object" ? p.error : undefined;
			// Hermes 有显式 exit_code / error 字段，以之为准（比正文启发式可靠）。
			if (!((typeof ec === "number" && ec !== 0) || !!er)) continue;
				res.failures++;
				const errHead = flat(out) || (typeof ec === "number" ? `exit_code=${ec}` : "tool reported error");
				let retry = null;
				let retryIdx = -1;
				for (let j = i + 1; j < Math.min(msgs.length, i + 20); j++) {
					const m2 = msgs[j];
					if (!m2 || m2.role !== "tool" || m2.tool_name !== m.tool_name) continue;
					let p2 = null;
					try { p2 = JSON.parse(m2.content || ""); } catch { /* noop */ }
					const o2 = p2 && typeof p2 === "object" ? String(p2.output ?? "") : String(m2.content ?? "");
					const e2 = p2 && typeof p2 === "object" ? p2.exit_code : undefined;
					const r2 = p2 && typeof p2 === "object" ? p2.error : undefined;
				if (!((typeof e2 === "number" && e2 !== 0) || !!r2)) { retry = m2; retryIdx = j; }
					break;
				}
				if (!retry) { res.rejected.noRetry = (res.rejected.noRetry || 0) + 1; continue; }
				if (retryIdx - i > MAX_GAP) { res.rejected.farRetry = (res.rejected.farRetry || 0) + 1; continue; }
				const oldC = callMap.get(m.tool_call_id);
				const newC = callMap.get(retry.tool_call_id);
				if (!oldC || !newC) { res.rejected.noCallRecord = (res.rejected.noCallRecord || 0) + 1; continue; }
				const strategy = buildStrategy(retry.tool_name || oldC.tool, oldC.args, newC.args, errHead);
				if (!strategy) { res.rejected.noArgDelta = (res.rejected.noArgDelta || 0) + 1; continue; }
				res.pairs++;
				res.out.push({ source: "hermes", session: String(s.id), tool: retry.tool_name || oldC.tool, error: clip(errHead, 200), strategy });
			}
		}
	} catch (e) {
		res.note = "hermes scan err: " + e.message;
	} finally {
		try { db.close(); } catch { /* noop */ }
	}
	return res;
}

// ────────────────────────────── 两级门：自动批 vs 人工 ──────────────────────────────
/**
 * 危险操作识别（两级门的分界线）。
 *
 * 原则：**只有「纯参数微调」才允许自动批**——即改动局限于命令的参数（加 --flag、
 * 换编码、改路径、加 2>/dev/null、补 --help…），不会改变系统状态语义。
 * 凡涉及 删除/权限/服务/重启/网络外发/装包/写盘/密钥/破坏性 git —— 一律留人工。
 *
 * 保守取向：宁可误判为「需人工」（多一条进报告），也不放过一次危险自动批。
 */
const RISKY_RE =
	/(\brm\b|\brmdir\b|\bunlink\b|--force\b|-rf\b|\bsudo\b|\bchmod\b|\bchown\b|\bsetfacl\b|\bpasswd\b|\buseradd\b|\buserdel\b|\bgroupadd\b|\bsystemctl\b|\bservice\s+\S+\s+(restart|stop|disable|mask)|\breboot\b|\bshutdown\b|\bkill\b|\bpkill\b|\bmkfs\b|\bdd\s+(if|of)=|\bmount\b|\bumount\b|\btruncate\b|\btee\b|\bapt(-get)?\s+(install|remove|purge|upgrade|autoremove)\b|\byum\s+(install|remove|erase)\b|\bdnf\s+(install|remove|erase)\b|\bpip3?\s+install\b|\bnpm\s+(i|install)\s+(-g|--global)\b|\bcurl\b[^|;]*\s(-X|--request)\s*(POST|PUT|DELETE|PATCH)|\bwget\b[^|;]*--post|\bscp\b|\brsync\b|\bssh\b|\bnc\b|\bncat\b|\bgit\s+(push|reset\s+--hard|clean|checkout\s+--)\b|\bDROP\s+TABLE\b|\bDELETE\s+FROM\b|\bUPDATE\s+\w+\s+SET\b|\bpassword\b|\bpasswd\b|\btoken\b|\bapi[_-]?key\b|\bsecret\b|\.env\b|credentials|openclaw\.json|config\.yaml|MEMORY\.md|AGENTS\.md|SOUL\.md)/i;

/** 分类：auto（可自动批）｜human（须人工） */
function classify(p) {
	const text = `${p.strategy}\n${p.error}`;
	const m = text.match(RISKY_RE);
	if (m) return { tier: "human", why: "risky-token:" + m[0].trim().slice(0, 24) };
	return { tier: "auto", why: "param-tweak-only" };
}

// ────────────────────────────── 守卫 → 可落基因 ──────────────────────────────
function guard(p) {
	const s = flat(p.strategy);
	if (!s) return { ok: false, why: "empty" };
	if (s.length < MIN_STRATEGY) return { ok: false, why: "too-short" };
	if (!REPAIR_SIGNAL_RE.test(s)) return { ok: false, why: "no-repair-signal" };
	if (NARRATION_RE.test(s)) return { ok: false, why: "narration-opener" };
	return { ok: true };
}

const oc = scanOpenClaw();
const hm = scanHermes();
const all = [...oc.out, ...hm.out];
const eligible = [];
const rejected = [];
for (const p of all) {
	const g = guard(p);
	if (!g.ok) {
		rejected.push({ source: p.source, tool: p.tool, why: g.why, head: flat(p.strategy).slice(0, 90) });
		continue;
	}
	const c = classify(p);
	eligible.push({ ...p, tier: c.tier, tierWhy: c.why });
}
const autoTier = eligible.filter((p) => p.tier === "auto");
const humanTier = eligible.filter((p) => p.tier === "human");
const rejectedReasons = rejected.reduce((a, r) => ((a[r.why] = (a[r.why] || 0) + 1), a), {});
for (const [k, v] of Object.entries({ ...oc.rejected, ...hm.rejected })) {
	rejectedReasons["pre:" + k] = (rejectedReasons["pre:" + k] || 0) + v;
}

const summary = {
	version: 3,
	dry: DRY,
	days: DAYS,
	extraction: "arg-diff (failed call vs successful retry)",
	sources: { openclawDb: oc.available, hermesDb: hm.available },
	openclaw: { sessions: oc.sessions, toolResults: oc.toolResults, failures: oc.failures, pairs: oc.pairs, rejected: oc.rejected, note: oc.note },
	hermes: { sessions: hm.sessions, tools: hm.tools, failures: hm.failures, pairs: hm.pairs, rejected: hm.rejected, note: hm.note },
	driftingCandidates: all.length,
	distillablePairs: eligible.length,
	tiers: { autoApprovable: autoTier.length, needsHuman: humanTier.length },
	needsHumanSamples: humanTier.slice(0, 5).map((p) => ({ source: p.source, tool: p.tool, why: p.tierWhy, head: flat(p.strategy).slice(0, 170) })),
	rejected: rejected.length,
	rejectedReasons,
	samples: eligible.slice(0, 5).map((p) => ({ source: p.source, tool: p.tool, error: p.error.slice(0, 130), strategy: p.strategy.slice(0, 300) })),
	action: DRY ? "NO_WRITE(dry-run)" : eligible.length ? "would-distill" : "no-pairs",
};
console.log(JSON.stringify(summary, null, 2));

if (COMMIT) {
	const AUTO_LOWRISK = process.argv.includes("--auto-approve-lowrisk");
	const rIdx = process.argv.indexOf("--report");
	const REPORT = rIdx >= 0 ? process.argv[rIdx + 1] : path.join(HOME, "pi-evox-lab/exp/metrics/distill-candidates-latest.md");

	const drafted = [];
	const autoApproved = [];
	const failed = [];
	let skippedDup = 0;
	for (const p of eligible) {
		try {
			const out = execFileSync(process.execPath, [
				LIGHT_CLI, "distill",
				"--signals", `${p.tool},exception`,
				"--strategy", p.strategy,
				"--summary", clip(`auto(${p.source}): ${p.error}`, 180),
				"--category", "repair",
			], { encoding: "utf8", timeout: 20000 });
			const m = out.match(/gene_[A-Za-z0-9_]+/);
			if (!m) {
				// 内容去重命中 = 正常结果（库中已有同 strategy），**不是失败**
				if (/内容去重|跳过/.test(out)) { skippedDup++; continue; }
				failed.push({ head: flat(p.strategy).slice(0, 70), err: "no gene id in output" });
				continue;
			}
			const gid = m[0];
			drafted.push({ ...p, gid });
			if (AUTO_LOWRISK && p.tier === "auto") {
				const a = execFileSync(process.execPath, [LIGHT_CLI, "approve", gid], { encoding: "utf8", timeout: 20000 });
				if (/已审核|approved/.test(a)) autoApproved.push({ ...p, gid });
			}
		} catch (e) {
			failed.push({ head: flat(p.strategy).slice(0, 70), err: String(e.message).slice(0, 90) });
		}
	}

	// ——— C：候选报告（待人工复核清单 + 一条命令批量批准）———
	const approvedIds = new Set(autoApproved.map((p) => p.gid));
	const pend = drafted.filter((p) => !approvedIds.has(p.gid));
	const L = [];
	L.push("# EvoX 蒸馏候选报告");
	L.push("");
	L.push(`生成时间 ${new Date().toISOString()} ｜ 窗口 ${DAYS} 天`);
	L.push(`候选 ${drafted.length + skippedDup} ｜ 新增 ${drafted.length} ｜ 去重跳过 ${skippedDup} ｜ 自动批准 ${autoApproved.length} ｜ **待人工复核 ${pend.length}** ｜ 失败 ${failed.length}`);
	L.push("");
	L.push(`## 待人工复核（${pend.length}）`);
	L.push("");
	if (pend.length) {
		L.push("批量批准（挑出你认可的，一次贴进终端即可）：");
		L.push("");
		L.push("```bash");
		L.push("cd ~/pi-evox-lab");
		for (const p of pend) L.push(`node code/light-cli.mjs approve ${p.gid}    # [${p.source}/${p.tool}] ${p.tierWhy}`);
		L.push("```");
		L.push("");
		for (const p of pend) {
			L.push(`### \`${p.gid}\` — ${p.source} · ${p.tool} · ${p.tierWhy}`);
			L.push(`- **错误**：${p.error}`);
			L.push(`- **修法**：${p.strategy}`);
			L.push("");
		}
	} else {
		L.push("（无）");
		L.push("");
	}
	L.push(`## 已自动批准（${autoApproved.length}，仅「参数微调型」，无危险操作 token）`);
	L.push("");
	for (const p of autoApproved) L.push(`- \`${p.gid}\` [${p.source}/${p.tool}] ${p.error.slice(0, 120)}`);
	if (!autoApproved.length) L.push("（无）");
	L.push("");
	if (failed.length) {
		L.push(`## 落库失败（${failed.length}）`);
		for (const f of failed) L.push(`- ${f.head} — ${f.err}`);
		L.push("");
	}
	try {
		fs.mkdirSync(path.dirname(REPORT), { recursive: true });
		fs.writeFileSync(REPORT, L.join("\n") + "\n");
	} catch (e) {
		console.error("report write failed:", e.message);
	}

	console.log(JSON.stringify({
		committed: true,
		drafted: drafted.length,
		skippedDuplicates: skippedDup,
		autoApproved: autoApproved.length,
		pendingHuman: pend.length,
		failed: failed.length,
		autoApproveLowRisk: AUTO_LOWRISK,
		report: REPORT,
		note: "自动批准仅限「参数微调型」；其余为 UNPROVEN/quarantined，须人工 approve 才会被召回",
	}, null, 2));
}
