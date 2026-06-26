/**
 * 智能路由模块
 * 根据查询语言、意图自动选择最佳搜索引擎
 */
import { SearchEngine, SearchOptions, EngineType } from './types';
/**
 * 搜索查询分析结果
 */
interface QueryAnalysis {
    /** 原始查询字符串 */
    query: string;
    /** 检测到的语言 */
    language: 'zh' | 'en' | 'mixed' | 'other';
    /** 查询意图 */
    intent: 'general' | 'academic' | 'technical' | 'news' | 'research';
    /** 是否包含学术关键词 */
    hasAcademicKeywords: boolean;
    /** 是否包含技术关键词 */
    hasTechnicalKeywords: boolean;
    /** 是否包含新闻关键词 */
    hasNewsKeywords: boolean;
    /** 关键词列表 */
    keywords: string[];
}
/**
 * 智能路由器
 */
export declare class SmartRouter {
    private engines;
    constructor();
    /**
     * 选择搜索引擎
     * @param query 搜索查询
     * @param options 搜索选项
     * @returns 选中的引擎列表（按优先级排序）
     */
    select(query: string, options?: SearchOptions): SearchEngine[];
    /**
     * 分析查询
     */
    analyzeQuery(query: string, options?: SearchOptions): QueryAnalysis;
    /**
     * 检测语言
     */
    detectLanguage(query: string): 'zh' | 'en' | 'mixed' | 'other';
    /**
     * 选择主引擎
     * v1.0.9: 添加场景化引擎选择
     */
    private selectPrimaryEngine;
    /**
     * 选择辅助引擎
     */
    private selectSecondaryEngines;
    /**
     * 选择备用引擎
     * v1.0.9: 根据查询复杂度动态决定备用引擎数量
     */
    private selectFallbackEngines;
    /**
     * 提取关键词
     */
    private extractKeywords;
    /**
     * 检查是否包含关键词
     */
    private hasKeywords;
    /**
     * 获取单个引擎
     */
    getEngine(type: EngineType): SearchEngine;
    /**
     * 获取所有引擎
     */
    getAllEngines(): Record<EngineType, SearchEngine>;
    /**
     * 获取引擎选择策略说明
     */
    getSelectionStrategy(analysis: QueryAnalysis): string;
}
export declare const smartRouter: SmartRouter;
export {};
//# sourceMappingURL=router.d.ts.map