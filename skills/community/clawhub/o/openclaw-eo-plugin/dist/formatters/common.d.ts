/**
 * Common Formatters
 * Shared helper functions for output formatting
 */
import type { ExpertResult } from '../skills/multi-expert-orchestrator.js';
export { textResult, errorResult };
declare function textResult(text: string, details?: Record<string, unknown>): {
    content: {
        type: "text";
        text: string;
    }[];
    details: Record<string, unknown>;
};
declare function errorResult(text: string): {
    content: {
        type: "text";
        text: string;
    }[];
    details: {
        success: boolean;
    };
};
export declare function formatDuration(durationMs: number): string;
export declare function formatExpertResults(results: ExpertResult[]): {
    succeeded: ExpertResult[];
    failed: ExpertResult[];
};
export declare function formatSucceededSection(succeeded: ExpertResult[], lines: string[]): void;
export declare function formatFailedSection(failed: ExpertResult[], lines: string[]): void;
export declare function formatNextSteps(steps: string[], lines: string[]): void;
export declare function formatHeader(title: string, meta: Record<string, string>, lines: string[]): void;
//# sourceMappingURL=common.d.ts.map