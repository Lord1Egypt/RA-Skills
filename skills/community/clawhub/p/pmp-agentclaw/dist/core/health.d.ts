/**
 * Project Health Check
 * Monitors project document completeness and freshness
 */
export interface HealthCheckInput {
    projectDir: string;
    maxRiskRegisterAge?: number;
}
export interface HealthCheckOutput {
    status: 'GREEN' | 'AMBER' | 'RED';
    issues: number;
    warnings: number;
    checks: Array<{
        name: string;
        status: 'pass' | 'warn' | 'fail';
        message: string;
        details?: string;
    }>;
    timestamp: string;
}
export declare const REQUIRED_DOCUMENTS: string[];
export declare const OPTIONAL_DOCUMENTS: string[];
/**
 * Run project health check
 */
export declare function checkHealth(input: HealthCheckInput): HealthCheckOutput;
/**
 * Format health check as Markdown
 */
export declare function formatHealthMarkdown(result: HealthCheckOutput): string;
/**
 * Format health check as JSON
 */
export declare function formatHealthJson(result: HealthCheckOutput): string;
//# sourceMappingURL=health.d.ts.map