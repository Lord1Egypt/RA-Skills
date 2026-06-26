/**
 * 智能搜索类型定义
 */
export interface EngineConfig {
    apiKey: string;
    enabled: boolean;
    priority: number;
    quotaLimit: number;
    quotaUsed: number;
    lastRotated: string;
}
export interface SecretConfig {
    engines: Record<string, EngineConfig>;
    metadata: {
        owner: string;
        createdAt: string;
        updatedAt: string;
        accessLog: Array<{
            engine: string;
            timestamp: string;
            action: string;
        }>;
    };
}
export interface SearchResult {
    title: string;
    url: string;
    snippet?: string;
    content?: string;
    engine: string;
    originalScore?: number;
    publishedDate?: string;
    finalScore?: number;
}
export interface SearchOptions {
    count?: number;
    language?: 'zh' | 'en' | 'auto';
    intent?: 'general' | 'academic' | 'technical' | 'news' | 'research';
    timeRange?: 'day' | 'week' | 'month' | 'year';
    timeout?: number;
    /** 深度研究模式（使用全部 5 个引擎） */
    deep?: boolean;
}
export interface SearchEngine {
    name: string;
    search(query: string, options: SearchOptions): Promise<SearchResult[]>;
    checkQuota(): Promise<QuotaInfo>;
}
export interface QuotaInfo {
    used: number;
    limit: number;
    remaining: number;
}
export interface SearchResponse {
    success: boolean;
    results: SearchResult[];
    enginesUsed: string[];
    fallback: boolean;
    error?: string;
}
export type EngineType = 'bailian' | 'tavily' | 'serper' | 'exa' | 'firecrawl';
export declare const ENGINE_PRIORITIES: Record<EngineType, number>;
export declare const ENGINE_QUOTAS: Record<EngineType, number>;
export declare const ENGINE_LABELS: Record<EngineType, string>;
//# sourceMappingURL=types.d.ts.map