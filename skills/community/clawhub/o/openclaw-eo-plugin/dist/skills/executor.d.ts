import { type SkillName, type SkillContext } from './index.js';
export interface PluginContext extends SkillContext {
    pluginId: string;
    userId?: string;
    channel?: string;
    workspace?: string;
}
export interface ExecuteOptions {
    skillName: SkillName;
    args: string;
    context: PluginContext;
    /** Override default expert team (comma-separated expert IDs) */
    teamOverride?: string;
    /** Timeout in ms (default: 300000) */
    timeoutMs?: number;
    /** Use progress reporting for long tasks (default: true for timeout >= 180000ms) */
    useProgressReporting?: boolean;
    /** Progress report interval in ms (default: 30000) */
    progressIntervalMs?: number;
    /** Callback for progress updates */
    onProgress?: (update: any) => void;
}
export interface ExecuteResult {
    success: boolean;
    output: string;
    skillName: SkillName;
    durationMs: number;
    expertUsed: string[];
    error?: string;
}
/**
 * Execute a skill by name with the given arguments and context.
 *
 * Core logic:
 * 1. Validate skill exists in registry
 * 2. Resolve expert from skill definition
 * 3. For long tasks (timeout >= 180000ms): use progress reporting
 * 4. For short tasks: use simple Promise.race timeout
 * 5. Return structured result with timing and expert info
 */
export declare function executeSkill(options: ExecuteOptions): Promise<ExecuteResult>;
/**
 * Execute multiple skills in parallel and aggregate results.
 */
export declare function executeSkillsBatch(requests: Omit<ExecuteOptions, 'context'>[], context: PluginContext): Promise<ExecuteResult[]>;
/**
 * Simple command router that executes a skill by name with string args.
 * Convenience wrapper for command-style invocations.
 */
export declare function routeSkillCommand(command: string, args: string, context: PluginContext): Promise<string>;
//# sourceMappingURL=executor.d.ts.map