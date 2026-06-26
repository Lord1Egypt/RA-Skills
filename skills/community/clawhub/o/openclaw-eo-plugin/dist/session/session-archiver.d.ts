export interface SessionArchive {
    sessionKey: string;
    workspace: string;
    lastMessageAt: number;
    messageCount: number;
    messages: SessionMessage[];
    summary?: string;
    tags: string[];
}
export interface SessionMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp: number;
    tools?: string[];
}
export interface ArchiveIndex {
    lastIndexedAt: number;
    sessionCount: number;
    totalMessages: number;
    topics: Map<string, TopicEntry>;
    decisions: Decision[];
    patterns: Pattern[];
}
export interface TopicEntry {
    topic: string;
    sessionKeys: string[];
    lastDiscussedAt: number;
    messageCount: number;
}
export interface Decision {
    id: string;
    content: string;
    sessionKey: string;
    timestamp: number;
    confirmed: boolean;
}
export interface Pattern {
    id: string;
    type: 'workflow' | 'command' | 'expert' | 'topic';
    description: string;
    occurrences: number;
    lastSeenAt: number;
    sessions: string[];
}
export declare class SessionArchiver {
    private workspaceRoot;
    private archiveDir;
    private indexPath;
    private archiveIndex;
    constructor(workspaceRoot: string);
    private loadIndex;
    private saveIndex;
    /**
     * Read session messages from OpenClaw session storage
     * Assumes OpenClaw stores sessions in ~/.openclaw/sessions/ or workspace
     */
    readSession(sessionKey: string): Promise<SessionArchive | null>;
    /**
     * Normalize session data from various formats
     * Supports nested format: { type: 'message', message: { role: 'user', content: [{ type: 'text', text: '...' }] } }
     */
    private normalizeSession;
    /**
     * Extract text content from various content formats
     * Handles Array.isArray(content) format: [{ type: 'text', text: '...' }, ...]
     */
    private extractContent;
    /**
     * Index a session - extract topics, decisions, patterns
     */
    indexSession(sessionKey: string): Promise<void>;
    /**
     * Extract topics from session messages
     */
    private extractTopics;
    /**
     * Extract decisions from session
     */
    private extractDecisions;
    /**
     * Extract workflow patterns
     */
    private extractPatterns;
    private recordPattern;
    /**
     * Get sessions related to a topic
     */
    getSessionsForTopic(topic: string): string[];
    /**
     * Get recent decisions
     */
    getRecentDecisions(limit?: number): Decision[];
    /**
     * Get top patterns
     */
    getTopPatterns(type?: Pattern['type'], limit?: number): Pattern[];
    /**
     * Get archive statistics
     */
    getStats(): {
        sessionCount: number;
        totalMessages: number;
        topicCount: number;
        patternCount: number;
    };
    /**
     * Search sessions by keyword
     */
    searchSessions(query: string, limit?: number): Promise<SessionArchive[]>;
    /**
     * Get full archive index
     */
    getArchiveIndex(): ArchiveIndex;
}
export declare function createSessionArchiver(workspaceRoot: string): SessionArchiver;
//# sourceMappingURL=session-archiver.d.ts.map