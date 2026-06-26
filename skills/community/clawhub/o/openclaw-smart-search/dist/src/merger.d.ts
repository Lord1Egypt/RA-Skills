/**
 * 结果合并模块
 * 多引擎结果去重、评分融合、排序
 */
import { SearchResult, EngineType } from './types';
/**
 * 合并选项
 */
export interface MergeOptions {
    /** 最大返回结果数 */
    maxResults?: number;
    /** 是否按 URL 去重 */
    dedupByUrl?: boolean;
    /** 是否按分数排序 */
    sortByScore?: boolean;
    /** 是否应用时间衰减 */
    applyTimeDecay?: boolean;
    /** 是否应用引擎权重 */
    applyEngineWeight?: boolean;
    /** 引擎权重覆盖 */
    engineWeights?: Partial<Record<EngineType, number>>;
    /** 时间衰减半衰期（天） */
    timeDecayHalfLife?: number;
}
/**
 * 结果合并器
 */
export declare class ResultMerger {
    private engineWeights;
    constructor(options?: {
        engineWeights?: Partial<Record<EngineType, number>>;
    });
    /**
     * 合并多个引擎的搜索结果
     * @param results 多个引擎的结果数组
     * @param options 合并选项
     * @returns 合并后的结果
     */
    merge(results: SearchResult[][], options?: MergeOptions): SearchResult[];
    /**
     * 展平多引擎结果
     */
    private flattenResults;
    /**
     * URL 标准化
     * 移除协议、www、尾部斜杠等，用于更好的去重
     */
    private normalizeUrl;
    /**
     * 按 URL 去重
     * 保留得分最高的结果
     */
    private deduplicateByUrl;
    /**
     * 计算最终得分
     */
    private calculateFinalScore;
    /**
     * 计算时间衰减因子
     * @param dateStr 发布日期
     * @param halfLife 半衰期（天）
     * @returns 衰减因子 (0-1)
     */
    private calculateTimeDecay;
    /**
     * 设置引擎权重
     */
    setEngineWeight(engine: EngineType, weight: number): void;
    /**
     * 获取引擎权重
     */
    getEngineWeight(engine: EngineType): number;
    /**
     * 获取合并统计信息
     */
    getMergeStats(results: SearchResult[][], merged: SearchResult[]): {
        totalResults: number;
        uniqueResults: number;
        duplicatesRemoved: number;
        enginesUsed: string[];
        avgScore: number;
    };
    /**
     * 按引擎分组结果
     */
    groupByEngine(results: SearchResult[]): Record<string, SearchResult[]>;
    /**
     * 获取每个引擎的最佳结果
     */
    getTopResultsByEngine(results: SearchResult[], topN?: number): Record<string, SearchResult[]>;
}
export declare const resultMerger: ResultMerger;
//# sourceMappingURL=merger.d.ts.map