/**
 * Memory Types - Cross-Session Memory System
 * Defines all types for the EO memory architecture
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
export declare enum MemoryPriority {
    P0_CRITICAL = 0,// Critical decisions - permanent retention
    P1_CONTEXT = 1,// Project context - 30 days retention
    P2_SUMMARY = 2,// Conversation summary - 7 days retention
    P3_TEMPORARY = 3
}
export declare const RETENTION_PERIODS: Record<MemoryPriority, number | null>;
export interface MemoryEntry<T = unknown> {
    id: string;
    key: string;
    value: T;
    priority: MemoryPriority;
    createdAt: number;
    updatedAt: number;
    expiresAt: number | null;
    sessionId?: string;
    tags: string[];
    metadata: Record<string, unknown>;
}
export interface GlobalMemoryEntry<T = unknown> extends MemoryEntry<T> {
    priority: MemoryPriority.P0_CRITICAL | MemoryPriority.P1_CONTEXT;
    locked: boolean;
    lockSessionId?: string;
}
export interface SessionMemoryEntry<T = unknown> extends MemoryEntry<T> {
    priority: MemoryPriority;
    archived: boolean;
}
export interface UserPreference {
    key: string;
    value: unknown;
    category: 'ui' | 'behavior' | 'project' | 'system';
    updatedAt: number;
}
export interface ProjectContext {
    projectId: string;
    projectName: string;
    status: 'active' | 'paused' | 'completed';
    lastAccessedAt: number;
    metadata: Record<string, unknown>;
}
export interface LongRunningTask {
    taskId: string;
    description: string;
    status: 'pending' | 'in_progress' | 'blocked' | 'completed';
    createdAt: number;
    updatedAt: number;
    blockedBy?: string[];
}
export interface MemorySyncEvent {
    type: 'load' | 'save' | 'archive' | 'clear' | 'conflict';
    sessionId: string;
    timestamp: number;
    entries: string[];
    conflictResolved?: boolean;
}
export interface SessionSnapshot {
    sessionId: string;
    startedAt: number;
    endedAt: number;
    summary: string;
    decisions: GlobalMemoryEntry[];
    context: ProjectContext[];
    tasks: LongRunningTask[];
    preferences: UserPreference[];
}
export interface MemorySystemOptions {
    storageDir?: string;
    maxMemorySize?: number;
    autoArchive?: boolean;
    conflictStrategy?: 'latest' | 'priority' | 'merge';
}
export interface IMemoryStore {
    get<T>(key: string): Promise<MemoryEntry<T> | null>;
    set<T>(key: string, entry: MemoryEntry<T>): Promise<void>;
    delete(key: string): Promise<boolean>;
    list(filter?: Partial<MemoryEntry>): Promise<MemoryEntry[]>;
    clear(): Promise<void>;
}
export interface MemoryContext {
    sessionId: string;
    userId?: string;
    channel?: string;
    api: OpenClawPluginApi;
}
//# sourceMappingURL=memory-types.d.ts.map