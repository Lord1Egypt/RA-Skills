// ============================================================================
// EO Task Distributor - Phase 3.3: Automatic Task Distribution
//
// Implements automatic task distribution based on expert types,
// load balancing, and result aggregation.
// ============================================================================
import { knowledgeGraph } from './knowledge-graph.js';
import { AgentCoordinator } from '../autonomy/agent-coordinator.js';
import { chainSignalManager, createChainTask } from '../workflow/progress-executor.js';
// ============================================================================
// Task Queue with Priority
// ============================================================================
class PriorityTaskQueue {
    tasks = new Map();
    add(task) {
        const distributed = {
            ...task,
            status: 'pending',
            assignedExperts: [],
            pendingExperts: [],
            completedExperts: [],
            results: new Map(),
            progress: 0,
            createdAt: Date.now(),
        };
        this.tasks.set(task.id, distributed);
        return distributed;
    }
    get(id) {
        return this.tasks.get(id);
    }
    update(id, updates) {
        const task = this.tasks.get(id);
        if (!task)
            return false;
        Object.assign(task, updates);
        return true;
    }
    remove(id) {
        return this.tasks.delete(id);
    }
    getPending() {
        return Array.from(this.tasks.values())
            .filter(t => t.status === 'pending' || t.status === 'distributing')
            .sort((a, b) => this.priorityValue(b) - this.priorityValue(a));
    }
    getInProgress() {
        return Array.from(this.tasks.values())
            .filter(t => t.status === 'in_progress');
    }
    getAll() {
        return Array.from(this.tasks.values());
    }
    priorityValue(task) {
        const pMap = { critical: 4, high: 3, normal: 2, low: 1 };
        let value = pMap[task.priority];
        if (task.deadline) {
            const timeLeft = task.deadline - Date.now();
            value += timeLeft > 0 ? timeLeft / 1000000 : -1000;
        }
        return value;
    }
}
// ============================================================================
// Task Distributor (Main Class)
// ============================================================================
export class TaskDistributor {
    taskQueue;
    coordinator;
    knowledgeGraph;
    aggregationConfig;
    constructor(coordinator, knowledgeGraph, aggregationConfig) {
        this.taskQueue = new PriorityTaskQueue();
        this.coordinator = coordinator;
        this.knowledgeGraph = knowledgeGraph;
        this.aggregationConfig = {
            method: 'weighted',
            maxOutputLength: 10000,
            includeConfidences: true,
            includeMinorityOpinions: true,
            ...aggregationConfig,
        };
    }
    // ============================================================================
    // Task Submission
    // ============================================================================
    /**
     * Submit a new task for distribution.
     */
    submitTask(task) {
        const id = 'task-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6);
        const fullTask = {
            ...task,
            id,
            createdAt: Date.now(),
        };
        const distributed = this.taskQueue.add(fullTask);
        return distributed;
    }
    /**
     * Submit multiple tasks.
     */
    submitTasks(tasks) {
        return tasks.map(t => this.submitTask(t));
    }
    // ============================================================================
    // Chain Task Support (for dependent multi-expert workflows)
    // ============================================================================
    /**
     * Submit a task with chain signal stages for dependent task coordination.
     * This allows downstream tasks to start preparation when upstream stages complete.
     *
     * @param task - Task specification
     * @param stages - Array of stage names that dependent tasks can wait on
     * @returns Object with task info and chain signal controls
     */
    submitChainTask(task, stages = ['start', 'progress', 'complete']) {
        // Submit the base task
        const distributedTask = this.submitTask(task);
        // Create chain signal for this task
        const chainResult = createChainTask({
            taskId: distributedTask.id,
            skillName: task.type, // Type compatibility
            args: '',
            context: {},
            stages,
        });
        // Update task status when chain completes
        chainResult.signal.listeners.add((signal) => {
            if (signal.status === 'completed') {
                this.taskQueue.update(distributedTask.id, {
                    status: 'completed',
                    progress: 1,
                });
            }
        });
        return {
            distributedTask,
            chainSignal: chainResult.signal,
            triggerStage: chainResult.triggerStage,
            waitForStage: chainResult.waitForStage,
            cleanup: () => chainSignalManager.cleanup(),
        };
    }
    /**
     * Wait for a dependency task to reach a specific stage before proceeding.
     * This enables "partial completion" where dependent tasks can start once a
     * critical stage (e.g., 'analyze') is done, without waiting for full completion.
     *
     * @param dependencyTaskId - The task ID to wait on
     * @param stageName - The stage name to wait for
     * @param timeoutMs - Max time to wait (default: 120000ms)
     * @returns Stage result if completed, or timeout indicator
     */
    async waitForDependencyStage(dependencyTaskId, stageName, timeoutMs = 120000) {
        const result = await chainSignalManager.waitForStage(dependencyTaskId, stageName, timeoutMs);
        return {
            ready: result.completed,
            output: result.output,
            timedOut: !result.completed,
        };
    }
    /**
     * Create a dependency chain between tasks where Task B can start its
     * preparation when Task A reaches a specific stage.
     *
     * @param taskA - First task (upstream)
     * @param taskB - Second task (downstream, depends on A)
     * @param unlockStageA - Stage in taskA that unlocks taskB
     * @param stagesA - Stages for taskA's chain signal
     * @returns Both chain task handles
     */
    createDependencyChain(taskA, taskB, unlockStageA = 'complete', stagesA = ['start', 'analyze', 'execute', 'complete']) {
        // Submit task A with chain signal
        const chainA = this.submitChainTask(taskA, stagesA);
        // Set task B to depend on task A's completion stage
        const taskBWithDeps = {
            ...taskB,
            dependencies: [...(taskB.dependencies || []), chainA.distributedTask.id],
        };
        const chainB = this.submitChainTask(taskBWithDeps);
        // Create unlock function
        const unlockTaskB = async () => {
            await this.waitForDependencyStage(chainA.distributedTask.id, unlockStageA);
        };
        return {
            chainA,
            chainB,
            unlockTaskB,
        };
    }
    // ============================================================================
    // Distribution Logic
    // ============================================================================
    /**
     * Distribute a task to available experts.
     */
    distribute(taskId) {
        const task = this.taskQueue.get(taskId);
        if (!task)
            return null;
        // Check dependencies
        if (task.dependencies && task.dependencies.length > 0) {
            const pendingDeps = task.dependencies.filter(depId => {
                const dep = this.taskQueue.get(depId);
                return dep && dep.status !== 'completed';
            });
            if (pendingDeps.length > 0) {
                return null; // Dependencies not met
            }
        }
        // Get available agents
        const allAgents = this.coordinator.getAllAgents();
        const availableAgents = allAgents
            .filter(a => a.isAvailable && a.currentLoad < 0.9)
            .sort((a, b) => this.matchScore(b) - this.matchScore(a));
        // Match task to best experts
        const selectedAgents = this.selectExperts(task, availableAgents);
        if (selectedAgents.length < task.minExperts) {
            // Not enough experts available
            this.taskQueue.update(taskId, {
                status: 'pending',
                pendingExperts: task.requiredExpertTypes,
            });
            return {
                taskId,
                success: false,
                assignedExperts: [],
                pendingAssignments: task.requiredExpertTypes,
                loadAfterDistribution: new Map(),
                estimatedCompletionMs: -1,
            };
        }
        // Assign task to selected experts
        const assigned = [];
        const loadAfter = new Map();
        selectedAgents.forEach(agent => {
            if (this.coordinator.assignTaskToAgent(taskId, agent.id)) {
                assigned.push(agent.id);
                loadAfter.set(agent.id, agent.currentLoad + 0.2);
            }
        });
        // Update task
        this.taskQueue.update(taskId, {
            status: 'distributing',
            assignedExperts: assigned,
            pendingExperts: [],
        });
        // Calculate estimated completion
        const avgLoad = Array.from(loadAfter.values()).reduce((a, b) => a + b, 0) / loadAfter.size;
        const estimatedCompletionMs = task.timeoutMs * (1 + avgLoad);
        return {
            taskId,
            success: true,
            assignedExperts: selectedAgents.slice(0, assigned.length),
            pendingAssignments: [],
            loadAfterDistribution: loadAfter,
            estimatedCompletionMs,
        };
    }
    /**
     * Auto-distribute all pending tasks.
     */
    autoDistribute() {
        const results = [];
        const pending = this.taskQueue.getPending();
        pending.forEach(task => {
            const result = this.distribute(task.id);
            if (result)
                results.push(result);
        });
        return results;
    }
    /**
     * Select best experts for a task based on requirements and load.
     */
    selectExperts(task, availableAgents) {
        const selected = [];
        const assignedRoles = new Set();
        // First pass: select preferred experts if specified
        if (task.preferredExpertIds) {
            const preferred = availableAgents.filter(a => task.preferredExpertIds.includes(a.id));
            selected.push(...preferred.slice(0, Math.min(2, task.maxExperts)));
            preferred.forEach(a => assignedRoles.add(a.role));
        }
        // Second pass: fill remaining slots with required roles
        for (const agent of availableAgents) {
            if (selected.length >= task.maxExperts)
                break;
            if (selected.some(a => a.id === agent.id))
                continue;
            // Check if this agent's role is needed
            const roleMatch = task.requiredExpertTypes.some(required => agent.role.includes(required) ||
                agent.expertise.some(e => e.includes(required)));
            if (roleMatch || assignedRoles.size < task.minExperts) {
                selected.push(agent);
                if (roleMatch)
                    assignedRoles.add(agent.role);
            }
        }
        return selected;
    }
    /**
     * Calculate how well an agent matches a task (relevance score).
     */
    matchScore(agent) {
        // Lower load = higher score
        const loadScore = 1 - agent.currentLoad;
        // Availability bonus
        const availabilityScore = agent.isAvailable ? 1 : 0.5;
        return loadScore * availabilityScore;
    }
    // ============================================================================
    // Result Collection
    // ============================================================================
    /**
     * Submit a result for a task.
     */
    submitResult(taskId, result) {
        const task = this.taskQueue.get(taskId);
        if (!task)
            return false;
        const fullResult = {
            ...result,
            timestamp: Date.now(),
        };
        task.results.set(result.expertId, fullResult);
        // Release agent load
        this.coordinator.releaseAgent(result.expertId);
        // Check if all experts completed
        if (task.results.size >= task.assignedExperts.length) {
            this.taskQueue.update(taskId, {
                status: 'aggregating',
                progress: 0.9,
            });
        }
        return true;
    }
    // ============================================================================
    // Result Aggregation
    // ============================================================================
    /**
     * Aggregate results from all experts into a final output.
     */
    aggregate(taskId) {
        const task = this.taskQueue.get(taskId);
        if (!task || task.results.size === 0)
            return null;
        const startTime = task.startedAt || task.createdAt;
        // Gather all results
        const results = Array.from(task.results.values());
        const successResults = results.filter(r => r.success);
        const failedCount = results.length - successResults.length;
        // Generate aggregated output based on method
        let primaryOutput;
        let confidence;
        let consensus;
        switch (this.aggregationConfig.method) {
            case 'concatenate':
                primaryOutput = this.aggregateConcatenate(successResults);
                confidence = successResults.length / task.assignedExperts.length;
                break;
            case 'weighted':
                ({ output: primaryOutput, confidence } = this.aggregateWeighted(successResults));
                break;
            case 'consensus':
                ({ output: primaryOutput, confidence, consensus } = this.aggregateConsensus(successResults));
                break;
            case 'hierarchical':
                primaryOutput = this.aggregateHierarchical(successResults);
                confidence = successResults.reduce((sum, r) => sum + r.confidence, 0) / successResults.length;
                break;
            default:
                primaryOutput = this.aggregateConcatenate(successResults);
                confidence = 0.5;
        }
        // Collect recommendations
        const recommendations = this.collectRecommendations(successResults);
        // Update task status
        this.taskQueue.update(taskId, {
            status: failedCount > 0 ? 'completed' : 'completed',
            progress: 1,
            completedAt: Date.now(),
        });
        return {
            taskId,
            success: successResults.length > 0,
            primaryOutput,
            expertOutputs: results,
            consensus,
            confidence,
            recommendations,
            durationMs: Date.now() - startTime,
            timestamp: Date.now(),
        };
    }
    aggregateConcatenate(results) {
        return results
            .map(r => `## ${r.expertName} (${r.expertRole})\n\n${r.output || 'No output'}\n\n---\n`)
            .join('\n')
            .slice(0, this.aggregationConfig.maxOutputLength);
    }
    aggregateWeighted(results) {
        // Sort by confidence
        const sorted = [...results].sort((a, b) => b.confidence - a.confidence);
        // Weight output sections by confidence
        const sections = sorted.map(r => {
            const weight = Math.round(r.confidence * 100);
            return `[${weight}% confidence] ${r.expertName}: ${r.output || r.keyPoints.join('; ')}`;
        });
        const totalConfidence = results.reduce((sum, r) => sum + r.confidence, 0) / results.length;
        return {
            output: sections.join('\n\n'),
            confidence: totalConfidence,
        };
    }
    aggregateConsensus(results) {
        // Find common key points
        const allPoints = results.flatMap(r => r.keyPoints);
        const pointCounts = new Map();
        allPoints.forEach(point => {
            pointCounts.set(point, (pointCounts.get(point) || 0) + 1);
        });
        // Find agreement level
        const agreement = Math.max(...Array.from(pointCounts.values())) / results.length;
        let level;
        if (agreement >= 0.9)
            level = 'unanimous';
        else if (agreement >= 0.7)
            level = 'strong';
        else if (agreement >= 0.5)
            level = 'majority';
        else
            level = 'plurality';
        // Identify conflicts
        const conflicts = [];
        const lowConfidenceResults = results.filter(r => r.confidence < 0.5);
        if (lowConfidenceResults.length > 0) {
            conflicts.push(`${lowConfidenceResults.length} experts expressed low confidence`);
        }
        // Find points that appear frequently (consensus points)
        const consensusPoints = Array.from(pointCounts.entries())
            .filter(([_, count]) => count >= results.length * 0.5)
            .map(([point]) => point);
        const output = consensusPoints.length > 0
            ? consensusPoints.map(p => `- ${p}`).join('\n')
            : results[0]?.output || 'No consensus reached';
        const avgConfidence = results.reduce((sum, r) => sum + r.confidence, 0) / results.length;
        return {
            output,
            confidence: avgConfidence * agreement,
            consensus: { level, agreement, conflicts: conflicts.length > 0 ? conflicts : undefined },
        };
    }
    aggregateHierarchical(results) {
        // Group by role
        const byRole = new Map();
        results.forEach(r => {
            if (!byRole.has(r.expertRole))
                byRole.set(r.expertRole, []);
            byRole.get(r.expertRole).push(r);
        });
        // Summarize each role's perspective
        const summaries = [];
        byRole.forEach((roleResults, role) => {
            const avgConfidence = roleResults.reduce((s, r) => s + r.confidence, 0) / roleResults.length;
            const combinedOutput = roleResults.map(r => r.output).join('\n');
            summaries.push(`### ${role} (${(avgConfidence * 100).toFixed(0)}% confidence)\n\n${combinedOutput}`);
        });
        return summaries.join('\n\n---\n\n');
    }
    collectRecommendations(results) {
        const recommendations = [];
        results.forEach(r => {
            if (r.suggestions)
                recommendations.push(...r.suggestions);
        });
        // Deduplicate
        return [...new Set(recommendations)];
    }
    // ============================================================================
    // Status & Monitoring
    // ============================================================================
    /**
     * Get task status.
     */
    getTaskStatus(taskId) {
        return this.taskQueue.get(taskId);
    }
    /**
     * Get all tasks.
     */
    getAllTasks() {
        return this.taskQueue.getAll();
    }
    /**
     * Get pending tasks count.
     */
    getPendingCount() {
        return this.taskQueue.getPending().length;
    }
    /**
     * Get in-progress tasks count.
     */
    getInProgressCount() {
        return this.taskQueue.getInProgress().length;
    }
    /**
     * Cancel a task.
     */
    cancel(taskId) {
        const task = this.taskQueue.get(taskId);
        if (!task)
            return false;
        // Release all assigned agents
        task.assignedExperts.forEach(expertId => {
            this.coordinator.releaseAgent(expertId);
        });
        return this.taskQueue.remove(taskId);
    }
}
// ============================================================================
// Global Instance
// ============================================================================
export const taskDistributor = new TaskDistributor(new AgentCoordinator(), knowledgeGraph);
export default TaskDistributor;
//# sourceMappingURL=task-distributor.js.map