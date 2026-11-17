import crypto from "node:crypto";
import path from "node:path";
import { SafeFiles, relativeParts } from "./safe-fs.ts";

const FALLBACK_WORKSPACE_DIR = process.env.OPENCLAW_WORKSPACE_DIR || process.cwd();
const HOOK_VERSION = "1.2.13";
// A fixed import marker lets operators verify the deployed version on restart.
console.info(`[hui-yi-signal-hook] loaded v${HOOK_VERSION}`);
// Debug adds lifecycle counts only; it never enables raw message/identifier logs.
const DEBUG_LOG = process.env.HUI_YI_HOOK_DEBUG === "1";
const MAX_LOG_BYTES = 256 * 1024;
const KEEP_LOG_BYTES = 128 * 1024;
const CONSECUTIVE_SESSION_WINDOW_DAYS = 14;
const FIELD_WEIGHTS: Record<string, number> = {
  title: 2.2,
  summary: 1.5,
  semantic_context: 1.8,
  tags: 1.0,
  triggers: 1.2,
  scenarios: 1.1,
  aliases: 2.2
};
const TRIGGER_DEFAULTS: Record<TriggerSource, { minRelevance: number; minConfidence: Confidence; limit: number }> = {
  skill_hit: { minRelevance: 0.30, minConfidence: "medium", limit: 3 },
  explicit_command: { minRelevance: 0.30, minConfidence: "medium", limit: 3 },
  heuristic_fallback: { minRelevance: 0.55, minConfidence: "high", limit: 2 },
  manual_probe: { minRelevance: 0.30, minConfidence: "medium", limit: 3 }
};
const CONFIDENCE_ORDER: Record<Confidence, number> = { none: 0, low: 1, medium: 2, high: 3 };
const DEFAULT_SESSION_SIGNALS: SessionSignals = {
  current_session_hits: 0,
  recent_session_hits: 0,
  cross_session_repeat_count: 0,
  consecutive_session_count: 0,
  last_activated: null
};

type Confidence = "none" | "low" | "medium" | "high";
type ScopeType = "user" | "chat";
type SignalStrength = "weak" | "medium" | "strong";
type TriggerSource = "skill_hit" | "explicit_command" | "heuristic_fallback" | "manual_probe";

type SessionSignals = {
  current_session_hits: number;
  recent_session_hits: number;
  cross_session_repeat_count: number;
  consecutive_session_count: number;
  last_activated: string | null;
};

type MatchMeta = {
  matched_fields: string[];
  overlap_terms: string[];
  raw_score: number;
  confidence: Confidence;
  query_coverage: number;
  match_eligible: boolean;
};

type SignalCandidate = {
  title: string | null;
  path: string | null;
  relevance: number;
  confidence: Confidence;
  matched_fields: string[];
  overlap_terms: string[];
  raw_score: number;
  evaluated_at: string;
  repetition_signal: number;
};

type TagsPayload = {
  _meta?: Record<string, unknown>;
  notes?: Record<string, any>[];
};

function extractSkillNames(value: unknown): string[] {
  if (Array.isArray(value)) {
    return value.map((item) => String(item || "").trim().toLowerCase()).filter(Boolean);
  }
  if (typeof value === "string") {
    return value
      .split(/[;,|]/)
      .map((item) => item.trim().toLowerCase())
      .filter(Boolean);
  }
  return [];
}

function hasExplicitHuiYiSkillHit(event: any): boolean {
  const metadata = event?.context?.metadata || {};
  const candidates = [
    metadata.selectedSkill,
    metadata.selected_skill,
    metadata.skill,
    metadata.skill_name,
    metadata.skillName,
    metadata.matchedSkill,
    metadata.matched_skill,
    metadata.skillHits,
    metadata.skill_hits,
    event?.context?.selectedSkill,
    event?.context?.skill,
    event?.context?.skillHits,
  ];

  for (const candidate of candidates) {
    const names = extractSkillNames(candidate);
    if (names.some((name) => name === "hui-yi" || name === "hui yi" || name === "hui_yi")) {
      return true;
    }
  }
  return false;
}

function explicitCommandQuery(event: any): string | null {
  // Use the mapped inbound body only. Processed agent text, quotations,
  // embedded examples, and conversational history words do not authorize I/O.
  // Providers that wrap Body in an envelope need an explicit host adapter.
  const body = event?.context?.body;
  if (typeof body !== "string") return null;
  const match = /^\/(?:hui-yi|hui_yi)[ \t]+([\s\S]+)$/i.exec(body);
  return match?.[1].trim() || null;
}

function parseFromAddress(rawFrom: unknown): { channel?: string; id?: string } {
  if (typeof rawFrom !== "string") return {};
  const trimmed = rawFrom.trim();
  if (!trimmed.includes(":")) return { id: trimmed };
  const [channel, ...rest] = trimmed.split(":");
  return { channel: channel || undefined, id: rest.join(":") || undefined };
}

function inferScopeType(event: any): "user" | "chat" {
  const metadata = event?.context?.metadata || {};
  const channelId = String(event?.context?.channelId || "");
  const parsedFrom = parseFromAddress(event?.context?.from);
  if (String(metadata.chat_type || metadata.chatType || "").toLowerCase() === "direct") return "user";
  if (typeof parsedFrom.id === "string" && /^ou_/i.test(parsedFrom.id)) return "user";
  if (channelId.startsWith("user:")) return "user";
  return "chat";
}

function inferScopeId(event: any, scopeType: "user" | "chat"): string | null {
  const metadata = event?.context?.metadata || {};
  const channelId = String(event?.context?.channelId || "");
  const parsedFrom = parseFromAddress(event?.context?.from);
  if (scopeType === "user") {
    const userCandidates = [
      metadata.senderId,
      metadata.sender_id,
      parsedFrom.id
    ];
    for (const candidate of userCandidates) {
      if (typeof candidate === "string" && candidate.trim()) return candidate.trim();
    }
    if (channelId.startsWith("user:")) return channelId.slice("user:".length);
  }
  const chatCandidates = [
    metadata.chatId,
    metadata.chat_id,
    parsedFrom.id
  ];
  for (const candidate of chatCandidates) {
    if (typeof candidate === "string" && candidate.trim()) return candidate.trim();
  }
  if (channelId.startsWith("chat:")) return channelId.slice("chat:".length);
  if (channelId.startsWith("user:")) return channelId.slice("user:".length);
  return channelId || null;
}

function resolveWorkspaceDir(event: any): string {
  const candidates = [
    event?.context?.workspaceDir,
    event?.context?.sessionEntry?.workspaceDir,
    event?.context?.cfg?.agents?.defaults?.workspace,
    FALLBACK_WORKSPACE_DIR
  ];
  for (const candidate of candidates) {
    if (typeof candidate === "string" && candidate.trim()) {
      return candidate.trim();
    }
  }
  return FALLBACK_WORKSPACE_DIR;
}

function appendHookLog(workspaceDir: string, payload: Record<string, unknown>): void {
  try {
    const files = new SafeFiles(path.join(workspaceDir, "hooks", "hui-yi-signal-hook"));
    const checked = files.check("hook.log", true);
    let previous = checked.stats ? files.read("hook.log") : "";
    if (Buffer.byteLength(previous, "utf8") > MAX_LOG_BYTES) {
      const buffer = Buffer.from(previous, "utf8");
      const tail = buffer.subarray(Math.max(0, buffer.length - KEEP_LOG_BYTES));
      const newlineIndex = tail.indexOf(0x0a);
      previous = (newlineIndex >= 0 ? tail.subarray(newlineIndex + 1) : Buffer.alloc(0)).toString("utf8");
    }
    files.write("hook.log", `${previous}${JSON.stringify(payload)}\n`);
  } catch {
    console.warn("[hui-yi-signal-hook] log write refused or unavailable");
  }
}

function todayIsoDate(): string {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  const dd = String(now.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

// Keep lexical rules aligned with core/matching.py and the shared fixture.
// Match confidence describes retrieval evidence, never the truth of a claim.
const FIELD_QUALITY: Record<string, number> = {
  title: 1.0, summary: 0.9, semantic_context: 0.85,
  tags: 0.95, triggers: 0.9, scenarios: 0.8, aliases: 1.0
};
const STRONG_FIELDS = new Set(["title", "summary", "tags", "triggers", "aliases"]);
const HAN_RUN = /[\u3400-\u4dbf\u4e00-\u9fff\u{20000}-\u{2fa1f}]+/gu;
const HAN_CHAR = /^[\u3400-\u4dbf\u4e00-\u9fff\u{20000}-\u{2fa1f}]$/u;
const EN_FILLER = new Set(`a an and are as at be been being but by can could did do does for from
  had has have how i if in is it its me my of on or our please remember
  recall so that the their them then there these they this those to us
  was we were what when where which who why will with would you your
  about again before earlier previously last time tell help some any
  information context thing things issue issues problem problems details
  note notes memory memories solution solutions situation`.split(/\s+/));
const ZH_FILLER = [
  "你还记得", "还记得", "回忆一下", "回忆下", "请帮我", "帮我", "请问",
  "告诉我", "能不能", "可不可以", "有没有", "为什么", "是什么",
  "什么时候", "上一次", "怎么回事", "之前", "以前", "上次", "曾经",
  "当时", "最近", "目前", "现在", "回忆", "记得", "记忆", "一下",
  "怎样", "怎么", "如何", "哪里", "哪些", "什么", "是否", "还是",
  "已经", "仍然", "就是", "那个", "这个", "这些", "那些", "关于",
  "有关", "相关", "我们", "你们", "他们", "我的", "你的", "用户",
  "麻烦", "以及", "然后", "的话", "时候", "可以", "需要", "希望",
  "问题", "解决", "处理", "方法", "记录", "笔记", "内容", "信息",
  "东西", "事情", "经验", "情况", "步骤", "帮助", "告诉"
].sort((a, b) => b.length - a.length || (a < b ? -1 : a > b ? 1 : 0));
const ZH_SPLIT = new RegExp(ZH_FILLER.join("|"), "u");
const ZH_PARTICLES = new Set(Array.from("的了呢吗啊吧呀着是和与及把被对从到这那有我你他"));

function normalizeMatchText(text: string | null | undefined): string {
  // NFKC covers full-width/compatibility forms. JS lacks casefold; include
  // common expanding/final-form folds in addition to Unicode lowercasing.
  return (text || "").normalize("NFKC").toLowerCase().replace(/ß/g, "ss").replace(/ς/g, "σ");
}

export function tokenize(text: string | null | undefined): string[] {
  const normalized = normalizeMatchText(text);
  const tokens: string[] = [];
  for (const run of normalized.matchAll(HAN_RUN)) {
    for (const phrase of run[0].split(ZH_SPLIT)) {
      const characters = Array.from(phrase.replace(/[的了呢吗啊吧呀]+$/u, ""));
      for (let index = 0; index < characters.length - 1; index++) {
        const pair = characters.slice(index, index + 2);
        if (!pair.every(character => ZH_PARTICLES.has(character))) tokens.push(pair.join(""));
      }
    }
  }
  const nonHan = normalized.replace(HAN_RUN, " ");
  for (const word of nonHan.match(/(?<![\p{L}\p{N}_])[a-z](?:\+\+|#)(?![\p{L}\p{N}_])/gu) || []) tokens.push(word);
  for (const word of nonHan.match(/[\p{L}\p{N}]+(?:[_.+-][\p{L}\p{N}]+)*/gu) || []) {
    if (!EN_FILLER.has(word) && Array.from(word).length >= 2) tokens.push(word);
  }
  return [...new Set(tokens)];
}

function fieldText(note: Record<string, any>, field: string): string {
  const value = note[field];
  if (Array.isArray(value)) return value.filter(item => item != null).map(String).join(" \n ");
  if (value == null) return "";
  return String(value);
}

export function noteIsRetrievable(note: Record<string, any>): boolean {
  if (note.active === false || note.superseded_by) return false;
  if (["superseded", "retracted", "deleted", "inactive"].includes(String(note.status || "").toLowerCase())) return false;
  if (note.is_fixture === true || note.fixture === true) return false;
  return !["fixture", "test_fixture"].includes(String(note.memory_type ?? note.type ?? "").toLowerCase());
}

function containsAlias(query: string, value: unknown): boolean {
  const alias = normalizeMatchText(String(value)).trim();
  if (!alias || !tokenize(alias).length) return false;
  const identifierChar = (character: string): boolean => Boolean(character) &&
    ("_.+-".includes(character) || (/^[\p{L}\p{N}]$/u.test(character) && !HAN_CHAR.test(character)));
  const characters = Array.from(alias);
  for (let index = query.indexOf(alias); index >= 0; index = query.indexOf(alias, index + 1)) {
    const before = Array.from(query.slice(0, index)).at(-1) || "";
    const after = Array.from(query.slice(index + alias.length))[0] || "";
    if (identifierChar(characters[0]) && identifierChar(before)) continue;
    if (identifierChar(characters.at(-1) || "") && identifierChar(after)) continue;
    return true;
  }
  return false;
}

export function detectMatch(note: Record<string, any>, query: string): [number, MatchMeta] {
  const queryTerms = new Set(tokenize(query));
  if (!queryTerms.size || !noteIsRetrievable(note)) {
    return [0.0, { matched_fields: [], overlap_terms: [], raw_score: 0.0,
      confidence: "none", query_coverage: 0.0, match_eligible: false }];
  }
  const matchedFields: string[] = [];
  const overlapTerms = new Set<string>();
  let rawScore = 0.0;
  let fieldQuality = 0.0;
  const normalizedQuery = normalizeMatchText(query);
  for (const [field, weight] of Object.entries(FIELD_WEIGHTS)) {
    let text = fieldText(note, field);
    if (field === "aliases") {
      const aliases = typeof note.aliases === "string" ? [note.aliases] : note.aliases;
      text = Array.isArray(aliases) ? aliases.filter(alias => containsAlias(normalizedQuery, alias)).map(String).join(" \n ") : "";
    }
    const fieldTerms = new Set(tokenize(text));
    const hits = [...queryTerms].filter(term => fieldTerms.has(term));
    if (hits.length) {
      matchedFields.push(field);
      for (const term of hits) overlapTerms.add(term);
      rawScore += weight * hits.length / queryTerms.size;
      fieldQuality = Math.max(fieldQuality, FIELD_QUALITY[field]);
    }
  }
  const coverage = overlapTerms.size / queryTerms.size;
  const confirmation = Math.min(Math.max(matchedFields.length - 1, 0), 2) / 2;
  const relevance = Math.min(1.0, coverage * (0.70 + 0.20 * fieldQuality + 0.10 * confirmation));
  let confidence: Confidence = "none";
  if (relevance >= 0.60 && matchedFields.some(field => STRONG_FIELDS.has(field))) confidence = "high";
  else if (relevance >= 0.30) confidence = "medium";
  else if (relevance >= 0.15) confidence = "low";
  return [relevance, {
    matched_fields: matchedFields.sort(), overlap_terms: [...overlapTerms].sort(), raw_score: rawScore,
    confidence, query_coverage: coverage, match_eligible: confidence === "medium" || confidence === "high"
  }];
}

function parseIsoDay(value: unknown): Date | null {
  if (typeof value !== "string" || !value.trim() || value.trim() === "-") return null;
  const match = value.trim().match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!match) return null;
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  if (!year || !month || !day) return null;
  return new Date(Date.UTC(year, month - 1, day));
}

function daysBetween(leftIso: string, rightIso: string): number {
  const left = parseIsoDay(leftIso);
  const right = parseIsoDay(rightIso);
  if (!left || !right) return 0;
  return Math.floor((left.getTime() - right.getTime()) / 86400000);
}

function normalizedSessionSignals(note: Record<string, any>): SessionSignals {
  const raw = note.session_signals && typeof note.session_signals === "object" ? note.session_signals : {};
  return {
    current_session_hits: Number(raw.current_session_hits || DEFAULT_SESSION_SIGNALS.current_session_hits),
    recent_session_hits: Number(raw.recent_session_hits || DEFAULT_SESSION_SIGNALS.recent_session_hits),
    cross_session_repeat_count: Number(raw.cross_session_repeat_count || DEFAULT_SESSION_SIGNALS.cross_session_repeat_count),
    consecutive_session_count: Number(raw.consecutive_session_count || DEFAULT_SESSION_SIGNALS.consecutive_session_count),
    last_activated: typeof raw.last_activated === "string" ? raw.last_activated : null
  };
}

function repetitionSignal(note: Record<string, any>, todayIso: string): number {
  const signals = normalizedSessionSignals(note);
  const currentHits = Math.max(0, signals.current_session_hits || 0);
  const recentHits = Math.max(0, signals.recent_session_hits || 0);
  const crossRepeat = Math.max(0, signals.cross_session_repeat_count || 0);
  const consecutive = Math.max(0, signals.consecutive_session_count || 0);
  let score = 0.0;
  score += Math.min(currentHits / 3.0, 1.0) * 0.40;
  score += Math.min(recentHits / 5.0, 1.0) * 0.25;
  score += Math.min(crossRepeat / 4.0, 1.0) * 0.20;
  score += Math.min(consecutive / 3.0, 1.0) * 0.15;

  if (signals.last_activated) {
    // Elapsed days since the last activation: today - last_activated.
    const age = Math.max(0, daysBetween(todayIso, signals.last_activated));
    if (age <= 1) score += 0.10;
    else if (age <= 3) score += 0.05;
  }

  return Math.max(0.0, Math.min(score, 1.0));
}

function loadTagsPayload(files: SafeFiles): TagsPayload {
  if (!files.check("tags.json", true).stats) return { _meta: { version: 5 }, notes: [] };
  const payload = JSON.parse(files.read("tags.json")) as TagsPayload;
  if (!payload || typeof payload !== "object" || !Array.isArray(payload.notes)) {
    throw new Error("Invalid cold-memory metadata");
  }
  return payload;
}

export function collectCandidates(
  notes: Record<string, any>[],
  queryText: string,
  minRelevance: number,
  minConfidence: Confidence,
  limit: number,
  todayIso: string
): SignalCandidate[] {
  const candidates: SignalCandidate[] = [];

  for (const note of notes) {
    const [relevance, meta] = detectMatch(note, queryText);
    if (!meta.match_eligible) continue;
    if (relevance < minRelevance) continue;
    if (meta.confidence === "none") continue;
    if (CONFIDENCE_ORDER[meta.confidence] < CONFIDENCE_ORDER[minConfidence]) continue;
    candidates.push({
      title: note.title == null ? null : String(note.title),
      path: note.path == null ? null : String(note.path),
      relevance,
      confidence: meta.confidence,
      matched_fields: meta.matched_fields,
      overlap_terms: meta.overlap_terms,
      raw_score: meta.raw_score,
      evaluated_at: todayIso,
      repetition_signal: repetitionSignal(note, todayIso)
    });
  }

  candidates.sort((left, right) => {
    const relevanceDelta = right.relevance - left.relevance;
    if (relevanceDelta !== 0) return relevanceDelta;
    return right.repetition_signal - left.repetition_signal;
  });
  return candidates.slice(0, limit);
}

function buildSessionKey(channel: string, scopeType: ScopeType, scopeId: string, threadId?: string): string {
  const tail = threadId ? `thread:${threadId}` : "main";
  return `${channel}:${scopeType}:${scopeId}:${tail}`;
}

function slugify(text: string): string {
  const value = text
    .trim()
    .toLowerCase()
    .replace(/[^\w\-\u4e00-\u9fff]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
  return value || "session";
}

function noteFilePath(files: SafeFiles, note: Record<string, any>): string {
  let raw = String(note.path || "").replace(/\\/g, "/");
  if (!raw) throw new Error("note path is empty");
  if (raw.startsWith("memory/cold/")) raw = raw.slice("memory/cold/".length);
  const parts = relativeParts(raw);
  const leaf = parts[parts.length - 1].toLowerCase();
  if (!leaf.endsWith(".md") || ["index.md", "retrieval-log.md", "_template.md"].includes(leaf)) throw new Error("Invalid note target");
  files.check(raw, true);
  return raw;
}

function sessionFingerprint(sessionKey: string): string {
  const digest = crypto.createHash("sha256").update(sessionKey, "utf8").digest("hex");
  return `sha256:${digest.slice(0, 16)}`;
}

function normalizeSignalHistory(history: unknown): string[] {
  if (!Array.isArray(history)) return [];
  return history.map((item: unknown) => {
    const parts = String(item).split("|");
    if (parts[0] && !parts[0].startsWith("sha256:")) {
      parts[0] = sessionFingerprint(parts[0]);
    }
    return parts.join("|");
  });
}

function findNote(notes: Record<string, any>[], target: string): Record<string, any> | null {
  const lookup = target.trim().toLowerCase();
  const targetWords = new Set(lookup.split(/\s+/).filter(Boolean));
  for (const note of notes) {
    const titleLower = String(note.title || "").trim().toLowerCase();
    const pathLower = String(note.path || "").trim().toLowerCase();
    const noteSlug = path.parse(pathLower).name;
    const allWordsInTitle = targetWords.size > 0 && [...targetWords].every((word) => titleLower.includes(word));
    if (titleLower === lookup || pathLower.endsWith(lookup) || noteSlug === lookup || allWordsInTitle) {
      return note;
    }
  }
  return null;
}

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function normalizedLines(text: string): string[] {
  const normalized = text.replace(/\r\n/g, "\n");
  const lines = normalized.split("\n");
  if (normalized.endsWith("\n")) lines.pop();
  return lines;
}

function findSectionBounds(lines: string[], heading: string): { start: number; end: number } | null {
  const marker = `## ${heading}`;
  for (let index = 0; index < lines.length; index += 1) {
    if (lines[index].trim() !== marker) continue;
    let end = index + 1;
    while (end < lines.length && !lines[end].startsWith("## ")) {
      end += 1;
    }
    return { start: index, end };
  }
  return null;
}

function extractMetricBlock(text: string, heading: string): string | null {
  const lines = normalizedLines(text);
  const bounds = findSectionBounds(lines, heading);
  if (!bounds) return null;
  return lines.slice(bounds.start + 1, bounds.end).join("\n");
}

function parseSectionMetric(text: string, heading: string, key: string, fallback: number): number {
  const block = extractMetricBlock(text, heading);
  if (block == null) return fallback;
  const pattern = new RegExp(`^-\\s*${escapeRegExp(key)}\\s*:\\s*(\\d+)\\s*$`, "m");
  const match = block.match(pattern);
  return match ? Number(match[1]) : fallback;
}

function parseSectionValue(text: string, heading: string, key: string): string | null {
  const block = extractMetricBlock(text, heading);
  if (block == null) return null;
  const pattern = new RegExp(`^-\\s*${escapeRegExp(key)}\\s*:\\s*(.+?)\\s*$`, "m");
  const match = block.match(pattern);
  return match ? match[1].trim() : null;
}

function parseSessionSignals(text: string): SessionSignals {
  return {
    current_session_hits: parseSectionMetric(text, "Session signals", "current_session_hits", 0),
    recent_session_hits: parseSectionMetric(text, "Session signals", "recent_session_hits", 0),
    cross_session_repeat_count: parseSectionMetric(text, "Session signals", "cross_session_repeat_count", 0),
    consecutive_session_count: parseSectionMetric(text, "Session signals", "consecutive_session_count", 0),
    last_activated: parseSectionValue(text, "Session signals", "last_activated")
  };
}

function replaceOrInsertSectionMetrics(text: string, heading: string, values: Record<string, unknown>): string {
  const blockLines = [
    `## ${heading}`,
    ...Object.entries(values).map(([key, value]) => `- ${key}: ${value}`),
    ""
  ];
  const lines = normalizedLines(text);
  const bounds = findSectionBounds(lines, heading);
  if (bounds) {
    return [...lines.slice(0, bounds.start), ...blockLines, ...lines.slice(bounds.end)].join("\n");
  }

  const prefixLines = [...lines];
  if (prefixLines.length && prefixLines[prefixLines.length - 1] !== "") {
    prefixLines.push("");
  }
  return [...prefixLines, ...blockLines].join("\n");
}

function applyCandidate(
  payload: TagsPayload,
  files: SafeFiles,
  candidate: SignalCandidate,
  sessionKey: string,
  strength: SignalStrength,
  source: string,
  todayIso: string
): { applied: string | null; skipped?: string; changed: boolean } {
  const notes = Array.isArray(payload.notes) ? payload.notes : [];
  const noteRef = candidate.path || candidate.title || "";
  // Candidates originate from metadata paths; do not re-resolve them through
  // fuzzy title/suffix matching after the same paths have been preflighted.
  const matched = candidate.path ? notes.find(note => note.path === candidate.path) : null;
  if (!matched) return { applied: null, skipped: `Note not found: ${noteRef}`, changed: false };

  const notePath = noteFilePath(files, matched);
  if (!files.check(notePath, true).stats) return { applied: null, skipped: "Backing note file missing", changed: false };

  const text = files.read(notePath);
  const signals = parseSessionSignals(text);
  const sessionHash = sessionFingerprint(sessionKey);
  const dedupKey = `${sessionHash}|${slugify(path.parse(notePath).name)}|${todayIso}|${source}`;
  const rawHistory = Array.isArray(matched.signal_history) ? matched.signal_history.map((item: unknown) => String(item)) : [];
  const history = normalizeSignalHistory(rawHistory);
  if (history.includes(dedupKey)) {
    if (history.join("\n") !== rawHistory.join("\n")) {
      matched.signal_history = history.slice(-20);
      payload._meta = payload._meta && typeof payload._meta === "object" ? payload._meta : {};
      payload._meta.updated = todayIso;
      return { applied: null, skipped: `Duplicate activation: ${matched.title || noteRef}`, changed: true };
    }
    return { applied: null, skipped: `Duplicate activation: ${matched.title || noteRef}`, changed: false };
  }

  const lastSessionKey = typeof matched.last_session_key === "string" ? matched.last_session_key : null;
  const sameSession = lastSessionKey === sessionHash;
  signals.current_session_hits = sameSession ? Number(signals.current_session_hits || 0) + 1 : 1;
  signals.recent_session_hits = Number(signals.recent_session_hits || 0) + ({ weak: 1, medium: 1, strong: 2 }[strength]);
  if (!sameSession) {
    signals.cross_session_repeat_count = Number(signals.cross_session_repeat_count || 0) + 1;
    const lastActivatedAge = signals.last_activated ? daysBetween(todayIso, signals.last_activated) : null;
    if (lastSessionKey && lastActivatedAge !== null && lastActivatedAge >= 0 && lastActivatedAge <= CONSECUTIVE_SESSION_WINDOW_DAYS) {
      signals.consecutive_session_count = Number(signals.consecutive_session_count || 0) + 1;
    } else {
      signals.consecutive_session_count = 1;
    }
  } else {
    signals.consecutive_session_count = Math.max(1, Number(signals.consecutive_session_count || 0));
  }
  signals.last_activated = todayIso;

  const newText = replaceOrInsertSectionMetrics(text, "Session signals", {
    current_session_hits: signals.current_session_hits,
    recent_session_hits: signals.recent_session_hits,
    cross_session_repeat_count: signals.cross_session_repeat_count,
    consecutive_session_count: signals.consecutive_session_count,
    last_activated: signals.last_activated
  });
  files.write(notePath, newText);

  matched.session_signals = signals;
  matched.last_seen = todayIso;
  matched.last_session_key = sessionHash;
  matched.signal_history = [...history, dedupKey].slice(-20);
  payload._meta = payload._meta && typeof payload._meta === "object" ? payload._meta : {};
  payload._meta.updated = todayIso;

  return { applied: candidate.path || candidate.title || noteRef, changed: true };
}

function runSignalPipeline(workspaceDir: string, query: string, sessionKey: string, triggerSource: TriggerSource): Record<string, unknown> {
  const defaults = TRIGGER_DEFAULTS[triggerSource] || TRIGGER_DEFAULTS.manual_probe;
  const memoryRoot = path.join(workspaceDir, "memory", "cold");
  const files = new SafeFiles(memoryRoot);
  const payload = loadTagsPayload(files);
  const notes = Array.isArray(payload.notes) ? payload.notes : [];
  const todayIso = todayIsoDate();
  const candidates = collectCandidates(notes, query, defaults.minRelevance, defaults.minConfidence, defaults.limit, todayIso);
  const applied: string[] = [];
  const skipped: string[] = [];
  let changed = false;

  // Reject poisoned destinations before making any note changes.
  files.check("tags.json", true);
  for (const candidate of candidates) noteFilePath(files, { path: candidate.path });

  for (const candidate of candidates) {
    const result = applyCandidate(payload, files, candidate, sessionKey, "weak", "signal_pipeline", todayIso);
    if (result.applied) applied.push(result.applied);
    if (result.skipped) skipped.push(result.skipped);
    if (result.changed) changed = true;
  }

  if (changed) {
    files.write("tags.json", `${JSON.stringify(payload, null, 2)}\n`);
  }

  return {
    ok: true,
    exitCode: 0,
    sessionHash: sessionFingerprint(sessionKey),
    dryRun: false,
    triggerSource,
    pipeline: {
      candidates,
      applied,
      skipped
    }
  };
}

const handler = async (event: any) => {
  const bootstrapWorkspaceDir = resolveWorkspaceDir(event);
  if (DEBUG_LOG) {
    appendHookLog(bootstrapWorkspaceDir, {
      ts: new Date().toISOString(),
      stage: "alive",
      hookVersion: HOOK_VERSION,
      isMessage: event?.type === "message",
      isPreprocessed: event?.action === "preprocessed",
      hasBodyForAgent: typeof event?.context?.bodyForAgent === "string"
    });
  }

  if (event?.type !== "message" || event?.action !== "preprocessed") return;
  const workspaceDir = bootstrapWorkspaceDir;
  const explicitSkillHit = hasExplicitHuiYiSkillHit(event);
  const commandQuery = explicitCommandQuery(event);
  // A selected skill or a leading explicit command authorizes this operation.
  // Native OpenClaw 2026.9.5 events do not carry skill-selection metadata.
  if (!explicitSkillHit && commandQuery === null) {
    if (DEBUG_LOG) {
      appendHookLog(workspaceDir, {
        ts: new Date().toISOString(),
        stage: "skipped",
        hookVersion: HOOK_VERSION,
        reason: "no_explicit_invocation"
      });
    }
    return;
  }
  const body = commandQuery ?? String(event?.context?.bodyForAgent || "");
  const triggerSource: TriggerSource = commandQuery !== null ? "explicit_command" : "skill_hit";

  const scopeType = inferScopeType(event);
  const scopeId = inferScopeId(event, scopeType);
  if (!scopeId) {
    if (DEBUG_LOG) {
      appendHookLog(workspaceDir, {
        ts: new Date().toISOString(),
        stage: "skipped",
        hookVersion: HOOK_VERSION,
        reason: "missing_scope_id"
      });
    }
    return;
  }

  const parsedFrom = parseFromAddress(event?.context?.from);
  const channel = String(parsedFrom.channel || event?.context?.provider || event?.context?.channelId || "feishu");
  const threadId = typeof event?.context?.metadata?.threadId === "string" ? event.context.metadata.threadId : undefined;

  const sessionKey = buildSessionKey(channel, scopeType, scopeId, threadId);
  // Channel values can contain identifiers too; keep only the fingerprint.
  appendHookLog(workspaceDir, {
    ts: new Date().toISOString(),
    stage: "triggered",
    hookVersion: HOOK_VERSION,
    triggerSource,
    scopeType,
    sessionHash: sessionFingerprint(sessionKey),
    hasThread: Boolean(threadId)
  });

  try {
    const result = runSignalPipeline(
      workspaceDir,
      body,
      sessionKey,
      triggerSource
    );
    const pipelineForLog = result.pipeline as { candidates: unknown[]; applied: unknown[]; skipped: unknown[] };
    appendHookLog(workspaceDir, {
      ts: new Date().toISOString(),
      stage: "completed",
      hookVersion: HOOK_VERSION,
      candidateCount: pipelineForLog.candidates.length,
      appliedCount: pipelineForLog.applied.length,
      skippedCount: pipelineForLog.skipped.length
    });

    const pipeline = result.pipeline as { applied?: string[]; candidates?: SignalCandidate[] };
    if (pipeline.applied?.length) {
      console.log(`[hui-yi-signal-hook] applied ${pipeline.applied.length} activation(s)`);
    } else if (pipeline.candidates?.length) {
      console.log(`[hui-yi-signal-hook] detected ${pipeline.candidates.length} candidate(s), no new activation`);
    }
  } catch (error) {
    appendHookLog(workspaceDir, {
      ts: new Date().toISOString(),
      stage: "pipeline_error",
      hookVersion: HOOK_VERSION,
      error: "filesystem_or_pipeline_error"
    });
    console.warn("[hui-yi-signal-hook] pipeline refused or failed; inspect local filesystem and metadata");
  }
};

export default handler;
