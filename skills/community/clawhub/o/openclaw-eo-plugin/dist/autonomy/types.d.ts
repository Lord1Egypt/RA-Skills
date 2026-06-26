/**
 * Autonomy Module Types
 */
export type Strategy = 'conservative' | 'balanced' | 'aggressive' | 'adaptive';
export type StrategyType = Strategy;
export interface StrategyWeights {
    riskWeight: number;
    speedWeight: number;
    qualityWeight?: number;
    costWeight?: number;
}
export interface DecisionOption {
    id: string;
    type: 'expert' | 'workflow' | 'action' | 'wait';
    name: string;
    description: string;
    estimatedRisk: number;
    estimatedSpeed: number;
    estimatedQuality?: number;
    estimatedCost?: number;
    requiresConfirmation: boolean;
    metadata?: Record<string, unknown>;
}
export interface DecisionContext {
    userMessage: string;
    sessionHistory: string[];
    activeWorkflow?: string;
    pendingTasks: string[];
    contextUsage: number;
    availableExperts: string[];
    availableWorkflows: string[];
    recentDecisions: Decision[];
    strategy: StrategyType;
    options?: DecisionOption[];
    metadata?: Record<string, unknown>;
}
export interface Decision {
    id: string;
    type?: 'binary' | 'multi_criteria' | 'quantitative' | 'quality' | 'composite';
    description?: string;
    timestamp: number;
    strategy?: Strategy;
    criteria?: Array<{
        name: string;
        weight: number;
        expectation?: number;
    }>;
    expectation?: number;
    timeoutMs?: number;
    context: DecisionContext;
    options: DecisionOption[];
    selectedOption: DecisionOption;
    reasoning: string;
    score: number;
}
export interface DecisionOutcome {
    success?: boolean;
    value?: number;
    criteriaScores?: number[];
    errors?: number;
    total?: number;
    accuracy?: number;
    speed?: number;
    efficiency?: number;
    satisfaction?: number;
    feedback?: string;
}
export interface Outcome {
    decisionId: string;
    result: 'success' | 'partial' | 'failure' | 'unknown';
    score: number;
    feedback?: string;
    executionTime: number;
    artifacts?: Record<string, unknown>;
}
export interface EffectScore {
    decisionId: string;
    score: number;
    grade: 'A' | 'B' | 'C' | 'D' | 'F';
    confidence: number;
    breakdown: Record<string, number>;
    latencyMs: number;
    scoredAt: number;
}
export interface ScoredOption {
    option: DecisionOption;
    score: number;
    riskScore: number;
    speedScore: number;
    qualityScore: number;
    costScore: number;
}
export interface OptimizationResult {
    improvedParameters: string[];
    averageScoreImprovement: number;
    recommendations: string[];
}
export interface EvolveResult {
    newRules: string[];
    retiredRules: string[];
    confidence: number;
    evidence: string[];
}
//# sourceMappingURL=types.d.ts.map