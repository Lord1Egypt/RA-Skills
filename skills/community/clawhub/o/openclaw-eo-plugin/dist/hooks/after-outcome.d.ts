/**
 * After Outcome Hook - Automatic outcome collection v2
 *
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve
 *
 * This hook automatically collects outcomes after tool calls
 * and feeds them to the EffectTracker for scoring
 */
import { type ScoringDecision, type ScoringOutcome } from '../autonomy/index.js';
export type OutcomeHookEvent = {
    type: 'tool_call';
    toolName: string;
    toolParams: Record<string, unknown>;
    success: boolean;
    durationMs: number;
    result?: unknown;
    error?: string;
} | {
    type: 'decision';
    decision: ScoringDecision;
    outcome: ScoringOutcome;
} | {
    type: 'task_complete';
    taskId: string;
    success: boolean;
    metrics?: {
        duration?: number;
        tokens?: number;
        errors?: number;
    };
};
/**
 * AfterOutcomeHook - Automatically collects outcomes
 *
 * Usage:
 * afterOutcomeHook.trigger({ type: 'tool_call', toolName: 'eo_plan', success: true, durationMs: 1234 })
 */
export declare class AfterOutcomeHook {
    private enabled;
    private minScoreThreshold;
    /**
     * Enable/disable the hook
     */
    setEnabled(enabled: boolean): void;
    /**
     * Check if hook is enabled
     */
    isEnabled(): boolean;
    /**
     * Set minimum score threshold for tracking
     */
    setMinScoreThreshold(threshold: number): void;
    /**
     * Trigger outcome collection
     */
    trigger(event: OutcomeHookEvent): void;
    /**
     * Handle tool call outcome
     */
    private handleToolCall;
    /**
     * Handle decision outcome
     */
    private handleDecision;
    /**
     * Handle task completion
     */
    private handleTaskComplete;
    /**
     * Get recent scores summary
     */
    getRecentSummary(): string;
}
export declare const afterOutcomeHook: AfterOutcomeHook;
//# sourceMappingURL=after-outcome.d.ts.map