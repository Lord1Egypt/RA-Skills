/** Build a summary of recent auto-captures and episodes. */
export declare function buildConsolidationContext(): string;
/**
 * Initialize the sleep cycle system.
 * Runs maintenance on startup + schedules a daily check via setInterval.
 * No child_process — all maintenance runs in-process.
 */
export declare function ensureSleepCycle(): Promise<void>;
