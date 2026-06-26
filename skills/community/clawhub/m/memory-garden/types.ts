// skills/types.ts - AUTO-GENERATED, DO NOT EDIT
// Generated: 2026-02-15T20:00:00Z
// Schema version: 2
//
// Memory Garden TypeScript types for OpenClaw skill integration.
// These types mirror the Go types in pkg/patterns/pattern.go and pkg/extract/types.go.

// === Core Types (Phase 0a) ===

export interface Pattern {
  // Core identity
  slug: string;
  cid: string;

  // Content
  claim: string;
  expansion: string;

  // Classification
  domain: string;
  related_domains?: string[];
  evidence_tier: EvidenceTier;
  tier: KnowledgeTier;

  // Metadata
  created_at: string;
  schema_version: number;

  // === CRDT Fields (Phase 1) ===
  n_count?: NCountCRDT;
  validations?: ValidationCRDT;

  // === Extraction Fields (Phase 2) ===
  extracted_from?: string;
  grounding_score?: number;
  lens?: Lens;
  context_hashes?: string[];

  // === Governance Fields (Phase 3) ===
  promoted_at?: string;
  approved_by?: string[];
  care_assessment?: CareAssessment;
  tombstoned?: boolean;
  tombstoned_at?: string;
  tombstoned_by?: string;
  tombstone_reason?: string;

  // === Sybil Detection Fields (Phase 3) ===
  first_seen_at?: string;
  increment_history?: IncrementRecord[];
}

export interface NCountCRDT {
  counters: Record<string, number>;
}

export interface ValidationCRDT {
  positive: Record<string, number>;
  negative: Record<string, number>;
}

export interface CareAssessment {
  harm_potential: number;
  misuse_risk: number;
  domain_sensitivity: number;
}

export interface IncrementRecord {
  node_id: string;
  timestamp: string;
  peer_meta?: PeerMeta;
}

export interface PeerMeta {
  ip_prefix?: string;
  user_agent?: string;
}

// === Type Aliases ===

export type KnowledgeTier = "output" | "pattern" | "principle" | "axiom";
export type EvidenceTier = "anecdotal" | "consensus" | "empirical" | "established";
export type Lens = "microscope" | "kaleidoscope" | "telescope";

// === Search Types ===

export interface SearchResult {
  pattern: Pattern;
  score: number;
  highlight: string;
}

export interface SearchOptions {
  query: string;
  limit?: number;
  domain?: string;
  min_tier?: KnowledgeTier;
}

// === API Types ===

export interface ToolCallRequest {
  name: string;
  arguments: Record<string, unknown>;
}

export interface ToolCallResponse {
  content: ContentBlock[];
}

export interface ContentBlock {
  type: "text";
  text: string;
}

export interface ErrorResponse {
  error: ErrorDetail;
}

export interface ErrorDetail {
  code: string;
  message: string;
  try?: string;
}

export interface HealthResponse {
  status: string;
  pattern_count: number;
  domain_count: number;
  version: string;
}

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;
}

export interface ToolListResponse {
  tools: ToolDefinition[];
}

// === Domain Stats Types ===

export interface DomainInfo {
  name: string;
  count: number;
}

export interface StatsResult {
  total_patterns: number;
  by_domain: Record<string, number>;
  by_tier: Record<string, number>;
  by_evidence: Record<string, number>;
}

// === Extraction Types (Phase 2) ===
// Issue 017 I3/M5: Types for OpenClaw skill integration
// Mirrors Go types in pkg/extract/types.go

/**
 * Input for pattern extraction.
 * Matches Go ExtractionInput struct.
 */
export interface ExtractionInput {
  query: string;           // Original user query
  response: string;        // AI response to extract from
  domain: string;          // Suggested domain (can be overridden by extractor)
  session_id: string;      // Client session for diversity tracking (snake_case for wire format)
  source: string;          // Source model (e.g., "claude-3-opus")
}

/**
 * Result of pattern extraction.
 * Matches Go ExtractionResult struct.
 */
export interface ExtractionResult {
  patterns: Pattern[];     // Extracted patterns
  confidence: number;      // Overall extraction confidence (0.0-1.0)
  duration_ms: number;     // Extraction duration in milliseconds
}

/**
 * Failed extraction record for dead-letter queue.
 * Issue 017 I6: Track failed extractions for retry/analysis.
 */
export interface ExtractionError {
  input: ExtractionInput;
  error: string;
  timestamp: string;
  retry_count: number;
}
