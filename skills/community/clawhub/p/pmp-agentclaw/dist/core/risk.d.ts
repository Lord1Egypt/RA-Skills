/**
 * Risk Management Calculations
 * PMBOK 7th Edition — Risk Management
 */
export type ProbabilityScore = 1 | 2 | 3 | 4 | 5;
export type ImpactScore = 1 | 2 | 3 | 4 | 5;
export type RiskZone = 'GREEN' | 'AMBER' | 'RED';
export interface RiskInput {
    id: string;
    description: string;
    category?: string;
    probability: ProbabilityScore;
    impact: ImpactScore;
    owner?: string;
    responseStrategy?: string;
}
export interface RiskOutput extends RiskInput {
    score: number;
    zone: RiskZone;
    action: string;
    priority: 'Low' | 'Medium' | 'High' | 'Critical';
}
export interface RiskMatrix {
    probabilityScale: Array<{
        score: ProbabilityScore;
        label: string;
        range: string;
    }>;
    impactScale: Array<{
        score: ImpactScore;
        label: string;
        description: string;
    }>;
    zones: {
        low: {
            range: [number, number];
            color: string;
            action: string;
        };
        medium: {
            range: [number, number];
            color: string;
            action: string;
        };
        high: {
            range: [number, number];
            color: string;
            action: string;
        };
    };
    responseStrategies: {
        threats: string[];
        opportunities: string[];
    };
}
export declare const DEFAULT_RISK_MATRIX: RiskMatrix;
/**
 * Score a single risk
 */
export declare function scoreRisk(risk: RiskInput, matrix?: RiskMatrix): RiskOutput;
/**
 * Score multiple risks
 */
export declare function scoreRisks(risks: RiskInput[], matrix?: RiskMatrix): RiskOutput[];
/**
 * Get risk matrix as formatted table
 */
export declare function getRiskMatrixTable(matrix?: RiskMatrix): string;
/**
 * Calculate risk statistics
 */
export declare function calculateRiskStats(risks: RiskOutput[]): {
    total: number;
    open: number;
    closed: number;
    highCount: number;
    mediumCount: number;
    lowCount: number;
    criticalCount: number;
    averageScore: number;
};
/**
 * Format risk matrix as Markdown (alias for getRiskMatrixTable)
 */
export declare function formatRiskMatrixMarkdown(matrix?: RiskMatrix): string;
//# sourceMappingURL=risk.d.ts.map