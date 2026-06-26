export type ClaudeMemoryKind = 'identity' | 'correction' | 'task' | 'project' | 'reference';
export interface ClaudeMemoryEntry {
    id: string;
    kind: ClaudeMemoryKind;
    summary: string;
    content: string;
    tags: string[];
    importance: number;
    createdAt: string;
    updatedAt: string;
    source: 'user' | 'assistant' | 'system';
}
export declare class ClaudeMemorySystem {
    private storePath;
    private entries;
    constructor(baseDir?: string, namespace?: string);
    addMemory(kind: ClaudeMemoryKind, summary: string, content: string, options?: {
        tags?: string[];
        importance?: number;
        source?: 'user' | 'assistant' | 'system';
    }): ClaudeMemoryEntry;
    retrieve(query: string, topK?: number): Array<{
        entry: ClaudeMemoryEntry;
        score: number;
        reasons: string[];
    }>;
    backgroundExtract(turnText: string): ClaudeMemoryEntry[];
    formatRetrievedContext(query: string, topK?: number): string;
    getStats(): Record<string, number>;
    private load;
    private save;
}
export default ClaudeMemorySystem;
