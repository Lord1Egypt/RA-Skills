// ============================================================================
// EO Progress Executor - Enhanced skill execution with progress reporting
// and chain-dependent task support
// ============================================================================
import { skills } from '../skills/index.js';
import { EXPERTS } from '../experts/data.js';
import { logger } from '../utils/logger.js';
// ---------------------------------------------------------------------------
// Default Logger
// ---------------------------------------------------------------------------
function createDefaultLogger() {
    return {
        info: (msg) => logger.info(`INFO: ${msg}`),
        warn: (msg) => console.warn(`[progress-executor] WARN: ${msg}`),
        error: (msg) => console.error(`[progress-executor] ERROR: ${msg}`),
        debug: (msg) => console.debug(`[progress-executor] DEBUG: ${msg}`),
    };
}
// ---------------------------------------------------------------------------
// Progress Executor
// ---------------------------------------------------------------------------
export class ProgressExecutor {
    activeTasks = new Map();
    /**
     * Execute a skill with progress reporting and adaptive timeout
     */
    async executeWithProgress(options) {
        const { skillName, args, context, timeoutMs = 300000, progressIntervalMs = 30000, maxTimeoutMs = 600000, onProgress, enableChainSignal = true, } = options;
        const logger = context.logger ?? createDefaultLogger();
        const startTime = Date.now();
        // 1. Validate skill
        const skill = skills[skillName];
        if (!skill) {
            return {
                success: false,
                output: '',
                skillName,
                durationMs: Date.now() - startTime,
                expertUsed: [],
                timedOut: false,
                error: `Skill not found: ${skillName}`,
            };
        }
        const taskId = `task-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
        // Register active task
        this.activeTasks.set(taskId, {
            startTime,
            skillName,
            status: 'running',
            lastProgress: 0,
            timeoutMs,
        });
        logger.info(`[execute-with-progress] Starting skill="${skillName}" taskId="${taskId}" baseTimeout=${timeoutMs}ms`);
        // 2. Build execution context with progress hook
        const execContext = {
            runtime: context.runtime,
            logger,
            sessionId: context.sessionId,
        };
        // 3. Execute with progress monitoring loop
        let elapsed = 0;
        let currentTimeout = timeoutMs;
        let lastProgressReport = 0;
        let adaptiveExtensions = 0;
        const maxExtensions = Math.floor((maxTimeoutMs - timeoutMs) / progressIntervalMs);
        const reportProgress = (stage, message, progress, canExtend = true) => {
            const update = {
                skillName,
                stage,
                elapsedMs: elapsed,
                progress,
                message,
                canExtend,
            };
            // Update task tracking
            const task = this.activeTasks.get(taskId);
            if (task) {
                task.lastProgress = progress;
            }
            if (onProgress) {
                onProgress(update);
            }
            else {
                logger.info(`[progress] ${stage}: ${message} (${progress}%, ${elapsed}ms elapsed)`);
            }
            lastProgressReport = Date.now();
        };
        try {
            // Start the skill execution in background
            const skillPromise = skill.execute(args, execContext);
            // Progress monitoring loop
            while (elapsed < maxTimeoutMs) {
                // Check if skill already completed
                const settled = await Promise.race([
                    skillPromise,
                    new Promise(resolve => setTimeout(() => resolve('timeout'), Math.min(currentTimeout, progressIntervalMs))),
                ]);
                if (settled !== 'timeout') {
                    // Skill completed
                    const result = await skillPromise;
                    const expertUsed = this.resolveExpert(skill.expert);
                    const output = typeof result === 'string' ? result : result.output ?? '';
                    const success = typeof result === 'string' ? true : result.success !== false;
                    this.activeTasks.delete(taskId);
                    reportProgress('completed', 'Skill completed successfully', 100, false);
                    logger.info(`[execute-with-progress] Completed skill="${skillName}" success=${success} durationMs=${Date.now() - startTime}`);
                    return {
                        success,
                        output,
                        skillName,
                        durationMs: Date.now() - startTime,
                        expertUsed,
                        timedOut: false,
                    };
                }
                // Timeout reached - check if we should continue
                elapsed += currentTimeout;
                // Calculate current progress estimate
                const estimatedProgress = Math.min(95, (elapsed / maxTimeoutMs) * 100);
                // Determine if we should extend timeout
                const shouldExtend = adaptiveExtensions < maxExtensions &&
                    this.activeTasks.get(taskId)?.status === 'running' &&
                    this.activeTasks.get(taskId)?.lastProgress < 100;
                if (shouldExtend) {
                    adaptiveExtensions++;
                    currentTimeout = progressIntervalMs;
                    reportProgress('executing', `Still running... (extended ${adaptiveExtensions}/${maxExtensions}, ${elapsed}ms elapsed)`, estimatedProgress, true);
                    logger.info(`[execute-with-progress] Extended timeout for skill="${skillName}" extension=${adaptiveExtensions} elapsed=${elapsed}ms`);
                }
                else {
                    // Max timeout reached - return current state
                    this.activeTasks.delete(taskId);
                    reportProgress('timeout_wait', `Max timeout reached (${maxTimeoutMs}ms), task may still be running`, estimatedProgress, false);
                    logger.warn(`[execute-with-progress] Timed out skill="${skillName}" after ${elapsed}ms`);
                    return {
                        success: false,
                        output: `Task timed out after ${elapsed}ms. The task may still be running in background.`,
                        skillName,
                        durationMs: elapsed,
                        expertUsed: [skill.expert],
                        timedOut: true,
                        error: `Timeout after ${elapsed}ms (base: ${timeoutMs}ms, max: ${maxTimeoutMs}ms, extensions: ${adaptiveExtensions})`,
                    };
                }
            }
            // Should not reach here, but handle it
            return {
                success: false,
                output: 'Max timeout exceeded',
                skillName,
                durationMs: elapsed,
                expertUsed: [skill.expert],
                timedOut: true,
                error: 'Max timeout exceeded',
            };
        }
        catch (err) {
            this.activeTasks.delete(taskId);
            const errorMsg = err instanceof Error ? err.message : String(err);
            logger.error(`[execute-with-progress] Failed skill="${skillName}" error="${errorMsg}"`);
            return {
                success: false,
                output: '',
                skillName,
                durationMs: Date.now() - startTime,
                expertUsed: [skill.expert],
                timedOut: false,
                error: errorMsg,
            };
        }
    }
    /**
     * Get status of all active tasks
     */
    getActiveTasks() {
        const now = Date.now();
        return Array.from(this.activeTasks.entries()).map(([taskId, task]) => ({
            taskId,
            skillName: task.skillName,
            elapsedMs: now - task.startTime,
            status: task.status,
            lastProgress: task.lastProgress,
        }));
    }
    /**
     * Check if a task is still running
     */
    isTaskRunning(taskId) {
        const task = this.activeTasks.get(taskId);
        return task?.status === 'running';
    }
    /**
     * Resolve expert ID to name(s)
     */
    resolveExpert(expertId) {
        const expert = EXPERTS[expertId];
        if (expert)
            return [expert.name];
        const roleKey = expertId.toLowerCase();
        const matchingExperts = Object.values(EXPERTS).filter(e => e.role === roleKey);
        if (matchingExperts.length > 0) {
            return matchingExperts.map(e => e.name);
        }
        return [expertId];
    }
}
// ---------------------------------------------------------------------------
// Chain Signal Manager - For dependent task coordination
// ---------------------------------------------------------------------------
export class ChainSignalManager {
    signals = new Map();
    logger = createDefaultLogger();
    /**
     * Create a new chain signal for a task
     */
    createSignal(taskId, stages = ['start', 'progress', 'complete']) {
        const signal = {
            taskId,
            status: 'pending',
            stages: new Map(stages.map(s => [s, { completed: false }])),
            listeners: new Set(),
            maxStages: stages.length,
        };
        this.signals.set(taskId, signal);
        this.logger.info(`[chain-signal] Created signal for task="${taskId}" stages=${stages.join(',')}`);
        return signal;
    }
    /**
     * Get a chain signal
     */
    getSignal(taskId) {
        return this.signals.get(taskId);
    }
    /**
     * Update signal stage - call this from the executing task
     */
    updateStage(taskId, stageName, output) {
        const signal = this.signals.get(taskId);
        if (!signal) {
            this.logger.warn(`[chain-signal] Signal not found for task="${taskId}"`);
            return false;
        }
        const stage = signal.stages.get(stageName);
        if (!stage) {
            this.logger.warn(`[chain-signal] Stage "${stageName}" not found in task="${taskId}"`);
            return false;
        }
        stage.completed = true;
        if (output !== undefined) {
            stage.output = output;
        }
        this.logger.info(`[chain-signal] Stage "${stageName}" completed for task="${taskId}"`);
        // Notify all listeners
        for (const listener of signal.listeners) {
            try {
                listener(signal);
            }
            catch (err) {
                this.logger.error(`[chain-signal] Listener error: ${err}`);
            }
        }
        // Check if all stages completed
        const allCompleted = Array.from(signal.stages.values()).every(s => s.completed);
        if (allCompleted) {
            signal.status = 'completed';
            this.logger.info(`[chain-signal] All stages completed for task="${taskId}"`);
        }
        return true;
    }
    /**
     * Subscribe to signal changes - for dependent tasks
     */
    subscribe(taskId, callback) {
        const signal = this.signals.get(taskId);
        if (!signal) {
            this.logger.warn(`[chain-signal] Cannot subscribe - signal not found for task="${taskId}"`);
            return () => { };
        }
        signal.listeners.add(callback);
        this.logger.info(`[chain-signal] Subscribed to task="${taskId}" (${signal.listeners.size} listeners)`);
        // Return unsubscribe function
        return () => {
            signal.listeners.delete(callback);
        };
    }
    /**
     * Wait for a specific stage to complete
     */
    async waitForStage(taskId, stageName, timeoutMs = 120000) {
        const signal = this.signals.get(taskId);
        if (!signal) {
            return { completed: false };
        }
        const stage = signal.stages.get(stageName);
        if (!stage) {
            return { completed: false };
        }
        // If already completed, return immediately
        if (stage.completed) {
            return { completed: true, output: stage.output };
        }
        // Wait for completion
        return new Promise((resolve) => {
            const timeout = setTimeout(() => {
                unsubscribe();
                resolve({ completed: false });
            }, timeoutMs);
            const unsubscribe = this.subscribe(taskId, (sig) => {
                const st = sig.stages.get(stageName);
                if (st?.completed) {
                    clearTimeout(timeout);
                    unsubscribe();
                    resolve({ completed: true, output: st.output });
                }
            });
        });
    }
    /**
     * Clean up completed signals
     */
    cleanup(olderThanMs = 3600000) {
        const now = Date.now();
        for (const [taskId, signal] of this.signals.entries()) {
            if (signal.status === 'completed' || signal.status === 'failed') {
                // Check if we should clean up (simple heuristic: no listeners = can clean)
                if (signal.listeners.size === 0) {
                    this.signals.delete(taskId);
                    this.logger.debug(`[chain-signal] Cleaned up signal for task="${taskId}"`);
                }
            }
        }
    }
}
// ---------------------------------------------------------------------------
// Convenience Functions
// ---------------------------------------------------------------------------
export const progressExecutor = new ProgressExecutor();
export const chainSignalManager = new ChainSignalManager();
/**
 * Execute a skill with standard timeout and progress reporting
 * Simple wrapper for backwards compatibility
 */
export async function executeWithProgressReporting(options) {
    return progressExecutor.executeWithProgress(options);
}
/**
 * Create a chain signal and return stage trigger functions
 */
export function createChainTask(options) {
    const { taskId, stages = ['start', 'progress', 'complete'] } = options;
    const signal = chainSignalManager.createSignal(taskId, stages);
    return {
        signal,
        triggerStage: (stageName, output) => chainSignalManager.updateStage(taskId, stageName, output),
        waitForStage: (stageName, timeoutMs) => chainSignalManager.waitForStage(taskId, stageName, timeoutMs),
    };
}
//# sourceMappingURL=progress-executor.js.map