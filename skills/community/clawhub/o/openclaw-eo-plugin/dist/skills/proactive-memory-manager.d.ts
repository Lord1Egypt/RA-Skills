/**
 * EO Proactive Memory Manager v1.0.0
 *
 * Inspired by Claude Code's memdir.ts and memoryTypes.ts
 * Handles proactive memory saving and loading for session continuity.
 *
 * Key features:
 * - Session-end: proactively distill key info to MEMORY.md + topics/
 * - Session-start: load relevant memories using semantic search
 * - Four memory types: user, feedback, project, reference
 * - MEMORY.md truncation (200 lines / 25KB)
 */
export declare const ENTRYPOINT_NAME = "MEMORY.md";
export declare const MAX_ENTRYPOINT_LINES = 200;
export declare const MAX_ENTRYPOINT_BYTES = 25000;
export declare const TOPICS_DIR = "topics";
export declare const MEMORY_DIR = "memory";
export declare const MEMORY_TYPES: readonly ["user", "feedback", "project", "reference"];
export type MemoryType = (typeof MEMORY_TYPES)[number];
export interface MemoryFrontmatter {
    name: string;
    description: string;
    type: MemoryType;
    created: string;
    updated: string;
    tags?: string[];
}
export interface MemoryEntry {
    frontmatter: MemoryFrontmatter;
    content: string;
    filePath: string;
}
export interface MemoryContext {
    sessionId: string;
    workspace: string;
    memoryDir: string;
    lastUpdated?: number;
}
export declare class ProactiveMemoryManager {
    private workspace;
    constructor(workspace: string);
    /**
     * Get the memory directory path
     */
    getMemoryDir(): string;
    /**
     * Get the topics directory path
     */
    getTopicsDir(): string;
    /**
     * Ensure memory directory structure exists
     */
    ensureMemoryStructure(): void;
    /**
     * Extract key information from session messages and save to memory
     */
    distillSessionMemory(sessionId: string, messages: SessionMessage[]): Promise<MemoryDistillResult>;
    /**
     * Categorize session messages into memory types
     */
    private categorizeMessages;
    private matchesPattern;
    private extractTitle;
    private summarize;
    private generateMemoryFileName;
    /**
     * Save a memory entry to a topic file
     */
    private saveMemoryEntry;
    /**
     * Update MEMORY.md index with new memory entry
     */
    private updateMemoryIndex;
    /**
     * Load all relevant memories for the current session
     */
    loadRelevantMemories(query?: string): Promise<RelevantMemoryResult>;
    /**
     * Parse MEMORY.md index entries
     */
    private parseIndexEntries;
    /**
     * Filter entries by relevance to query
     */
    private filterByRelevance;
    /**
     * Truncate MEMORY.md content to line AND byte caps
     */
    truncateIndex(content: string): {
        content: string;
        wasLineTruncated: boolean;
        wasByteTruncated: boolean;
    };
    private formatBytes;
    /**
     * Get memory system statistics
     */
    getMemoryStats(): MemoryStats;
}
interface SessionMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp?: number;
}
interface IndexEntry {
    title: string;
    filePath: string;
    description: string;
    type: MemoryType;
}
interface LoadedMemory extends IndexEntry {
    content: string;
    loaded: boolean;
}
export interface MemoryDistillResult {
    saved: string[];
    skipped: string[];
    total: number;
}
export interface RelevantMemoryResult {
    memories: LoadedMemory[];
    indexLoaded: boolean;
    truncated: boolean;
    totalIndexed?: number;
}
export interface MemoryStats {
    topicCount: number;
    totalSize: number;
    indexSize: number;
    indexLines: number;
    truncated: boolean;
}
export declare function createMemoryManager(workspace: string): ProactiveMemoryManager;
export {};
//# sourceMappingURL=proactive-memory-manager.d.ts.map