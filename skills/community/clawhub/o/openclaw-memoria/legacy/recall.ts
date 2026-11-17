/**
 * Memoria — Recall hook (Layer 6: before_prompt_build)
 *
 * Extracted from index.ts Phase 2.2 — pure mechanical move, zero logic change.
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";
import type { MemoriaConfig } from "./core/config.js";
import type { MemoriaDB, Fact } from "./core/db.js";
import type { EmbeddingManager } from "./core/embeddings.js";
import type { KnowledgeGraph } from "./core/graph.js";
import type { TopicManager } from "./core/topics.js";
import type { ObservationManager } from "./core/observations.js";
import type { ProceduralMemory } from "./core/procedural.js";
import type { ContextTreeBuilder } from "./core/context-tree.js";
import { AdaptiveBudget } from "./core/budget.js";
import type { FeedbackManager } from "./core/feedback.js";
import type { LifecycleManager } from "./core/lifecycle.js";
import type { ExpertiseManager } from "./core/expertise.js";
import type { PatternManager } from "./core/patterns.js";
import type { RevisionManager } from "./core/revision.js";
import { scoreAndRank, getHotFacts, HOT_TIER_CONFIG } from "./core/scoring.js";
import { formatRecallContext } from "./core/format.js";
import type { PrefetchCache } from "./prefetch.js";
import type { SelfObserver } from "./core/self-observation.js";

export interface RecallDeps {
  api: OpenClawPluginApi;
  cfg: MemoriaConfig;
  db: MemoriaDB;
  embeddingMgr: EmbeddingManager;
  graph: KnowledgeGraph;
  topicMgr: TopicManager;
  observationMgr: ObservationManager;
  proceduralMem: ProceduralMemory;
  treeBuilder: ContextTreeBuilder;
  budget: AdaptiveBudget;
  feedbackMgr: FeedbackManager;
  lifecycleMgr: LifecycleManager;
  expertiseMgr: ExpertiseManager;
  patternMgr: PatternManager;
  revisionMgr: RevisionManager;
  prefetchCache?: PrefetchCache;
  selfObserver?: SelfObserver;
}

/**
 * Strip OpenClaw envelope metadata and Memoria headers from a raw prompt
 * to extract the actual user message for recall matching.
 */
export function extractUserPrompt(rawPrompt: string): string {
  if (!rawPrompt || rawPrompt.length < 3) return "";
  let prompt = rawPrompt;
  const lastJsonEnd = rawPrompt.lastIndexOf("```\n\n");
  if (lastJsonEnd !== -1 && rawPrompt.includes("untrusted metadata")) {
    prompt = rawPrompt.slice(lastJsonEnd + 5).trim();
  }
  if (prompt.startsWith("## 🧠 Memoria")) {
    const afterMemoria = prompt.indexOf("\n\n", prompt.indexOf("Conversation info"));
    if (afterMemoria !== -1) prompt = prompt.slice(afterMemoria).trim();
  }
  if (!prompt || prompt.length < 3) {
    prompt = rawPrompt.slice(-500).trim();
  }
  return prompt;
}

/**
 * Core recall computation — extracted so it can be called from:
 * 1. before_prompt_build (sync fallback)
 * 2. prefetch on message_received (async, ahead of time)
 *
 * Returns the formatted context string, or undefined if nothing to inject.
 */
export async function computeRecall(
  prompt: string,
  messageCount: number,
  deps: Omit<RecallDeps, "prefetchCache">
): Promise<string | undefined> {
  const { api, cfg, db, embeddingMgr, graph, topicMgr, observationMgr,
  proceduralMem, treeBuilder, budget, feedbackMgr, lifecycleMgr,
  expertiseMgr, patternMgr, revisionMgr } = deps;

  if (!prompt || prompt.length < 3) return undefined;

  try {

  // ── User signal detection (correction / frustration) ──
  try {
    const signal = feedbackMgr.analyzeUserMessage(prompt);
    if (signal.isCorrection || signal.isFrustration) {
      const penalized = feedbackMgr.applyUserSignal(signal.penalty);
      const parts: string[] = [];
      if (signal.isCorrection) parts.push("correction detected");
      if (signal.isFrustration) parts.push("frustration detected");
      if (penalized.length > 0) {
        api.logger.info?.(`memoria: user signal (${parts.join(" + ")}) → ${penalized.length} facts penalized by ${signal.penalty}`);
      }
    }
  } catch (e) { api?.logger?.debug?.('memoria:recall: ' + String(e)); }

  // Adaptive budget: compute how many facts to inject based on context usage
  const tokenEstimate = AdaptiveBudget.estimateTokens(messageCount);
  const budgetResult = budget.compute(tokenEstimate);
  const recallLimit = budgetResult.limit;

  const penaltyLog = budget.penalty > 0 ? `, penalty -${budget.penalty}` : "";
  api.logger.debug?.(`memoria: budget ${budgetResult.zone} (${(budgetResult.usage * 100).toFixed(0)}% used${penaltyLog}) → ${recallLimit} facts`);

  // Hot tier: always-injected facts
  const hotFactsRaw = db.hotFacts(HOT_TIER_CONFIG.minAccessCount, HOT_TIER_CONFIG.staleAfterDays, HOT_TIER_CONFIG.maxHotFacts);
  const hotIds = new Set(hotFactsRaw.map(f => f.id));
  const hotScored = getHotFacts(hotFactsRaw);
  const hotLimit = hotScored.length;
  const searchLimit = Math.max(recallLimit - hotLimit, 2);

  // Hybrid search: FTS5 + cosine + temporal scoring
  let topFacts: Array<{ id: string; fact: string; category: string; confidence: number; temporalScore: number }>;

  if (embeddingMgr.embeddedCount() > 0) {
    const results = await embeddingMgr.hybridSearch(prompt, searchLimit, {
      ftsWeight: 0.35,
      cosineWeight: 0.45,
      temporalWeight: 0.20,
    });
    topFacts = results.filter(f => f.confidence >= 0.5 && !hotIds.has(f.id));
  } else {
    const fetchLimit = Math.min(searchLimit * 2, 20);
    const facts = db.searchFacts(prompt, fetchLimit);
    if (!facts || facts.length === 0 && hotScored.length === 0) return undefined;
    const relevant = (facts || []).filter(f => f.confidence >= 0.5 && !hotIds.has(f.id));
    const scored = scoreAndRank(relevant);
    topFacts = scored.slice(0, searchLimit);
  }

  if (topFacts.length === 0) return undefined;

  // Graph enrichment: find entities in the query, traverse graph for related facts
  let graphFacts: Fact[] = [];
  try {
    const entities = graph.findEntitiesInText(prompt);
    if (entities.length > 0) {
      const related = graph.getRelatedFacts(entities.map(e => e.name), 2, 3);
      const existingIds = new Set(topFacts.map(f => f.id));
      for (const r of related) {
        if (!existingIds.has(r.id)) {
          const fact = db.getFact(r.id);
          if (fact) graphFacts.push(fact);
        }
      }

      // Hebbian: reinforce connections between co-accessed entities
      const entityIds = entities.map(e => e.id).filter(Boolean) as string[];
      if (entityIds.length >= 2) {
        graph.hebbianReinforce(entityIds);
      }
    }
  } catch (e) { api?.logger?.debug?.('memoria:graph-enrichment: ' + String(e)); }

  // Topic enrichment: find relevant topics and add their facts
  const expandedQueries = embeddingMgr.expandQuery(prompt);
  let topicFacts: Fact[] = [];
  try {
    const relevantTopics = await topicMgr.findRelevantTopics(prompt, 3, expandedQueries);
    if (relevantTopics.length > 0) {
      const existingIds = new Set([...topFacts.map(f => f.id), ...graphFacts.map(f => f.id)]);
      for (const rt of relevantTopics) {
        for (const factText of rt.facts.slice(0, 3)) {
          const found = db.searchFacts(factText.slice(0, 80), 1);
          if (found.length > 0 && !existingIds.has(found[0].id)) {
            topicFacts.push(found[0]);
            existingIds.add(found[0].id);
          }
        }
      }
      if (relevantTopics.length > 0) {
        api.logger.debug?.(`memoria: topics matched: ${relevantTopics.map(t => t.topic.name).join(", ")}`);
      }
    }
  } catch (e) { api?.logger?.debug?.('memoria:topic-enrichment: ' + String(e)); }

  // Observations: synthesized multi-fact summaries
  let observationContext = "";
  try {
    const relevantObs = await observationMgr.getRelevantObservations(prompt);
    if (relevantObs.length > 0) {
      observationContext = observationMgr.formatForRecall(relevantObs);
      api.logger.debug?.(`memoria: ${relevantObs.length} observations matched`);
    }
  } catch (e) { api?.logger?.debug?.('memoria:observations-recall: ' + String(e)); }

  // Procedural memory: search for matching "how-to" procedures
  let proceduresContext = "";
  const matchedProcedureIds: string[] = [];
  try {
    // Strategy 1: Direct text search
    let procedures = proceduralMem.search(prompt, 3);

    // Strategy 2: If few results, expand via Graph entities
    if (procedures.length < 2) {
      try {
        const graphEntities = graph.findEntitiesInText(prompt);
        if (graphEntities.length > 0) {
          const relatedTerms = graphEntities
            .flatMap((e: any) => [e.name, ...(e.aliases || [])])
            .slice(0, 5);
          for (const term of relatedTerms) {
            const extra = proceduralMem.search(term, 2);
            for (const p of extra) {
              if (!procedures.find(existing => existing.id === p.id)) {
                procedures.push(p);
              }
            }
          }
          if (procedures.length > 3) procedures = procedures.slice(0, 3);
        }
      } catch (e) { api?.logger?.debug?.('memoria:graph-expansion: ' + String(e)); }
    }

    if (procedures.length > 0) {
      // Limit to max 2 procedures, show max 3 steps each (avoid context bloat)
      const MAX_PROCEDURES = 2;
      const MAX_STEPS = 3;
      const procTexts: string[] = [];
      for (const proc of procedures.slice(0, MAX_PROCEDURES)) {
        matchedProcedureIds.push(proc.id);
        const successRate = proc.success_count / Math.max(proc.success_count + proc.failure_count, 1);
        const degThreshold = cfg.procedural?.degradedThreshold ?? 0.5;
        const isStale = proceduralMem.needsDocCheck(proc);
        const isDegraded = proc.degradation_score > degThreshold;
        const status = isDegraded ? "⚠ degraded"
          : isStale ? "🕰️ stale — verify before using"
          : proc.preferred ? "★ preferred" : "✓";
        const qualityStr = `quality: ${(proc.quality.overall * 100).toFixed(0)}%`;
        const versionStr = proc.version > 1 ? ` v${proc.version}` : '';
        const gotchaStr = proc.gotchas ? `\n  ⚠ Gotchas: ${proc.gotchas.slice(0, 200)}` : '';
        const staleStr = isStale ? `\n  🕰️ Stale — verify before using` : '';
        const truncatedSteps = proc.steps.slice(0, MAX_STEPS);
        const moreSteps = proc.steps.length > MAX_STEPS ? `\n  ... (+${proc.steps.length - MAX_STEPS} more steps)` : '';
        procTexts.push(
          `**${proc.name}**${versionStr} ${status} (${(successRate * 100).toFixed(0)}% success, ${qualityStr}):\n` +
          truncatedSteps.map((s, i) => `  ${i + 1}. ${s.slice(0, 300)}`).join('\n') +
          moreSteps +
          gotchaStr +
          staleStr
        );
      }
      proceduresContext = `\n## 🔧 Known Procedures\n${procTexts.join('\n\n')}\n`;
      api.logger.debug?.(`memoria: ${procedures.length} procedures matched, showing ${Math.min(procedures.length, MAX_PROCEDURES)} (graph-expanded)`);
    }
  } catch (e) { api?.logger?.debug?.('memoria:procedural-recall: ' + String(e)); }

  // Context tree: organize facts hierarchically, weight by query
  let finalFacts: Fact[] = [];
  try {
    // Build set of fact IDs that are members of active (non-stale) clusters
    let clusteredFactIds: Set<string> = new Set();
    try {
      const clusters = db.raw.prepare(
        "SELECT tags FROM facts WHERE fact_type = 'cluster' AND superseded = 0"
      ).all() as Array<{ tags: string }>;
      for (const c of clusters) {
        try {
          const meta = JSON.parse(c.tags);
          if (!meta.stale && Array.isArray(meta.memberIds)) {
            for (const id of meta.memberIds) clusteredFactIds.add(id);
          }
        } catch (e) { api?.logger?.debug?.('memoria:json-parse: ' + String(e)); }
      }
    } catch (e) { api?.logger?.debug?.('memoria:cluster-parse: ' + String(e)); }

    // Apply lifecycle multiplier + expertise boost + cluster-member deprioritization
    const allFactsCandidates = [...hotScored, ...topFacts, ...graphFacts, ...topicFacts].map((f: any) => {
      let mult = lifecycleMgr.getRecallMultiplier(f.lifecycle_state);
      if (clusteredFactIds.has(f.id) && f.fact_type !== "cluster") {
        mult *= 0.6;
      }
      try {
        const factTopics = db.raw.prepare(
          "SELECT t.name FROM topics t JOIN fact_topics ft ON ft.topic_id = t.id WHERE ft.fact_id = ?"
        ).all(f.id) as Array<{ name: string }>;
        if (factTopics.length > 0) {
          const boost = expertiseMgr.applyExpertiseBoost(1.0, factTopics.map(t => t.name));
          if (boost > 1.0) mult *= boost;
        }
      } catch (e) { api?.logger?.debug?.('memoria:expertise: ' + String(e)); }
      mult *= patternMgr.applyPatternBoost(1.0, f.fact_type);
      if ((f as any).temporalScore) {
        return { ...f, temporalScore: (f as any).temporalScore * mult };
      }
      return f;
    });
    const tree = await treeBuilder.build(allFactsCandidates as any, prompt);

    finalFacts = treeBuilder.extractFacts(tree, recallLimit) as any;

    if (tree.roots.length > 0) {
      const treeView = treeBuilder.renderTree(tree, 2);
      api.logger.debug?.(`memoria tree:\n${treeView}`);
    }
  } catch (e) {
    api?.logger?.debug?.('memoria:tree-build: ' + String(e));
    finalFacts = [...topFacts, ...graphFacts, ...topicFacts].slice(0, recallLimit) as any;
  }

  if (finalFacts.length === 0 && !observationContext && !proceduresContext) return undefined;

  // Self-observation: append agent profile if enough data
  let selfObsContext = "";
  try {
    if (deps.selfObserver) {
      selfObsContext = deps.selfObserver.formatForPrompt();
    }
  } catch (e) { api?.logger?.debug?.('memoria:self-obs-recall: ' + String(e)); }

  const context = formatRecallContext(finalFacts as any, observationContext) + proceduresContext + selfObsContext;

  // Track access + feedback loop + budget learning + lifecycle update
  const ids = finalFacts.map(f => f.id);
  try { db.trackAccess(ids); } catch (e) { api?.logger?.debug?.('memoria:track-access: ' + String(e)); }
  try { feedbackMgr.recordRecall(ids, prompt); } catch (e) { api?.logger?.debug?.('memoria:feedback-record: ' + String(e)); }
  try { budget.recordRecall(recallLimit); } catch (e) { api?.logger?.debug?.('memoria:budget-record: ' + String(e)); }

  try {
    for (const fact of finalFacts) {
      lifecycleMgr.updateLifecycle(fact);
    }
  } catch (e) { api?.logger?.debug?.('memoria:lifecycle-update: ' + String(e)); }

  // Proactive revision: check if any settled facts need refinement (async, non-blocking)
  setImmediate(async () => {
    try {
      const revResult = await revisionMgr.checkAndRevise();
      if (revResult.revised > 0) {
        api.logger.info?.(`memoria: proactive revision completed (${revResult.revised} refined, ${revResult.created} new facts)`);
      }
    } catch (err) {
      api.logger.debug?.(`memoria: proactive revision failed: ${String(err)}`);
    }
  });

  const hotNote = hotLimit > 0 ? `, ${hotLimit} hot` : "";
  const graphNote = graphFacts.length > 0 ? `, +${graphFacts.length} graph` : "";
  const obsNote = observationContext ? ", +obs" : "";
  api.logger.info?.(`memoria: recall injected ${finalFacts.length} facts${obsNote} (${hotNote}${graphNote}, tree+hybrid) for "${prompt.slice(0, 50)}..."`);
  return context;
  } catch (err) {
  api.logger.warn?.(`memoria: recall failed: ${String(err)}`);
  return undefined;
  }
}

/**
 * Register the before_prompt_build hook (recall / Layer 6).
 * Checks prefetch cache first; falls back to sync computeRecall.
 */
export function registerRecallHook(deps: RecallDeps): void {
  const { api, cfg, prefetchCache } = deps;

  if (!cfg.autoRecall) return;

  api.on("before_prompt_build", async (event: any, _ctx: any) => {
    try {
      const rawPrompt = typeof event.prompt === "string" ? event.prompt : "";
      if (!rawPrompt || rawPrompt.length < 3) return undefined;

      // ── Prefetch cache: check if recall was already computed async ──
      if (prefetchCache) {
        const cached = await prefetchCache.get(rawPrompt, 3_000);
        if (cached?.result) {
          api.logger.debug?.(`memoria: ⚡ prefetch HIT (computed in ${cached.computeTimeMs}ms, age ${Date.now() - cached.timestamp}ms)`);
          return { prependContext: cached.result };
        }
        if (cached) {
          api.logger.debug?.(`memoria: prefetch completed but no results`);
        } else {
          api.logger.debug?.(`memoria: prefetch MISS — falling back to sync recall`);
        }
      }

      // Sync fallback: compute recall now
      const prompt = extractUserPrompt(rawPrompt);
      const msgCount = (event as any).messageCount || (event as any).messages?.length || 0;
      const context = await computeRecall(prompt, msgCount, deps);
      if (!context) return undefined;
      return { prependContext: context };
    } catch (err) {
      api.logger.warn?.(`memoria: recall hook failed: ${String(err)}`);
      return undefined;
    }
  });
}
