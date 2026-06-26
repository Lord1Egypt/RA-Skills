/**
 * Effect Scoring System
 *
 * Provides quantitative evaluation of decision quality and agent performance.
 * Core of the self-optimization loop.
 *
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve
 */
export type { Decision, DecisionOutcome, EffectScore, Strategy } from './types.js';
/**
 * Simple linear scoring: score = result / expectation * baseScore
 * Range: 0-100
 */
export declare function linearScore(result: number, expectation: number, baseScore?: number): number;
/**
 * Binary scoring: success = 1, failure = 0
 */
export declare function binaryScore(success: boolean, baseScore?: number): number;
/**
 * Weighted scoring for multi-criteria outcomes
 * Weights sum to 1.0
 */
export declare function weightedScore(criteria: Array<{
    score: number;
    weight: number;
}>): number;
/**
 * Time-based scoring: faster = better
 * score = baseScore * speedFactor, where speedFactor > 1 means faster than expected
 */
export declare function timeScore(actualMs: number, expectedMs: number, baseScore?: number): number;
/**
 * Quality scoring: based on error rate or quality metrics
 * score = (1 - errorRate) * baseScore
 */
export declare function qualityScore(errors: number, total: number, baseScore?: number): number;
/**
 * Composite scoring: combines multiple dimensions
 */
export declare function compositeScore(params: {
    accuracy?: number;
    speed?: number;
    efficiency?: number;
    satisfaction?: number;
    weights?: {
        accuracy: number;
        speed: number;
        efficiency: number;
        satisfaction: number;
    };
}): number;
export interface ScoringDecision {
    id: string;
    type: 'binary' | 'multi_criteria' | 'quantitative' | 'quality' | 'composite';
    description: string;
    criteria?: Array<{
        name: string;
        weight: number;
        expectation?: number;
    }>;
    expectation?: number;
    timeoutMs?: number;
    timestamp: number;
}
export interface ScoringOutcome {
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
export interface ScoringScore {
    decisionId: string;
    score: number;
    grade: 'A' | 'B' | 'C' | 'D' | 'F';
    confidence: number;
    breakdown: Record<string, number>;
    latencyMs: number;
    scoredAt: number;
}
export declare class EffectScoreCalculator {
    /**
     * Calculate score from a completed decision and its outcome
     */
    static calculate(decision: ScoringDecision, outcome: ScoringOutcome): ScoringScore;
    /**
     * Calculate confidence level (0-1) based on evidence quality
     */
    static calculateConfidence(decision: ScoringDecision, outcome: ScoringOutcome): number;
    /**
     * Convert numeric score to letter grade
     */
    static scoreToGrade(score: number): 'A' | 'B' | 'C' | 'D' | 'F';
}
export declare class AutoScorer {
    /**
     * Auto-generate a score based on implicit feedback
     */
    static fromImplicitFeedback(decision: ScoringDecision, context: {
        userFeedback?: 'positive' | 'negative' | 'neutral';
        repeatedTask?: boolean;
        taskAbandoned?: boolean;
        quickApproval?: boolean;
        modifications?: number;
    }): ScoringOutcome;
    /**
     * Score based on outcome type
     */
    static fromOutcomeType(outcome: ScoringOutcome): number;
}
export declare class ScoreAggregator {
    /**
     * Aggregate multiple scores with trend analysis
     */
    static aggregate(scores: ScoringScore[]): {
        avgScore: number;
        trend: 'improving' | 'stable' | 'declining';
        grade: 'A' | 'B' | 'C' | 'D' | 'F';
        percentile: number;
        stats: {
            min: number;
            max: number;
            count: number;
            stdDev: number;
        };
    };
}
//# sourceMappingURL=effect-scorer.d.ts.map