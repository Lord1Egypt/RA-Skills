/**
 * Smart Search - 统一智能搜索
 * 主入口文件
 *
 * 功能：
 * - 智能路由：根据语言和意图选择最佳引擎
 * - 结果合并：多引擎结果去重、评分融合
 * - 超时控制：单个引擎超时 5 秒，不影响其他引擎
 * - 自动降级：主引擎失败时自动切换到备选引擎
 */
import { SearchOptions, SearchResponse } from './types';
/**
 * 智能搜索主函数
 *
 * @param query 搜索查询
 * @param options 搜索选项
 * @returns 搜索响应
 */
export declare function smartSearch(query: string, options?: SearchOptions): Promise<SearchResponse>;
/**
 * 快速搜索（仅使用主引擎）
 */
export declare function quickSearch(query: string, options?: SearchOptions): Promise<SearchResponse>;
/**
 * 学术搜索（使用 Exa 引擎）
 */
export declare function academicSearch(query: string, options?: SearchOptions): Promise<SearchResponse>;
/**
 * 技术搜索（使用 Exa 引擎）
 */
export declare function technicalSearch(query: string, options?: SearchOptions): Promise<SearchResponse>;
/**
 * 新闻搜索（使用 Tavily 引擎）
 */
export declare function newsSearch(query: string, options?: SearchOptions): Promise<SearchResponse>;
//# sourceMappingURL=index.d.ts.map