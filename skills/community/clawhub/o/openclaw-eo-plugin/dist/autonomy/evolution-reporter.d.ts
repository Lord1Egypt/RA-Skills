/**
 * Evolution Report Generator
 *
 * Generates automated evolution reports from Dream output
 * Part of the self-optimization loop: Dream → Report → Evolution
 */
export interface EvolutionReport {
    id: string;
    date: string;
    period: string;
    scoreSummary: {
        avgScore: number;
        grade: string;
        trend: string;
        totalTracked: number;
        successRate: number;
    };
    patterns: Array<{
        name: string;
        description: string;
        confidence: number;
    }>;
    patches: Array<{
        id: string;
        name: string;
        risk: string;
        status: string;
    }>;
    recommendations: string[];
    nextSteps: string[];
    generatedAt: number;
}
/**
 * Generate an evolution report
 */
export declare function generateEvolutionReport(periodMs?: number): EvolutionReport;
/**
 * Format report as markdown
 */
export declare function formatReportAsMarkdown(report: EvolutionReport): string;
export declare const evolutionReporter: {
    generate: typeof generateEvolutionReport;
    format: typeof formatReportAsMarkdown;
};
//# sourceMappingURL=evolution-reporter.d.ts.map