/**
 * LocalMemoryStore — Advanced brain-like memory store
 * 
 * Features:
 * - Hierarchical memory (working/short-term/long-term)
 * - Entity extraction and tracking
 * - Importance scoring with decay
 * - Semantic chunking for long content
 * - Cross-session learning
 * - Memory importance based on recency, relevance, and usage
 * - Context-aware retrieval
 */

import { randomUUID } from "node:crypto";
import { resolve } from "node:path";
import { homedir } from "node:os";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";

// ─── Types ────────────────────────────────────────────────────────────────────

export interface MemoryEntry {
  id: string;
  content: string;
  tfidf: Record<string, number>;
  importance: number;           // 0-1, calculated from multiple factors
  accessCount: number;         // How many times this was retrieved
  lastAccessed: string;         // ISO timestamp
  accessHistory: string[];      // Recent access timestamps
  
  // Brain-like structure
  chunkOf?: string;             // Parent chunk if this is a chunk
  chunks?: string[];            // Child chunk IDs if this is a summary
  
  metadata: {
    sessionKey?: string;
    category: "preference" | "fact" | "decision" | "entity" | "skill" | "context" | "other";
    createdAt: string;
    updatedAt: string;
    accessedAt: string;
    source?: "user" | "assistant" | "system";
    messageType?: "exchange" | "summary" | "entity" | "preference" | "fact";
    
    // Entity tracking
    entities?: string[];        // Extracted entities (names, places, etc.)
    tags?: string[];            // Semantic tags
    
    // Memory links (IDs of related memories)
    links?: string[];
    
    // Composite key for deduplication
    contentHash?: string;
  };
}

export interface SearchResult {
  id: string;
  content: string;
  similarity: number;
  importance: number;
  recency: number;              // 0-1, newer = higher
  metadata: MemoryEntry["metadata"];
  score: number;                // Combined relevance score
}

export interface StoreConfig {
  containerTag: string;
  debug: boolean;
  maxMemories?: number;
  pruneOlderThanDays?: number;
  
  // Brain settings
  decayRate?: number;           // How fast importance decays (0-1)
  chunkThreshold?: number;      // Min chars to trigger chunking
  chunkSize?: number;          // Target chars per chunk
  maxChunks?: number;          // Max chunks per summary
  
  // Recall settings
  importanceWeight?: number;    // Weight for importance in scoring
  recencyWeight?: number;       // Weight for recency in scoring
  relevanceWeight?: number;     // Weight for TF-IDF relevance
}

interface MemoryStats {
  totalMemories: number;
  totalChunks: number;
  avgImportance: number;
  categoryBreakdown: Record<string, number>;
  lastCleanup: string;
}

// ─── Tokenizer & TF-IDF ───────────────────────────────────────────────────────

/** Enhanced tokenizer that preserves important patterns */
function tokenize(text: string): string[] {
  return text
    .toLowerCase()
    .replace(/[^a-zäöüß0-9\s]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 2);
}

/** Extract entities (names, emails, URLs, etc.) */
function extractEntities(text: string): string[] {
  const entities: string[] = [];
  
  // Emails
  const emails = text.match(/[\w.-]+@[\w.-]+\.\w+/g);
  if (emails) entities.push(...emails);
  
  // URLs
  const urls = text.match(/https?:\/\/[^\s]+/g);
  if (urls) entities.push(...urls);
  
  // Capitalized words (potential names/entities)
  const caps = text.match(/[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)*/g);
  if (caps) entities.push(...caps.slice(0, 5));
  
  // Hashtags and mentions
  const hashtags = text.match(/[#@][\w]+/g);
  if (hashtags) entities.push(...hashtags);
  
  return [...new Set(entities)];
}

/** Extract semantic tags from content */
function extractTags(text: string): string[] {
  const tags: string[] = [];
  const lower = text.toLowerCase();
  
  // Domain-specific tags
  const tagMap: Record<string, string[]> = {
    "code|programming|script|function|api": ["coding", "development"],
    "email|mail|send|outlook": ["email", "communication"],
    "file|document|folder|directory": ["files", "organization"],
    "server|hosting|deploy|ssh|plesk": ["infrastructure", "server"],
    "memory|brain|remember|forget": ["memory", "cognition"],
    "task|todo|project|deadline": ["tasks", "productivity"],
    "money|cost|price|budget|revenue": ["finance", "business"],
    "meeting|call|calendar|schedule": ["calendar", "coordination"],
    "password|security|auth|login": ["security", "credentials"],
    "error|bug|issue|problem": ["debugging", "issues"],
  };
  
  for (const [pattern, tagList] of Object.entries(tagMap)) {
    if (new RegExp(pattern).test(lower)) {
      tags.push(...tagList);
    }
  }
  
  return [...new Set(tags)].slice(0, 5);
}

function computeTF(tokens: string[]): Record<string, number> {
  const tf: Record<string, number> = {};
  for (const token of tokens) {
    tf[token] = (tf[token] ?? 0) + 1;
  }
  const len = tokens.length;
  for (const token in tf) {
    tf[token] /= len;
  }
  return tf;
}

function computeIDF(documents: string[][]): Record<string, number> {
  const idf: Record<string, number> = {};
  const N = documents.length;
  const docFreq: Record<string, number> = {};

  for (const doc of documents) {
    const seen = new Set(doc);
    for (const term of seen) {
      docFreq[term] = (docFreq[term] ?? 0) + 1;
    }
  }

  for (const term in docFreq) {
    idf[term] = Math.log((N + 1) / (docFreq[term] + 1)) + 1;
  }

  return idf;
}

function computeTFIDF(tf: Record<string, number>, idf: Record<string, number>): Record<string, number> {
  const vec: Record<string, number> = {};
  for (const term in tf) {
    vec[term] = tf[term] * (idf[term] ?? 1);
  }
  return vec;
}

function cosineSimilarity(a: Record<string, number>, b: Record<string, number>): number {
  const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
  let dot = 0, normA = 0, normB = 0;
  for (const k of keys) {
    const av = a[k] ?? 0;
    const bv = b[k] ?? 0;
    dot += av * bv;
    normA += av * av;
    normB += bv * bv;
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB) + 1e-8);
}

// ─── Content Hashing for Deduplication ───────────────────────────────────────

function hashContent(content: string): string {
  let hash = 0;
  const normalized = content.toLowerCase().replace(/\s+/g, ' ').trim();
  for (let i = 0; i < normalized.length; i++) {
    const char = normalized.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash).toString(16);
}

/** Sanitize container tag to prevent path traversal */
function sanitizeContainerTag(tag: string): string {
  return tag
    .replace(/[^a-zA-Z0-9_-]/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '')
    .slice(0, 64); // Max 64 chars
}

// ─── Category Detection ───────────────────────────────────────────────────────

function detectCategory(text: string): MemoryEntry["metadata"]["category"] {
  const lower = text.toLowerCase();
  
  if (/\b(immer|nur|nie|bevorzug|präferiert|like|love|hate|prefer|want|need|never|always)\b/i.test(lower)) return "preference";
  if (/\b(entschieden|beschlossen|geplant|wird|werden|machen|setup|installiert|aktiviert|configured|decided|will use|going with|chose|selected)\b/i.test(lower)) return "decision";
  if (/\b(skill|können|fähig|ability|experienced|proficient|know how)\b/i.test(lower)) return "skill";
  if (/\b(ich bin|mein|unser|Name|Email|Konto|team|firma|unternehmen|company|name|called|named)\b/i.test(lower)) return "entity";
  if (/\b(ist|sind|hat|haben|war|waren|is|are|has|have|was|were)\b/i.test(lower) && text.length < 500) return "fact";
  return "other";
}

// ─── Importance Scoring ───────────────────────────────────────────────────────

/**
 * Calculate importance based on multiple factors:
 * - Content length (longer = more important up to a point)
 * - Entity count (more entities = more important)
 * - Category (decisions and preferences score higher)
 * - User vs assistant (user content scores higher)
 */
function calculateImportance(
  content: string,
  metadata: MemoryEntry["metadata"],
  accessCount: number,
): number {
  let score = 0.3; // Base score
  
  // Length factor (optimal range: 100-1000 chars)
  const len = content.length;
  if (len > 100 && len < 1000) score += 0.2;
  else if (len >= 1000 && len < 5000) score += 0.15;
  else if (len >= 5000) score += 0.1;
  else if (len < 50) score -= 0.1;
  
  // Entity factor
  const entityCount = (metadata.entities?.length ?? 0);
  score += Math.min(entityCount * 0.05, 0.2);
  
  // Category factor
  if (metadata.category === "decision") score += 0.25;
  else if (metadata.category === "preference") score += 0.2;
  else if (metadata.category === "entity") score += 0.15;
  else if (metadata.category === "skill") score += 0.2;
  
  // Source factor (user content is more important)
  if (metadata.source === "user") score += 0.15;
  
  // Access factor (memories that have been accessed multiple times are valuable)
  score += Math.min(accessCount * 0.02, 0.15);
  
  return Math.max(0.1, Math.min(1, score));
}

/**
 * Apply time-based decay to importance
 */
function applyDecay(importance: number, createdAt: string, decayRate: number): number {
  const ageMs = Date.now() - new Date(createdAt).getTime();
  const ageDays = ageMs / (24 * 60 * 60 * 1000);
  const decay = Math.exp(-decayRate * ageDays);
  return importance * decay;
}

// ─── Semantic Chunker ─────────────────────────────────────────────────────────

/**
 * Split long content into meaningful chunks
 */
function chunkContent(content: string, chunkSize: number, maxChunks: number): string[] {
  if (content.length <= chunkSize) return [content];
  
  const chunks: string[] = [];
  const sentences = content.match(/[^.!?]+[.!?]+/g) || [content];
  let currentChunk = "";
  
  for (const sentence of sentences) {
    if (currentChunk.length + sentence.length > chunkSize && currentChunk.length > 0) {
      chunks.push(currentChunk.trim());
      if (chunks.length >= maxChunks) break;
      currentChunk = sentence;
    } else {
      currentChunk += " " + sentence;
    }
  }
  
  if (chunks.length < maxChunks && currentChunk.trim()) {
    chunks.push(currentChunk.trim());
  }
  
  return chunks;
}

// ─── Store ───────────────────────────────────────────────────────────────────

export class LocalMemoryStore {
  private memories: MemoryEntry[] = [];
  private idf: Record<string, number> = {};
  private dirty = false;
  public readonly containerTag: string;
  private storePath: string;
  
  // Config
  private maxMemories: number;
  private pruneOlderThanDays: number;
  private decayRate: number;
  private chunkThreshold: number;
  private chunkSize: number;
  private maxChunks: number;
  private importanceWeight: number;
  private recencyWeight: number;
  private relevanceWeight: number;
  
  // Runtime stats
  private stats: MemoryStats = {
    totalMemories: 0,
    totalChunks: 0,
    avgImportance: 0.5,
    categoryBreakdown: {},
    lastCleanup: new Date().toISOString(),
  };

  constructor(cfg: StoreConfig) {
    this.containerTag = sanitizeContainerTag(cfg.containerTag);
    this.maxMemories = cfg.maxMemories ?? 500;
    this.pruneOlderThanDays = cfg.pruneOlderThanDays ?? 30;
    this.decayRate = cfg.decayRate ?? 0.05;
    this.chunkThreshold = cfg.chunkThreshold ?? 2000;
    this.chunkSize = cfg.chunkSize ?? 800;
    this.maxChunks = cfg.maxChunks ?? 3;
    this.importanceWeight = cfg.importanceWeight ?? 0.25;
    this.recencyWeight = cfg.recencyWeight ?? 0.25;
    this.relevanceWeight = cfg.relevanceWeight ?? 0.5;
    
    this.storePath = resolve(homedir(), ".openclaw", "memory", `${this.containerTag}.json`);
    this.load();
  }

  // ── Persistence ─────────────────────────────────────────────────────────

  private load() {
    try {
      const dir = resolve(homedir(), ".openclaw", "memory");
      if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

      if (existsSync(this.storePath)) {
        const raw = readFileSync(this.storePath, "utf-8");
        const data = JSON.parse(raw);
        this.memories = Array.isArray(data.memories) ? data.memories : [];
        this.stats = data.stats ?? this.stats;
        this.rebuildIDF();
      }
    } catch {
      this.memories = [];
    }
  }

  private save() {
    if (!this.dirty) return;
    try {
      const dir = resolve(homedir(), ".openclaw", "memory");
      if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
      
      // Prune before saving
      this.prune();
      
      const data = {
        memories: this.memories,
        stats: this.stats,
        version: "0.4.0",
      };
      
      writeFileSync(this.storePath, JSON.stringify(data, null, 2), "utf-8");
      this.dirty = false;
    } catch (err) {
      console.error("[local-memory] save failed:", err);
    }
  }

  private rebuildIDF() {
    const docs = this.memories.map((m) => tokenize(m.content));
    this.idf = computeIDF(docs);
  }

  // ── Pruning ────────────────────────────────────────────────────────────

  private prune() {
    const now = Date.now();
    const maxAge = this.pruneOlderThanDays * 24 * 60 * 60 * 1000;
    
    // Filter out old memories (but keep high-importance ones longer)
    const beforePrune = this.memories.length;
    this.memories = this.memories.filter((m) => {
      const age = now - new Date(m.metadata.createdAt).getTime();
      // Keep if: not old OR very important
      if (age < maxAge) return true;
      if (m.importance > 0.7) return true; // Protect important memories
      return false;
    });
    
    // If still over limit, remove lowest importance
    if (this.memories.length > this.maxMemories) {
      // Sort by importance (with decay applied)
      const now = Date.now();
      this.memories.sort((a, b) => {
        const ageA = (now - new Date(a.metadata.createdAt).getTime()) / (24 * 60 * 60 * 1000);
        const ageB = (now - new Date(b.metadata.createdAt).getTime()) / (24 * 60 * 60 * 1000);
        const scoreA = a.importance * Math.exp(-this.decayRate * ageA);
        const scoreB = b.importance * Math.exp(-this.decayRate * ageB);
        return scoreB - scoreA;
      });
      
      // Keep only top maxMemories
      const removed = this.memories.splice(this.maxMemories);
      
      // Also remove orphaned chunks
      const keptIds = new Set(this.memories.map(m => m.id));
      this.memories = this.memories.filter(m => 
        !m.chunkOf || keptIds.has(m.chunkOf)
      );
    }
    
    const pruned = beforePrune - this.memories.length;
    if (pruned > 0) {
      console.log(`[local-memory] pruned ${pruned} memories (${this.memories.length} remaining)`);
      this.rebuildIDF();
      this.updateStats();
    }
    
    this.stats.lastCleanup = new Date().toISOString();
  }

  private updateStats() {
    this.stats.totalMemories = this.memories.length;
    this.stats.totalChunks = this.memories.filter(m => !!m.chunkOf).length;
    
    const categories: Record<string, number> = {};
    let totalImp = 0;
    
    for (const m of this.memories) {
      const cat = m.metadata.category;
      categories[cat] = (categories[cat] ?? 0) + 1;
      totalImp += m.importance;
    }
    
    this.stats.avgImportance = totalImp / this.memories.length;
    this.stats.categoryBreakdown = categories;
  }

  // ── CRUD ──────────────────────────────────────────────────────────────

  async add(
    content: string,
    metadata: Partial<MemoryEntry["metadata"]> = {},
  ): Promise<string> {
    // Check for duplicate
    const contentHash = hashContent(content);
    const existing = this.memories.find(m => m.metadata.contentHash === contentHash);
    if (existing) {
      // Update access and bump importance slightly
      existing.accessCount++;
      existing.lastAccessed = new Date().toISOString();
      existing.accessHistory.push(new Date().toISOString());
      existing.metadata.accessedAt = new Date().toISOString();
      this.dirty = true;
      return existing.id;
    }

    // Chunk if too long
    const chunks = chunkContent(content, this.chunkSize, this.maxChunks);
    const isChunked = chunks.length > 1;
    
    const tokens = tokenize(chunks[0]); // Use first chunk for TF-IDF
    const tf = computeTF(tokens);
    const tfidf = computeTFIDF(tf, this.idf);
    
    // Extract entities and tags from full content
    const entities = metadata.entities ?? extractEntities(content);
    const tags = metadata.tags ?? extractTags(content);
    
    const category = metadata.category ?? detectCategory(content);
    const now = new Date().toISOString();
    
    const id = randomUUID();
    const entry: MemoryEntry = {
      id,
      content: chunks[0], // Store first chunk as main content
      tfidf,
      importance: calculateImportance(content, { ...metadata, category }, 0),
      accessCount: 0,
      lastAccessed: now,
      accessHistory: [],
      metadata: {
        category,
        createdAt: now,
        updatedAt: now,
        accessedAt: now,
        sessionKey: metadata.sessionKey,
        source: metadata.source,
        messageType: metadata.messageType,
        entities,
        tags,
        contentHash,
        links: metadata.links ?? [],
      },
    };

    this.memories.push(entry);

    // Create child chunks if chunked
    if (isChunked && chunks.length > 1) {
      entry.chunks = [];
      for (let i = 1; i < chunks.length; i++) {
        const chunkId = await this.addChunk(chunks[i], id, category, metadata);
        entry.chunks.push(chunkId);
      }
    }

    // Update IDF incrementally
    const newDocs = [tokens];
    const newIDF = computeIDF(newDocs);
    for (const term in newIDF) {
      this.idf[term] = newIDF[term];
    }

    this.dirty = true;
    this.updateStats();
    this.save();
    return id;
  }

  private async addChunk(
    content: string,
    parentId: string,
    category: MemoryEntry["metadata"]["category"],
    metadata: Partial<MemoryEntry["metadata"]>,
  ): Promise<string> {
    const tokens = tokenize(content);
    const tf = computeTF(tokens);
    const tfidf = computeTFIDF(tf, this.idf);
    
    const now = new Date().toISOString();
    const id = randomUUID();
    
    const chunkEntry: MemoryEntry = {
      id,
      content,
      tfidf,
      importance: 0.3, // Chunks have lower base importance
      accessCount: 0,
      lastAccessed: now,
      accessHistory: [],
      chunkOf: parentId,
      metadata: {
        category,
        createdAt: now,
        updatedAt: now,
        accessedAt: now,
        sessionKey: metadata.sessionKey,
        source: metadata.source,
        entities: extractEntities(content),
        tags: extractTags(content),
      },
    };

    this.memories.push(chunkEntry);
    return id;
  }

  /**
   * Enhanced search with brain-like scoring:
   * - TF-IDF relevance
   * - Importance (with decay)
   * - Recency
   * - Access frequency
   */
  async search(
    query: string,
    limit = 10,
    threshold = 0.1,
  ): Promise<SearchResult[]> {
    const queryTokens = tokenize(query);
    const queryTF = computeTF(queryTokens);
    const queryTFIDF = computeTFIDF(queryTF, this.idf);
    const now = Date.now();

    const scored = this.memories
      .filter(m => !m.chunkOf) // Don't return chunks directly
      .map((entry) => {
        const relevance = cosineSimilarity(queryTFIDF, entry.tfidf);
        
        // Get all chunks for this memory
        const allContent = [entry.content];
        if (entry.chunks) {
          for (const chunkId of entry.chunks) {
            const chunk = this.memories.find(m => m.id === chunkId);
            if (chunk) allContent.push(chunk.content);
          }
        }
        
        // Recalculate relevance across all content
        const fullTfidf = computeTFIDF(computeTF(tokenize(allContent.join(" "))), this.idf);
        const fullRelevance = cosineSimilarity(queryTFIDF, fullTfidf);
        
        // Time since last access (in days)
        const lastAccessAge = (now - new Date(entry.lastAccessed).getTime()) / (24 * 60 * 60 * 1000);
        const recency = Math.exp(-0.1 * lastAccessAge); // Exponential decay
        
        // Time since creation
        const age = (now - new Date(entry.metadata.createdAt).getTime()) / (24 * 60 * 60 * 1000);
        const ageDecay = Math.exp(-this.decayRate * age);
        
        // Importance with decay
        const decayedImportance = entry.importance * ageDecay;
        
        // Access frequency boost
        const accessBoost = Math.min(entry.accessCount * 0.01, 0.2);
        
        // Combined score
        const score = 
          (this.relevanceWeight * fullRelevance) +
          (this.importanceWeight * (decayedImportance + accessBoost)) +
          (this.recencyWeight * recency);

        // Update access tracking
        entry.accessCount++;
        entry.lastAccessed = new Date().toISOString();
        entry.accessHistory.push(new Date().toISOString());
        if (entry.accessHistory.length > 10) {
          entry.accessHistory = entry.accessHistory.slice(-10);
        }
        entry.metadata.accessedAt = new Date().toISOString();

        return {
          id: entry.id,
          content: allContent.join("\n\n"),
          similarity: fullRelevance,
          importance: decayedImportance,
          recency,
          metadata: entry.metadata,
          score,
        };
      });

    const filtered = scored
      .filter((s) => s.score >= threshold)
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);

    this.dirty = true;
    return filtered;
  }

  /**
   * Get memories by category
   */
  async getByCategory(category: MemoryEntry["metadata"]["category"]): Promise<MemoryEntry[]> {
    return this.memories.filter(m => m.metadata.category === category && !m.chunkOf);
  }

  /**
   * Get entities (people, places, things we know about)
   */
  async getEntities(): Promise<MemoryEntry[]> {
    return this.memories.filter(m => m.metadata.category === "entity" && !m.chunkOf);
  }

  /**
   * Get preferences (user likes, dislikes, habits)
   */
  async getPreferences(): Promise<MemoryEntry[]> {
    return this.memories.filter(m => m.metadata.category === "preference" && !m.chunkOf);
  }

  /**
   * Get recent memories
   */
  async getRecent(limit = 10): Promise<MemoryEntry[]> {
    return [...this.memories]
      .filter(m => !m.chunkOf)
      .sort((a, b) => new Date(b.metadata.createdAt).getTime() - new Date(a.metadata.createdAt).getTime())
      .slice(0, limit);
  }

  /**
   * Get frequently accessed memories
   */
  async getFrequent(limit = 10): Promise<MemoryEntry[]> {
    return [...this.memories]
      .filter(m => !m.chunkOf)
      .sort((a, b) => b.accessCount - a.accessCount)
      .slice(0, limit);
  }

  async delete(id: string): Promise<void> {
    const entry = this.memories.find(m => m.id === id);
    if (!entry) return;
    
    // Also delete child chunks
    if (entry.chunks) {
      for (const chunkId of entry.chunks) {
        const idx = this.memories.findIndex(m => m.id === chunkId);
        if (idx !== -1) this.memories.splice(idx, 1);
      }
    }
    
    const idx = this.memories.findIndex(m => m.id === id);
    if (idx !== -1) {
      this.memories.splice(idx, 1);
      this.dirty = true;
      this.updateStats();
    }
  }

  async forgetByQuery(
    query: string,
    limit = 1,
  ): Promise<{ success: boolean; message: string }> {
    const results = await this.search(query, limit);
    if (results.length === 0) {
      return { success: false, message: "No matching memory found." };
    }
    await this.delete(results[0].id);
    const preview = results[0].content.slice(0, 100);
    return {
      success: true,
      message: `Forgot: "${preview}${results[0].content.length > 100 ? "…" : ""}"`,
    };
  }

  async wipeAll(): Promise<{ deletedCount: number }> {
    const count = this.memories.length;
    this.memories = [];
    this.idf = {};
    this.dirty = true;
    this.updateStats();
    this.save();
    return { deletedCount: count };
  }

  async count(): Promise<number> {
    return this.memories.filter(m => !m.chunkOf).length;
  }

  async listAll(limit = 100): Promise<MemoryEntry[]> {
    return [...this.memories]
      .filter(m => !m.chunkOf)
      .sort(
        (a, b) =>
          new Date(b.metadata.accessedAt).getTime() -
          new Date(a.metadata.accessedAt).getTime()
      )
      .slice(0, limit);
  }

  async getStats(): Promise<MemoryStats> {
    return { ...this.stats };
  }

  /**
   * Build a user profile from memory (like Supermemory's profile system)
   */
  async buildProfile(): Promise<{
    static: string[];
    dynamic: string[];
    entities: string[];
    preferences: string[];
  }> {
    const entities = new Set<string>();
    const preferences = new Set<string>();
    const staticFacts: string[] = [];
    const dynamicFacts: string[] = [];

    for (const m of this.memories) {
      if (m.chunkOf) continue;
      
      // Collect entities
      if (m.metadata.entities) {
        for (const e of m.metadata.entities) {
          entities.add(e);
        }
      }
      
      // Collect by category
      if (m.metadata.category === "entity") {
        staticFacts.push(m.content);
      } else if (m.metadata.category === "preference") {
        preferences.add(m.content);
      } else if (m.metadata.category === "fact") {
        // Recent facts are dynamic, old facts become static
        const age = Date.now() - new Date(m.metadata.createdAt).getTime();
        if (age < 7 * 24 * 60 * 60 * 1000) { // Less than 7 days old
          dynamicFacts.push(m.content);
        } else {
          staticFacts.push(m.content);
        }
      }
    }

    return {
      static: [...new Set(staticFacts)].slice(0, 20),
      dynamic: [...new Set(dynamicFacts)].slice(0, 10),
      entities: [...entities].slice(0, 20),
      preferences: [...preferences].slice(0, 20),
    };
  }

  /**
   * Link related memories together
   */
  async linkMemories(id1: string, id2: string): Promise<void> {
    const m1 = this.memories.find(m => m.id === id1);
    const m2 = this.memories.find(m => m.id === id2);
    if (!m1 || !m2) return;
    
    if (!m1.metadata.links) m1.metadata.links = [];
    if (!m2.metadata.links) m2.metadata.links = [];
    
    if (!m1.metadata.links.includes(id2)) m1.metadata.links.push(id2);
    if (!m2.metadata.links.includes(id1)) m2.metadata.links.push(id1);
    
    this.dirty = true;
  }

  /**
   * Get related memories (via links or shared entities)
   */
  async getRelated(memoryId: string, limit = 5): Promise<SearchResult[]> {
    const memory = this.memories.find(m => m.id === memoryId);
    if (!memory) return [];
    
    // Get IDs of directly linked memories
    const linkedIds = memory.metadata.links ?? [];
    
    // Get memories with shared entities
    const sharedEntityIds: string[] = [];
    if (memory.metadata.entities) {
      for (const entity of memory.metadata.entities) {
        for (const m of this.memories) {
          if (m.id !== memoryId && m.metadata.entities?.includes(entity)) {
            sharedEntityIds.push(m.id);
          }
        }
      }
    }
    
    // Combine and fetch
    const allIds = [...new Set([...linkedIds, ...sharedEntityIds])].slice(0, limit);
    const now = Date.now();
    
    return allIds.map(id => {
      const m = this.memories.find(x => x.id === id)!;
      return {
        id: m.id,
        content: m.content,
        similarity: 0.5,
        importance: m.importance,
        recency: Math.exp(-0.1 * (now - new Date(m.lastAccessed).getTime()) / (24 * 60 * 60 * 1000)),
        metadata: m.metadata,
        score: 0.5,
      };
    });
  }
}
