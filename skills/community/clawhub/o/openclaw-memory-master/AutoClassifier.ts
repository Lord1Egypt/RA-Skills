/**
 * Memory-Master Token 优化模块
 *
 * 基于 Mem0/MemOS 最佳实践
 * - 智能 Token 预算分配
 * - 记忆优先级排序
 * - 动态压缩触发
 *
 * 目标：节省 60-70% Token（参考 Mem0/MemOS）
 */
/**
 * 记忆优先级
 */
export declare enum MemoryPriority {
    CRITICAL = 1,// 关键信息（永久保留）
    HIGH = 2,// 重要信息（保留 30 天）
    MEDIUM = 3,// 一般信息（保留 7 天）
    LOW = 4
}
/**
 * Token 预算配置
 */
export interface TokenBudgetConfig {
    maxTokens: number;
    criticalReserve: number;
    compressionThreshold: number;
}
/**
 * 记忆条目（带优先级）
 */
export interface PrioritizedMemory {
    id: string;
    content: string;
    priority: MemoryPriority;
    tokens: number;
    timestamp: number;
    lastAccessed?: number;
    accessCount: number;
}
/**
 * Token 优化器
 */
export declare class TokenOptimizer {
    private config;
    private memoryDir;
    constructor(memoryDir?: string, config?: Partial<TokenBudgetConfig>);
    /**
     * 估算 Token 数
     */
    estimateTokens(text: string): number;
    /**
     * 计算记忆优先级
     */
    calculatePriority(content: string, metadata?: {
        type?: string;
        tags?: string[];
    }): MemoryPriority;
    /**
     * 智能 Token 分配
     */
    allocateTokens(memories: PrioritizedMemory[]): {
        allocated: PrioritizedMemory[];
        saved: number;
    };
    /**
     * 动态压缩触发
     */
    shouldCompress(currentTokens: number): boolean;
    /**
     * 获取压缩建议
     */
    getCompressionSuggestions(memories: PrioritizedMemory[]): CompressionSuggestion[];
    /**
     * 更新访问统计
     */
    updateAccessStats(memoryId: string): void;
    /**
     * 获取访问统计
     */
    getAccessStats(memoryId: string): {
        count: number;
        lastAccess: number;
    } | null;
    /**
     * 清理旧统计
     */
    cleanupOldStats(days?: number): void;
}
/**
 * 压缩建议
 */
export interface CompressionSuggestion {
    id: string;
    action: 'compress' | 'delete' | 'archive';
    reason: string;
    savedTokens: number;
}
/**
 * Token 优化报告
 */
export interface TokenOptimizationReport {
    totalTokens: number;
    allocatedTokens: number;
    savedTokens: number;
    savingsRate: number;
    suggestions: CompressionSuggestion[];
}
/**
 * 生成优化报告
 */
export declare function generateOptimizationReport(memories: PrioritizedMemory[], optimizer: TokenOptimizer): Promise<TokenOptimizationReport>;
export default TokenOptimizer;
