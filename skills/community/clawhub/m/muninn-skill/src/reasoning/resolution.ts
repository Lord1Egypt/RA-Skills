/**
 * Muninn Memory Contradiction Resolution
 * Phase 3: Auto-Resolution Strategies
 * 
 * Provides:
 * - Auto-resolution strategies (keep both, prefer recent, prefer confirmed)
 * - Resolution decision logic
 * - Integration with staleness detection
 */

import { ContradictionStore, MemoryContradiction, ResolutionStrategy } from './memory-contradiction.js';
import { calculateStaleness, StalenessInfo } from '../storage/audit.js';

export type ResolutionDecision = {
  strategy: ResolutionStrategy;
  winning_memory_id: string;
  losing_memory_id: string;
  confidence: number;
  reasoning: string;
};

/**
 * Resolve contradictions automatically based on configured strategy
 */
export class ContradictionResolver {
  private store: ContradictionStore;
  private defaultStrategy: ResolutionStrategy;
  
  constructor(
    store: ContradictionStore,
    defaultStrategy: ResolutionStrategy = 'prefer_recent'
  ) {
    this.store = store;
    this.defaultStrategy = defaultStrategy;
  }
  
  /**
   * Resolve a contradiction using the specified strategy
   */
  async resolve(
    contradiction: MemoryContradiction,
    strategy?: ResolutionStrategy,
    getMemoryInfo?: (id: string) => { created_at: string; last_confirmed_at?: string; content: string }
  ): Promise<ResolutionDecision> {
    const useStrategy = strategy || this.defaultStrategy;
    
    let decision: ResolutionDecision;
    
    switch (useStrategy) {
      case 'keep_both':
        decision = await this.resolveKeepBoth(contradiction);
        break;
      case 'prefer_recent':
        decision = await this.resolvePreferRecent(contradiction, getMemoryInfo);
        break;
      case 'prefer_confirmed':
        decision = await this.resolvePreferConfirmed(contradiction, getMemoryInfo);
        break;
      case 'supersede':
        decision = await this.resolveSupersede(contradiction, getMemoryInfo);
        break;
      default:
        decision = await this.resolvePreferRecent(contradiction, getMemoryInfo);
    }
    
    // Apply the resolution
    this.store.resolveContradiction(
      contradiction.id,
      useStrategy,
      'system',
      decision.reasoning
    );
    
    return decision;
  }
  
  /**
   * Keep both memories - just flag for awareness
   */
  private async resolveKeepBoth(contradiction: MemoryContradiction): Promise<ResolutionDecision> {
    return {
      strategy: 'keep_both',
      winning_memory_id: contradiction.memory_a_id, // Neither wins
      losing_memory_id: '', // Neither loses
      confidence: 0.5,
      reasoning: 'Both memories retained - no resolution applied. Contradiction flagged for human review if needed.'
    };
  }
  
  /**
   * Prefer the more recent memory
   */
  private async resolvePreferRecent(
    contradiction: MemoryContradiction,
    getMemoryInfo?: (id: string) => { created_at: string; last_confirmed_at?: string; content: string }
  ): Promise<ResolutionDecision> {
    const memAInfo = getMemoryInfo ? getMemoryInfo(contradiction.memory_a_id) : null;
    const memBInfo = getMemoryInfo ? getMemoryInfo(contradiction.memory_b_id) : null;
    
    let winner: string;
    let loser: string;
    let reasoning: string;
    
    // If we have memory info, compare timestamps
    if (memAInfo && memBInfo) {
      const timeA = new Date(memAInfo.created_at).getTime();
      const timeB = new Date(memBInfo.created_at).getTime();
      
      if (timeA > timeB) {
        winner = contradiction.memory_a_id;
        loser = contradiction.memory_b_id;
        reasoning = `Memory A (created ${memAInfo.created_at}) is more recent than Memory B (created ${memBInfo.created_at})`;
      } else if (timeB > timeA) {
        winner = contradiction.memory_b_id;
        loser = contradiction.memory_a_id;
        reasoning = `Memory B (created ${memBInfo.created_at}) is more recent than Memory A (created ${memAInfo.created_at})`;
      } else {
        // Same timestamp - use contradiction score as tiebreaker
        winner = contradiction.memory_a_id;
        loser = contradiction.memory_b_id;
        reasoning = 'Same creation time, defaulting to first memory';
      }
    } else {
      // Fallback: use memory ID (assumes newer IDs are more recent)
      winner = contradiction.memory_a_id;
      loser = contradiction.memory_b_id;
      reasoning = 'No timestamp info available, defaulting to first memory';
    }
    
    return {
      strategy: 'prefer_recent',
      winning_memory_id: winner,
      losing_memory_id: loser,
      confidence: 0.7,
      reasoning
    };
  }
  
  /**
   * Prefer the confirmed memory (has been verified)
   */
  private async resolvePreferConfirmed(
    contradiction: MemoryContradiction,
    getMemoryInfo?: (id: string) => { created_at: string; last_confirmed_at?: string; content: string }
  ): Promise<ResolutionDecision> {
    const memAInfo = getMemoryInfo ? getMemoryInfo(contradiction.memory_a_id) : null;
    const memBInfo = getMemoryInfo ? getMemoryInfo(contradiction.memory_b_id) : null;
    
    let winner: string;
    let loser: string;
    let reasoning: string;
    
    if (memAInfo && memBInfo) {
      const hasConfirmationA = !!memAInfo.last_confirmed_at;
      const hasConfirmationB = !!memBInfo.last_confirmed_at;
      
      if (hasConfirmationA && !hasConfirmationB) {
        winner = contradiction.memory_a_id;
        loser = contradiction.memory_b_id;
        reasoning = 'Memory A has been confirmed, Memory B has not';
      } else if (hasConfirmationB && !hasConfirmationA) {
        winner = contradiction.memory_b_id;
        loser = contradiction.memory_a_id;
        reasoning = 'Memory B has been confirmed, Memory A has not';
      } else if (hasConfirmationA && hasConfirmationB) {
        // Both confirmed - use most recent confirmation
        const confirmA = new Date(memAInfo.last_confirmed_at!).getTime();
        const confirmB = new Date(memBInfo.last_confirmed_at!).getTime();
        
        if (confirmA > confirmB) {
          winner = contradiction.memory_a_id;
          loser = contradiction.memory_b_id;
          reasoning = 'Memory A was more recently confirmed';
        } else {
          winner = contradiction.memory_b_id;
          loser = contradiction.memory_a_id;
          reasoning = 'Memory B was more recently confirmed';
        }
      } else {
        // Neither confirmed - fall back to prefer recent
        return this.resolvePreferRecent(contradiction, getMemoryInfo);
      }
    } else {
      // Fall back to recent
      return this.resolvePreferRecent(contradiction, getMemoryInfo);
    }
    
    return {
      strategy: 'prefer_confirmed',
      winning_memory_id: winner,
      losing_memory_id: loser,
      confidence: 0.8,
      reasoning
    };
  }
  
  /**
   * Supersede - mark the older memory as invalidated
   */
  private async resolveSupersede(
    contradiction: MemoryContradiction,
    getMemoryInfo?: (id: string) => { created_at: string; content: string }
  ): Promise<ResolutionDecision> {
    // Supersede is like prefer_recent but with stronger resolution
    // and marks the losing memory as invalidated
    const decision = await this.resolvePreferRecent(contradiction, getMemoryInfo);
    
    return {
      strategy: 'supersede',
      winning_memory_id: decision.winning_memory_id,
      losing_memory_id: decision.losing_memory_id,
      confidence: decision.confidence + 0.1,
      reasoning: decision.reasoning + '. Older memory marked as superseded.'
    };
  }
  
  /**
   * Batch resolve multiple contradictions
   */
  async resolveBatch(
    contradictions: MemoryContradiction[],
    strategy?: ResolutionStrategy,
    getMemoryInfo?: (id: string) => { created_at: string; last_confirmed_at?: string; content: string }
  ): Promise<ResolutionDecision[]> {
    const results: ResolutionDecision[] = [];
    
    for (const contradiction of contradictions) {
      const decision = await this.resolve(contradiction, strategy, getMemoryInfo);
      results.push(decision);
    }
    
    return results;
  }
}

// =============================================================================
// RESOLUTION POLICY HELPERS
// =============================================================================

/**
 * Determine best resolution strategy based on context
 */
export function determineBestStrategy(
  contradiction: MemoryContradiction,
  options: {
    autoResolveEnabled: boolean;
    highStalenessThreshold: number;
    getStaleness?: (memoryId: string) => StalenessInfo;
  }
): ResolutionStrategy | null {
  if (!options.autoResolveEnabled) {
    return null; // Don't auto-resolve
  }
  
  // Get staleness if available
  const stalenessA = options.getStaleness?.(contradiction.memory_a_id);
  const stalenessB = options.getStaleness?.(contradiction.memory_b_id);
  
  // If either memory is very stale, prefer the other one
  if (stalenessA && stalenessA.staleness_score >= options.highStalenessThreshold) {
    return 'prefer_recent';
  }
  
  if (stalenessB && stalenessB.staleness_score >= options.highStalenessThreshold) {
    return 'prefer_recent';
  }
  
  // High confidence contradictions should be resolved
  if (contradiction.contradiction_score >= 0.8) {
    return 'prefer_recent';
  }
  
  // Medium confidence - mark for review instead of auto-resolve
  if (contradiction.contradiction_score >= 0.6 && contradiction.contradiction_score < 0.8) {
    return null; // Don't auto-resolve medium confidence
  }
  
  // Low confidence - keep both
  return 'keep_both';
}

/**
 * Generate a resolution report
 */
export function generateResolutionReport(
  resolutions: ResolutionDecision[]
): {
  total: number;
  by_strategy: Record<ResolutionStrategy, number>;
  avg_confidence: number;
  recommendations: string[];
} {
  const byStrategy: Record<ResolutionStrategy, number> = {
    keep_both: 0,
    prefer_recent: 0,
    prefer_confirmed: 0,
    supersede: 0
  };
  
  let totalConfidence = 0;
  
  for (const r of resolutions) {
    byStrategy[r.strategy]++;
    totalConfidence += r.confidence;
  }
  
  const recommendations: string[] = [];
  
  if (byStrategy.keep_both > resolutions.length * 0.3) {
    recommendations.push('Many contradictions kept unresolved - consider reviewing threshold settings');
  }
  
  if (byStrategy.supersede > 0) {
    recommendations.push('Some memories were marked as superseded - verify invalid_at was updated');
  }
  
  const avgConfidence = resolutions.length > 0 ? totalConfidence / resolutions.length : 0;
  if (avgConfidence < 0.6) {
    recommendations.push('Low average confidence - consider raising resolution threshold');
  }
  
  return {
    total: resolutions.length,
    by_strategy: byStrategy,
    avg_confidence: avgConfidence,
    recommendations
  };
}