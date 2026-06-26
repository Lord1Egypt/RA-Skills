/**
 * Sessions Module Stub
 * This module provides session management for multi-expert orchestration.
 * Placeholder implementation - replace with actual OpenClaw sessions API.
 */
export interface SessionHandle {
    sessionId: string;
    waitForCompletion(): Promise<any>;
    abort(): void;
}
export interface SpawnOptions {
    task: string;
    mode?: string;
    timeout?: number;
    retries?: number;
}
export declare function spawn(options: SpawnOptions): SessionHandle;
export declare function getSession(id: string): SessionHandle | null;
export declare function endSession(id: string): void;
//# sourceMappingURL=sessions.d.ts.map