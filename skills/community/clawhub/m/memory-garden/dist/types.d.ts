export interface Pattern {
    slug: string;
    cid: string;
    claim: string;
    expansion: string;
    domain: string;
    related_domains?: string[];
    evidence_tier: EvidenceTier;
    tier: KnowledgeTier;
    created_at: string;
    schema_version: number;
    n_count?: NCountCRDT;
    validations?: ValidationCRDT;
    extracted_from?: string;
    grounding_score?: number;
    lens?: Lens;
    context_hashes?: string[];
    promoted_at?: string;
    approved_by?: string[];
    care_assessment?: CareAssessment;
    tombstoned?: boolean;
    tombstoned_at?: string;
    tombstoned_by?: string;
    tombstone_reason?: string;
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
export type KnowledgeTier = "output" | "pattern" | "principle" | "axiom";
export type EvidenceTier = "anecdotal" | "consensus" | "empirical" | "established";
export type Lens = "microscope" | "kaleidoscope" | "telescope";
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
/**
 * Input for pattern extraction.
 * Matches Go ExtractionInput struct.
 */
export interface ExtractionInput {
    query: string;
    response: string;
    domain: string;
    session_id: string;
    source: string;
}
/**
 * Result of pattern extraction.
 * Matches Go ExtractionResult struct.
 */
export interface ExtractionResult {
    patterns: Pattern[];
    confidence: number;
    duration_ms: number;
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
//# sourceMappingURL=types.d.ts.map