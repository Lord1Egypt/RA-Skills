/**
 * Memory Palace - Cognitive Enhancement Layer for OpenClaw
 * 
 * A skill for persistent memory management with semantic search,
 * knowledge graph, and cognitive enhancement features.
 * 
 * @packageDocumentation
 */

// Core
export { MemoryPalaceManager, type MemoryPalaceManagerOptions } from './manager.js';
export { FileStorage, serializeMemory, deserializeMemory } from './storage.js';

// Types
export type {
  Memory,
  StoreParams,
  UpdateParams,
  RecallOptions,
  SearchResult,
  ListOptions,
  Stats,
  MemoryStatus,
  MemorySource,
  MemoryType,
  ExperienceCategory,
  ExperienceMeta,
  VectorSearchProvider,
  VectorSearchResult,
  RecordExperienceOptions,
  GetExperiencesOptions,
  VerifyExperienceOptions,
} from './types.js';

// Cognitive modules
export { TopicCluster, type MemoryCluster, type ClusteringOptions } from './cognitive/cluster.js';
export { EntityTracker, type Entity, type EntityType, type EntityTrackingResult } from './cognitive/entity.js';
export { KnowledgeGraphBuilder, type KnowledgeGraph, type GraphNode, type GraphEdge, type TraversalOptions } from './cognitive/graph.js';

// Background tasks
export { ConflictDetector, type Conflict, type ConflictType, type ConflictOptions } from './background/conflict.js';
export { MemoryCompressor, type CompressionResult, type CompressionStrategy, type CompressionOptions } from './background/compress.js';
export { LocalVectorSearchProvider, createLocalVectorSearch, type LocalVectorSearchConfig } from './background/vector-search.js';
export { TimeReasoningEngine, createTimeReasoning, type TimeContext } from './background/time-reasoning.js';
export { ConceptExpander, createConceptExpander, type ConceptExpansion } from './background/concept-expansion.js';

// LLM-enhanced features (v1.1)
export {
  // Types
  type LLMOptions,
  type LLMResult,
  type SummarizeResult,
  type ExtractedExperience,
  type ParsedTime,
  type ExpandedConcepts,
  type CompressedMemory,
  type ExtractOptions,
  type TimeParseOptions,
  type ConceptExpandOptions,
  // Core
  SubagentClient,
  defaultClient,
  callLLMJSON,
  callLLMWithFallback,
  // Modules
  LLMSummarizer,
  defaultSummarizer,
  summarizeMemory,
  type SummarizerOptions,
  ExperienceExtractor,
  defaultExtractor,
  extractExperiences,
  TimeParserLLM,
  defaultTimeParser,
  parseTime,
  ConceptExpanderLLM,
  defaultExpander,
  expandConcepts,
  SmartCompressor,
  defaultCompressor,
  compressMemories,
  LLM_MODULE_VERSION,
} from './llm/index.js';

// Re-export LLM CompressionOptions with alias to avoid conflict
export { type CompressionOptions as LLMCompressionOptions } from './llm/types.js';

// Experience Management (v1.2)
export {
  ExperienceManager,
  createExperienceManager,
} from './experience-manager.js';