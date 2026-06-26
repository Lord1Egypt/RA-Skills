/**
 * Memory Palace - Type Definitions
 * 
 * Core types for the memory palace system.
 */

/**
 * Memory status
 */
export type MemoryStatus = 'active' | 'archived' | 'deleted';

/**
 * Memory source
 */
export type MemorySource = 'conversation' | 'document' | 'system' | 'user';

/**
 * Memory type - distinguishes different kinds of memories
 */
export type MemoryType = 'fact' | 'experience' | 'lesson' | 'preference' | 'decision';

/**
 * Experience category
 */
export type ExperienceCategory = 'development' | 'operations' | 'product' | 'communication' | 'general';

/**
 * Experience metadata for type='experience' memories
 */
export interface ExperienceMeta {
  /** Category of experience */
  category: ExperienceCategory | string;
  /** Applicable scenarios description */
  applicability: string;
  /** Source (task ID or conversation topic) */
  source: string;
  /** Whether verified as effective */
  verified: boolean;
  /** Number of times verified */
  verifiedCount?: number;
  /** When last verified */
  lastVerifiedAt?: Date;
  /** Effectiveness score (0-1), computed: Math.min(1, verifiedCount * 0.3 + usageCount * 0.1) */
  effectivenessScore: number;
  /** Number of times this experience was queried/used */
  usageCount: number;
  /** When last used/queried */
  lastUsedAt?: Date;
}

/**
 * Memory relation type
 */
export type RelationType = 'relates_to' | 'refines' | 'contradicts';

/**
 * A relation between two memories
 */
export interface MemoryRelation {
  /** Relation type */
  type: RelationType;
  /** Target memory ID */
  targetId: string;
  /** Optional note about this relation */
  note?: string;
}

/**
 * Memory decay metrics for Ebbinghaus forgetting curve simulation
 */
export interface MemoryDecayMetrics {
  /** Decay score (0-1), 1=fresh, 0=forgotten */
  decayScore: number;
  /** Number of times this memory has been accessed */
  accessCount: number;
  /** Last access timestamp */
  lastAccessedAt?: Date;
}

/**
 * Memory record stored in palace
 */
export interface Memory {
  /** Unique identifier */
  id: string;
  
  /** Raw content */
  content: string;
  
  /** Optional LLM-generated summary */
  summary?: string;
  
  /** Tags for categorization */
  tags: string[];
  
  /** Importance score (0-1) */
  importance: number;
  
  /** Current status */
  status: MemoryStatus;
  
  /** Source of this memory */
  source: MemorySource;
  
  /** Location/path within palace */
  location: string;
  
  /** Creation timestamp */
  createdAt: Date;
  
  /** Last update timestamp */
  updatedAt: Date;
  
  /** Deletion timestamp (if soft-deleted) */
  deletedAt?: Date;
  
  /** Memory type (distinguishes different kinds of memories) */
  type?: MemoryType;
  
  /** Experience metadata (only for type='experience' memories) */
  experienceMeta?: ExperienceMeta;
  
  /** Relations to other memories (max 5) */
  relations?: MemoryRelation[];
  
  /** Ebbinghaus forgetting curve metrics */
  decay?: MemoryDecayMetrics;
}

/**
 * Verified experience result with shortcut fields
 */
export interface VerifiedExperienceResult extends Memory {
  /** Shortcut: verified status */
  verified: boolean;
  /** Shortcut: verification count */
  verifiedCount: number;
  /** Shortcut: last verification timestamp */
  verifiedAt?: Date;
}

/**
 * Parameters for storing a new memory
 */
export interface StoreParams {
  /** Memory content */
  content: string;
  
  /** Location within palace (default: "default") */
  location?: string;
  
  /** Tags for categorization */
  tags?: string[];
  
  /** Importance score (0-1, default: 0.5) */
  importance?: number;
  
  /** Source type */
  source?: MemorySource;
  
  /** Optional summary */
  summary?: string;
  
  /** Memory type */
  type?: MemoryType;
  
  /** Experience metadata (only for type='experience') */
  experienceMeta?: ExperienceMeta;

  /** Relations to other memories */
  relations?: MemoryRelation[];
}

/**
 * Parameters for updating a memory
 */
export interface UpdateParams {
  /** Memory ID */
  id: string;
  
  /** New content */
  content?: string;
  
  /** New tags (replaces existing) */
  tags?: string[];
  
  /** New importance */
  importance?: number;
  
  /** New status */
  status?: MemoryStatus;
  
  /** New summary */
  summary?: string;
  
  /** Append to existing tags instead of replacing */
  appendTags?: boolean;
  
  /** Relations to other memories */
  relations?: MemoryRelation[];
}

/**
 * Search/recall options
 */
export interface RecallOptions {
  /** Filter by location */
  location?: string;
  
  /** Filter by tags (all must match) */
  tags?: string[];
  
  /** Maximum results (default: 10) */
  topK?: number;
  
  /** Minimum importance score */
  minImportance?: number;
  
  /** Include archived memories */
  includeArchived?: boolean;
}

/**
 * Parameters for getting a memory (object-style)
 */
export interface GetParams {
  id: string;
}

/**
 * Parameters for recalling memories (object-style)
 */
export interface RecallParams {
  query: string;
  location?: string;
  tags?: string[];
  topK?: number;
  minImportance?: number;
  includeArchived?: boolean;
}

/**
 * Parameters for getting relevant experiences (object-style)
 */
export interface GetRelevantParams {
  context: string;
  limit?: number;
}

/**
 * Search result
 */
export interface SearchResult {
  /** Memory record */
  memory: Memory;
  
  /** Relevance score (0-1) */
  score: number;
  
  /** Match highlights */
  highlights?: string[];
  
  /** Whether this result is from fallback (text) search */
  isFallback?: boolean;
}

/**
 * List options
 */
export interface ListOptions {
  /** Filter by location */
  location?: string;
  
  /** Filter by tags (all must match) */
  tags?: string[];
  
  /** Filter by status */
  status?: MemoryStatus;
  
  /** Maximum results */
  limit?: number;
  
  /** Offset for pagination */
  offset?: number;
  
  /** Sort by field */
  sortBy?: 'createdAt' | 'updatedAt' | 'importance';
  
  /** Sort order */
  sortOrder?: 'asc' | 'desc';
}

/**
 * Statistics
 */
export interface Stats {
  /** Total memories */
  total: number;
  
  /** Active memories */
  active: number;
  
  /** Archived memories */
  archived: number;
  
  /** Deleted (in trash) */
  deleted: number;
  
  /** Memories by location */
  byLocation: Record<string, number>;
  
  /** Memories by tag */
  byTag: Record<string, number>;
  
  /** Average importance */
  avgImportance: number;
  
  /** Storage path */
  storagePath: string;
  
  /** Vector search status */
  vectorSearch?: {
    enabled: boolean;
    provider?: string;
  };
}

/**
 * Vector search interface (for OpenClaw integration)
 */
export interface VectorSearchProvider {
  /** Search for similar content */
  search(query: string, topK: number, filter?: Record<string, unknown>): Promise<VectorSearchResult[]>;
  
  /** Index a document */
  index(id: string, content: string, metadata?: Record<string, unknown>): Promise<void>;
  
  /** Remove from index */
  remove(id: string): Promise<void>;
}

/**
 * Vector search result
 */
export interface VectorSearchResult {
  id: string;
  score: number;
  metadata?: Record<string, unknown>;
}

// ==================== Experience-related types ====================

/**
 * Options for recording an experience
 */
export interface RecordExperienceOptions {
  /** Experience content */
  content: string;
  
  /** Category (development/operations/product/communication/general) */
  category?: ExperienceCategory | string;
  
  /** Applicable scenarios */
  applicability: string;
  
  /** Source (task ID or conversation topic) */
  source: string;
  
  /** Tags (auto-added with 'experience' tag) */
  tags?: string[];
  
  /** Importance (default: 0.7 for experiences) */
  importance?: number;
  
  /** Location (default: 'experiences') */
  location?: string;
}

/**
 * Options for getting experiences
 */
export interface GetExperiencesOptions {
  /** Filter by category */
  category?: ExperienceCategory | string;
  
  /** Filter by applicable scenario (partial match) */
  applicability?: string;
  
  /** Only return verified experiences */
  verified?: boolean;
  
  /** Maximum results */
  limit?: number;
  
  /** Sort by verification count */
  sortByVerified?: boolean;
}

/**
 * Options for verifying an experience
 */
export interface VerifyExperienceOptions {
  /** Experience ID */
  id: string;
  
  /** Whether the experience is effective */
  effective: boolean;
}