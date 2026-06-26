/**
 * Eviction Policy
 * Determines which items to evict when context needs to be freed
 */
import type { EvictionCandidate, EvictionPolicy, SummarizableItem } from './types.js';
export declare class EvictionPolicyEngine {
    private policy;
    constructor(policy?: Partial<EvictionPolicy>);
    /**
     * Calculate eviction score for an item
     * Lower score = more likely to evict
     */
    calculateScore(item: SummarizableItem, position: number, totalItems: number): number;
    /**
     * Score all items and return eviction candidates sorted by score
     */
    scoreItems(items: SummarizableItem[]): EvictionCandidate[];
    /**
     * Select items to evict to achieve target reduction
     */
    selectForEviction(items: SummarizableItem[], targetReduction: number): SummarizableItem[];
    /**
     * Get current policy
     */
    getPolicy(): EvictionPolicy;
    /**
     * Update policy
     */
    updatePolicy(policy: Partial<EvictionPolicy>): void;
}
//# sourceMappingURL=eviction-policy.d.ts.map