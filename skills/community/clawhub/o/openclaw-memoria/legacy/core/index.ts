/**
 * @primo-studio/memoria-core — Standalone multi-layer cognitive memory engine
 * 
 * Public API for embedding Memoria into any JavaScript/TypeScript application.
 * Zero dependency on OpenClaw — works standalone or integrated.
 * 
 * @example
 * ```typescript
 * import { Memoria } from '@primo-studio/memoria-core';
 * 
 * const memoria = await Memoria.init({
 *   dbPath: './my-app.db',
 *   provider: 'ollama',
 *   model: 'qwen3.5:4b',
 *   embeddingModel: 'nomic-embed-text-v2-moe'
 * });
 * 
 * await memoria.store('User prefers dark mode', 'preference', 0.95);
 * const results = await memoria.recall('What theme does the user like?');
 * console.log(results.facts);
 * 
 * memoria.close();
 * ```
 */

import fs from "fs";
import { MemoriaDB } from "./db.js";
import { SelectiveMemory } from "./selective.js";
import { EmbeddingManager } from "./embeddings.js";
import { KnowledgeGraph } from "./graph.js";
import { ContextTreeBuilder } from "./context-tree.js";
import { AdaptiveBudget } from "./budget.js";
import { MdSync } from "./sync.js";
import { MdRegenManager } from "./md-regen.js";
import { FallbackChain } from "./fallback.js";
import type { FallbackProviderConfig } from "./fallback.js";
import { TopicManager } from "./topics.js";
import { lmStudioEmbed, openaiEmbed } from "./providers/openai-compat.js";
import type { EmbedProvider, LLMProvider } from "./providers/types.js";
import { EmbedFallback } from "./embed-fallback.js";
import { ObservationManager } from "./observations.js";
import { FactClusterManager } from "./fact-clusters.js";
import { FeedbackManager } from "./feedback.js";
import { IdentityParser } from "./identity-parser.js";
import { LifecycleManager } from "./lifecycle.js";
import { RevisionManager } from "./revision.js";
import { HebbianManager } from "./hebbian.js";
import { ExpertiseManager } from "./expertise.js";
import { ProceduralMemory } from "./procedural.js";
import { PatternManager } from "./patterns.js";
import { formatRecallContext } from "./format.js";
import { normalizeCategory } from "./extraction.js";

// ─── Public API Types ───

export interface MemoriaInitOptions {
  /** Path to SQLite database file (will be created if not exists) */
  dbPath: string;
  
  /** Optional workspace path for markdown sync (.md files) */
  workspacePath?: string;
  
  /** LLM provider: 'ollama' | 'openai' | 'anthropic' | 'lmstudio' */
  provider?: string;
  
  /** LLM model name (e.g., 'qwen3.5:4b', 'gpt-5.4-nano') */
  model?: string;
  
  /** Embedding model name (e.g., 'nomic-embed-text-v2-moe', 'text-embedding-3-small') */
  embeddingModel?: string;
  
  /** Embedding dimensions (default: 768) */
  embeddingDimensions?: number;
  
  /** Base URL for provider (e.g., 'http://localhost:11434') */
  baseUrl?: string;
  
  /** API key for cloud providers (OpenAI, Anthropic) */
  apiKey?: string;
  
  /** Language for prompts: 'fr' | 'en' (default: 'en') */
  language?: string;
  
  /** Fallback chain configuration (optional) */
  fallback?: Array<{
    type: string;
    model?: string;
    baseUrl?: string;
    apiKey?: string;
  }>;
  
  /** Recall limit (max facts to return) */
  recallLimit?: number;
  
  /** Enable debug logging */
  debug?: boolean;
}

export interface StoreResult {
  factId: number;
  stored: boolean;
  reason?: string;
}

export interface RecallResult {
  facts: Array<{
    id: number;
    fact: string;
    category: string;
    confidence: number;
    score: number;
    created_at: string;
  }>;
  totalFound: number;
}

export interface RecallOptions {
  limit?: number;
  minConfidence?: number;
  categories?: string[];
}

export interface MemoriaStats {
  totalFacts: number;
  totalEmbeddings: number;
  totalRelations: number;
  totalTopics: number;
  totalPatterns: number;
  totalObservations: number;
  lifecycleDistribution: Record<string, number>;
  categoryCounts: Record<string, number>;
}

// ─── Main Memoria Class ───

export class Memoria {
  db: MemoriaDB;
  selective: SelectiveMemory;
  embeddings: EmbeddingManager;
  graph: KnowledgeGraph;
  topics: TopicManager;
  procedural: ProceduralMemory;
  patterns: PatternManager;
  observations: ObservationManager;
  feedback: FeedbackManager;
  lifecycle: LifecycleManager;
  revision: RevisionManager;
  hebbian: HebbianManager;
  expertise: ExpertiseManager;
  factClusters: FactClusterManager;
  contextTree: ContextTreeBuilder;
  budget: AdaptiveBudget;
  mdSync?: MdSync;
  mdRegen?: MdRegenManager;
  
  private llm: LLMProvider;
  private embedder: EmbedProvider;
  private recallLimit: number;
  private logger: { info?: (msg: string) => void; warn?: (msg: string) => void; debug?: (msg: string) => void };

  private constructor(
    db: MemoriaDB,
    llm: LLMProvider,
    embedder: EmbedProvider,
    options: MemoriaInitOptions,
    logger: { info?: (msg: string) => void; warn?: (msg: string) => void; debug?: (msg: string) => void }
  ) {
    this.db = db;
    this.llm = llm;
    this.embedder = embedder;
    this.recallLimit = options.recallLimit || 8;
    this.logger = logger;

    // Initialize all managers
    this.embeddings = new EmbeddingManager(db, embedder);
    this.selective = new SelectiveMemory(db, llm, {
      dupThreshold: 0.85,
      contradictionCheck: true,
      enrichEnabled: true,
    }, this.embeddings);
    
    this.graph = new KnowledgeGraph(db, llm);
    this.topics = new TopicManager(db, llm, embedder, {
      emergenceThreshold: 3,
      mergeOverlap: 0.7,
      subtopicThreshold: 5,
    });
    this.procedural = new ProceduralMemory(db, llm);
    this.patterns = new PatternManager(db, llm);
    this.observations = new ObservationManager(db);
    this.feedback = new FeedbackManager(db);
    this.lifecycle = new LifecycleManager(db);
    this.revision = new RevisionManager(db, llm);
    this.hebbian = new HebbianManager(db);
    this.expertise = new ExpertiseManager(db);
    this.factClusters = new FactClusterManager(db);
    this.contextTree = new ContextTreeBuilder(db);
    this.budget = new AdaptiveBudget(db);

    if (options.workspacePath && fs.existsSync(options.workspacePath)) {
      this.mdSync = new MdSync(options.workspacePath, db);
      this.mdRegen = new MdRegenManager(options.workspacePath, db);
    }
  }

  /**
   * Initialize a new Memoria instance
   */
  static async init(options: MemoriaInitOptions): Promise<Memoria> {
    const logger = {
      info: options.debug ? (msg: string) => console.log(`[memoria] ${msg}`) : undefined,
      warn: (msg: string) => console.warn(`[memoria] ${msg}`),
      debug: options.debug ? (msg: string) => console.debug(`[memoria] ${msg}`) : undefined,
    };

    // Create database
    const db = new MemoriaDB(options.dbPath);

    // Build fallback chain
    const provider = options.provider || 'ollama';
    const model = options.model || 'gemma3:4b';
    const baseUrl = options.baseUrl || (provider === 'ollama' ? 'http://localhost:11434' : undefined);
    
    const fallbackProviders: FallbackProviderConfig[] = options.fallback?.map(f => ({
      name: `${f.type}:${f.model || 'auto'}`,
      type: f.type as 'ollama' | 'openai' | 'lmstudio' | 'anthropic',
      model: f.model,
      baseUrl: f.baseUrl,
      apiKey: f.apiKey,
    })) || [
      {
        name: `${provider}:${model}`,
        type: provider as 'ollama' | 'openai' | 'lmstudio' | 'anthropic',
        model,
        baseUrl,
        apiKey: options.apiKey,
        timeoutMs: 12000,
      },
    ];

    const llm = new FallbackChain({ providers: fallbackProviders }, logger);

    // Build embedding fallback
    const embedModel = options.embeddingModel || 'nomic-embed-text-v2-moe';
    const embedDimensions = options.embeddingDimensions || 768;
    
    const embedProviders: EmbedProvider[] = [];
    
    if (provider === 'ollama' || !provider) {
      try {
        const { ollamaEmbed } = await import('./providers/ollama.js');
        embedProviders.push(ollamaEmbed(embedModel, embedDimensions, baseUrl || 'http://localhost:11434'));
      } catch (e) {
        logger.debug?.(`Failed to load Ollama embed: ${e}`);
      }
    }
    
    if (provider === 'lmstudio') {
      embedProviders.push(lmStudioEmbed(embedModel, embedDimensions));
    }
    
    if (provider === 'openai' && options.apiKey) {
      embedProviders.push(openaiEmbed(embedModel, options.apiKey, embedDimensions));
    }

    const embedder = embedProviders.length > 1
      ? new EmbedFallback(embedProviders, logger)
      : embedProviders[0];

    if (!embedder) {
      throw new Error('No embedding provider available');
    }

    logger.info?.(`Memoria initialized: provider=${provider}, model=${model}, embed=${embedModel}`);

    return new Memoria(db, llm, embedder, options, logger);
  }

  /**
   * Store a new fact in memory
   */
  async store(fact: string, category?: string, confidence?: number): Promise<StoreResult> {
    const normalizedCategory = normalizeCategory(category || 'savoir');
    const finalConfidence = confidence ?? 0.8;

    try {
      // Check duplicates/contradictions
      const result = await this.selective.storeFact(fact, normalizedCategory, finalConfidence);
      
      if (!result.stored) {
        return { factId: -1, stored: false, reason: result.reason };
      }

      // Embed
      try {
        await this.embeddings.embedFact(result.factId);
      } catch (e) {
        this.logger.warn?.(`Embedding failed for fact ${result.factId}: ${e}`);
      }

      // Extract entities/relations
      try {
        await this.graph.extractFromFact(result.factId);
      } catch (e) {
        this.logger.debug?.(`Graph extraction failed: ${e}`);
      }

      return { factId: result.factId, stored: true };
    } catch (e) {
      this.logger.warn?.(`Failed to store fact: ${e}`);
      return { factId: -1, stored: false, reason: String(e) };
    }
  }

  /**
   * Recall facts based on a query
   */
  async recall(query: string, options?: RecallOptions): Promise<RecallResult> {
    const limit = options?.limit || this.recallLimit;
    const minConfidence = options?.minConfidence || 0.3;
    const categories = options?.categories;

    try {
      const results = await this.selective.recall(query, limit, minConfidence, categories);
      
      return {
        facts: results.map(r => ({
          id: r.id,
          fact: r.fact,
          category: r.category,
          confidence: r.confidence,
          score: r.score,
          created_at: r.created_at,
        })),
        totalFound: results.length,
      };
    } catch (e) {
      this.logger.warn?.(`Recall failed: ${e}`);
      return { facts: [], totalFound: 0 };
    }
  }

  /**
   * Query memory with natural language (future: dialectic reasoning)
   */
  async query(naturalLanguageQuestion: string): Promise<string> {
    // TODO: implement dialectic reasoning layer
    const results = await this.recall(naturalLanguageQuestion, { limit: 5 });
    
    if (results.facts.length === 0) {
      return "No relevant information found in memory.";
    }

    return formatRecallContext(results.facts.map(f => ({
      id: f.id,
      fact: f.fact,
      category: f.category,
      confidence: f.confidence,
      score: f.score,
      created_at: f.created_at,
    })));
  }

  /**
   * Get memory statistics
   */
  async stats(): Promise<MemoriaStats> {
    const totalFacts = this.db.db.prepare('SELECT COUNT(*) as count FROM facts').get() as { count: number };
    const totalEmbeddings = this.db.db.prepare('SELECT COUNT(*) as count FROM embeddings').get() as { count: number };
    const totalRelations = this.db.db.prepare('SELECT COUNT(*) as count FROM relations').get() as { count: number };
    const totalTopics = this.db.db.prepare('SELECT COUNT(*) as count FROM topics').get() as { count: number };
    const totalPatterns = this.db.db.prepare('SELECT COUNT(*) as count FROM facts WHERE fact_type = "pattern"').get() as { count: number };
    const totalObservations = this.db.db.prepare('SELECT COUNT(*) as count FROM observations').get() as { count: number };

    const lifecycleRows = this.db.db.prepare('SELECT lifecycle_state, COUNT(*) as count FROM facts GROUP BY lifecycle_state').all() as Array<{ lifecycle_state: string; count: number }>;
    const lifecycleDistribution: Record<string, number> = {};
    for (const row of lifecycleRows) {
      lifecycleDistribution[row.lifecycle_state || 'unknown'] = row.count;
    }

    const categoryRows = this.db.db.prepare('SELECT category, COUNT(*) as count FROM facts GROUP BY category').all() as Array<{ category: string; count: number }>;
    const categoryCounts: Record<string, number> = {};
    for (const row of categoryRows) {
      categoryCounts[row.category] = row.count;
    }

    return {
      totalFacts: totalFacts.count,
      totalEmbeddings: totalEmbeddings.count,
      totalRelations: totalRelations.count,
      totalTopics: totalTopics.count,
      totalPatterns: totalPatterns.count,
      totalObservations: totalObservations.count,
      lifecycleDistribution,
      categoryCounts,
    };
  }

  /**
   * Close database connection
   */
  close(): void {
    this.db.db.close();
  }
}

// ─── Re-export everything for advanced usage ───

export { MemoriaDB } from "./db.js";
export { SelectiveMemory } from "./selective.js";
export { EmbeddingManager } from "./embeddings.js";
export { KnowledgeGraph } from "./graph.js";
export { TopicManager } from "./topics.js";
export { ProceduralMemory } from "./procedural.js";
export { PatternManager } from "./patterns.js";
export { ObservationManager } from "./observations.js";
export { FeedbackManager } from "./feedback.js";
export { LifecycleManager } from "./lifecycle.js";
export { RevisionManager } from "./revision.js";
export { HebbianManager } from "./hebbian.js";
export { ExpertiseManager } from "./expertise.js";
export { FactClusterManager } from "./fact-clusters.ts";
export { ContextTreeBuilder } from "./context-tree.js";
export { AdaptiveBudget } from "./budget.js";
export { FallbackChain } from "./fallback.js";
export { EmbedFallback } from "./embed-fallback.js";
export { MdSync } from "./sync.js";
export { MdRegenManager } from "./md-regen.js";
export { IdentityParser } from "./identity-parser.js";

export type { EmbedProvider, LLMProvider } from "./providers/types.js";
export type { FallbackProviderConfig } from "./fallback.js";
export { ollamaEmbed } from "./providers/ollama.js";
export { lmStudioEmbed, openaiEmbed } from "./providers/openai-compat.js";
export { anthropicEmbed } from "./providers/anthropic.js";
