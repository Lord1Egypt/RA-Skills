import type { ExpertResult, CheckpointResult } from '../types/index.js';
export interface VerifySkillInput {
    target: string;
    type: 'code' | 'architecture' | 'test' | 'security' | 'performance' | 'accessibility';
    criteria?: string[];
    depth?: 'quick' | 'standard' | 'deep';
}
export interface VerifySkillContext {
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
export interface VerifySkillResult {
    success: boolean;
    output: string;
    expertResults: ExpertResult[];
    checkpointResults: CheckpointResult[];
    durationMs: number;
    overallPassed: boolean;
    error?: string;
}
export declare const verifySkill: {
    name: string;
    description: string;
    expert: string;
    role: string;
    execute(args: string, context: VerifySkillContext): Promise<VerifySkillResult>;
};
//# sourceMappingURL=verify-skill.d.ts.map