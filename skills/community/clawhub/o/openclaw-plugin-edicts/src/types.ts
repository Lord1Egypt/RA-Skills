/**
 * User-provided input when adding an edict.
 */
export interface EdictInput {
  /** The edict content text */
  text: string;
  /** Category for grouping (auto-normalized) */
  category: string;
  /** Dedup/supersession key — edicts with same key replace each other */
  key?: string;
  /** Free-form tags (auto-normalized) */
  tags?: string[];
  /** How confident are we in this edict */
  confidence?: 'verified' | 'inferred' | 'user';
  /** Provenance — who/what established this edict */
  source?: string;
  /** Time-to-live classification */
  ttl?: 'ephemeral' | 'event' | 'durable' | 'permanent';
  /** Expiration date (ISO 8601) for ephemeral/event edicts */
  expiresAt?: string;
  /** Duration until expiry. String: '30m', '2h', '7d'. Number or numeric string: seconds. */
  expiresIn?: string | number;
}

/**
 * A fully resolved edict with all runtime fields.
 */
export interface Edict {
  /** Unique identifier — key-derived or sequential */
  id: string;
  /** The edict content text */
  text: string;
  /** Category (normalized) */
  category: string;
  /** Tags (normalized) */
  tags: string[];
  /** Confidence level */
  confidence: 'verified' | 'inferred' | 'user';
  /** Provenance */
  source: string;
  /** Dedup/supersession key */
  key?: string;
  /** Time-to-live classification */
  ttl: 'ephemeral' | 'event' | 'durable' | 'permanent';
  /** Expiration date (ISO 8601) */
  expiresAt?: string;
  /** Creation timestamp (ISO 8601) */
  created: string;
  /** Last update timestamp (ISO 8601) */
  updated: string;
  /** Last time this edict was accessed via get/render (ISO 8601) */
  lastAccessed?: string;
  /** Cached token count (internal) */
  _tokens?: number;
}

/**
 * A superseded edict stored in history.
 */
export interface HistoryEntry {
  /** Original ID with timestamp suffix */
  id: string;
  /** The original edict text */
  text: string;
  /** ID of the edict that replaced this one, or 'expired' */
  supersededBy: string;
  /** When this entry was archived (ISO 8601) */
  archivedAt: string;
}

export interface MutationResult {
  action: 'created' | 'updated' | 'deleted' | 'superseded' | 'not_found';
  found?: boolean;
  id?: string;
  edict?: Edict;
  pruned: number;
  /** Capacity/limit warnings (informational) */
  warnings?: string[];
}

export interface CapacityStatus {
  countUsage: number;
  tokenUsage: number;
  categories: Record<string, { count: number; limit?: number; overLimit: boolean }>;
  warnings: string[];
}

export interface CompactionGroup {
  keyPrefix: string;
  category: string;
  edicts: Edict[];
}

export interface ReviewOptions {
  expiryLookaheadDays?: number;
}

export interface ReviewResult {
  stale: Edict[];
  expiringSoon: Edict[];
  capacity: CapacityStatus;
  compactionCandidates: CompactionGroup[];
}

export interface EdictStats {
  total: number;
  history: number;
  tokenCount: number;
  tokenBudget: number;
  tokenBudgetRemaining: number;
  byCategory: Record<string, number>;
  byConfidence: Record<string, number>;
  byTtl: Record<string, number>;
  byTag: Record<string, number>;
}

export interface ImportResult {
  imported: number;
  historyImported: number;
  pruned: number;
}

export interface FindQuery {
  id?: string;
  key?: string;
  category?: string;
  tag?: string;
  confidence?: 'verified' | 'inferred' | 'user';
  ttl?: 'ephemeral' | 'event' | 'durable' | 'permanent';
  text?: string;
}

/**
 * Tokenizer function signature.
 * Takes text, returns approximate token count.
 */
export type Tokenizer = (text: string) => number;

/**
 * Custom renderer function signature.
 * Takes active edicts, returns formatted string.
 */
export type Renderer = (edicts: Edict[]) => string;

/**
 * Configuration options for EdictStore.
 */
export interface EdictStoreOptions {
  /** Path to the edicts file. Default: './edicts.yaml' */
  path?: string;
  /** Storage format. Default: 'yaml' (inferred from extension) */
  format?: 'yaml' | 'json';
  /** Maximum number of edicts. Default: 200 */
  maxEdicts?: number;
  /** Maximum total token budget. Default: 4000 */
  tokenBudget?: number;
  /** Custom tokenizer function. Default: chars/4 approximation */
  tokenizer?: Tokenizer;
  /** Allowed categories. Empty/undefined = any category allowed */
  categories?: string[];
  /** Custom renderer function. Overrides built-in formats */
  renderer?: Renderer;
  /** Days before a durable edict is considered stale. Default: 90 */
  staleThresholdDays?: number;
  /** Per-category soft limits. e.g., { product: 30, internal: 20 } */
  categoryLimits?: Record<string, number>;
  /** Default soft limit for categories not explicitly listed */
  defaultCategoryLimit?: number;
  /** Default TTL in seconds for ephemeral edicts with no explicit expiry. Default: 86400 (24h) */
  defaultEphemeralTtlSeconds?: number;
  /** Auto-save after mutations and prune operations. Default: true */
  autoSave?: boolean;
}

/**
 * Internal file structure matching YAML/JSON on disk.
 */
export type StoredEdict = Omit<Edict, '_tokens'>;

export interface EdictFileSchema {
  version: number;
  config: {
    maxEdicts: number;
    tokenBudget: number;
    categories: string[];
    staleThresholdDays?: number;
    categoryLimits?: Record<string, number>;
    defaultCategoryLimit?: number;
    defaultEphemeralTtlSeconds?: number;
  };
  edicts: StoredEdict[];
  history: HistoryEntry[];
}
