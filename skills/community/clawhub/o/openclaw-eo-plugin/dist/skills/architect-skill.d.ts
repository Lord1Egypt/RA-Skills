import type { ExpertResult } from '../types/index.js';
export interface ArchitectSkillInput {
    task: string;
    style?: 'monolithic' | 'microservices' | 'serverless' | 'event-driven' | 'layered';
    language?: string;
    cloud?: 'aws' | 'gcp' | 'azure' | 'multi-cloud' | 'on-premise';
    constraints?: string[];
}
export interface ArchitectSkillContext {
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
export interface ArchitectSkillResult {
    success: boolean;
    output: string;
    expertResults: ExpertResult[];
    durationMs: number;
    architecture?: ArchitectureSummary;
    error?: string;
}
export interface ArchitectureSummary {
    style: string;
    language: string;
    layers: ArchitectureLayer[];
    modules: ArchitectureModule[];
    risks: ArchitectureRisk[];
}
export interface ArchitectureLayer {
    name: string;
    responsibility: string;
    technologies: string[];
}
export interface ArchitectureModule {
    name: string;
    responsibility: string;
    api?: string;
    dependencies: string[];
}
export interface ArchitectureRisk {
    name: string;
    impact: 'low' | 'medium' | 'high';
    probability: 'low' | 'medium' | 'high';
    mitigation: string;
}
export declare const architectSkill: {
    name: string;
    description: string;
    expert: string;
    role: string;
    execute(args: string, context: ArchitectSkillContext): Promise<ArchitectSkillResult>;
};
//# sourceMappingURL=architect-skill.d.ts.map