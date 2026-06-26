/**
 * Memory-Master 评测基准模块
 *
 * 基于 SkillCraft / SkillsBench 论文
 * - 基础评测指标
 * - 性能监控
 * - 质量报告
 */
/**
 * 评测指标
 */
export interface Metrics {
    retrievalAccuracy?: number;
    relevanceScore?: number;
    avgResponseTime?: number;
    p95ResponseTime?: number;
    p99ResponseTime?: number;
    tokenSavingsRate?: number;
    compressionRate?: number;
    userSatisfaction?: number;
    errorRate?: number;
}
/**
 * 评测结果
 */
export interface BenchmarkResult {
    id: string;
    name: string;
    timestamp: number;
    metrics: Metrics;
    details?: Record<string, any>;
}
/**
 * 性能监控器
 */
export declare class PerformanceMonitor {
    private metricsFile;
    private responseTimes;
    constructor(memoryDir?: string);
    /**
     * 记录响应时间
     */
    recordResponseTime(timeMs: number): void;
    /**
     * 记录检索准确性
     */
    recordRetrievalAccuracy(isRelevant: boolean): void;
    /**
     * 记录 Token 使用
     */
    recordTokenUsage(original: number, optimized: number): void;
    /**
     * 记录错误
     */
    recordError(errorType: string): void;
    /**
     * 获取当前指标
     */
    getMetrics(): Metrics;
    /**
     * 计算响应时间统计
     */
    private calculateResponseTimeStats;
    /**
     * 生成评测报告
     */
    generateBenchmarkReport(name?: string): BenchmarkResult;
    /**
     * 保存评测报告
     */
    saveBenchmarkReport(report: BenchmarkResult): void;
    /**
     * 加载指标
     */
    private loadMetrics;
    /**
     * 保存指标
     */
    private saveMetrics;
    /**
     * 生成 ID
     */
    private generateId;
    /**
     * 清理旧报告
     */
    cleanupOldReports(days?: number): void;
}
/**
 * SkillCraft 风格评测
 */
export declare class SkillCraftBenchmark {
    private monitor;
    constructor(memoryDir?: string);
    /**
     * 评测工具使用能力
     */
    evaluateToolUsage(tasks: Array<{
        name: string;
        context: string;
        expectedTool: string;
    }>): Promise<{
        accuracy: number;
        efficiency: number;
        report: string;
    }>;
    /**
     * 执行任务（模拟）
     */
    private executeTask;
    /**
     * 生成 SkillCraft 报告
     */
    private generateSkillCraftReport;
}
/**
 * SkillsBench 风格评测
 */
export declare class SkillsBenchBenchmark {
    private monitor;
    constructor(memoryDir?: string);
    /**
     * 跨任务技能评测
     */
    evaluateAcrossTasks(tasks: Array<{
        category: string;
        name: string;
        difficulty: 'easy' | 'medium' | 'hard';
    }>): Promise<{
        byCategory: Record<string, number>;
        byDifficulty: Record<string, number>;
        overall: number;
        report: string;
    }>;
    /**
     * 执行任务（模拟）
     */
    private executeTasks;
    /**
     * 生成 SkillsBench 报告
     */
    private generateSkillsBenchReport;
}
