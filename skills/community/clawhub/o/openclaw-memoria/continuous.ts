/**
 * 🧠 Memoria — Continuous Learning (Layer 21)
 * 
 * This module implements real-time fact extraction from conversation flow,
 * independent of session end or compaction. Like a child learning while walking.
 * 
 * Exports:
 *   - CONTINUOUS_URGENT_PATTERNS — regex patterns for urgent/error signals
 *   - registerContinuousHooks() — attach message_received + llm_output hooks
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";
import type { MemoriaConfig } from "./core/config.js";
import type { MemoriaDB } from "./core/db.js";
import type { SelectiveMemory } from "./core/selective.js";
import type { LLMProvider } from "./core/providers/types.js";
import type { IdentityParser } from "./core/identity-parser.js";
import { LLM_EXTRACT_PROMPT, parseJSON, normalizeCategory } from "./core/extraction.js";
import type { PrefetchCache } from "./prefetch.js";
import { computeRecall, extractUserPrompt } from "./recall.js";
import type { RecallDeps } from "./recall.js";
import type { WriteAheadLog } from "./core/wal.js";
import type { SelfObserver } from "./core/self-observation.js";

// ─── Constants ───

export const CONTINUOUS_URGENT_PATTERNS = [
  // Frustration / explicit error signals
  /\bne\s+fais?\s+plus\b/i, /\bne\s+jamais\b/i, /\bputain\b/i, /\bmerde\b/i,
  /\bc'est\s+la\s+[23]\w*\s+fois\b/i, /\bj'ai\s+d[uû]\b/i,
  /\bdoublon\b/i, /\berreur\b/i, /\bcrash\b/i, /\bcassé\b/i, /\bmort\b/i,
  /\brevert\b/i, /\brollback\b/i, /\bhotfix\b/i,
  /\btu\s+as\s+pas\s+(compris|appris|retenu)\b/i,
  /\bpourquoi\s+tu\s+(refais?|recommence)\b/i,
  // English equivalents
  /\bnever\s+do\b/i, /\bdon'?t\s+ever\b/i, /\bbroke\b/i, /\bdead\b/i,
  /\bduplicate\b/i, /\bmistake\b/i,
];

// Correction patterns — user is correcting the agent's behavior/output
export const CORRECTION_PATTERNS = [
  // Direct corrections (FR)
  /\bnon\s*[,!.]?\s*(c'est|c'etait|il\s+faut|faut)\b/i,
  /\bc'est\s+pas\s+(ça|ca|correct|bon)\b/i,
  /\bje\s+t'ai\s+dit\s+(que|de)\b/i,
  /\bje\s+t'avais\s+dit\b/i,
  /\bt'as\s+pas\s+(compris|lu|vu|fait)\b/i,
  /\bc'est\s+faux\b/i, /\bc'est\s+pas\s+ce\s+que\b/i,
  /\bregarde\s+bien\b/i, /\brelis\b/i,
  /\bje\s+voulais\s+dire\b/i, /\bpas\s+comme\s+(ça|ca)\b/i,
  /\btu\s+(comprends|captes)\s+pas\b/i,
  /\ben\s+fait\s*[,!]\s*(c'est|il|faut)\b/i,
  /\btu\s+te\s+trompe/i, /\bmauvais/i,
  // Direct corrections (EN)
  /\bno\s*[,!.]?\s*(it'?s|that'?s|you\s+should|I\s+said|I\s+meant)\b/i,
  /\bthat'?s\s+(wrong|incorrect|not\s+(right|what))\b/i,
  /\bactually\s*[,!]/i, /\bI\s+already\s+told\s+you\b/i,
  /\byou\s+(misunderstood|didn'?t\s+(understand|read|listen))\b/i,
];

const SELF_ERROR_PATTERNS = [
  /erreur.*j'ai\s+(fait|commis|créé)/i,
  /mon\s+erreur/i, /j'aurais\s+d[uû]/i,
  /je\s+n'aurais\s+pas\s+d[uû]/i,
  /confond[ure]/i, /par\s+erreur/i,
  /ERREUR\s+CRITIQUE/i,
];

// ─── Hook Registration ───

interface ContinuousState {
  buffer: Array<{ role: "user" | "assistant"; text: string; ts: number }>;
  turnCount: number;
  lastExtraction: number;
  inProgress: boolean;
}

/**
 * Register continuous learning hooks on the OpenClaw API.
 * Buffers user messages + assistant responses, triggers extraction when:
 *   - Urgent: user frustration/error keywords (immediate, bypasses cooldown)
 *   - Self-error: assistant self-admission of mistake
 *   - Periodic: every N turns (default 4) with cooldown
 * 
 * Requires:
 *   - cfg.autoCapture = true (master capture switch)
 *   - cfg.continuous.enabled !== false (layer switch, default true)
 */
export interface ContinuousHooksState {
  /** Returns true if continuous extraction has run at least once this session */
  hasExtracted(): boolean;
}

export function registerContinuousHooks(
  api: OpenClawPluginApi,
  cfg: MemoriaConfig,
  db: MemoriaDB,
  selective: SelectiveMemory,
  extractLlm: LLMProvider,
  identityParser: IdentityParser,
  postProcessNewFacts: (source: "capture" | "compaction") => Promise<void>,
  prefetchCache?: PrefetchCache,
  recallDeps?: Omit<RecallDeps, "prefetchCache">,
  wal?: WriteAheadLog,
  selfObserver?: SelfObserver
): ContinuousHooksState {
  const ENABLED = cfg.continuous?.enabled !== false && cfg.autoCapture;
  if (!ENABLED) return { hasExtracted: () => false };

  const COOLDOWN_MS = cfg.continuous?.cooldownMs ?? 45_000;
  const MAX_BUFFER = 10;
  const NORMAL_INTERVAL = cfg.continuous?.interval ?? 4;

  const state: ContinuousState = {
    buffer: [],
    turnCount: 0,
    lastExtraction: 0,
    inProgress: false,
  };

  // ── message_received: buffer user messages + detect urgent ──
  api.on("message_received", async (event: any, _ctx: any) => {
    try {
      if (!event.content || event.content.length < 5) return;
      // Skip heartbeat/system messages
      if (/^(HEARTBEAT|Read HEARTBEAT|NO_REPLY)/i.test(event.content)) return;

      // ── WAL: persist message IMMEDIATELY (< 1ms, crash-safe) ──
      if (wal) {
        try { wal.write("user", event.content); }
        catch (e) { api.logger.debug?.(`memoria: WAL write error: ${String(e)}`); }
      }

      state.buffer.push({
        role: "user",
        text: event.content.slice(0, 3000),
        ts: Date.now(),
      });
      if (state.buffer.length > MAX_BUFFER) state.buffer.shift();
      state.turnCount++;

      // ── Async prefetch: start recall computation NOW ──
      // By the time before_prompt_build fires, the result will be cached
      // Debounce: skip if last prefetch was < 5s ago (prevents loop on rapid messages)
      const now = Date.now();
      const PREFETCH_DEBOUNCE_MS = 5_000;
      if (prefetchCache && recallDeps && event.content.length > 10 &&
          (now - state.lastExtraction > PREFETCH_DEBOUNCE_MS || state.turnCount <= 1)) {
        const userMsg = extractUserPrompt(event.content);
        if (userMsg.length > 5) {
          prefetchCache.startPrefetch(event.content, async () => {
            api.logger.debug?.(`memoria: 🚀 prefetch started for message (${userMsg.length} chars)`);
            return computeRecall(userMsg, state.turnCount, recallDeps);
          });
        }
      }

      // Check for correction signals — user is fixing agent's mistake
      const isCorrection = CORRECTION_PATTERNS.some(p => p.test(event.content));
      if (isCorrection) {
        api.logger.info?.(`memoria: 📝 continuous — correction detected in user message`);
        // Self-observation: record correction signal
        if (selfObserver) {
          try { selfObserver.record("correction", event.content); }
          catch (e) { api.logger.debug?.(`memoria: self-obs error: ${String(e)}`); }
        }
        // Log to .learnings/ for self-improving-agent coupling
        try {
          const workspacePath = cfg.workspacePath || process.env.OPENCLAW_WORKSPACE || "";
          if (workspacePath) {
            const fs = await import("fs");
            const path = await import("path");
            const learningsDir = path.join(workspacePath, ".learnings");
            const learningsFile = path.join(learningsDir, "LEARNINGS.md");
            if (fs.existsSync(learningsFile)) {
              const now = new Date();
              const timestamp = now.toISOString().slice(0, 16).replace("T", " ");
              const snippet = event.content.slice(0, 200).replace(/\n/g, " ");
              const entry = `\n### ${timestamp} — Correction\n- **Category**: correction\n- **What happened**: User corrected the agent\n- **Context**: "${snippet}"\n- **Source**: memoria auto-detection\n\n`;
              fs.appendFileSync(learningsFile, entry);
              api.logger.debug?.(`memoria: correction logged to .learnings/LEARNINGS.md`);
            }
          }
        } catch (e) {
          api.logger.debug?.(`memoria: failed to write .learnings: ${String(e)}`);
        }
        await doContinuousExtraction(api, cfg, db, selective, extractLlm, identityParser, postProcessNewFacts, state, "correction");
        return; // correction already triggers extraction, skip urgent check
      }

      // Check for urgent signals in user message — extract immediately
      const isUrgent = CONTINUOUS_URGENT_PATTERNS.some(p => p.test(event.content));
      if (isUrgent) {
        api.logger.info?.(`memoria: ⚡ continuous — urgent signal detected in user message`);
        // Self-observation: frustration or error detection
        if (selfObserver) {
          try { selfObserver.record("frustration", event.content); }
          catch (e) { api.logger.debug?.(`memoria: self-obs error: ${String(e)}`); }
        }
        await doContinuousExtraction(api, cfg, db, selective, extractLlm, identityParser, postProcessNewFacts, state, "urgent");
      }
    } catch (err) {
      api.logger.debug?.(`memoria: continuous message_received error: ${String(err)}`);
    }
  });

  // ── llm_output: buffer assistant responses + trigger periodic ──
  api.on("llm_output", async (event: any, _ctx: any) => {
    try {
      const texts = event.assistantTexts?.filter((t: any) => t && t.length > 15) || [];
      if (texts.length === 0) return;

      const combined = texts.join("\n").slice(0, 3000);
      // Skip empty/system responses
      if (/^(HEARTBEAT_OK|NO_REPLY)$/i.test(combined.trim())) return;

      // ── WAL: persist assistant response IMMEDIATELY ──
      if (wal) {
        try { wal.write("assistant", combined); }
        catch (e) { api.logger.debug?.(`memoria: WAL write error: ${String(e)}`); }
      }

      state.buffer.push({
        role: "assistant",
        text: combined,
        ts: Date.now(),
      });
      if (state.buffer.length > MAX_BUFFER) state.buffer.shift();

      // Check for self-detected errors in assistant response
      const selfError = SELF_ERROR_PATTERNS.some(p => p.test(combined));
      if (selfError) {
        api.logger.info?.(`memoria: ⚡ continuous — self-detected error in assistant response`);
        await doContinuousExtraction(api, cfg, db, selective, extractLlm, identityParser, postProcessNewFacts, state, "self-error");
      }

      // Normal periodic extraction
      if (state.turnCount >= NORMAL_INTERVAL) {
        const now = Date.now();
        if (now - state.lastExtraction > COOLDOWN_MS) {
          await doContinuousExtraction(api, cfg, db, selective, extractLlm, identityParser, postProcessNewFacts, state, "periodic");
        }
      }
    } catch (err) {
      api.logger.debug?.(`memoria: continuous llm_output error: ${String(err)}`);
    }
  });

  return { hasExtracted: () => state.lastExtraction > 0 };
}

// ─── Extraction Logic ───

/**
 * Layer 21: Continuous Learning — micro-extraction from rolling buffer.
 * 
 * Triggers:
 *   - "periodic": every N turns (default 4), with cooldown
 *   - "urgent": immediate on user frustration/error keywords (bypasses cooldown)
 *   - "self-error": immediate on assistant self-admission phrases
 * 
 * Uses same LLM_EXTRACT_PROMPT + selective + postProcessNewFacts as agent_end.
 * Guarded by state.inProgress lock to prevent concurrent runs.
 * Buffer is snapshot + cleared before extraction to avoid re-processing.
 */
async function doContinuousExtraction(
  api: OpenClawPluginApi,
  cfg: MemoriaConfig,
  db: MemoriaDB,
  selective: SelectiveMemory,
  extractLlm: LLMProvider,
  identityParser: IdentityParser,
  postProcessNewFacts: (source: "capture" | "compaction") => Promise<void>,
  state: ContinuousState,
  trigger: "periodic" | "urgent" | "self-error" | "correction"
): Promise<void> {
  if (state.buffer.length < 2) return;
  if (state.inProgress) return; // prevent concurrent extractions

  const now = Date.now();
  // Urgent bypasses cooldown, others respect it
  if (trigger === "periodic" && now - state.lastExtraction < (cfg.continuous?.cooldownMs ?? 45_000)) return;

  state.inProgress = true;
  state.lastExtraction = now;
  state.turnCount = 0;

  // Snapshot and clear buffer to avoid re-processing same messages
  const snapshot = [...state.buffer];
  state.buffer.length = 0;

  // Build context from snapshot
  const context = snapshot
    .map(m => `[${m.role}]: ${m.text}`)
    .join("\n---\n");

  const urgencyHint = trigger === "urgent"
    ? "\n\n⚠️ SIGNAL D'URGENCE DÉTECTÉ — L'utilisateur exprime une frustration ou signale une erreur. PRIORITÉ MAXIMALE aux faits de catégorie 'erreur'."
    : trigger === "self-error"
    ? "\n\n⚠️ L'ASSISTANT A DÉTECTÉ SA PROPRE ERREUR — Capturer ce qui s'est mal passé, pourquoi, et ce qu'il ne faut plus faire."
    : trigger === "correction"
    ? "\n\n📝 CORRECTION DÉTECTÉE — L'utilisateur corrige l'assistant. Capturer : (1) ce que l'assistant a fait de FAUX, (2) ce qui est CORRECT selon l'utilisateur, (3) la RÈGLE à retenir pour ne pas répéter. Catégorie = 'erreur' ou 'preference' selon le contexte."
    : "";

  const prompt = LLM_EXTRACT_PROMPT
    .replace("{TEXT}", context + urgencyHint)
    .replace("{MAX_FACTS}", String(Math.min(cfg.captureMaxFacts, trigger === "periodic" ? 3 : 5)));

  try {
    const result = await extractLlm.generateWithMeta!(prompt, {
      maxTokens: 768,
      temperature: 0.1,
      format: "json",
      timeoutMs: 20000,
    });

    if (!result?.response) return;

    const parsed = parseJSON(result.response) as { facts?: Array<{ fact: string; category: string; type?: string; confidence: number }> };
    if (!parsed?.facts || parsed.facts.length === 0) return;

    let stored = 0, skipped = 0, enriched = 0, superseded = 0;
    for (const f of parsed.facts) {
      if (!f.fact || f.fact.length < 5) continue;
      if (f.confidence < 0.7) continue;

      const factType = (f.type === "episodic") ? "episodic" : "semantic";
      try {
        const category = normalizeCategory(f.category);
        const relevance = identityParser.calculateRelevance(f.fact, category);
        const res = await selective.processAndApply(
          f.fact, category, f.confidence, cfg.defaultAgent, factType, relevance
        );
        if (res.stored) {
          if (res.action === "enrich") enriched++;
          else if (res.action === "supersede") superseded++;
          else stored++;
        } else { skipped++; }
      } catch (e) {
        api?.logger?.debug?.('memoria:contradiction-check: ' + String(e));
        const category = normalizeCategory(f.category);
        const relevance = identityParser.calculateRelevance(f.fact, category);
        db.storeFact({
          id: `fact_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
          fact: f.fact, category, confidence: f.confidence,
          source: `continuous-${trigger}`,
          tags: "[]", agent: cfg.defaultAgent,
          created_at: Date.now(), updated_at: Date.now(),
          fact_type: factType, relevance_weight: relevance,
        });
        stored++;
      }
    }

    const parts: string[] = [];
    if (stored > 0) parts.push(`${stored} new`);
    if (enriched > 0) parts.push(`${enriched} enriched`);
    if (superseded > 0) parts.push(`${superseded} superseded`);
    if (skipped > 0) parts.push(`${skipped} skipped`);
    if (parts.length > 0) {
      api.logger.info?.(`memoria: ⚡ continuous [${trigger}] — ${parts.join(", ")}`);
      // Post-process (embed, graph, topics, etc.)
      if (stored > 0 || enriched > 0) {
        await postProcessNewFacts("capture");
      }
    }
  } catch (err) {
    api.logger.debug?.(`memoria: continuous extraction failed: ${String(err)}`);
  } finally {
    state.inProgress = false;
  }
}
