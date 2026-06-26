import type { EOSkill } from '../types/index.js';
export interface OpenClawSkillManifest {
    name: string;
    description: string;
    triggers: string[];
    experts: string[];
    steps?: OpenClawSkillStep[];
    output?: string;
    version?: string;
}
export interface OpenClawSkillStep {
    step: number;
    expert: string;
    input: string;
    output: string;
    verify?: string;
    timeoutMs?: number;
}
/**
 * EO standard commands that map to Claude Code capabilities
 */
export declare const EO_COMMAND_MAPPINGS: Record<string, {
    claudeCodeCommand: string;
    description: string;
    defaultExperts: string[];
}>;
/**
 * Convert an EO Skill to OpenClaw Skill Manifest format
 */
export declare function eoSkillToOpenClawSkill(eoSkill: EOSkill): OpenClawSkillManifest;
/**
 * Convert an OpenClaw Skill Manifest to EO Skill format
 */
export declare function openClawSkillToEoSkill(manifest: OpenClawSkillManifest): EOSkill;
/**
 * Create a skill from an EO command
 */
export declare function createSkillFromCommand(command: string, context?: Record<string, unknown>): OpenClawSkillManifest | null;
/**
 * Parse a skill trigger and extract the command name
 */
export declare function parseSkillTrigger(trigger: string): string | null;
/**
 * Build expert prompt from EO expert definition
 */
export declare function buildExpertPrompt(expertName: string, expertRole: string, task: string, context?: Record<string, unknown>): string;
/**
 * Aggregate results from multiple experts into a coherent output
 */
export declare function aggregateExpertResults(results: Array<{
    expertName: string;
    output: string;
    success: boolean;
}>, command: string): string;
//# sourceMappingURL=skill-adapter.d.ts.map