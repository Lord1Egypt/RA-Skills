import { SearchEngine, SearchResult, SearchOptions, QuotaInfo } from '../types';
/**
 * Tavily 搜索引擎适配器
 * API 文档: https://docs.tavily.com/docs/tavily-api/rest-api#search
 */
export declare class TavilyEngine implements SearchEngine {
    name: string;
    private secretManager;
    private readonly baseUrl;
    private readonly timeout;
    search(query: string, options: SearchOptions): Promise<SearchResult[]>;
    checkQuota(): Promise<QuotaInfo>;
}
//# sourceMappingURL=tavily.d.ts.map