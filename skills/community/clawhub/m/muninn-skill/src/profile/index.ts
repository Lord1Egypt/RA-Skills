/**
 * Muninn Profile Abstraction
 * 
 * Builds static + dynamic profiles from memory, similar to Supermemory.
 * Static: Long-term facts (preferences, skills, roles)
 * Dynamic: Recent context (current projects, recent activity)
 * 
 * Inspired by Supermemory's profile approach:
 * https://supermemory.ai/docs/concepts/user-profiles
 */

import { Database } from 'better-sqlite3';

export interface UserProfile {
  static: string[];   // Long-term facts
  dynamic: string[];  // Recent context
  tokenCount: number;
}

export interface ProfileOptions {
  maxStaticFacts?: number;   // Default: 10
  maxDynamicFacts?: number;   // Default: 5
  maxTokenBudget?: number;    // Default: 200 tokens
  userId?: string;
}

// Token estimation (roughly 4 chars per token)
function estimateTokens(text: string): number {
  return Math.ceil(text.length / 4);
}

// Deduplicate similar facts
function deduplicateFacts(facts: string[]): string[] {
  const seen = new Set<string>();
  const unique: string[] = [];
  
  for (const fact of facts) {
    // Normalize for comparison
    const normalized = fact.toLowerCase().trim();
    
    // Check if similar fact exists
    let isDupe = false;
    for (const existing of seen) {
      if (existing.includes(normalized) || normalized.includes(existing)) {
        isDupe = true;
        break;
      }
    }
    
    if (!isDupe) {
      seen.add(normalized);
      unique.push(fact);
    }
  }
  
  return unique;
}

// Format fact for profile
function formatFact(row: {
  entity_name?: string;
  entity_type?: string;
  summary?: string;
  predicate?: string;
  object_value?: string;
  name?: string;
  type?: string;
}): string {
  if (row.predicate && row.object_value) {
    return `${row.entity_name || 'User'} ${row.predicate} ${row.object_value}`;
  }
  if (row.summary) {
    return row.summary;
  }
  if (row.name && row.type) {
    return `${row.name} (${row.type})`;
  }
  return '';
}

/**
 * Build static profile from long-term facts
 */
async function buildStaticProfile(
  db: Database,
  userId: string,
  maxFacts: number
): Promise<string[]> {
  const facts: string[] = [];
  
  // Query entities that represent long-term facts
  // Preferences, skills, roles have high strength
  const staticEntities = db.prepare(`
    SELECT 
      e.name,
      e.type,
      e.summary,
      f.predicate,
      f.object_value,
      f.strength,
      f.memory_type
    FROM entities e
    JOIN facts f ON f.subject_entity_id = e.id
    WHERE f.invalidated_at IS NULL
      AND f.valid_until IS NULL
      AND f.memory_type IN ('fact', 'preference')
      AND f.strength >= 0.5
    ORDER BY f.strength DESC, f.created_at DESC
    LIMIT ?
  `).all(maxFacts) as any[];
  
  for (const row of staticEntities) {
    const fact = formatFact(row);
    if (fact) {
      facts.push(fact);
    }
  }
  
  // Also include high-confidence entity summaries
  const entities = db.prepare(`
    SELECT name, type, summary
    FROM entities
    WHERE summary IS NOT NULL
      AND type IN ('person', 'org', 'project', 'skill')
    ORDER BY updated_at DESC
    LIMIT ?
  `).all(Math.floor(maxFacts / 2)) as any[];
  
  for (const row of entities) {
    const fact = `${row.name}: ${row.summary}`;
    facts.push(fact);
  }
  
  return deduplicateFacts(facts).slice(0, maxFacts);
}

/**
 * Build dynamic profile from recent activity
 */
async function buildDynamicProfile(
  db: Database,
  userId: string,
  maxFacts: number
): Promise<string[]> {
  const facts: string[] = [];
  
  // Query recent episodes and facts (last 30 days)
  const recentFacts = db.prepare(`
    SELECT 
      e.name AS entity_name,
      e.type AS entity_type,
      f.predicate,
      f.object_value,
      f.created_at,
      f.memory_type
    FROM facts f
    JOIN entities e ON f.subject_entity_id = e.id
    WHERE f.invalidated_at IS NULL
      AND f.valid_until IS NULL
      AND datetime(f.created_at) > datetime('now', '-30 days')
    ORDER BY f.created_at DESC
    LIMIT ?
  `).all(maxFacts) as any[];
  
  for (const row of recentFacts) {
    const fact = formatFact(row);
    if (fact) {
      facts.push(fact);
    }
  }
  
  // Also include recent episodes
  const recentEpisodes = db.prepare(`
    SELECT content, occurred_at
    FROM episodes
    WHERE datetime(occurred_at) > datetime('now', '-7 days')
    ORDER BY occurred_at DESC
    LIMIT ?
  `).all(Math.floor(maxFacts / 2)) as any[];
  
  for (const row of recentEpisodes) {
    // Extract key point from episode (first sentence, max 100 chars)
    const content = row.content;
    const firstSentence = content.split(/[.!?]/)[0]?.substring(0, 100);
    if (firstSentence) {
      facts.push(firstSentence.trim());
    }
  }
  
  return deduplicateFacts(facts).slice(0, maxFacts);
}

/**
 * Build complete user profile
 */
export async function buildProfile(
  db: Database,
  options: ProfileOptions = {}
): Promise<UserProfile> {
  const {
    maxStaticFacts = 10,
    maxDynamicFacts = 5,
    userId = 'default'
  } = options;
  
  const staticFacts = await buildStaticProfile(db, userId, maxStaticFacts);
  const dynamicFacts = await buildDynamicProfile(db, userId, maxDynamicFacts);
  
  const allText = [...staticFacts, ...dynamicFacts].join(' ');
  const tokenCount = estimateTokens(allText);
  
  return {
    static: staticFacts,
    dynamic: dynamicFacts,
    tokenCount
  };
}

/**
 * Format profile for system prompt injection
 */
export function formatProfile(profile: UserProfile): string {
  const lines: string[] = [];
  
  if (profile.static.length > 0) {
    lines.push('## About the User');
    lines.push('');
    for (const fact of profile.static) {
      lines.push(`- ${fact}`);
    }
    lines.push('');
  }
  
  if (profile.dynamic.length > 0) {
    lines.push('## Recent Context');
    lines.push('');
    for (const fact of profile.dynamic) {
      lines.push(`- ${fact}`);
    }
  }
  
  return lines.join('\n');
}

/**
 * Cache profile in database
 */
export async function cacheProfile(
  db: Database,
  userId: string,
  profile: UserProfile
): Promise<void> {
  // Cache static profile
  db.prepare(`
    INSERT OR REPLACE INTO profiles (id, user_id, profile_type, facts, token_count, updated_at)
    VALUES (?, ?, 'static', ?, ?, datetime('now'))
  `).run(
    `${userId}_static`,
    userId,
    JSON.stringify(profile.static),
    profile.tokenCount
  );
  
  // Cache dynamic profile
  db.prepare(`
    INSERT OR REPLACE INTO profiles (id, user_id, profile_type, facts, token_count, updated_at)
    VALUES (?, ?, 'dynamic', ?, ?, datetime('now'))
  `).run(
    `${userId}_dynamic`,
    userId,
    JSON.stringify(profile.dynamic),
    profile.tokenCount
  );
}

/**
 * Get cached profile from database
 */
export async function getCachedProfile(
  db: Database,
  userId: string
): Promise<UserProfile | null> {
  const staticRow = db.prepare(`
    SELECT facts, token_count
    FROM profiles
    WHERE user_id = ? AND profile_type = 'static'
    ORDER BY updated_at DESC
    LIMIT 1
  `).get(userId) as any;
  
  const dynamicRow = db.prepare(`
    SELECT facts, token_count
    FROM profiles
    WHERE user_id = ? AND profile_type = 'dynamic'
    ORDER BY updated_at DESC
    LIMIT 1
  `).get(userId) as any;
  
  if (!staticRow && !dynamicRow) {
    return null;
  }
  
  return {
    static: staticRow ? JSON.parse(staticRow.facts) : [],
    dynamic: dynamicRow ? JSON.parse(dynamicRow.facts) : [],
    tokenCount: (staticRow?.token_count || 0) + (dynamicRow?.token_count || 0)
  };
}

/**
 * Get profile (from cache or build fresh)
 */
export async function getProfile(
  db: Database,
  options: ProfileOptions = {}
): Promise<UserProfile> {
  const { userId = 'default' } = options;
  
  // Try cache first (refresh if older than 1 day)
  const cached = await getCachedProfile(db, userId);
  
  if (cached) {
    // Check if cache is fresh (less than 1 day old)
    const staticRow = db.prepare(`
      SELECT updated_at FROM profiles
      WHERE user_id = ? AND profile_type = 'static'
    `).get(userId) as any;
    
    if (staticRow) {
      const updatedAt = new Date(staticRow.updated_at);
      const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
      
      if (updatedAt > oneDayAgo) {
        return cached;
      }
    }
  }
  
  // Build fresh profile
  const profile = await buildProfile(db, options);
  
  // Cache it
  await cacheProfile(db, userId, profile);
  
  return profile;
}

export default {
  buildProfile,
  formatProfile,
  getProfile,
  cacheProfile,
  getCachedProfile
};