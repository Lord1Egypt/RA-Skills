import { SearchEngine, SearchResult, SearchOptions, QuotaInfo } from '../types';
/**
 * Firecrawl 搜索引擎适配器
 * API 文档: https://docs.firecrawl.dev/api-reference/endpoint/search
 * 专注于网页抓取和内容提取
 */
export declare class FirecrawlEngine implements SearchEngine {
    name: string;
    private secretManager;
    private readonly baseUrl;
    private readonly timeout;
    search(query: string, options: SearchOptions): Promise<SearchResult[]>;
    checkQuota(): Promise<QuotaInfo>;
}
//# sourceMappingURL=firecrawl.d.ts.map