import { SearchEngine, SearchResult, SearchOptions, QuotaInfo } from '../types';
/**
 * 百炼搜索引擎适配器
 *
 * 安全说明：
 * 使用 spawn() 而非 exec() 执行外部命令，参数作为数组传递，不经过 shell 解析。
 * 这避免了 shell 注入攻击的风险。spawn() + shell: false 是安全的命令执行方式。
 */
export declare class BailianEngine implements SearchEngine {
    name: string;
    private secretManager;
    search(query: string, options: SearchOptions): Promise<SearchResult[]>;
    /**
     * 安全执行 mcporter 命令
     * 使用 spawn 避免命令注入，参数作为数组传递不经 shell 解析
     */
    private executeMcporter;
    checkQuota(): Promise<QuotaInfo>;
}
//# sourceMappingURL=bailian.d.ts.map