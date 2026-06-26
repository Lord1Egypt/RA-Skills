/**
 * Memory-Master 记忆压缩模块
 *
 * 基于 Claude Code 六层压缩设计
 * 简化为 3 阶段压缩：
 * - L1: 原始记录（保留 7 天）
 * - L2: 摘要提炼（保留 30 天）
 * - L3: 关键事实（永久保留）
 */
/**
 * 压缩级别
 */
export type CompactLevel = 'L1' | 'L2' | 'L3';
/**
 * 压缩选项
 */
export interface CompactOptions {
    force?: boolean;
    level?: CompactLevel;
    dryRun?: boolean;
}
/**
 * 压缩结果
 */
export interface CompactResult {
    success: boolean;
    compressed: number;
    savedTokens: number;
    compressionRate: number;
    details?: CompactDetail[];
}
/**
 * 压缩详情
 */
export interface CompactDetail {
    id: string;
    from: string;
    to: string;
    savedTokens: number;
    level: CompactLevel;
}
/**
 * 记忆压缩器
 */
export declare class MemoryCompactor {
    private memoryDir;
    constructor(memoryDir?: string);
    /**
     * 执行压缩
     */
    compact(options?: CompactOptions): Promise<CompactResult>;
    /**
     * 压缩内容
     */
    private compressContent;
    /**
     * 压缩单条记忆
     */
    private compressMemory;
    /**
     * 生成摘要
     */
    private generateSummary;
    /**
     * 提取关键事实
     */
    private extractKeyFacts;
    /**
     * 应用压缩
     */
    private applyCompression;
    /**
     * 提取记忆
     */
    private extractMemories;
    /**
     * 估算 token 数
     */
    private estimateTokens;
    /**
     * 计算文件天数
     */
    private getDaysOld;
}
export default MemoryCompactor;
