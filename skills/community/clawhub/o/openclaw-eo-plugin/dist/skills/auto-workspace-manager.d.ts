/**
 * EO Auto Workspace Manager v1.0.0
 *
 * Automatic session-to-workspace binding system.
 * Solves the memory cross-contamination problem when using OpenClaw
 * across multiple sessions (e.g., multiple Feishu groups).
 *
 * Key features:
 * - Detect new sessions automatically
 * - Create dedicated workspace per session/project
 * - Manage OpenClaw bindings dynamically
 * - Support session migration and cleanup
 */
export interface SessionInfo {
    sessionId: string;
    channel: 'feishu' | 'discord' | 'telegram' | 'web' | 'unknown';
    peerId?: string;
    peerType?: 'group' | 'channel' | 'user';
    projectName?: string;
    workspace?: string;
    agentId?: string;
    createdAt: number;
    lastActiveAt: number;
}
export interface WorkspaceBinding {
    sessionId: string;
    workspace: string;
    agentId: string;
    channel: string;
    peerId?: string;
    boundAt: number;
}
export interface AgentConfig {
    id: string;
    name: string;
    workspace: string;
    channels?: string[];
}
export interface OpenClawConfig {
    agents?: {
        list?: AgentConfig[];
    };
    bindings?: BindingConfig[];
}
export interface BindingConfig {
    type: 'route';
    agentId: string;
    match: {
        channel: string;
        peer?: {
            kind: 'group' | 'channel' | 'user';
            id: string;
        };
    };
}
export declare class AutoWorkspaceManager {
    private basePath;
    private sessionRegistryPath;
    private sessionRegistry;
    private bindingRegistry;
    constructor(basePath?: string);
    private loadRegistry;
    private saveRegistry;
    /**
     * Register a new session or update existing one
     */
    registerSession(sessionId: string, info: Partial<SessionInfo>): SessionInfo;
    /**
     * Get session info
     */
    getSession(sessionId: string): SessionInfo | undefined;
    /**
     * List all registered sessions
     */
    listSessions(): SessionInfo[];
    /**
     * Find sessions by criteria
     */
    findSessions(criteria: Partial<SessionInfo>): SessionInfo[];
    /**
     * Create a new workspace for a session/project
     */
    createWorkspace(projectName: string, template?: string): WorkspaceInfo;
    /**
     * Get or create workspace for a project
     */
    getOrCreateWorkspace(projectName: string): WorkspaceInfo;
    /**
     * Create an agent configuration
     */
    createAgent(projectName: string, workspace: string): AgentConfig;
    /**
     * Add a session binding to OpenClaw config
     */
    addSessionBinding(sessionId: string, agentId: string, channel: string, peerId?: string): boolean;
    /**
     * Infer peer kind from peer ID pattern
     */
    private inferPeerKind;
    /**
     * Complete one-click setup for a new session
     * This is the main entry point for the skill
     */
    setupNewSession(params: {
        sessionId: string;
        channel: string;
        peerId?: string;
        projectName?: string;
        agentName?: string;
    }): Promise<SessionSetupResult>;
    /**
     * Extract project name from peer ID
     */
    private extractProjectFromPeer;
    /**
     * Check if gateway restart is needed
     */
    needsGatewayRestart(): boolean;
    /**
     * Get command to restart gateway
     */
    getRestartCommand(): string;
    /**
     * Generate status report
     */
    generateStatusReport(): StatusReport;
}
export interface WorkspaceInfo {
    path: string;
    name: string;
    alreadyExisted: boolean;
}
export interface SessionSetupResult {
    success: boolean;
    sessionId: string;
    projectName: string;
    workspace: string;
    agentId: string;
    bindingAdded: boolean;
    message: string;
}
export interface StatusReport {
    totalSessions: number;
    totalWorkspaces: number;
    activeSessions: number;
    recentBindings: WorkspaceBinding[];
}
export declare function createWorkspaceManager(basePath?: string): AutoWorkspaceManager;
//# sourceMappingURL=auto-workspace-manager.d.ts.map