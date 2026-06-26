export type TaskType = 'planning' | 'architecture' | 'frontend-dev' | 'backend-dev' | 'fullstack-dev' | 'testing' | 'security-audit' | 'deployment' | 'code-review' | 'academic-paper' | 'marketing-content' | 'multi-expert';
export type TaskComplexity = 'low' | 'medium' | 'high';
export type ExpertRole = 'architect' | 'planner' | 'frontend' | 'backend' | 'qa' | 'security' | 'devops' | 'code-reviewer' | 'senior-dev' | 'performance-engineer';
export interface TaskContext {
    taskId: string;
    taskType: TaskType;
    description: string;
    complexity?: TaskComplexity;
    domains?: string[];
    techStack?: string[];
    requirements?: string;
    constraints?: string;
}
export interface Checkpoint {
    checkpointId: string;
    checkpointName: string;
    passed: boolean;
    durationMs: number;
    warnings?: number;
    failedItems?: string[];
}
export interface TaskFeedback {
    feedbackId: string;
    taskId: string;
    context: TaskContext;
    execution: {
        success: boolean;
        durationMs: number;
        outputQuality?: 'excellent' | 'good' | 'fair' | 'poor';
        errorCount?: number;
        revisionCount?: number;
    };
    checkpoints?: Checkpoint[];
    expertContributions?: ExpertContribution[];
    userFeedback?: UserFeedback;
    timestamp: number;
}
export interface ExpertContribution {
    expertId: string;
    role: ExpertRole;
    contributionScore: number;
    checkpointResults?: Checkpoint[];
}
export interface UserFeedback {
    rating: number;
    approved: boolean;
    revisionNeeded: boolean;
    comments?: string;
}
export interface Pattern {
    patternId: string;
    name: string;
    description: string;
    taskType: TaskType;
    domain?: string;
    frequency: number;
    confidence: number;
    severity: 'low' | 'medium' | 'high';
    evidence: string[];
    recommendedActions?: string[];
    status: 'mined' | 'approved' | 'rejected' | 'applied';
    createdAt: number;
    updatedAt: number;
}
export interface SelfLearningConfig {
    version: string;
    enabled: boolean;
    feedback: {
        autoCollect: boolean;
        collectOnCheckpoint: boolean;
        collectOnCompletion: boolean;
        requireUserReview: boolean;
        autoScoreThreshold: number;
    };
    patternMining: {
        enabled: boolean;
        autoMine: boolean;
        minSuccessCases: number;
        confidenceThreshold: number;
        approvalRequired: boolean;
        autoApproveThreshold: number;
    };
    weightAdjustment: {
        enabled: boolean;
        autoAdjust: boolean;
        adjustmentInterval: 'daily' | 'weekly' | 'monthly';
        learningRate: number;
        minWeight: number;
        maxWeight: number;
        emaSmoothing: number;
        perTaskTypeTracking: boolean;
    };
    knowledge: {
        tier1RetentionDays: number;
        tier2RetentionDays: number;
        tier3RetentionDays: number;
        tier4RetentionDays: number;
        distillSchedule: 'daily' | 'weekly' | 'monthly';
    };
    logging: {
        level: 'debug' | 'info' | 'warn' | 'error';
        dailySummary: boolean;
        eventRetentionDays: number;
        summaryRetentionDays: number;
    };
    expertRoles: ExpertRole[];
    taskTypes: TaskType[];
}
export interface ExpertRecommendation {
    expertId: string;
    role: ExpertRole;
    name: string;
    matchScore: number;
    weight: number;
    specialization?: string;
    historicalSuccessRate?: number;
}
export interface DreamScenario {
    scenarioId: string;
    name: string;
    context: TaskContext;
    hypothesis: string;
    status: 'active' | 'simulated' | 'validated' | 'rejected';
    createdAt: number;
}
export interface DreamResult {
    scenarioId: string;
    outcome: 'success' | 'failure' | 'partial';
    insights: string[];
    generatedPattern?: Pattern;
    simulationDurationMs: number;
}
export interface SessionStats {
    totalSessions: number;
    activeSessions: number;
    completedSessions: number;
    failedSessions: number;
    avgDurationMs: number;
}
//# sourceMappingURL=types.d.ts.map