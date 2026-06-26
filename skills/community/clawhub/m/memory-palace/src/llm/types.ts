/**
 * Memory Palace v1.1 - LLM Types
 * 
 * Type definitions for LLM-enhanced features.
 */

import type { Memory } from '../types.js';

/**
 * LLM call options
 */
export interface LLMOptions {
  /** Task description for the LLM */
  task: string;
  /** Timeout in seconds (default: 30) */
  timeoutSeconds?: number;
  /** Model to use (optional, uses default) */
  model?: string;
  /** Maximum retries on failure (default: 2) */
  maxRetries?: number;
  /** Enable fallback to rule-based engine on failure */
  enableFallback?: boolean;
}

/**
 * LLM call result
 */
export interface LLMResult<T> {
  /** Whether the call succeeded */
  success: boolean;
  /** Parsed result data */
  data?: T;
  /** Error message if failed */
  error?: string;
  /** Time taken in milliseconds */
  duration: number;
  /** Whether fallback was used */
  usedFallback?: boolean;
  /** Number of retries attempted */
  retries?: number;
}

/**
 * Summarize result from LLMSummarizer
 */
export interface SummarizeResult {
  /** One-sentence summary (max 50 chars) */
  summary: string;
  /** Key points extracted */
  keyPoints: string[];
  /** LLM-evaluated importance (0-1) */
  importance: number;
  /** Suggested tags */
  suggestedTags: string[];
  /** Category classification */
  category: string;
}

/**
 * Extracted experience from ExperienceExtractor
 */
export interface ExtractedExperience {
  /** Experience description */
  experience: string;
  /** Applicable context/scenarios */
  context: string;
  /** Lessons learned */
  lessons: string[];
  /** Best practices identified */
  bestPractices: string[];
  /** Related topics */
  relatedTopics: string[];
}

/**
 * Parsed time from TimeParserLLM
 */
export interface ParsedTime {
  /** Resolved date in YYYY-MM-DD format */
  date: string;
  /** Confidence score (0-1) */
  confidence: number;
}

/**
 * Expanded concepts from ConceptExpanderLLM
 */
export interface ExpandedConcepts {
  /** Expanded keywords (5-10 items) */
  keywords: string[];
  /** Related domains (2-3 items) */
  domains: string[];
}

/**
 * Compressed memory from SmartCompressor
 */
export interface CompressedMemory {
  /** Original memory IDs that were compressed */
  originalIds: string[];
  /** Compressed content */
  compressedContent: string;
  /** Key information preserved */
  preservedKeyInfo: string[];
  /** Compression ratio (original size / compressed size) */
  compressionRatio: number;
  /** Overall summary */
  summary: string;
}

/**
 * Experience extraction options
 */
export interface ExtractOptions {
  /** Focus area for extraction */
  focusArea?: string;
  /** Maximum experiences to extract */
  maxExperiences?: number;
}

/**
 * Compression options
 */
export interface CompressionOptions {
  /** Minimum memories to compress */
  minMemories?: number;
  /** Maximum content length after compression */
  maxContentLength?: number;
  /** Preserve these key phrases */
  preservePhrases?: string[];
}

/**
 * Compression options (alias for backwards compatibility)
 */
export type LLMCompressionOptions = CompressionOptions;

/**
 * Time parse options
 */
export interface TimeParseOptions {
  /** Reference date for relative time (default: today) */
  referenceDate?: string;
  /** Locale for parsing (default: 'zh-CN') */
  locale?: string;
}

/**
 * Concept expand options
 */
export interface ConceptExpandOptions {
  /** Maximum keywords to return */
  maxKeywords?: number;
  /** Maximum domains to return */
  maxDomains?: number;
  /** Include related concepts from existing memories */
  useMemoryContext?: boolean;
}

/**
 * Subagent response structure
 */
export interface SubagentResponse {
  /** Response content */
  content: string;
  /** Whether the subagent completed successfully */
  success: boolean;
  /** Error message if failed */
  error?: string;
}

/**
 * Fallback function type
 */
export type FallbackFunction<T> = () => Promise<T> | T;