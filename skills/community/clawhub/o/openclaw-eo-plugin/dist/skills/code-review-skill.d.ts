import type { ExpertResult } from '../types/index.js';
export interface CodeReviewSkillInput {
    files?: string[];
    prUrl?: string;
    focus?: string[];
    depth?: 'quick' | 'standard' | 'deep';
    commit?: string;
    branch?: string;
    repo?: string;
}
export interface CodeReviewSkillContext {
    runtime: {
        subagent: {
            run: (params: {
                sessionKey: string;
                message: string;
                extraSystemPrompt?: string;
                provider?: string;
                model?: string;
            }) => Promise<{
                runId: string;
            }>;
            waitForRun: (params: {
                runId: string;
                timeoutMs?: number;
            }) => Promise<{
                status: string;
                error?: string;
            }>;
            getSessionMessages: (params: {
                sessionKey: string;
                limit?: number;
            }) => Promise<{
                messages: unknown[];
            }>;
        };
    };
    logger: {
        info: (msg: string) => void;
        warn: (msg: string) => void;
        error: (msg: string) => void;
    };
    sessionId?: string;
}
export interface CodeReviewSkillResult {
    success: boolean;
    output: string;
    expertResults: ExpertResult[];
    findings: CodeReviewFinding[];
    durationMs: number;
    error?: string;
}
export interface CodeReviewFinding {
    id: string;
    severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
    category: 'security' | 'performance' | 'correctness' | 'maintainability' | 'style';
    file?: string;
    line?: string;
    description: string;
    suggestion?: string;
}
export declare const codeReviewSkill: {
    name: string;
    description: string;
    expert: string;
    role: string;
    execute(args: string, context: CodeReviewSkillContext): Promise<CodeReviewSkillResult>;
};
//# sourceMappingURL=code-review-skill.d.ts.map