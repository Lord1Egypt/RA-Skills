/**
 * Eviction Policy
 * Determines which items to evict when context needs to be freed
 */
import { DEFAULT_EVICTION_POLICY } from './types.js';
export class EvictionPolicyEngine {
    policy;
    constructor(policy = {}) {
        this.policy = { ...DEFAULT_EVICTION_POLICY, ...policy };
    }
    /**
     * Calculate eviction score for an item
     * Lower score = more likely to evict
     */
    calculateScore(item, position, totalItems) {
        let score = 100; // Start with max score
        // Importance factor (higher importance = higher score)
        score += item.importance;
        // Age factor (older = lower score, but not below 0)
        const ageMs = Date.now() - item.timestamp;
        const ageHours = ageMs / (1000 * 60 * 60);
        score -= ageHours * 5; // Lose 5 points per hour
        // Position factor (recent items get bonus)
        const recencyBonus = ((totalItems - position) / totalItems) * 20;
        score += recencyBonus;
        // Type factor (some types are more preservable)
        switch (item.type) {
            case 'message':
                score += 10;
                break;
            case 'tool_call':
                score += 5;
                break;
            case 'result':
                score += 15;
                break;
            case 'system':
                score -= 10;
                break;
        }
        // Never evict very high importance items
        if (item.importance >= 90) {
            score = Math.max(score, 95);
        }
        return Math.max(0, Math.min(100, score));
    }
    /**
     * Score all items and return eviction candidates sorted by score
     */
    scoreItems(items) {
        const totalItems = items.length;
        return items.map((item, index) => {
            const score = this.calculateScore(item, index, totalItems);
            let reason = '';
            if (item.importance < this.policy.minImportance) {
                reason = `Low importance (${item.importance} < ${this.policy.minImportance})`;
            }
            else if (Date.now() - item.timestamp > this.policy.maxAge) {
                reason = `Too old (>${this.policy.maxAge / 60000}min)`;
            }
            else if (item.type === 'system') {
                reason = 'System message (low value)';
            }
            else {
                reason = `General eviction (score: ${score.toFixed(1)})`;
            }
            return { item, score, reason };
        }).sort((a, b) => a.score - b.score); // Lowest score first = evict first
    }
    /**
     * Select items to evict to achieve target reduction
     */
    selectForEviction(items, targetReduction) {
        const preserveRecent = this.policy.preserveRecent;
        const candidates = this.scoreItems(items);
        // Don't evict recent items
        const preservableIndices = new Set(items.slice(-preserveRecent).map((_, i) => items.length - preserveRecent + i));
        const toEvict = [];
        let currentReduction = 0;
        const target = Math.ceil(items.length * targetReduction);
        for (const candidate of candidates) {
            const itemIndex = items.indexOf(candidate.item);
            if (preservableIndices.has(itemIndex))
                continue;
            toEvict.push(candidate.item);
            currentReduction++;
            if (currentReduction >= target)
                break;
        }
        return toEvict;
    }
    /**
     * Get current policy
     */
    getPolicy() {
        return { ...this.policy };
    }
    /**
     * Update policy
     */
    updatePolicy(policy) {
        this.policy = { ...this.policy, ...policy };
    }
}
//# sourceMappingURL=eviction-policy.js.map