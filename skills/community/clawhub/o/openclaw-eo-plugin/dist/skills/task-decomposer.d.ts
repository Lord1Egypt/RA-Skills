/**
 * Task Decomposer - Breaks down tasks into最小可执行单元
 *
 * 核心原则：每个最小任务应该在 3-5分钟 内完成
 *
 * 最小任务单元定义：
 * - 单一文件创建/修改
 * - 单一函数实现
 * - 单个测试用例
 * - 单次API调用
 * - 单一配置更新
 */
export interface DecomposedTask {
    id: string;
    name: string;
    description: string;
    estimatedMinutes: number;
    expertType: 'frontend' | 'backend' | 'qa' | 'devops' | 'security' | 'architect' | 'planner';
    dependencies: string[];
    parallelizable: boolean;
    codeLocation?: string;
}
export interface TaskDecomposition {
    originalTask: string;
    totalTasks: number;
    estimatedTotalMinutes: number;
    tasks: DecomposedTask[];
    parallelGroups: string[][];
    criticalPath: string[];
}
/**
 * Task Decomposer class
 */
export declare class TaskDecomposer {
    private static readonly MAX_TASK_MINUTES;
    private static readonly MIN_TASK_MINUTES;
    /**
     * Decompose a task into最小可执行单元
     *
     * @param taskDescription - Original task description
     * @param context - Optional context (codebase, language, framework)
     * @returns TaskDecomposition with broken down tasks
     */
    decompose(taskDescription: string, context?: {
        language?: string;
        framework?: string;
        codebasePath?: string;
    }): TaskDecomposition;
    /**
     * Check if task is feature development
     */
    private isFeatureDevelopment;
    /**
     * Check if task is bug fix
     */
    private isBugFix;
    /**
     * Check if task is refactoring
     */
    private isRefactoring;
    /**
     * Check if task is testing
     */
    private isTesting;
    /**
     * Check if task is deployment
     */
    private isDeployment;
    /**
     * Decompose feature development task
     */
    private decomposeFeature;
    /**
     * Decompose bug fix task
     */
    private decomposeBugFix;
    /**
     * Decompose refactoring task
     */
    private decomposeRefactoring;
    /**
     * Decompose testing task
     */
    private decomposeTesting;
    /**
     * Decompose deployment task
     */
    private decomposeDeployment;
    /**
     * Generic decomposition for unknown task types
     */
    private decomposeGeneric;
    /**
     * Calculate parallel groups based on dependencies
     */
    private calculateParallelGroups;
    /**
     * Calculate critical path (longest path through dependencies)
     */
    private calculateCriticalPath;
    /**
     * Guess file location from task description
     */
    private guessFileLocation;
    /**
     * Format decomposition as markdown for display
     */
    formatAsMarkdown(decomposition: TaskDecomposition): string;
}
export declare const taskDecomposer: TaskDecomposer;
//# sourceMappingURL=task-decomposer.d.ts.map