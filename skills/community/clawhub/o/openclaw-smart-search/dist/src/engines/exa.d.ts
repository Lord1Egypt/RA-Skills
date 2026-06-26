import { SearchEngine, SearchResult, SearchOptions, QuotaInfo } from '../types';
/**
 * Exa 搜索引擎适配器
 * API 文档: https://docs.exa.ai/reference/search
 * 专注于学术和技术搜索
 */
export declare class ExaEngine implements SearchEngine {
    name: string;
    private secretManager;
    private readonly baseUrl;
    private readonly timeout;
    search(query: string, options: SearchOptions): Promise<SearchResult[]>;
    checkQuota(): Promise<QuotaInfo>;
}
//# sourceMappingURL=exa.d.ts.map