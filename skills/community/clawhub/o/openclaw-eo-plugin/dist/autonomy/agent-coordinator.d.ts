export interface AgentInfo {
    id: string;
    name: string;
    role: string;
    expertise: string[];
    currentLoad: number;
    isAvailable: boolean;
    lastActive: number;
}
export interface CoordinationTask {
    id: string;
    type: 'planning' | 'analysis' | 'decision' | 'review' | 'custom';
    priority: 'low' | 'normal' | 'high' | 'critical';
    description: string;
    requiredExpertRoles: string[];
    minExperts: number;
    deadline?: number;
    payload: any;
}
export interface CoordinatedResult {
    taskId: string;
    success: boolean;
    consensus: 'unanimous' | 'majority' | 'plurality' | 'none';
    votes?: VoteResult[];
    aggregatedOutput?: string;
    conflicts?: ConflictReport[];
    expertContributions: Map<string, ExpertContribution>;
    durationMs: number;
    timestamp: number;
}
export interface VoteResult {
    expertId: string;
    expertName: string;
    vote: 'approve' | 'reject' | 'abstain';
    confidence: number;
    reasoning?: string;
}
export interface ConflictReport {
    conflictId: string;
    experts: string[];
    disagreement: string;
    severity: 'minor' | 'major' | 'critical';
    resolution?: string;
}
export interface ExpertContribution {
    expertId: string;
    expertName: string;
    role: string;
    output: string;
    keyPoints: string[];
    confidence: number;
    timestamp: number;
}
export interface CoordinatorConfig {
    enableLoadBalancing: boolean;
    enableConflictResolution: boolean;
    consensusThreshold: number;
    maxRetries: number;
    taskTimeoutMs: number;
    enableVoting: boolean;
}
export declare class AgentCoordinator {
    private config;
    private taskQueue;
    private loadBalancer;
    private conflictResolver;
    private agents;
    constructor(config?: Partial<CoordinatorConfig>);
    registerAgent(agent: Omit<AgentInfo, 'currentLoad' | 'isAvailable' | 'lastActive'>): void;
    unregisterAgent(agentId: string): void;
    getAgent(agentId: string): AgentInfo | undefined;
    getAllAgents(): AgentInfo[];
    submitTask(task: CoordinationTask): void;
    getNextTask(): CoordinationTask | undefined;
    cancelTask(taskId: string): boolean;
    getQueueSize(): number;
    /**
     * Coordinate a multi-expert task with consensus building.
     * This is the main entry point for Phase 3 collaboration.
     */
    coordinate(task: CoordinationTask, expertOutputs: Map<string, ExpertContribution>): Promise<CoordinatedResult>;
    /**
     * Auto-generate votes from expert contributions.
     */
    private generateVotes;
    /**
     * Aggregate multiple expert outputs into a coherent result.
     */
    private aggregateOutputs;
    private resolveConflictDescription;
    assignTaskToAgent(taskId: string, agentId: string): boolean;
    releaseAgent(agentId: string): void;
    getStatus(): {
        queueSize: number;
        agentCount: number;
        availableAgents: number;
        averageLoad: number;
    };
}
export declare function createCoordinator(config?: Partial<CoordinatorConfig>): AgentCoordinator;
export declare const PHASE3_EXPERTS: {
    coordinator: {
        id: string;
        name: string;
        role: string;
        expertise: string[];
    };
    synthesizer: {
        id: string;
        name: string;
        role: string;
        expertise: string[];
    };
    monitor: {
        id: string;
        name: string;
        role: string;
        expertise: string[];
    };
};
export default AgentCoordinator;
//# sourceMappingURL=agent-coordinator.d.ts.map