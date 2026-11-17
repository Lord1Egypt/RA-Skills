/**
 * Memoria — Capture hooks (Layer 1: agent_end + after_compaction)
 *
 * Extracted from index.ts Phase 2.2 — pure mechanical move, zero logic change.
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";
import type { MemoriaConfig } from "./core/config.js";
import type { MemoriaDB } from "./core/db.js";
import type { SelectiveMemory } from "./core/selective.js";
import type { LLMProvider } from "./core/providers/types.js";
import type { IdentityParser } from "./core/identity-parser.js";
import type { ProceduralMemory } from "./core/procedural.js";
import type { FeedbackManager } from "./core/feedback.js";
import type { AdaptiveBudget } from "./core/budget.js";
import type { ContinuousHooksState } from "./continuous.js";
import { LLM_EXTRACT_PROMPT, parseJSON, normalizeCategory } from "./core/extraction.js";

export interface CaptureDeps {
  api: OpenClawPluginApi;
  cfg: MemoriaConfig;
  db: MemoriaDB;
  selective: SelectiveMemory;
  extractLlm: LLMProvider;
  identityParser: IdentityParser;
  proceduralMem: ProceduralMemory;
  feedbackMgr: FeedbackManager;
  budget: AdaptiveBudget;
  postProcessNewFacts: (source: "capture" | "compaction") => Promise<void>;
  continuousState: ContinuousHooksState;
}

/**
 * Register the agent_end hook (session capture, Layer 1).
 * Extracts facts from session messages + procedures from tool calls.
 */
export function registerAgentEndHook(deps: CaptureDeps): void {
  const { api, cfg, db, selective, extractLlm, identityParser,
    proceduralMem, feedbackMgr, postProcessNewFacts, continuousState } = deps;

  if (!cfg.autoCapture) return;

  api.on("agent_end", async (event: any, _ctx: any) => {
    if (!event.success || !event.messages || event.messages.length === 0) return;

    // Track how many messages continuous already processed
    const continuousAlreadyCaptured = continuousState.hasExtracted();

    try {
      // ── Feedback loop: measure if recalled facts were used in responses ──
      try {
        const assistantTexts: string[] = [];
        for (const msg of event.messages) {
          if (!msg || typeof msg !== "object") continue;
          const m = msg as Record<string, unknown>;
          if (m.role !== "assistant") continue;
          const c = m.content;
          if (typeof c === "string" && c.length > 10) assistantTexts.push(c);
          else if (Array.isArray(c)) {
            for (const part of c) {
              if (part && typeof part === "object" && (part as any).type === "text") {
                const t = (part as any).text;
                if (typeof t === "string" && t.length > 10) assistantTexts.push(t);
              }
            }
          }
        }
        if (assistantTexts.length > 0) {
          const responseText = assistantTexts.slice(-3).join("\n");
          const fb = await feedbackMgr.processResponse(responseText);
          if (fb.used + fb.ignored > 0) {
            api.logger.debug?.(`memoria: feedback — ${fb.used} used, ${fb.ignored} ignored (${fb.details.length} total)`);
          }
        }
      } catch (e) { api?.logger?.debug?.('memoria:feedback-process: ' + String(e)); }

      // Collect user + assistant texts
      const texts: string[] = [];
      for (const msg of event.messages) {
        if (!msg || typeof msg !== "object") continue;
        const m = msg as Record<string, unknown>;
        const role = m.role as string;
        if (role !== "user" && role !== "assistant") continue;

        const content = m.content;
        if (typeof content === "string" && content.length > 10) {
          texts.push(content.slice(0, 3000)); // truncate for LLM
        } else if (Array.isArray(content)) {
          for (const part of content) {
            if (part && typeof part === "object" && (part as any).type === "text") {
              const t = (part as any).text;
              if (typeof t === "string" && t.length > 10) texts.push(t.slice(0, 3000));
            }
          }
        }
      }

      if (texts.length === 0) return;

      // If continuous learning already captured during this session,
      // only extract from messages NOT yet seen (reduce duplicate LLM calls)
      const effectiveTexts = continuousAlreadyCaptured
        ? texts.slice(-1) // Only the very last message (likely not yet captured)
        : texts.slice(-3);

      if (effectiveTexts.length === 0) return;

      // Take last messages (most relevant)
      const recentTexts = effectiveTexts.join("\n---\n");
      const prompt = LLM_EXTRACT_PROMPT
        .replace("{TEXT}", recentTexts)
        .replace("{MAX_FACTS}", String(cfg.captureMaxFacts));

      const result = await extractLlm.generateWithMeta!(prompt, {
        maxTokens: 1024,
        temperature: 0.1,
        format: "json",
        timeoutMs: 30000,
      });

      if (!result) {
        api.logger.debug?.("memoria: capture skipped — all LLM providers failed");
        return;
      }

      const parsed = parseJSON(result.response) as { facts?: Array<{ fact: string; category: string; type?: string; confidence: number }> };
      if (!parsed?.facts || parsed.facts.length === 0) return;

      let stored = 0;
      let skipped = 0;
      let enriched = 0;
      let superseded = 0;
      for (const f of parsed.facts) {
        if (!f.fact || f.fact.length < 5) continue;
        if (f.confidence < 0.7) continue;

        const factType = (f.type === "episodic") ? "episodic" : "semantic";

        try {
          const category = normalizeCategory(f.category);
          const relevance = identityParser.calculateRelevance(f.fact, category);
          const result = await selective.processAndApply(
            f.fact,
            category,
            f.confidence,
            cfg.defaultAgent,
            factType,
            relevance
          );
          if (result.stored) {
            if (result.action === "enrich") enriched++;
            else if (result.action === "supersede") superseded++;
            else stored++;
          } else {
            skipped++;
          }
        } catch (e) {
          api?.logger?.debug?.('memoria:selective-store: ' + String(e));
          // Fallback: store directly if selective fails
          const category = normalizeCategory(f.category);
          const relevance = identityParser.calculateRelevance(f.fact, category);
          db.storeFact({
            id: `fact_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
            fact: f.fact,
            category,
            confidence: f.confidence,
            source: "auto-capture",
            tags: "[]",
            agent: cfg.defaultAgent,
            created_at: Date.now(),
            updated_at: Date.now(),
            fact_type: factType,
            relevance_weight: relevance,
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
        api.logger.info?.(`memoria: capture — ${parts.join(", ")}`);
      }

      // Post-processing: embed + graph + topics + sync
      if (stored > 0 || enriched > 0) {
        await postProcessNewFacts("capture");
      }

      // ── Procedural Memory: extract successful command sequences ──
      try {
        // DEBUG: log what we receive
        const toolCallCount = event.toolCalls?.length || 0;
        const messageCount = event.messages?.length || 0;
        api.logger.info?.(`[DEBUG] agent_end — toolCalls: ${toolCallCount}, messages: ${messageCount}`);

        // Strategy A: Try toolCalls first (if available)
        let proc: any = null;
        if (event.toolCalls && event.toolCalls.length >= 2) {
          api.logger.info?.(`[DEBUG] Trying toolCalls extraction...`);
          const lastMessage = event.messages[event.messages.length - 1];
          const lastText = typeof lastMessage === "object" && (lastMessage as any).content
            ? String((lastMessage as any).content).toLowerCase()
            : "";

          const successKeywords = ["success", "done", "published", "deployed", "completed", "✓", "✅"];
          const isSuccess = successKeywords.some(kw => lastText.includes(kw));

          if (isSuccess) {
            proc = await proceduralMem.extractProcedure(
              event.toolCalls as any,
              'success',
              `Session: ${event.agentId || cfg.defaultAgent}`
            );
          }
        }

        // Strategy B: Fallback to parsing messages (more robust)
        if (!proc && event.messages && event.messages.length >= 3) {
          api.logger.info?.(`[DEBUG] Trying message extraction...`);
          proc = await proceduralMem.extractFromMessages(
            event.messages as any,
            `Session: ${event.agentId || cfg.defaultAgent}`
          );
        }

        if (proc) {
          api.logger.info?.(`memoria: procedural ✅ captured "${proc.name}" (${proc.steps.length} steps)`);
        } else {
          api.logger.debug?.(`[DEBUG] No procedure extracted (toolCalls=${toolCallCount}, messages=${messageCount})`);
        }
      } catch (err) {
        api.logger.warn?.(`[DEBUG] procedural extraction error: ${String(err)}`);
      }

    } catch (err) {
      api.logger.warn?.(`memoria: capture failed: ${String(err)}`);
    }
  });
}

/**
 * Register the after_compaction hook (compaction capture, Layer 1).
 * Saves facts from LCM compaction summaries before they are lost.
 */
export function registerCompactionHook(deps: CaptureDeps): void {
  const { api, cfg, db, selective, extractLlm, identityParser,
    proceduralMem, budget, postProcessNewFacts } = deps;

  api.on("after_compaction", async (event: any, _ctx: any) => {
    // Budget learning: compaction happened → we may have been too aggressive
    try { budget.onCompaction(); } catch (e) { api?.logger?.debug?.('memoria:budget-compaction: ' + String(e)); }
    const penaltyNote = budget.penalty > 0 ? ` (compaction penalty: -${budget.penalty} facts)` : "";
    if (penaltyNote) api.logger.debug?.(`memoria: budget adjusted${penaltyNote}`);

    try {
      const summary = typeof event.summary === "string" ? event.summary : "";
      if (!summary || summary.length < 50) return;

      const prompt = LLM_EXTRACT_PROMPT
        .replace("{TEXT}", summary.slice(0, 4000))
        .replace("{MAX_FACTS}", String(cfg.captureMaxFacts));

      const result = await extractLlm.generateWithMeta!(prompt, {
        maxTokens: 1024,
        temperature: 0.1,
        format: "json",
        timeoutMs: 30000,
      });

      if (!result) {
        api.logger.debug?.("memoria: compaction capture skipped — all LLM providers failed");
        return;
      }

      const parsed = parseJSON(result.response) as { facts?: Array<{ fact: string; category: string; type?: string; confidence: number }> };
      if (!parsed?.facts || parsed.facts.length === 0) return;

      let stored = 0;
      let skipped = 0;
      for (const f of parsed.facts) {
        if (!f.fact || f.fact.length < 5 || f.confidence < 0.7) continue;
        const factType = (f.type === "episodic") ? "episodic" : "semantic";
        try {
          const category = normalizeCategory(f.category);
          const relevance = identityParser.calculateRelevance(f.fact, category);
          const result = await selective.processAndApply(
            f.fact, category, f.confidence, cfg.defaultAgent, factType, relevance
          );
          if (result.stored) stored++;
          else skipped++;
        } catch (e) {
          api?.logger?.debug?.('memoria:compaction-store: ' + String(e));
          const category = normalizeCategory(f.category);
          const relevance = identityParser.calculateRelevance(f.fact, category);
          db.storeFact({
            id: `fact_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
            fact: f.fact,
            category,
            confidence: f.confidence,
            source: "compaction",
            tags: "[]",
            agent: cfg.defaultAgent,
            created_at: Date.now(),
            updated_at: Date.now(),
            fact_type: factType,
            relevance_weight: relevance,
          });
          stored++;
        }
      }

      if (stored > 0 || skipped > 0) {
        api.logger.info?.(`memoria: compaction — ${stored} stored, ${skipped} skipped (dedup/noise)`);
      }

      // Enrich compaction facts: embed + graph + topics + sync
      if (stored > 0) {
        await postProcessNewFacts("compaction");
      }

      // ── Procedural Memory: extract from compaction summary ──
      try {
        const fakeMessages = [{ role: 'assistant', content: summary }];
        const proc = await proceduralMem.extractFromMessages(
          fakeMessages as any,
          `Compaction summary: ${event.agentId || cfg.defaultAgent}`
        );
        if (proc) {
          api.logger.info?.(`memoria: procedural ✅ captured from compaction "${proc.name}" (${proc.steps.length} steps)`);
        }
      } catch (err) {
        api.logger.debug?.(`[DEBUG] procedural compaction extraction error: ${String(err)}`);
      }

    } catch (err) {
      api.logger.warn?.(`memoria: compaction capture failed: ${String(err)}`);
    }
  });
}
