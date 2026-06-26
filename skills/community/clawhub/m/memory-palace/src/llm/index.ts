/**
 * Memory Palace v1.1 - LLM Module
 * 
 * Unified exports for all LLM-enhanced features.
 */

// Types
export type {
  LLMOptions,
  LLMResult,
  SummarizeResult,
  ExtractedExperience,
  ParsedTime,
  ExpandedConcepts,
  CompressedMemory,
  ExtractOptions,
  CompressionOptions,
  TimeParseOptions,
  ConceptExpandOptions,
  SubagentResponse,
  FallbackFunction,
} from './types.js';

// Core client
export { SubagentClient, defaultClient, callLLMJSON, callLLMWithFallback } from './subagent-client.js';

// Summarizer
export { 
  LLMSummarizer, 
  defaultSummarizer, 
  summarizeMemory,
  type SummarizerOptions 
} from './summarizer.js';

// Experience extractor
export { 
  ExperienceExtractor, 
  defaultExtractor, 
  extractExperiences 
} from './experience-extractor.js';

// Time parser
export { 
  TimeParserLLM, 
  defaultTimeParser, 
  parseTime 
} from './time-parser.js';

// Concept expander
export { 
  ConceptExpanderLLM, 
  defaultExpander, 
  expandConcepts 
} from './concept-expander.js';

// Smart compressor
export { 
  SmartCompressor, 
  defaultCompressor, 
  compressMemories 
} from './smart-compressor.js';

/**
 * LLM module version
 */
export const LLM_MODULE_VERSION = '1.1.0';