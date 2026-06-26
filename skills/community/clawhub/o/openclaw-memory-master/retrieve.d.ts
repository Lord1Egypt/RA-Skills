/**
 * Memory Retriever v4.1 - 增强版记忆检索
 *
 * 基于 Generative Agents + Mem0 + MemoryBank 最佳实践
 *
 * 新增功能：
 * - 重要性评分（近因 + 重要性 + 相关性）
 * - 情感维度（情感类型 + 情感强度）
 * - 动态 Top-K 优化
 * - 混合检索（语义 + 关键词 + 时间）
 *
 * @author 小鬼 👻 + Jake
 * @version 4.1.0
 */
/**
 * 情感类型
 */
export type EmotionType = 'positive' | 'negative' | 'neutral' | 'joy' | 'sadness' | 'anger' | 'surprise' | 'fear' | 'disgust';
/**
 * 记忆项（增强版）
 */
export interface MemoryItem {
    id: string;
    content: string;
    type: '情景' | '语义' | '程序' | '人设';
    timestamp: number;
    metadata?: {
        topic?: string;
        project?: string;
        emotion?: EmotionType;
        emotionIntensity?: number;
        importance?: number;
        tags?: string[];
    };
    recencyScore?: number;
    importanceScore?: number;
    relevanceScore?: number;
    combinedScore?: number;
}
/**
 * 检索选项（增强版）
 */
export interface RetrieveOptions {
    type?: 'procedural' | 'temporal' | 'relational' | 'persona' | 'factual';
    limit?: number;
    recencyWeight?: number;
    importanceWeight?: number;
    relevanceWeight?: number;
    emotion?: EmotionType;
    minEmotionIntensity?: number;
    dynamicK?: boolean;
    minK?: number;
    maxK?: number;
    startTime?: number;
    endTime?: number;
    hybridSearch?: boolean;
    keywordBoost?: number;
}
/**
 * 检索结果（增强版）
 */
export interface RetrieveResult {
    memories: MemoryItem[];
    total: number;
    query?: string;
    searchType?: string;
    scores?: {
        avgRecency: number;
        avgImportance: number;
        avgRelevance: number;
    };
    emotions?: {
        positive: number;
        negative: number;
        neutral: number;
    };
}
/**
 * 增强版记忆检索器
 */
export declare class MemoryRetrieverV41 {
    private memoryDir;
    private indexCache;
    constructor(memoryDir?: string);
    /**
     * 检索记忆（增强版）
     */
    retrieve(query: string, options?: RetrieveOptions): Promise<RetrieveResult>;
    /**
     * 加载记忆
     */
    private loadMemories;
    /**
     * 过滤记忆
     */
    private filterMemories;
    /**
     * 计算评分（参考 Generative Agents）
     */
    private calculateScores;
    /**
     * 动态 Top-K（参考 Mem0）
     */
    private calculateDynamicK;
    /**
     * 计算统计信息
     */
    private calculateStats;
    /**
     * 解析 MEMORY.md
     */
    private parseMemoryMd;
    /**
     * 解析每日记忆
     */
    private parseDailyMemory;
    /**
     * 解析 Wiki 记忆（v4.1 新增）
     */
    private parseWikiMemory;
    /**
     * 提取 ID
     */
    private extractId;
    /**
     * 检测情感（v4.1 新增，简单实现）
     */
    detectEmotion(content: string): {
        emotion: EmotionType;
        intensity: number;
    };
    /**
     * 清除缓存
     */
    clearCache(): void;
}
