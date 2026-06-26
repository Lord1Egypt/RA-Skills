import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const FALLBACK_WORKSPACE_DIR = process.env.OPENCLAW_WORKSPACE_DIR || process.cwd();
const HOOK_VERSION = "2026-06-10-privacy-minimized-logging-v3";
// Set HUI_YI_HOOK_DEBUG=1 to restore verbose diagnostics (per-event alive/skipped
// entries with raw identifiers and body previews). Default logging persists no
// message content and only hashed scope identifiers.
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
  scenarios: 1.1
};
const TRIGGER_DEFAULTS: Record<TriggerSource, { minRelevance: number; minConfidence: Confidence; limit: number }> = {
  skill_hit: { minRelevance: 0.30, minConfidence: "medium", limit: 3 },
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
type TriggerSource = "skill_hit" | "heuristic_fallback" | "manual_probe";

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

function looksLikeHuiYiIntent(text: string): boolean {
  const q = (text || "").toLowerCase();
  if (!q.trim()) return false;
  const patterns = [
    /(?:之前|以前).*(?:聊过|说过|提过|做过|处理|决定|记录)/,
    /有记录吗/,
    /你记得吗/,
    /回忆(?:一下|下|之前|以前|历史)?/,
    /(?:历史|以前|之前).*(?:对话|聊天|记录|决定|方案|上下文)/,
    /(?:延续|接着).*(?:之前|以前|上次|历史)/,
    /archive this/i,
    /cool this down/i,
    /hui\s*-?yi/i,
    /cold memory/i,
    /do you remember/i,
    /remember (?:when|what|how|that time)/i,
    /as (?:we|i) (?:discussed|mentioned) (?:before|earlier|previously)/i,
    /what did we do before/i
  ];
  return patterns.some((pattern) => pattern.test(text));
}

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
    const logPath = path.join(workspaceDir, "hooks", "hui-yi-signal-hook", "hook.log");
    fs.mkdirSync(path.dirname(logPath), { recursive: true });

    if (fs.existsSync(logPath)) {
      const stats = fs.statSync(logPath);
      if (stats.size > MAX_LOG_BYTES) {
        const buffer = fs.readFileSync(logPath);
        const tail = buffer.subarray(Math.max(0, buffer.length - KEEP_LOG_BYTES));
        const newlineIndex = tail.indexOf(0x0a);
        fs.writeFileSync(logPath, newlineIndex >= 0 ? tail.subarray(newlineIndex + 1) : tail);
      }
    }

    fs.appendFileSync(logPath, `${JSON.stringify(payload)}\n`, "utf8");
  } catch (error) {
    console.warn(`[hui-yi-signal-hook] log write error: ${error instanceof Error ? error.message : String(error)}`);
  }
}

function todayIsoDate(): string {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  const dd = String(now.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function readJsonFile<T>(filePath: string, fallback: T): T {
  try {
    if (!fs.existsSync(filePath)) return fallback;
    return JSON.parse(fs.readFileSync(filePath, "utf8")) as T;
  } catch {
    return fallback;
  }
}

function saveJsonFile(filePath: string, payload: unknown): void {
  fs.writeFileSync(filePath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function tokenize(text: string | null | undefined): string[] {
  if (!text) return [];
  return text
    .toLowerCase()
    .split(/[^\w\-\u4e00-\u9fff]+/g)
    .map((part) => part.trim())
    .filter(Boolean);
}

function fieldText(note: Record<string, any>, field: string): string {
  const value = note[field];
  if (Array.isArray(value)) return value.map((item) => String(item ?? "")).join(" ");
  if (value == null) return "";
  return String(value);
}

function detectMatch(note: Record<string, any>, query: string): [number, MatchMeta] {
  const queryTerms = tokenize(query);
  if (!queryTerms.length) {
    return [0.0, { matched_fields: [], overlap_terms: [], raw_score: 0.0, confidence: "none" }];
  }

  const matchedFields = new Set<string>();
  const overlapTerms = new Set<string>();
  let rawScore = 0.0;

  for (const [field, weight] of Object.entries(FIELD_WEIGHTS)) {
    const text = fieldText(note, field);
    const fieldLower = text.toLowerCase();
    const fieldTerms = new Set(tokenize(text));
    let fieldHits = 0;

    for (const term of queryTerms) {
      if (fieldLower.includes(term)) {
        rawScore += weight;
        fieldHits += 1;
        overlapTerms.add(term);
      } else if (fieldTerms.has(term)) {
        rawScore += weight * 0.8;
        fieldHits += 1;
        overlapTerms.add(term);
      }
    }

    if (fieldHits) {
      matchedFields.add(field);
      rawScore += Math.min(fieldHits, 3) * 0.15;
    }
  }

  const combinedTerms = new Set(tokenize(`${fieldText(note, "semantic_context")} ${fieldText(note, "summary")}`));
  if (combinedTerms.size) {
    const uniqueQueryTerms = new Set(queryTerms);
    let overlapCount = 0;
    for (const term of uniqueQueryTerms) {
      if (combinedTerms.has(term)) overlapCount += 1;
    }
    rawScore += (overlapCount / Math.max(uniqueQueryTerms.size, 1)) * 2.0;
  }

  const relevance = Math.min(1.0, rawScore <= 0 ? 0.0 : Math.log1p(rawScore) / Math.log(10));
  const strongFields = new Set(["title", "summary", "tags", "triggers"]);
  const hasStrongField = [...matchedFields].some((field) => strongFields.has(field));

  let confidence: Confidence = "none";
  if (relevance >= 0.60 && hasStrongField) {
    confidence = "high";
  } else if (relevance >= 0.30 && (hasStrongField || matchedFields.size >= 2)) {
    confidence = "medium";
  } else if (relevance >= 0.15) {
    confidence = "low";
  }

  return [
    relevance,
    {
      matched_fields: [...matchedFields].sort(),
      overlap_terms: [...overlapTerms].sort(),
      raw_score: rawScore,
      confidence
    }
  ];
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

function loadTagsPayload(memoryRoot: string): TagsPayload {
  const payload = readJsonFile<TagsPayload>(path.join(memoryRoot, "tags.json"), { _meta: { version: 5 }, notes: [] });
  if (!payload || typeof payload !== "object" || !Array.isArray(payload.notes)) {
    return { _meta: { version: 5 }, notes: [] };
  }
  return payload;
}

function collectCandidates(
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

function noteFilePath(memoryRoot: string, note: Record<string, any>): string {
  let raw = String(note.path || "").replace(/\\/g, "/").trim();
  if (!raw) throw new Error("note path is empty");
  if (raw.startsWith("memory/cold/")) raw = raw.slice("memory/cold/".length);
  if (path.isAbsolute(raw)) throw new Error(`absolute note paths are not allowed: ${raw}`);
  const parts = raw.split("/").filter(Boolean);
  if (!parts.length || parts.some((part) => part === ".." || part === ".")) {
    throw new Error(`unsafe note path outside memory root: ${raw}`);
  }
  const root = path.resolve(memoryRoot);
  const resolved = path.resolve(root, ...parts);
  const relative = path.relative(root, resolved);
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error(`note path escapes memory root: ${raw}`);
  }
  return resolved;
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
  memoryRoot: string,
  candidate: SignalCandidate,
  sessionKey: string,
  strength: SignalStrength,
  source: string,
  todayIso: string
): { applied: string | null; skipped?: string; changed: boolean } {
  const notes = Array.isArray(payload.notes) ? payload.notes : [];
  const noteRef = candidate.path || candidate.title || "";
  const matched = noteRef ? findNote(notes, noteRef) : null;
  if (!matched) return { applied: null, skipped: `Note not found: ${noteRef}`, changed: false };

  const notePath = noteFilePath(memoryRoot, matched);
  if (!fs.existsSync(notePath)) return { applied: null, skipped: `Backing note file missing: ${notePath}`, changed: false };

  const text = fs.readFileSync(notePath, "utf8");
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
  fs.writeFileSync(notePath, newText, "utf8");

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
  const payload = loadTagsPayload(memoryRoot);
  const notes = Array.isArray(payload.notes) ? payload.notes : [];
  const todayIso = todayIsoDate();
  const candidates = collectCandidates(notes, query, defaults.minRelevance, defaults.minConfidence, defaults.limit, todayIso);
  const applied: string[] = [];
  const skipped: string[] = [];
  let changed = false;

  for (const candidate of candidates) {
    const result = applyCandidate(payload, memoryRoot, candidate, sessionKey, "weak", "signal_pipeline", todayIso);
    if (result.applied) applied.push(result.applied);
    if (result.skipped) skipped.push(result.skipped);
    if (result.changed) changed = true;
  }

  if (changed) {
    saveJsonFile(path.join(memoryRoot, "tags.json"), payload);
  }

  return {
    ok: true,
    exitCode: 0,
    sessionHash: sessionFingerprint(sessionKey),
    dryRun: false,
    triggerSource,
    pipeline: {
      query,
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
      seenType: event?.type || null,
      seenAction: event?.action || null,
      contextDump: {
        channelId: event?.context?.channelId ?? null,
        from: event?.context?.from ?? null,
        parsedFrom: parseFromAddress(event?.context?.from),
        metadata: event?.context?.metadata ?? null,
        hasBodyForAgent: typeof event?.context?.bodyForAgent === "string",
        bodyPreview: typeof event?.context?.bodyForAgent === "string" ? event.context.bodyForAgent.slice(0, 120) : null
      }
    });
  }

  if (event?.type !== "message" || event?.action !== "preprocessed") return;
  const body = String(event?.context?.bodyForAgent || "");
  const workspaceDir = bootstrapWorkspaceDir;
  const explicitSkillHit = hasExplicitHuiYiSkillHit(event);
  const heuristicIntent = looksLikeHuiYiIntent(body);

  if (!explicitSkillHit && !heuristicIntent) {
    if (DEBUG_LOG) {
      appendHookLog(workspaceDir, {
        ts: new Date().toISOString(),
        stage: "skipped",
        hookVersion: HOOK_VERSION,
        reason: "no_skill_hit_or_intent_match",
        action: event?.action,
        type: event?.type,
        bodyPreview: body.slice(0, 200)
      });
    }
    return;
  }

  const scopeType = inferScopeType(event);
  const scopeId = inferScopeId(event, scopeType);
  if (!scopeId) {
    if (DEBUG_LOG) {
      appendHookLog(workspaceDir, {
        ts: new Date().toISOString(),
        stage: "skipped",
        hookVersion: HOOK_VERSION,
        reason: "missing_scope_id",
        bodyPreview: body.slice(0, 200)
      });
    }
    return;
  }

  const parsedFrom = parseFromAddress(event?.context?.from);
  const channel = String(parsedFrom.channel || event?.context?.provider || event?.context?.channelId || "feishu");
  const threadId = typeof event?.context?.metadata?.threadId === "string" ? event.context.metadata.threadId : undefined;

  const sessionKey = buildSessionKey(channel, scopeType, scopeId, threadId);
  // Default logs keep only hashed scope material: raw scope/thread identifiers
  // and message previews are persisted solely under HUI_YI_HOOK_DEBUG=1.
  appendHookLog(workspaceDir, {
    ts: new Date().toISOString(),
    stage: "triggered",
    hookVersion: HOOK_VERSION,
    triggerSource: explicitSkillHit ? "skill_hit" : "heuristic_fallback",
    channel,
    scopeType,
    sessionHash: sessionFingerprint(sessionKey),
    hasThread: Boolean(threadId),
    ...(DEBUG_LOG
      ? { scopeId, threadId: threadId || null, bodyPreview: body.slice(0, 200) }
      : {})
  });

  try {
    const result = runSignalPipeline(
      workspaceDir,
      body,
      sessionKey,
      explicitSkillHit ? "skill_hit" : "heuristic_fallback"
    );
    const pipelineForLog = result.pipeline as Record<string, unknown>;
    appendHookLog(workspaceDir, {
      ts: new Date().toISOString(),
      stage: "completed",
      hookVersion: HOOK_VERSION,
      result: DEBUG_LOG ? result : { ...result, pipeline: { ...pipelineForLog, query: undefined } }
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
      error: error instanceof Error ? error.message : String(error)
    });
    console.warn(`[hui-yi-signal-hook] pipeline error: ${error instanceof Error ? error.message : String(error)}`);
  }
};

export default handler;
