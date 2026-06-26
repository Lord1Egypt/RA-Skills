/**
 * Muninn Budget Retrieval System
 * 
 * Token-aware memory retrieval with profile injection.
 * Inspired by Supermemory's profile-first approach.
 * 
 * https://supermemory.ai/docs/concepts/user-profiles
 */

import { Database } from 'better-sqlite3';
import { buildProfile, formatProfile, UserProfile } from '../profile/index.js';

export interface BudgetOptions {
  maxTokens: number;          // Total token budget
  profileRatio?: number;     // Ratio for profile (default: 0.2 = 20%)
  includeProfile?: boolean;  // Include profile (default: true)
  includeMemories?: boolean;  // Include memories (default: true)
  userId?: string;
}

export interface BudgetResult {
  profile?: {
    static: string[];
    dynamic: string[];
    formatted: string;
    tokenCount: number;
  };
  memories: string[];
  tokensUsed: number;
  tokensRemaining: number;
}

/**
 * Estimate token count (roughly 4 chars per token)
 */
function estimateTokens(text: string): number {
  return Math.ceil(text.length / 4);
}

/**
 * Estimate tokens for memory array
 */
function estimateMemoryTokens(memories: any[]): number {
  return memories.reduce((sum, m) => {
    const content = typeof m === 'string' ? m : (m.content || '');
    return sum + estimateTokens(content);
  }, 0);
}

/**
 * Select memories within token budget
 */
function selectMemoriesWithinBudget(
  memories: any[],
  maxTokens: number
): any[] {
  const selected: any[] = [];
  let tokens = 0;
  
  // Sort by relevance (assuming already sorted by caller)
  for (const memory of memories) {
    const content = typeof memory === 'string' ? memory : (memory.content || '');
    const memTokens = estimateTokens(content);
    
    if (tokens + memTokens <= maxTokens) {
      selected.push(memory);
      tokens += memTokens;
    }
  }
  
  return selected;
}

/**
 * Format memories for context
 */
function formatMemories(memories: any[]): string {
  return memories.map((m, i) => {
    const content = typeof m === 'string' ? m : (m.content || '');
    return `${i + 1}. ${content}`;
  }).join('\n');
}

/**
 * Retrieve with token budget
 * 
 * This is the main entry point for budget-aware retrieval.
 * Returns profile + memories within token budget.
 */
export async function retrieveWithBudget(
  db: Database,
  query: string,
  options: BudgetOptions
): Promise<BudgetResult> {
  const {
    maxTokens,
    profileRatio = 0.2,
    includeProfile = true,
    includeMemories = true,
    userId = 'default'
  } = options;
  
  let tokensUsed = 0;
  let profileData: BudgetResult['profile'] = undefined;
  
  // 1. Build profile (cheap, high value)
  if (includeProfile) {
    const profile = await buildProfile(db, { userId });
    const formatted = formatProfile(profile);
    const profileTokens = estimateTokens(formatted);
    
    // Check if profile fits within budget
    if (profileTokens <= maxTokens * profileRatio) {
      profileData = {
        static: profile.static,
        dynamic: profile.dynamic,
        formatted,
        tokenCount: profileTokens
      };
      tokensUsed += profileTokens;
    }
  }
  
  // 2. Calculate remaining budget for memories
  const memoryBudget = maxTokens - tokensUsed - 50; // 50 token buffer
  
  // 3. Retrieve memories
  let memories: any[] = [];
  
  if (includeMemories && memoryBudget > 0) {
    // Query relevant memories (simplified - should use hybrid search)
    const rows = db.prepare(`
      SELECT 
        e.name AS entity_name,
        f.predicate,
        f.object_value,
        f.strength,
        f.created_at
      FROM facts f
      JOIN entities e ON f.subject_entity_id = e.id
      WHERE f.invalidated_at IS NULL
        AND f.valid_until IS NULL
      ORDER BY f.strength DESC, f.created_at DESC
      LIMIT 100
    `).all() as any[];
    
    // Format for selection
    memories = rows.map(row => {
      return `${row.entity_name} ${row.predicate} ${row.object_value || ''}`;
    }).filter(c => c && c.length > 0);
    
    // Filter by query relevance (simple keyword match)
    const queryLower = query.toLowerCase();
    const queryWords = queryLower.split(/\s+/);
    
    memories = memories.sort((a, b) => {
      const aMatches = queryWords.filter(w => a.toLowerCase().includes(w)).length;
      const bMatches = queryWords.filter(w => b.toLowerCase().includes(w)).length;
      return bMatches - aMatches;
    });
    
    // Select within budget
    memories = selectMemoriesWithinBudget(memories, memoryBudget);
    tokensUsed += estimateMemoryTokens(memories);
  }
  
  return {
    profile: profileData,
    memories: memories.map(m => typeof m === 'string' ? m : (m.content || m)),
    tokensUsed,
    tokensRemaining: maxTokens - tokensUsed
  };
}

/**
 * Retrieve with hybrid search + budget
 * Uses vector similarity when available
 */
export async function retrieveWithHybridSearch(
  db: Database,
  query: string,
  options: BudgetOptions & { embedding?: number[] }
): Promise<BudgetResult> {
  // For now, fall back to basic retrieval
  // In production, this would use vector similarity
  return retrieveWithBudget(db, query, options);
}

/**
 * Format result for LLM context
 */
export function formatForContext(result: BudgetResult): string {
  const parts: string[] = [];
  
  if (result.profile) {
    parts.push(result.profile.formatted);
    parts.push('');
  }
  
  if (result.memories.length > 0) {
    parts.push('## Relevant Memories');
    parts.push('');
    parts.push(formatMemories(result.memories));
  }
  
  parts.push('');
  parts.push(`(${result.tokensUsed} tokens used, ${result.tokensRemaining} remaining)`);
  
  return parts.join('\n');
}

/**
 * Budget-aware memory briefing
 * Replaces memory_briefing with token-aware version
 */
export async function memoryBriefingWithBudget(
  db: Database,
  context: string,
  maxTokens: number = 500
): Promise<string> {
  const result = await retrieveWithBudget(db, context, {
    maxTokens,
    includeProfile: true,
    includeMemories: true
  });
  
  return formatForContext(result);
}

/**
 * Quick profile retrieval
 * Just the profile, no memories (for fast context)
 */
export async function getQuickProfile(
  db: Database,
  userId: string = 'default'
): Promise<string> {
  const profile = await buildProfile(db, { userId, maxStaticFacts: 10 });
  return formatProfile(profile);
}

export default {
  retrieveWithBudget,
  retrieveWithHybridSearch,
  formatForContext,
  memoryBriefingWithBudget,
  getQuickProfile,
  estimateTokens
};