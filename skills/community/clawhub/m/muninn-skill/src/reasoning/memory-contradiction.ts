/**
 * Muninn Memory Contradiction Detection
 * Phase 3: Contradiction Detection for Memory Content
 * 
 * Provides:
 * - Semantic similarity check for new memories vs existing
 * - Contradiction scoring (confidence that new memory contradicts old)
 * - Flagging system for human review
 * - Integration with existing relationship-based contradiction (reasoning/contradiction.ts)
 */

import { v4 as uuidv4 } from 'uuid';
import Database from 'better-sqlite3';
import crypto from 'crypto';

// Inline cosineSimilarity function (not exported from index.ts)
function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) return 0;
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  if (magA === 0 || magB === 0) return 0;
  return dotProduct / (magA * magB);
}

// Import generateEmbedding from storage for similarity calculations
let generateEmbeddingFn: ((text: string) => Promise<number[]>) | null = null;

function getEmbeddingFn(): (text: string) => Promise<number[]> {
  if (!generateEmbeddingFn) {
    // Dynamic import to avoid circular dependencies
    const storage = require('./storage/index.js');
    generateEmbeddingFn = storage.generateEmbedding;
  }
  return generateEmbeddingFn;
}

// Types for memory contradiction detection
export type ContradictionDetectionMethod = 'embedding' | 'rule' | 'llm';
export type ResolutionStatus = 'unresolved' | 'auto_resolved' | 'human_resolved' | 'ignored';
export type ResolutionStrategy = 'keep_both' | 'prefer_recent' | 'prefer_confirmed' | 'supersede';

export interface MemoryContradiction {
  id: string;
  memory_a_id: string;
  memory_b_id: string;
  entity: string;
  value_a: string;
  value_b: string;
  detection_method: ContradictionDetectionMethod;
  confidence: number;
  similarity_score: number;        // Semantic similarity (high = similar content)
  contradiction_score: number;     // How likely they contradict (0-1)
  resolution_status: ResolutionStatus;
  resolution_strategy?: ResolutionStrategy;
  resolved_at?: string;
  resolved_by?: string;
  resolution_note?: string;
  created_at: string;
}

export interface ContradictionCheckRequest {
  memory_id: string;
  content: string;
  entities: string[];
  threshold?: number;             // Similarity threshold for flagging (default: 0.85)
  max_comparisons?: number;        // Max existing memories to compare (default: 50)
}

export interface ContradictionCheckResult {
  has_contradiction: boolean;
  contradictions: Array<{
    existing_memory_id: string;
    similarity: number;
    contradiction_score: number;
    reason: string;
  }>;
  checked_count: number;
  flagged_for_review: boolean;
}

// =============================================================================
// SQL SCHEMA FOR MEMORY CONTRADICTIONS
// =============================================================================

export const CONTRADICTION_SQL_SCHEMA = `
-- Memory contradiction flags (content-based, not relationship-based)
CREATE TABLE IF NOT EXISTS memory_contradictions (
  id TEXT PRIMARY KEY,
  memory_a_id TEXT NOT NULL,
  memory_b_id TEXT NOT NULL,
  entity TEXT,
  value_a TEXT,
  value_b TEXT,
  detection_method TEXT NOT NULL,
  confidence REAL DEFAULT 0,
  similarity_score REAL DEFAULT 0,
  contradiction_score REAL DEFAULT 0,
  resolution_status TEXT DEFAULT 'unresolved',
  resolution_strategy TEXT,
  resolved_at TEXT,
  resolved_by TEXT,
  resolution_note TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_contradictions_memory_a ON memory_contradictions(memory_a_id);
CREATE INDEX IF NOT EXISTS idx_contradictions_memory_b ON memory_contradictions(memory_b_id);
CREATE INDEX IF NOT EXISTS idx_contradictions_entity ON memory_contradictions(entity);
CREATE INDEX IF NOT EXISTS idx_contradictions_status ON memory_contradictions(resolution_status);
CREATE INDEX IF NOT EXISTS idx_contradictions_created ON memory_contradictions(created_at DESC);

-- Contradiction review queue for human review
CREATE TABLE IF NOT EXISTS contradiction_review_queue (
  id TEXT PRIMARY KEY,
  contradiction_id TEXT NOT NULL,
  priority INTEGER DEFAULT 0,      -- Higher = more urgent
  assigned_to TEXT,
  review_note TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  reviewed_at TEXT,
  FOREIGN KEY (contradiction_id) REFERENCES memory_contradictions(id)
);

CREATE INDEX IF NOT EXISTS idx_review_queue_status ON contradiction_review_queue(reviewed_at);
`;

// Known contradiction patterns for rule-based detection
const CONTRADICTION_PATTERNS = [
  { positive: 'not', negative: 'is', score: 0.9 },
  { positive: 'never', negative: 'always', score: 0.8 },
  { positive: 'no', negative: 'yes', score: 0.85 },
  { positive: 'false', negative: 'true', score: 0.95 },
  { positive: 'cannot', negative: 'can', score: 0.8 },
  { positive: "doesn't", negative: 'does', score: 0.85 },
  { positive: "won't", negative: 'will', score: 0.85 },
  { positive: 'disabled', negative: 'enabled', score: 0.9 },
  { positive: 'off', negative: 'on', score: 0.75 },
  { positive: 'failed', negative: 'succeeded', score: 0.9 },
  { positive: 'negative', negative: 'positive', score: 0.85 },
  { positive: 'wrong', negative: 'right', score: 0.85 },
  { positive: 'bad', negative: 'good', score: 0.7 },
  { positive: 'impossible', negative: 'possible', score: 0.8 },
  { positive: 'declined', negative: 'increased', score: 0.75 },
  { positive: 'decreased', negative: 'increased', score: 0.8 },
];

// =============================================================================
// CONTRADICTION DETECTION STORE
// =============================================================================

export class ContradictionStore {
  private db: Database.Database;
  
  constructor(db: Database.Database) {
    this.db = db;
    this.initializeTables();
  }
  
  private initializeTables(): void {
    this.db.exec(CONTRADICTION_SQL_SCHEMA);
  }
  
  /**
   * Check if new memory content contradicts existing memories
   */
  async checkForContradictions(
    request: ContradictionCheckRequest,
    getExistingMemories: (limit: number) => Array<{ id: string; content: string; entities: string[]; created_at: string; last_confirmed_at?: string }>
  ): Promise<ContradictionCheckResult> {
    const threshold = request.threshold ?? 0.85;
    const maxComparisons = request.max_comparisons ?? 50;
    
    // Get existing memories (excluding the one being checked)
    const existingMemories = getExistingMemories(maxComparisons)
      .filter(m => m.id !== request.memory_id);
    
    const contradictions: ContradictionCheckResult['contradictions'] = [];
    let checkedCount = 0;
    
    // Generate embedding for new memory
    const newEmbedding = await getEmbeddingFn()(request.content);
    
    for (const existing of existingMemories) {
      checkedCount++;
      
      // 1. Quick entity overlap check - skip if no common entities
      const commonEntities = request.entities.filter(e => 
        existing.entities.some(ee => ee.toLowerCase() === e.toLowerCase())
      );
      
      if (commonEntities.length === 0 && request.entities.length > 0) {
        continue; // Skip - no entity overlap
      }
      
      // 2. Generate embedding and calculate similarity
      let similarityScore = 0;
      try {
        const existingEmbedding = await getEmbeddingFn()(existing.content);
        similarityScore = cosineSimilarity(newEmbedding, existingEmbedding);
      } catch (e) {
        // Fallback to simple text similarity if embedding fails
        similarityScore = this.calculateTextSimilarity(request.content, existing.content);
      }
      
      // Skip if similarity is too low (not related content)
      if (similarityScore < 0.5) continue;
      
      // 3. Calculate contradiction score
      const contradictionScore = await this.calculateContradictionScore(
        request.content,
        existing.content,
        similarityScore
      );
      
      // 4. Flag if above threshold
      if (contradictionScore >= threshold && similarityScore >= threshold) {
        contradictions.push({
          existing_memory_id: existing.id,
          similarity: similarityScore,
          contradiction_score: contradictionScore,
          reason: this.generateContradictionReason(request.content, existing.content)
        });
        
        // Record the contradiction in the database
        await this.recordContradiction(
          request.memory_id,
          existing.id,
          commonEntities[0],
          request.content.substring(0, 100),
          existing.content.substring(0, 100),
          'embedding',
          similarityScore,
          contradictionScore
        );
      }
    }
    
    return {
      has_contradiction: contradictions.length > 0,
      contradictions,
      checked_count: checkedCount,
      flagged_for_review: contradictions.length >= 2
    };
  }
  
  /**
   * Calculate contradiction score between two pieces of content
   */
  private async calculateContradictionScore(
    newContent: string,
    existingContent: string,
    similarityScore: number
  ): Promise<number> {
    const newLower = newContent.toLowerCase();
    const existingLower = existingContent.toLowerCase();
    
    // Check for rule-based contradictions first
    for (const pattern of CONTRADICTION_PATTERNS) {
      const newHasPositive = newLower.includes(pattern.positive);
      const existingHasNegative = existingLower.includes(pattern.negative);
      const newHasNegative = newLower.includes(pattern.negative);
      const existingHasPositive = existingLower.includes(pattern.positive);
      
      if ((newHasPositive && existingHasNegative) || (newHasNegative && existingHasPositive)) {
        return pattern.score;
      }
    }
    
    // Check for direct value conflicts in structured data
    const newNumbers = newContent.match(/\$[\d,]+|\d+%/g) || [];
    const existingNumbers = existingContent.match(/\$[\d,]+|\d+%/g) || [];
    
    for (const newNum of newNumbers) {
      for (const existingNum of existingNumbers) {
        if (newNum !== existingNum && this.isOppositeDirection(newNum, existingNum)) {
          return 0.7;
        }
      }
    }
    
    // Check temporal contradictions (e.g., "was" vs "will be", "before" vs "after")
    const temporalPatterns = [
      ['was', 'will be'],
      ['before', 'after'],
      ['yesterday', 'tomorrow'],
      ['previous', 'next'],
      ['earlier', 'later'],
      ['past', 'future']
    ];
    
    for (const [t1, t2] of temporalPatterns) {
      if (newLower.includes(t1) && existingLower.includes(t2)) {
        return 0.75;
      }
      if (newLower.includes(t2) && existingLower.includes(t1)) {
        return 0.75;
      }
    }
    
    // If high similarity but no obvious contradiction, likely NOT a contradiction
    // (same content being reinforced)
    if (similarityScore > 0.9) {
      return 0.1;
    }
    
    // For moderate similarity with different entities, medium contradiction score
    return similarityScore * 0.3;
  }
  
  /**
   * Check if two numeric values represent opposite directions
   */
  private isOppositeDirection(a: string, b: string): boolean {
    // Parse numbers from strings like "$1,234" or "50%"
    const numA = parseFloat(a.replace(/[$,%]/g, ''));
    const numB = parseFloat(b.replace(/[$,%]/g, ''));
    
    if (isNaN(numA) || isNaN(numB)) return false;
    
    // Check for significant difference (>20%) suggesting contradiction
    const avg = (Math.abs(numA) + Math.abs(numB)) / 2;
    const diff = Math.abs(numA - numB) / avg;
    
    return diff > 0.2;
  }
  
  /**
   * Simple text similarity fallback
   */
  private calculateTextSimilarity(a: string, b: string): number {
    const wordsA = new Set(a.toLowerCase().split(/\s+/));
    const wordsB = new Set(b.toLowerCase().split(/\s+/));
    
    const intersection = new Set([...wordsA].filter(x => wordsB.has(x)));
    const union = new Set([...wordsA, ...wordsB]);
    
    return intersection.size / union.size;
  }
  
  /**
   * Generate human-readable reason for contradiction
   */
  private generateContradictionReason(newContent: string, existingContent: string): string {
    const newLower = newContent.toLowerCase();
    const existingLower = existingContent.toLowerCase();
    
    // Check rule-based patterns
    for (const pattern of CONTRADICTION_PATTERNS) {
      if (newLower.includes(pattern.positive) && existingLower.includes(pattern.negative)) {
        return `Contains "${pattern.positive}" vs "${pattern.negative}"`;
      }
      if (newLower.includes(pattern.negative) && existingLower.includes(pattern.positive)) {
        return `Contains "${pattern.negative}" vs "${pattern.positive}"`;
      }
    }
    
    // Check temporal
    if ((newLower.includes('yesterday') && existingLower.includes('tomorrow')) ||
        (newLower.includes('tomorrow') && existingLower.includes('yesterday'))) {
      return 'Conflicting time references (yesterday vs tomorrow)';
    }
    
    return 'High semantic similarity with conflicting content';
  }
  
  /**
   * Record a contradiction in the database
   */
  private async recordContradiction(
    memoryAId: string,
    memoryBId: string,
    entity: string | undefined,
    valueA: string,
    valueB: string,
    method: ContradictionDetectionMethod,
    similarity: number,
    contradictionScore: number
  ): Promise<MemoryContradiction> {
    // Check if this contradiction already exists
    const existing = this.db.prepare(`
      SELECT id FROM memory_contradictions
      WHERE (memory_a_id = ? AND memory_b_id = ?)
         OR (memory_a_id = ? AND memory_b_id = ?)
    `).get(memoryAId, memoryBId, memoryBId, memoryAId);
    
    if (existing) {
      // Update existing
      this.db.prepare(`
        UPDATE memory_contradictions SET
          similarity_score = ?, contradiction_score = ?, created_at = datetime('now')
        WHERE id = ?
      `).run(similarity, contradictionScore, (existing as any).id);
      
      return this.getContradiction((existing as any).id)!;
    }
    
    // Create new
    const id = `mc_${uuidv4().slice(0, 8)}`;
    
    this.db.prepare(`
      INSERT INTO memory_contradictions (
        id, memory_a_id, memory_b_id, entity, value_a, value_b,
        detection_method, similarity_score, contradiction_score, created_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    `).run(
      id, memoryAId, memoryBId, entity || null, valueA, valueB,
      method, similarity, contradictionScore
    );
    
    return this.getContradiction(id)!;
  }
  
  /**
   * Get a specific contradiction
   */
  getContradiction(id: string): MemoryContradiction | null {
    const row = this.db.prepare('SELECT * FROM memory_contradictions WHERE id = ?').get(id) as any;
    return row ? this.parseRow(row) : null;
  }
  
  /**
   * Get all unresolved contradictions
   */
  getUnresolvedContradictions(limit: number = 50): MemoryContradiction[] {
    const rows = this.db.prepare(`
      SELECT * FROM memory_contradictions
      WHERE resolution_status = 'unresolved'
      ORDER BY contradiction_score DESC, created_at DESC
      LIMIT ?
    `).all(limit) as any[];
    
    return rows.map(this.parseRow);
  }
  
  /**
   * Get contradictions for a specific memory
   */
  getContradictionsForMemory(memoryId: string): MemoryContradiction[] {
    const rows = this.db.prepare(`
      SELECT * FROM memory_contradictions
      WHERE memory_a_id = ? OR memory_b_id = ?
      ORDER BY contradiction_score DESC
    `).all(memoryId, memoryId) as any[];
    
    return rows.map(this.parseRow);
  }
  
  /**
   * Resolve a contradiction
   */
  resolveContradiction(
    id: string,
    strategy: ResolutionStrategy,
    resolvedBy: string,
    note?: string
  ): MemoryContradiction | null {
    const now = new Date().toISOString();
    
    this.db.prepare(`
      UPDATE memory_contradictions SET
        resolution_status = 'auto_resolved',
        resolution_strategy = ?,
        resolved_at = ?,
        resolved_by = ?,
        resolution_note = ?
      WHERE id = ?
    `).run(strategy, now, resolvedBy, note || null, id);
    
    return this.getContradiction(id);
  }
  
  /**
   * Mark contradiction as ignored
   */
  ignoreContradiction(id: string, ignoredBy: string, note?: string): MemoryContradiction | null {
    const now = new Date().toISOString();
    
    this.db.prepare(`
      UPDATE memory_contradictions SET
        resolution_status = 'ignored',
        resolved_at = ?,
        resolved_by = ?,
        resolution_note = ?
      WHERE id = ?
    `).run(now, ignoredBy, note || `Ignored: ${note || 'No reason provided'}`, id);
    
    return this.getContradiction(id);
  }
  
  /**
   * Get contradiction statistics
   */
  getStats(): {
    total: number;
    unresolved: number;
    auto_resolved: number;
    human_resolved: number;
    ignored: number;
    avg_contradiction_score: number;
  } {
    const stats = this.db.prepare(`
      SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN resolution_status = 'unresolved' THEN 1 ELSE 0 END) as unresolved,
        SUM(CASE WHEN resolution_strategy = 'auto_resolved' THEN 1 ELSE 0 END) as auto_resolved,
        SUM(CASE WHEN resolution_status = 'human_resolved' THEN 1 ELSE 0 END) as human_resolved,
        SUM(CASE WHEN resolution_status = 'ignored' THEN 1 ELSE 0 END) as ignored,
        AVG(contradiction_score) as avg_score
      FROM memory_contradictions
    `).get() as any;
    
    return {
      total: stats.total || 0,
      unresolved: stats.unresolved || 0,
      auto_resolved: stats.auto_resolved || 0,
      human_resolved: stats.human_resolved || 0,
      ignored: stats.ignored || 0,
      avg_contradiction_score: stats.avg_score || 0
    };
  }
  
  /**
   * Add to review queue
   */
  addToReviewQueue(contradictionId: string, priority: number = 0, assignedTo?: string): void {
    const id = `crq_${uuidv4().slice(0, 8)}`;
    
    this.db.prepare(`
      INSERT INTO contradiction_review_queue (id, contradiction_id, priority, assigned_to)
      VALUES (?, ?, ?, ?)
    `).run(id, contradictionId, priority, assignedTo || null);
  }
  
  /**
   * Get items in review queue
   */
  getReviewQueue(limit: number = 20): Array<{ contradiction: MemoryContradiction; priority: number }> {
    const rows = this.db.prepare(`
      SELECT m.*, cr.priority, cr.assigned_to, cr.review_note
      FROM memory_contradictions m
      INNER JOIN contradiction_review_queue cr ON m.id = cr.contradiction_id
      WHERE cr.reviewed_at IS NULL
      ORDER BY cr.priority DESC, m.contradiction_score DESC
      LIMIT ?
    `).all(limit) as any[];
    
    return rows.map(row => ({
      contradiction: this.parseRow(row),
      priority: row.priority
    }));
  }
  
  private parseRow(row: any): MemoryContradiction {
    return {
      id: row.id,
      memory_a_id: row.memory_a_id,
      memory_b_id: row.memory_b_id,
      entity: row.entity,
      value_a: row.value_a,
      value_b: row.value_b,
      detection_method: row.detection_method,
      confidence: row.confidence,
      similarity_score: row.similarity_score,
      contradiction_score: row.contradiction_score,
      resolution_status: row.resolution_status,
      resolution_strategy: row.resolution_strategy,
      resolved_at: row.resolved_at,
      resolved_by: row.resolved_by,
      resolution_note: row.resolution_note,
      created_at: row.created_at
    };
  }
}

// =============================================================================
// CONVENIENCE FUNCTIONS
// =============================================================================

/**
 * Quick check if content contradicts existing memories
 */
export async function quickContradictionCheck(
  db: Database.Database,
  content: string,
  entities: string[],
  threshold: number = 0.85
): Promise<boolean> {
  const store = new ContradictionStore(db);
  
  // Simple similarity check without full comparison
  const generateEmbedding = getEmbeddingFn();
  const contentEmbedding = await generateEmbedding(content);
  
  // Get some recent memories for quick check
  const recentMemories = db.prepare(`
    SELECT id, content, entities FROM memories
    WHERE deleted_at IS NULL
    ORDER BY created_at DESC
    LIMIT 20
  `).all() as any[];
  
  for (const mem of recentMemories) {
    const memEntities = JSON.parse(mem.entities || '[]');
    const common = entities.filter(e => 
      memEntities.some((me: string) => me.toLowerCase() === e.toLowerCase())
    );
    
    if (common.length > 0) {
      try {
        const memEmbedding = await generateEmbedding(mem.content);
        const similarity = cosineSimilarity(contentEmbedding, memEmbedding);
        
        if (similarity >= threshold) {
          return true;
        }
      } catch (e) {
        // Skip on error
      }
    }
  }
  
  return false;
}