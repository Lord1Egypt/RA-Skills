import { AgentKnowledgeGraph } from './knowledge-graph.js';
export type DecisionOption = {
    id: string;
    label: string;
    description: string;
    pros?: string[];
    cons?: string[];
    confidence: number;
    votes?: number;
};
export interface ExpertOpinion {
    expertId: string;
    expertName: string;
    expertRole: string;
    recommendation: 'approve' | 'reject' | 'abstain' | 'modify';
    confidence: number;
    reasoning: string;
    concerns?: string[];
    suggestions?: string[];
    alternative?: string;
}
export interface DebateSession {
    id: string;
    topic: string;
    options: DecisionOption[];
    experts: string[];
    opinions: ExpertOpinion[];
    currentRound: number;
    maxRounds: number;
    status: 'collecting' | 'debating' | 'voting' | 'decided';
    consensusLevel: 'unanimous' | 'strong' | 'majority' | 'plurality' | 'deadlock';
    decision?: string;
    createdAt: number;
    updatedAt: number;
}
export interface VotingResult {
    optionId: string;
    optionLabel: string;
    votes: {
        expertId: string;
        expertName: string;
        weight: number;
    }[];
    totalWeight: number;
    percentage: number;
}
export interface ConsensusResult {
    success: boolean;
    consensusLevel: DebateSession['consensusLevel'];
    winningOption?: DecisionOption;
    votingResults: VotingResult[];
    summary: string;
    minorityConcerns?: ExpertOpinion[];
    recommendations?: string[];
}
export interface TriggerConfig {
    votingThreshold: number;
    minDebateRounds: number;
    maxDebateRounds: number;
    enableAutoTrigger: boolean;
    consensusTimeoutMs: number;
    weightByExpertise: boolean;
    weightByConfidence: boolean;
}
export declare class DebateManager {
    private sessions;
    private knowledgeGraph;
    private config;
    constructor(knowledgeGraph: AgentKnowledgeGraph, config?: Partial<TriggerConfig>);
    /**
     * Create a new debate session.
     */
    createSession(topic: string, options: DecisionOption[], expertIds: string[]): DebateSession;
    /**
     * Get session by ID.
     */
    getSession(id: string): DebateSession | undefined;
    /**
     * Add an expert opinion to a session.
     */
    addOpinion(sessionId: string, opinion: Omit<ExpertOpinion, 'expertName' | 'expertRole'>): boolean;
    /**
     * Progress to next debate round.
     */
    nextRound(sessionId: string): DebateSession | null;
    /**
     * Conduct voting on current options.
     */
    vote(sessionId: string): VotingResult[];
    /**
     * Determine consensus from voting results.
     */
    determineConsensus(sessionId: string): ConsensusResult;
    private getExpertInfo;
    private calculateExpertiseWeight;
    private recordDebateExperience;
    private generateRecommendations;
    private generateSummary;
    /**
     * Check if a new message should trigger multi-expert collaboration.
     */
    shouldTrigger(context: {
        messageLength: number;
        hasTechnicalTerms: boolean;
        hasDecisionKeywords: boolean;
        isComplexTask: boolean;
    }): boolean;
    /**
     * Analyze message to detect if it's a decision request.
     */
    analyzeMessage(message: string): {
        isDecisionRequest: boolean;
        decisionType?: string;
        urgency?: 'low' | 'normal' | 'high';
        complexity?: 'low' | 'medium' | 'high';
    };
}
export declare const debateManager: DebateManager;
export default DebateManager;
//# sourceMappingURL=multi-expert-trigger.d.ts.map