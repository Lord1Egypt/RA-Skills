import type { CollaborationSession, ExpertResult, ExpertTeam } from '../types/index.js';
export declare class SessionManager {
    private sessions;
    private history;
    private maxHistory;
    /**
     * Create a new collaboration session
     */
    createSession(task: string, context?: Record<string, unknown>): CollaborationSession;
    /**
     * Get a session by ID
     */
    getSession(sessionId: string): CollaborationSession | undefined;
    /**
     * Add a team to a session
     */
    addTeamToSession(sessionId: string, team: ExpertTeam): boolean;
    /**
     * Add a result from an expert to a session
     */
    addExpertResult(sessionId: string, result: ExpertResult): boolean;
    /**
     * Complete a session
     */
    completeSession(sessionId: string, status?: 'completed' | 'failed'): boolean;
    /**
     * List all active sessions
     */
    listActiveSessions(): CollaborationSession[];
    /**
     * List recent completed sessions
     */
    listRecentSessions(limit?: number): CollaborationSession[];
    /**
     * Get session summary
     */
    getSessionSummary(sessionId: string): string;
    /**
     * Clean up stale sessions
     */
    cleanupStaleSessions(maxAgeMs?: number): number;
}
export declare const sessionManager: SessionManager;
//# sourceMappingURL=session-manager.d.ts.map