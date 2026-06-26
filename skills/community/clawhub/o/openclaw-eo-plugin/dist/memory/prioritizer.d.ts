/**
 * Memory Prioritizer
 * Manages memory entry priorities and retention policies
 */
import { MemoryPriority, type MemoryEntry, type SessionMemoryEntry } from './memory-types.js';
export declare class MemoryPrioritizer {
    /**
     * Calculate expiration time based on priority
     */
    static calculateExpiresAt(priority: MemoryPriority): number | null;
    /**
     * Check if a memory entry has expired
     */
    static isExpired(entry: MemoryEntry): boolean;
    /**
     * Filter out expired entries
     */
    static filterExpired<T extends MemoryEntry>(entries: T[]): T[];
    /**
     * Sort entries by priority (ascending = P0 first)
     */
    static sortByPriority<T extends MemoryEntry>(entries: T[]): T[];
    /**
     * Resolve conflict between two entries using priority + recency
     */
    static resolveConflict<T extends MemoryEntry>(existing: T, incoming: T): T;
    /**
     * Calculate conflict resolution score
     * Used when merging multiple entries
     */
    static calculateScore(entry: MemoryEntry): number;
    /**
     * Determine if an entry should be archived to global memory
     */
    static shouldArchiveToGlobal(entry: SessionMemoryEntry): boolean;
    /**
     * Determine if an entry should be saved to session memory
     */
    static shouldSaveToSession(entry: MemoryEntry): boolean;
    /**
     * Classify a memory entry by analyzing its content
     */
    static classifyEntry(key: string, value: unknown): MemoryPriority;
    /**
     * Clean up old entries beyond retention
     */
    static cleanup<T extends MemoryEntry>(entries: T[], maxAge?: number): T[];
}
//# sourceMappingURL=prioritizer.d.ts.map