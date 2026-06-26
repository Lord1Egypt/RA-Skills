/**
 * Memory Prioritizer
 * Manages memory entry priorities and retention policies
 */
import { MemoryPriority, RETENTION_PERIODS, } from './memory-types.js';
// Priority weight for conflict resolution
const PRIORITY_WEIGHTS = {
    [MemoryPriority.P0_CRITICAL]: 1000,
    [MemoryPriority.P1_CONTEXT]: 100,
    [MemoryPriority.P2_SUMMARY]: 10,
    [MemoryPriority.P3_TEMPORARY]: 1,
};
export class MemoryPrioritizer {
    /**
     * Calculate expiration time based on priority
     */
    static calculateExpiresAt(priority) {
        const period = RETENTION_PERIODS[priority];
        if (period === null)
            return null;
        return Date.now() + period;
    }
    /**
     * Check if a memory entry has expired
     */
    static isExpired(entry) {
        if (entry.expiresAt === null)
            return false;
        return Date.now() > entry.expiresAt;
    }
    /**
     * Filter out expired entries
     */
    static filterExpired(entries) {
        return entries.filter(e => !this.isExpired(e));
    }
    /**
     * Sort entries by priority (ascending = P0 first)
     */
    static sortByPriority(entries) {
        return [...entries].sort((a, b) => a.priority - b.priority);
    }
    /**
     * Resolve conflict between two entries using priority + recency
     */
    static resolveConflict(existing, incoming) {
        // P0 always wins over non-P0
        if (existing.priority === MemoryPriority.P0_CRITICAL && existing.priority !== incoming.priority) {
            return existing;
        }
        if (incoming.priority === MemoryPriority.P0_CRITICAL && existing.priority !== incoming.priority) {
            return incoming;
        }
        // Same priority: latest wins
        if (existing.priority === incoming.priority) {
            return incoming.updatedAt > existing.updatedAt ? incoming : existing;
        }
        // Different priorities: higher priority wins
        return existing.priority < incoming.priority ? existing : incoming;
    }
    /**
     * Calculate conflict resolution score
     * Used when merging multiple entries
     */
    static calculateScore(entry) {
        const age = Date.now() - entry.updatedAt;
        const ageFactor = Math.max(0, 1 - age / (7 * 24 * 60 * 60 * 1000)); // Decay over 7 days
        return PRIORITY_WEIGHTS[entry.priority] * (1 + ageFactor);
    }
    /**
     * Determine if an entry should be archived to global memory
     */
    static shouldArchiveToGlobal(entry) {
        // P0 and P1 should be archived
        return entry.priority <= MemoryPriority.P1_CONTEXT && !entry.archived;
    }
    /**
     * Determine if an entry should be saved to session memory
     */
    static shouldSaveToSession(entry) {
        // All entries except P3 (temporary) should be saved to session
        return entry.priority < MemoryPriority.P3_TEMPORARY;
    }
    /**
     * Classify a memory entry by analyzing its content
     */
    static classifyEntry(key, value) {
        const keyLower = key.toLowerCase();
        const valueStr = JSON.stringify(value).toLowerCase();
        // P0: Critical decision keywords
        const criticalKeywords = ['decision', 'approved', 'rejected', 'commit', 'cancel', 'delete', 'permanent'];
        if (criticalKeywords.some(k => keyLower.includes(k))) {
            return MemoryPriority.P0_CRITICAL;
        }
        // P1: Project context keywords
        const contextKeywords = ['project', 'context', 'milestone', 'task', 'roadmap', 'team', 'goal'];
        if (contextKeywords.some(k => keyLower.includes(k))) {
            return MemoryPriority.P1_CONTEXT;
        }
        // P2: Summary keywords
        const summaryKeywords = ['summary', 'result', 'output', 'response', 'conclusion'];
        if (summaryKeywords.some(k => keyLower.includes(k))) {
            return MemoryPriority.P2_SUMMARY;
        }
        // P3: Temporary state keywords
        const tempKeywords = ['temp', 'cache', 'draft', 'pending', 'processing', 'loading'];
        if (tempKeywords.some(k => keyLower.includes(k))) {
            return MemoryPriority.P3_TEMPORARY;
        }
        // Default to P2 for unknown entries
        return MemoryPriority.P2_SUMMARY;
    }
    /**
     * Clean up old entries beyond retention
     */
    static cleanup(entries, maxAge) {
        const now = Date.now();
        return entries.filter(e => {
            // Never expire P0
            if (e.priority === MemoryPriority.P0_CRITICAL)
                return true;
            // Apply max age if specified
            if (maxAge && now - e.updatedAt > maxAge)
                return false;
            // Apply priority-based expiration
            if (e.expiresAt !== null && now > e.expiresAt)
                return false;
            return true;
        });
    }
}
//# sourceMappingURL=prioritizer.js.map