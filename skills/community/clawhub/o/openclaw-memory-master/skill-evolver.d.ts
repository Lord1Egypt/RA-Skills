/**
 * Memory-Master 记忆检索模块
 *
 * 支持 5 种查询类型（基于 Karpathy 方法论）
 * - procedural: 流程查询
 * - temporal: 时间查询
 * - relational: 关系查询
 * - persona: 偏好查询
 * - factual: 事实查询
 */
/**
 * 查询类型
 */
export type QueryType = 'procedural' | 'temporal' | 'relational' | 'persona' | 'factual';
/**
 * 检索选项
 */
export interface RetrieveOptions {
    type?: QueryType;
    limit?: number;
    timeRange?: {
        start?: string;
        end?: string;
    };
    includeRaw?: boolean;
}
/**
 * 记忆条目
 */
export interface Memory {
    id: string;
    type: string;
    content: string;
    timestamp: number;
    metadata?: {
        source?: string;
        topic?: string;
        project?: string;
    };
    path?: string;
}
/**
 * 检索结果
 */
export interface RetrieveResult {
    success: boolean;
    queryType: QueryType;
    memories: Memory[];
    timeMs: number;
}
/**
 * 记忆检索器
 */
export declare class MemoryRetriever {
    private memoryDir;
    private memoryFile;
    constructor(memoryDir?: string);
    /**
     * 检索记忆
     */
    retrieve(query: string, options?: RetrieveOptions): Promise<RetrieveResult>;
    /**
     * 自动分类查询类型
     */
    private classifyQuery;
    /**
     * 流程查询
     */
    private searchProcedural;
    /**
     * 时间查询
     */
    private searchTemporal;
    /**
     * 关系查询
     */
    private searchRelational;
    /**
     * 偏好查询
     */
    private searchPersona;
    /**
     * 事实查询
     */
    private searchFactual;
    /**
     * 从章节提取记忆
     */
    private extractMemoriesFromSection;
    /**
     * 从文件提取记忆
     */
    private extractMemoriesFromFile;
    /**
     * 按相关性排序
     */
    private rankByRelevance;
    /**
     * 计算相关性分数
     */
    private calculateRelevance;
    /**
     * 解析时间范围
     */
    private parseTimeRange;
    /**
     * 解析时间戳
     */
    private parseTimestamp;
    /**
     * 获取日期字符串
     */
    private getDateString;
}
export default MemoryRetriever;
