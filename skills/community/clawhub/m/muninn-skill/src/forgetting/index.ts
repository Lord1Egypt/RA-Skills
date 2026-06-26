/**
 * Muninn Auto-Forgetting System
 * 
 * Handles temporal fact expiration and memory decay.
 * Inspired by Supermemory's automatic forgetting.
 * 
 * https://supermemory.ai/docs/concepts/graph-memory
 */

import { Database } from 'better-sqlite3';

export interface TemporalFact {
  id: string;
  content: string;
  expires_at: Date | null;
  memory_type: 'fact' | 'preference' | 'episode';
  strength: number;
}

export interface ForgettingResult {
  expired: number;
  decayed: number;
  totalForgotten: number;
}

/**
 * Temporal patterns for auto-expiration detection
 */
const TEMPORAL_PATTERNS = [
  { pattern: /exam\s+(tomorrow|next\s+week|on\s+\d+)/i, expiry: 'relative' },
  { pattern: /meeting\s+(today|tomorrow|next\s+\w+)/i, expiry: 'event' },
  { pattern: /deadline\s+(is|on)\s+\d+/i, expiry: 'event' },
  { pattern: /flight\s+(on|at)\s+\d+/i, expiry: 'event' },
  { pattern: /traveling\s+(this\s+week|next\s+week)/i, expiry: 'relative' },
  { pattern: /vacation\s+(this\s+week|next\s+week)/i, expiry: 'relative' },
  { pattern: /in\s+\w+\s+(today|tomorrow|this\s+week)/i, expiry: 'relative' },
  { pattern: /(today|tomorrow|this\s+week|next\s+week)\s*$/i, expiry: 'relative' },
];

/**
 * Parse relative temporal expressions
 */
function parseTemporalExpression(expression: string): Date | null {
  const now = new Date();
  const lower = expression.toLowerCase();
  
  // Today
  if (lower === 'today') {
    const eod = new Date(now);
    eod.setHours(23, 59, 59, 999);
    return eod;
  }
  
  // Tomorrow
  if (lower === 'tomorrow') {
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(23, 59, 59, 999);
    return tomorrow;
  }
  
  // This week
  if (lower === 'this week') {
    const eow = new Date(now);
    // End of Sunday
    const daysUntilSunday = 7 - eow.getDay();
    eow.setDate(eow.getDate() + daysUntilSunday);
    eow.setHours(23, 59, 59, 999);
    return eow;
  }
  
  // Next week
  if (lower === 'next week') {
    const nextWeek = new Date(now);
    nextWeek.setDate(nextWeek.getDate() + 7);
    nextWeek.setHours(23, 59, 59, 999);
    return nextWeek;
  }
  
  // Next month
  if (lower === 'next month') {
    const nextMonth = new Date(now);
    nextMonth.setMonth(nextMonth.getMonth() + 1);
    return nextMonth;
  }
  
  return null;
}

/**
 * Detect if content contains temporal fact that should expire
 */
export function detectTemporalFact(content: string): Date | null {
  for (const { pattern, expiry } of TEMPORAL_PATTERNS) {
    const match = content.match(pattern);
    if (match) {
      if (expiry === 'relative') {
        return parseTemporalExpression(match[1] || match[0]);
      }
      // For 'event' type, try to parse the matched text
      return parseTemporalExpression(match[1] || match[0]);
    }
  }
  return null;
}

/**
 * Classify memory type from content
 */
export function classifyMemoryType(content: string): 'fact' | 'preference' | 'episode' {
  const lower = content.toLowerCase();
  
  // Preferences: "I prefer", "I like", "I use"
  if (/i\s+(prefer|like|use|always|never|usually)/i.test(content)) {
    return 'preference';
  }
  
  // Episodes: past tense, events, meetings
  if (/^(yesterday|last\s+\w+|earlier|this\s+morning)/i.test(content)) {
    return 'episode';
  }
  if (/(met|went|had|attended|happened)/i.test(content)) {
    return 'episode';
  }
  
  // Temporal markers indicate episode
  if (detectTemporalFact(content)) {
    return 'episode';
  }
  
  // Default to fact
  return 'fact';
}

/**
 * Forget expired facts
 */
export async function forgetExpired(db: Database): Promise<number> {
  const now = new Date().toISOString();
  
  const result = db.prepare(`
    DELETE FROM facts
    WHERE expires_at IS NOT NULL 
      AND expires_at < ?
      AND memory_type = 'episode'
    RETURNING id
  `).run(now);
  
  return result.changes;
}

/**
 * Decay old episodes
 * Reduce strength of episodic memories older than 30 days
 */
export async function decayEpisodes(db: Database): Promise<number> {
  const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString();
  
  // Decay strength by 10%
  db.prepare(`
    UPDATE facts
    SET strength = strength * 0.9
    WHERE memory_type = 'episode'
      AND created_at < ?
      AND strength > 0.1
  `).run(thirtyDaysAgo);
  
  // Delete if strength drops below threshold
  const result = db.prepare(`
    DELETE FROM facts
    WHERE memory_type = 'episode'
      AND strength < 0.1
    RETURNING id
  `).run();
  
  return result.changes;
}

/**
 * Strengthen preference with repetition
 */
export async function strengthenPreference(
  db: Database,
  factId: string
): Promise<void> {
  db.prepare(`
    UPDATE facts
    SET strength = MIN(strength + 0.1, 1.0),
        repetition_count = repetition_count + 1
    WHERE id = ? AND memory_type = 'preference'
  `).run(factId);
}

/**
 * Run full forgetting cycle
 * Called during sleep cycle
 */
export async function runForgettingCycle(db: Database): Promise<ForgettingResult> {
  const expired = await forgetExpired(db);
  const decayed = await decayEpisodes(db);
  
  return {
    expired,
    decayed,
    totalForgotten: expired + decayed
  };
}

/**
 * Set expiration on temporal fact
 */
export async function setFactExpiration(
  db: Database,
  factId: string,
  expiresAt: Date
): Promise<void> {
  db.prepare(`
    UPDATE facts
    SET expires_at = ?,
        memory_type = 'episode'
    WHERE id = ?
  `).run(expiresAt.toISOString(), factId);
}

/**
 * Get facts expiring soon (for debugging)
 */
export async function getExpiringFacts(
  db: Database,
  withinDays: number = 7
): Promise<TemporalFact[]> {
  const cutoff = new Date(Date.now() + withinDays * 24 * 60 * 60 * 1000).toISOString();
  
  const rows = db.prepare(`
    SELECT 
      f.id,
      e.summary || ' ' || f.predicate || ' ' || COALESCE(f.object_value, '') as content,
      f.expires_at,
      f.memory_type,
      f.strength
    FROM facts f
    JOIN entities e ON f.subject_entity_id = e.id
    WHERE f.expires_at IS NOT NULL
      AND f.expires_at < ?
      AND f.invalidated_at IS NULL
    ORDER BY f.expires_at ASC
  `).all(cutoff) as any[];
  
  return rows.map(row => ({
    id: row.id,
    content: row.content,
    expires_at: row.expires_at ? new Date(row.expires_at) : null,
    memory_type: row.memory_type,
    strength: row.strength
  }));
}

/**
 * Initialize forgetting module
 */
export function initForgetting(db: Database): void {
  // Check if temporal_patterns table exists
  const tableExists = db.prepare(`
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name='temporal_patterns'
  `).get();
  
  if (!tableExists) {
    // Run migration
    console.log('Forgetting module: temporal_patterns table not found, skipping seed');
  }
}

export default {
  detectTemporalFact,
  classifyMemoryType,
  forgetExpired,
  decayEpisodes,
  strengthenPreference,
  runForgettingCycle,
  setFactExpiration,
  getExpiringFacts,
  initForgetting
};