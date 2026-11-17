/**
 * Memoria — Multi-layer memory plugin for OpenClaw (Phase 2.2)
 *
 * THIN ADAPTER — imports, initializes, and wires OpenClaw hooks.
 * All logic lives in focused modules:
 *   - config.ts          — MemoriaConfig, parseConfig, provider factories
 *   - extraction.ts      — LLM_EXTRACT_PROMPT, parseJSON, normalizeCategory
 *   - format.ts          — formatRecallContext
 *   - recall.ts          — before_prompt_build hook (Layer 6)
 *   - continuous.ts      — message_received + llm_output hooks (Layer 21)
 *   - procedural-hooks.ts — after_tool_call hook (Layer 1b)
 *   - capture.ts         — agent_end + after_compaction hooks (Layer 1)
 *   - orchestrator.ts    — postProcessNewFacts cascade pipeline
 */

import fs from "fs";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";
import { MemoriaDB } from "./core/db.js";
import { WriteAheadLog } from "./core/wal.js";
import { SelfObserver } from "./core/self-observation.js";
import { AutoSkillCreator } from "./core/auto-skill.js";
import { DialecticMemory } from "./core/dialectic.js";
import { SelectiveMemory } from "./core/selective.js";
import { EmbeddingManager } from "./core/embeddings.js";
import { KnowledgeGraph } from "./core/graph.js";
import { ContextTreeBuilder } from "./core/context-tree.js";
import { AdaptiveBudget } from "./core/budget.js";
import { MdSync } from "./core/sync.js";
import { MdRegenManager } from "./core/md-regen.js";
import { FallbackChain } from "./core/fallback.js";
import type { FallbackProviderConfig } from "./core/fallback.js";
import { TopicManager } from "./core/topics.js";
import { lmStudioEmbed, openaiEmbed } from "./core/providers/openai-compat.js";
import type { EmbedProvider, LLMProvider } from "./core/providers/types.js";
import { EmbedFallback } from "./core/embed-fallback.js";
import { ObservationManager } from "./core/observations.js";
import { FactClusterManager } from "./core/fact-clusters.js";
import { FeedbackManager } from "./core/feedback.js";
import { IdentityParser } from "./core/identity-parser.js";
import { LifecycleManager } from "./core/lifecycle.js";
import { RevisionManager } from "./core/revision.js";
import { HebbianManager } from "./core/hebbian.js";
import { ExpertiseManager } from "./core/expertise.js";
import { ProceduralMemory } from "./core/procedural.js";
import { PatternManager } from "./core/patterns.js";

// Refactored modules
import { parseConfig, createEmbedProvider, type MemoriaConfig, type MemoriaLayer } from "./core/config.js";
import { createPostProcessNewFacts } from "./orchestrator.js";
import { registerContinuousHooks } from "./continuous.js";
import { registerRecallHook } from "./recall.js";
import { PrefetchCache } from "./prefetch.js";
import { registerProceduralHook } from "./procedural-hooks.js";
import { registerAgentEndHook, registerCompactionHook } from "./capture.js";

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || `${process.env.HOME}/.openclaw/workspace`;

export function register(api: OpenClawPluginApi): void {
  const rawPluginConfig = (api as any).pluginConfig as Record<string, unknown> | undefined;
  const cfg = parseConfig(rawPluginConfig);

  const db = new MemoriaDB(WORKSPACE);
  const wal = new WriteAheadLog(db.raw);
  const selfObserver = new SelfObserver(db.raw);
  // autoSkill is initialized later, after proceduralMem is created
  let autoSkill: AutoSkillCreator;

  // Process any unprocessed WAL entries from a previous crash
  const unprocessedCount = wal.unprocessedCount();
  if (unprocessedCount > 0) {
    api.logger.info?.(`memoria: WAL has ${unprocessedCount} unprocessed entries from previous session — will process on next extraction`);
  }
  // Cleanup old processed WAL entries
  const cleaned = wal.cleanup(7);
  if (cleaned > 0) {
    api.logger.debug?.(`memoria: WAL cleanup: removed ${cleaned} old processed entries`);
  }

  // ─── Fallback chain: config providers → default chain ───
  api.logger.info?.(`[memoria] Config loaded: fallback=${cfg.fallback.length} providers, llm=${cfg.llm.provider}/${cfg.llm.model}, embed=${cfg.embed.provider}/${cfg.embed.model}`);
  const fallbackProviders: FallbackProviderConfig[] = cfg.fallback.length > 0
    ? cfg.fallback
    : [
        {
          name: "ollama",
          type: "ollama" as const,
          model: cfg.llm.model || "gemma3:4b",
          baseUrl: cfg.llm.provider === "ollama" ? (cfg.llm.baseUrl || "http://localhost:11434") : "http://localhost:11434",
          timeoutMs: 12000,
          embedModel: cfg.embed.model || "nomic-embed-text-v2-moe",
          embedDimensions: cfg.embed.dimensions || 768,
        },
        {
          name: "openai",
          type: "openai" as const,
          model: "gpt-5.4-nano",
          baseUrl: "https://api.openai.com/v1",
          apiKey: cfg.llm.apiKey || process.env.OPENAI_API_KEY || "",
          timeoutMs: 15000,
        },
        {
          name: "lmstudio",
          type: "lmstudio" as const,
          model: "auto",
          baseUrl: "http://localhost:1234/v1",
          timeoutMs: 12000,
        },
      ];

  const chain = new FallbackChain(
    { providers: fallbackProviders },
    { info: api.logger.info?.bind(api.logger), warn: api.logger.warn?.bind(api.logger), debug: api.logger.debug?.bind(api.logger) },
  );

  // ─── Per-layer LLM overrides ───
  const overrides = cfg.llm.overrides || {};
  function layerLLM(layer: MemoriaLayer): LLMProvider {
    const ov = overrides[layer];
    if (!ov) return chain;
    const provCfg: FallbackProviderConfig = {
      name: `${layer}:${ov.provider}`,
      type: ov.provider,
      model: ov.model,
      baseUrl: ov.baseUrl,
      apiKey: ov.apiKey || cfg.llm.apiKey || process.env.OPENAI_API_KEY || "",
    };
    return new FallbackChain(
      { providers: [provCfg, ...fallbackProviders] },
      { info: api.logger.info?.bind(api.logger), warn: api.logger.warn?.bind(api.logger), debug: api.logger.debug?.bind(api.logger) },
    );
  }

  const extractLlm = layerLLM("extract");
  const contradictionLlm = layerLLM("contradiction");
  const graphLlm = layerLLM("graph");
  const topicsLlm = layerLLM("topics");

  // Log active overrides
  const activeOverrides = Object.keys(overrides).filter(k => overrides[k as MemoriaLayer]);
  if (activeOverrides.length > 0) {
    api.logger.info?.(`memoria: per-layer LLM overrides: ${activeOverrides.map(k => `${k}=${overrides[k as MemoriaLayer]!.provider}/${overrides[k as MemoriaLayer]!.model}`).join(", ")}`);
  }

  // ─── Embedding fallback chain ───
  const primaryEmbed = createEmbedProvider(cfg.embed);
  const embedProviders: EmbedProvider[] = [primaryEmbed];
  if (cfg.embed.provider !== "lmstudio") {
    try { embedProviders.push(lmStudioEmbed(cfg.embed.model, cfg.embed.dimensions)); } catch (e) { api?.logger?.debug?.('memoria:embed-fallback: ' + String(e)); }
  }
  if (cfg.embed.provider !== "openai" && (cfg.embed.apiKey || cfg.llm.apiKey || process.env.OPENAI_API_KEY)) {
    try { embedProviders.push(openaiEmbed("text-embedding-3-small", cfg.embed.apiKey || cfg.llm.apiKey || process.env.OPENAI_API_KEY || "", cfg.embed.dimensions)); } catch (e) { api?.logger?.debug?.('memoria:embed-fallback: ' + String(e)); }
  }
  const embedder = embedProviders.length > 1
    ? new EmbedFallback(embedProviders, { info: api.logger.info?.bind(api.logger), warn: api.logger.warn?.bind(api.logger) })
    : primaryEmbed;
  const embeddingMgr = new EmbeddingManager(db, embedder);

  // ─── Manager instances ───
  const selective = new SelectiveMemory(db, contradictionLlm, {
    dupThreshold: 0.85,
    contradictionCheck: true,
    enrichEnabled: true,
  }, embeddingMgr);

  const graph = new KnowledgeGraph(db, graphLlm);
  const treeBuilder = new ContextTreeBuilder(db);
  const topicMgr = new TopicManager(db, topicsLlm, embedder, {
    emergenceThreshold: 3,
    mergeOverlap: 0.7,
    subtopicThreshold: 5,
    scanInterval: 15,
  });
  const identityParser = new IdentityParser(cfg.workspacePath);
  const lifecycleMgr = new LifecycleManager(db, {
    freshDays: cfg.lifecycle?.freshDays ?? 15,
    settledMinAccess: cfg.lifecycle?.settledMinAccess ?? 3,
    dormantAfterDays: cfg.lifecycle?.dormantAfterDays ?? 60,
    detailCursor: cfg.lifecycle?.detailCursor ?? 5,
    revisionRecallThreshold: cfg.lifecycle?.revisionRecallThreshold ?? 10,
  });
  const revisionMgr = new RevisionManager(db, chain);
  const hebbianMgr = new HebbianManager(db);
  const expertiseMgr = new ExpertiseManager(db);
  const proceduralLlm = layerLLM("procedural");
  const proceduralMem = new ProceduralMemory(db.raw, proceduralLlm, {
    reflectEvery: cfg.procedural?.reflectEvery ?? 3,
    degradedThreshold: cfg.procedural?.degradedThreshold ?? 0.5,
    defaultSafety: cfg.procedural?.defaultSafety ?? 0.8,
    staleDays: cfg.procedural?.staleDays ?? 30,
    docCheckDays: cfg.procedural?.docCheckDays ?? 60,
  });
  proceduralMem.ensureSchema();
  autoSkill = new AutoSkillCreator(proceduralMem, WORKSPACE, cfg.autoSkill);

  const patternMgr = new PatternManager(db, extractLlm, cfg.patterns);

  // Apply staleness penalties — once per process
  const stalenessKey = '__memoria_staleness_applied';
  if (!(globalThis as any)[stalenessKey]) {
    (globalThis as any)[stalenessKey] = true;
    const stalenessResult = proceduralMem.applyStalenessPenalties();
    if (stalenessResult.updated > 0 || stalenessResult.flaggedForDocCheck > 0) {
      console.log(`[memoria] 🕰️ Staleness check: ${stalenessResult.updated} aged, ${stalenessResult.flaggedForDocCheck} flagged for doc check`);
    }
  }

  const budget = new AdaptiveBudget({
    contextWindow: cfg.contextWindow || 200000,
    maxFacts: cfg.recallLimit || 12,
    minFacts: 2,
  });
  const mdSync = new MdSync(db, {
    workspacePath: cfg.workspacePath || process.env.HOME + "/.openclaw/workspace",
    dbToMd: cfg.syncMd !== false,
    mdToDb: false,
  });
  const mdRegen = new MdRegenManager(db, cfg.workspacePath || process.env.HOME + "/.openclaw/workspace", {
    recentDays: 30,
    maxFactsPerFile: 150,
    archiveNotice: true,
  });

  const observationMgr = new ObservationManager(db, chain, embedder, {
    emergenceThreshold: 3,
    matchThreshold: 0.6,
    maxRecallObservations: Math.max(Math.floor(cfg.recallLimit / 3), 2),
    maxEvidencePerObservation: 15,
  });

  const clusterMgr = new FactClusterManager(db, chain);
  const feedbackMgr = new FeedbackManager(db);

  // Cross-layer: when selective supersedes a fact, cascade to ALL layers
  selective.onSupersede = (supersededId, _newId) => {
    try {
      const parts: string[] = [];
      const obsAffected = observationMgr.onFactSuperseded(supersededId);
      if (obsAffected > 0) parts.push(`${obsAffected} obs`);
      const graphAffected = graph.onFactSuperseded(supersededId);
      if (graphAffected > 0) parts.push(`${graphAffected} graph`);
      const topicAffected = topicMgr.onFactSuperseded(supersededId);
      if (topicAffected > 0) parts.push(`${topicAffected} topics`);
      const embRemoved = embeddingMgr.onFactSuperseded(supersededId);
      if (embRemoved) parts.push("1 embed");
      if (parts.length > 0) {
        api.logger.debug?.(`memoria: supersede cascade for ${supersededId} — ${parts.join(", ")}`);
      }
    } catch (e) { api?.logger?.debug?.('memoria:supersede-cascade: ' + String(e)); }
  };

  mdSync.ensureSchema(db);

  // ─── Boot stats ───
  const stats = db.stats();
  const embCount = embeddingMgr.embeddedCount();
  const gStats = graph.stats();
  const tStats = topicMgr.stats();
  const oStats = observationMgr.stats();
  const cStats = clusterMgr.stats();
  let pluginVersion = "3.2.0";
  try {
    const pkgPath = new URL("./package.json", import.meta.url);
    const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf-8"));
    pluginVersion = pkg.version || pluginVersion;
  } catch (e) { api?.logger?.debug?.('memoria:version-read: ' + String(e)); }
  const lifecycleRefresh = lifecycleMgr.refreshAll();

  try {
    const reparented = topicMgr.reparentExistingTopics();
    if (reparented > 0) {
      api.logger.info?.(`memoria: reparented ${reparented} orphan topics`);
    }
  } catch (e) { api?.logger?.debug?.('memoria:topic-reparent: ' + String(e)); }

  const lifecycleStats = lifecycleMgr.getStats();
  const hebbianStats = hebbianMgr.getStats();
  const expertiseStats = expertiseMgr.getStats();
  const procStats = proceduralMem.getStats();
  const patStats = patternMgr.stats();
  const fbStats = feedbackMgr.getStats();
  const fbNote = fbStats.totalWithFeedback > 0 ? `, feedback: ${fbStats.totalWithFeedback} tracked (avg ${fbStats.avgUsefulness.toFixed(1)})` : "";
  const lifecycleNote = ` | lifecycle: ${lifecycleStats.fresh ?? 0}f/${lifecycleStats.settled ?? 0}s/${lifecycleStats.dormant ?? 0}d (cursor:${lifecycleMgr.detailCursor})`;
  const hebbianNote = ` | graph: ${hebbianStats.strong} strong, ${hebbianStats.weak} weak`;
  const expertiseNote = ` | expertise: ${expertiseStats.expert}★★★/${expertiseStats.experienced}★★/${expertiseStats.familiar}★`;
  const procNote = procStats.total > 0
    ? ` | procedures: ${procStats.healthy}✓/${procStats.degraded}⚠${(procStats.stale ?? 0) > 0 ? `/${procStats.stale}🕰️` : ''}`
    : "";
  const patNote = patStats.total > 0 ? ` | patterns: ${patStats.total} (avg ${patStats.avgOccurrences} occ)` : "";
  const contEnabled = cfg.continuous?.enabled !== false && cfg.autoCapture;
  const contInterval = cfg.continuous?.interval ?? 4;
  const contNote = contEnabled ? ` | continuous: every ${contInterval} turns` : "";
  api.logger.info?.(`memoria: v${pluginVersion} registered (${stats.active} facts, ${cStats.total} clusters, ${oStats.total} observations, ${embCount} embedded, ${gStats.entities} entities, ${gStats.relations} relations, ${tStats.totalTopics} topics${fbNote}${lifecycleNote}${hebbianNote}${expertiseNote}${procNote}${patNote}${contNote}, fallback: ${chain.providerNames.join(" → ")})`);

  const fileSizes = mdRegen.fileSizes();
  const totalLines = Object.values(fileSizes).reduce((sum, f) => sum + f.lines, 0);
  api.logger.info?.(`memoria: workspace .md files = ${totalLines} lines total (regen available to bound growth)`);

  // Background: embed unembedded facts on boot
  const unembedded = embeddingMgr.unembeddedFacts(100);
  if (unembedded.length > 0) {
    api.logger.info?.(`memoria: ${unembedded.length} facts need embedding, starting background indexing...`);
    embeddingMgr.embedBatch(unembedded.map(f => ({ id: f.id, text: f.fact })))
      .then(n => api.logger.info?.(`memoria: background embed complete — ${n} facts indexed`))
      .catch(err => api.logger.warn?.(`memoria: background embed failed: ${String(err)}`));
  }

  // ─── Dialectic Memory (Layer 24) ───
  const dialectic = new DialecticMemory({
    db, embeddingMgr, graph, topicMgr: topicMgr!,
    proceduralMem, observationMgr, llm: extractLlm,
  });

  // Expose dialectic.query() for external use (e.g., tools, commands)
  (api as any)._memoriaDialectic = dialectic;

  // ─── Create shared post-processing pipeline ───
  const postProcessNewFacts = createPostProcessNewFacts(
    api, db, embeddingMgr, graph, hebbianMgr, topicMgr,
    observationMgr, clusterMgr, mdSync, mdRegen, patternMgr
  );

  // ─── Prefetch cache (async recall, inspired by Hermes) ───
  const prefetchCache = new PrefetchCache(30_000);

  // ─── Register all hooks ───

  // Layer 6: Recall (before_prompt_build)
  registerRecallHook({
    api, cfg, db, embeddingMgr, graph, topicMgr, observationMgr,
    proceduralMem, treeBuilder, budget, feedbackMgr, lifecycleMgr,
    expertiseMgr, patternMgr, revisionMgr, prefetchCache, selfObserver,
  });

  // RecallDeps without prefetchCache — for prefetch computation
  const recallDepsForPrefetch = {
    api, cfg, db, embeddingMgr, graph, topicMgr, observationMgr,
    proceduralMem, treeBuilder, budget, feedbackMgr, lifecycleMgr,
    expertiseMgr, patternMgr, revisionMgr, selfObserver,
  };

  // Layer 21: Continuous Learning (message_received + llm_output)
  const continuousState = registerContinuousHooks(
    api, cfg, db, selective, extractLlm, identityParser, postProcessNewFacts,
    prefetchCache, recallDepsForPrefetch, wal, selfObserver,
  );

  // Layer 1b: Real-time procedural capture (after_tool_call)
  registerProceduralHook(api, cfg, extractLlm, proceduralMem, graph);

  // Layer 1: Session capture (agent_end + after_compaction)
  const captureDeps = {
    api, cfg, db, selective, extractLlm, identityParser,
    proceduralMem, feedbackMgr, budget, postProcessNewFacts, continuousState,
  };
  registerAgentEndHook(captureDeps);
  registerCompactionHook(captureDeps);

  // Layer 23: Auto Skill Creation + Self-Observation success tracking (agent_end)
  api.on("agent_end", async (event: any, _ctx: any) => {
    try {
      // Record session success in self-observation
      if (event.success && selfObserver) {
        const msgCount = event.messages?.length || 0;
        const toolCount = event.toolCallCount || 0;
        if (msgCount > 2 || toolCount > 0) {
          // Detect domain from conversation content
          const lastMsgs = (event.messages || [])
            .slice(-5)
            .map((m: any) => m.content || "")
            .join(" ");
          selfObserver.record("success", lastMsgs.slice(0, 500));
        }
      }

      // Check for mature procedures → promote to skill files
      if (event.success) {
        const promoted = autoSkill.checkAndPromote();
        if (promoted > 0) {
          api.logger.info?.(`memoria: 🎓 auto-skill: ${promoted} procedure(s) promoted to skill files`);
        }
      }
    } catch (err) {
      api.logger.debug?.(`memoria: auto-skill/self-obs agent_end error: ${String(err)}`);
    }
  });
}

export default { register };
