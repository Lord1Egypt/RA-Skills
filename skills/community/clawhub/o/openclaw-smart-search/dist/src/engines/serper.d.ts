import { SearchEngine, SearchResult, SearchOptions, QuotaInfo } from '../types';
/**
 * Serper 搜索引擎适配器
 * API 文档: https://serper.dev/api
 * 提供谷歌搜索结果
 */
export declare class SerperEngine implements SearchEngine {
    name: string;
    private secretManager;
    private readonly baseUrl;
    private readonly timeout;
    search(query: string, options: SearchOptions): Promise<SearchResult[]>;
    checkQuota(): Promise<QuotaInfo>;
}
//# sourceMappingURL=serper.d.ts.map