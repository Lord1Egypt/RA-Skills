/** Get utility score for a memory ID (default 0.5). */
export declare function getUtilityScore(id: string): number;
/** Fast BM25 pre-filter via FTS5. Falls back to keyword matching if FTS5 unavailable. */
export declare function searchChunksFTS(query: string, limit?: number): Promise<any[]>;
/** Check for duplicate content. Returns chunks with high text overlap. */
export declare function findSimilarChunks(text: string, limit?: number): Promise<any[]>;
/** One-time schema check — read-only, no writes to main.sqlite. */
export declare function ensureUtilityColumn(): Promise<void>;
/** Update utility score in the sidecar file. Validates the ID exists in main.sqlite first. */
export declare function rewardMemory(id: string, scalar?: number): Promise<boolean>;
/** Query chunks table — read-only from main.sqlite, enriched with sidecar scores. */
export declare function queryChunks(limit?: number): Promise<any[]>;
