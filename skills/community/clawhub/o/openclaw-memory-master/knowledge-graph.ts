/**
 * Memory-Master v4.0
 *
 * 基于 Karpathy 方法论 + Anthropic 官方经验 + Claude Code 架构
 * 整合 30 篇行业最佳实践笔记
 *
 * @author 小鬼 👻 + Jake
 * @version 4.0.0
 */
import { MemoryCapture, CaptureOptions, CaptureResult } from './capture';
import { MemoryRetriever, RetrieveOptions, RetrieveResult, Memory } from './retrieve';
import { MemoryCompactor, CompactOptions, CompactResult } from './compact';
import { filterSensitiveData, detectSensitiveData, runFilterTests } from './filter';
import { TokenOptimizer, TokenOptimizationReport, generateOptimizationReport } from './token-optimizer';
import { SkillEvolver } from './skill-evolver';
import { PerformanceMonitor, SkillCraftBenchmark, SkillsBenchBenchmark } from './benchmark';
/**
 * Memory-Master 主类
 */
export declare class MemoryMaster {
    private captureModule;
    private retrieveModule;
    private compactor;
    private tokenOptimizer;
    private skillEvolver;
    private monitor;
    private skillCraftBenchmark;
    private skillsBenchBenchmark;
    constructor(memoryDir?: string);
    /**
     * 捕捉记忆
     */
    capture(content: string, options?: CaptureOptions): Promise<CaptureResult>;
    /**
     * 检索记忆
     */
    retrieve(query: string, options?: RetrieveOptions): Promise<RetrieveResult>;
    /**
     * 压缩记忆
     */
    compact(options?: CompactOptions): Promise<CompactResult>;
    /**
     * 过滤敏感数据
     */
    filter(content: string): Promise<import("./filter").FilterResult>;
    /**
     * 检测敏感数据
     */
    detect(content: string): Promise<import("./filter").DetectedSensitive[]>;
    /**
     * Token 优化
     */
    optimizeTokens(): Promise<TokenOptimizationReport>;
    /**
     * 记录经验
     */
    recordExperience(context: string, action: string, result: 'success' | 'failure', feedback?: string): Promise<import("./skill-evolver").Experience>;
    /**
     * 技能蒸馏
     */
    distillSkills(): Promise<import("./skill-evolver").Skill[]>;
    /**
     * 获取评测报告
     */
    getBenchmarkReport(name?: string): Promise<import("./benchmark").BenchmarkResult>;
    /**
     * 运行 SkillCraft 评测
     */
    runSkillCraftBenchmark(tasks: any[]): Promise<{
        accuracy: number;
        efficiency: number;
        report: string;
    }>;
    /**
     * 运行 SkillsBench 评测
     */
    runSkillsBenchBenchmark(tasks: any[]): Promise<{
        byCategory: Record<string, number>;
        byDifficulty: Record<string, number>;
        overall: number;
        report: string;
    }>;
    /**
     * 运行测试
     */
    test(): Promise<void>;
}
/**
 * 导出类型
 */
export { MemoryCapture, MemoryRetriever, MemoryCompactor, TokenOptimizer, SkillEvolver, PerformanceMonitor, SkillCraftBenchmark, SkillsBenchBenchmark, CaptureOptions, CaptureResult, RetrieveOptions, RetrieveResult, CompactOptions, CompactResult, TokenOptimizationReport, Memory, };
/**
 * 导出工具函数
 */
export { filterSensitiveData, detectSensitiveData, runFilterTests, generateOptimizationReport, };
export default MemoryMaster;
