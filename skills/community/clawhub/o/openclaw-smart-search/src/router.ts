/**
 * 智能路由模块
 * 根据查询语言、意图自动选择最佳搜索引擎
 */

import { SearchEngine, SearchOptions, EngineType, ENGINE_PRIORITIES } from './types';
import { getEngine, getAllEngines } from './engines/index';

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
 * 学术关键词
 */
const ACADEMIC_KEYWORDS = [
  // 中文
  '论文', '研究', '学术', 'arxiv', '论文',
  '文献', '期刊', '会议', '博士', '硕士',
  '综述', '引用', '影响因子', 'SCI', 'EI',
  // 英文
  'paper', 'research', 'arxiv', 'paper',
  'publication', 'journal', 'conference', 'thesis',
  'dissertation', 'review', 'citation', 'scholar',
  'study', 'preprint', 'doi', 'abstract'
];

/**
 * 技术关键词
 */
const TECHNICAL_KEYWORDS = [
  // 中文
  '代码', '编程', 'API', '开发', '框架',
  '算法', '架构', '部署', '配置', '文档',
  'GitHub', 'Stack Overflow', '教程', '实现',
  // 英文
  'code', 'programming', 'api', 'development', 'framework',
  'algorithm', 'architecture', 'deployment', 'configuration',
  'github', 'stackoverflow', 'tutorial', 'implementation',
  'programming', 'developer', 'library', 'sdk'
];

/**
 * 新闻关键词
 */
const NEWS_KEYWORDS = [
  // 中文
  '新闻', '最新', '动态', '今天', '近期',
  '发布', '公告', '突发', '热点', '头条',
  // 英文
  'news', 'latest', 'today', 'recent', 'breaking',
  'announcement', 'headline', 'update', 'release'
];

/**
 * 语言检测正则
 */
const CHINESE_REGEX = /[\u4e00-\u9fff]/g;
const ENGLISH_REGEX = /[a-zA-Z]/g;

/**
 * 智能路由器
 */
export class SmartRouter {
  private engines: Record<EngineType, SearchEngine>;
  
  constructor() {
    // 将引擎数组转换为 Record 类型
    const engineList = getAllEngines();
    this.engines = {
      bailian: getEngine('bailian'),
      tavily: getEngine('tavily'),
      serper: getEngine('serper'),
      exa: getEngine('exa'),
      firecrawl: getEngine('firecrawl')
    };
  }
  
  /**
   * 选择搜索引擎
   * @param query 搜索查询
   * @param options 搜索选项
   * @returns 选中的引擎列表（按优先级排序）
   */
  select(query: string, options: SearchOptions = {}): SearchEngine[] {
    // 分析查询
    const analysis = this.analyzeQuery(query, options);
    
    console.log('[DEBUG] Router.select:', {
      query,
      analysis: {
        query: analysis.query,
        keywords: analysis.keywords,
        language: analysis.language,
        intent: analysis.intent
      }
    });
    
    // 选择引擎
    const selectedEngines: SearchEngine[] = [];
    const selectedTypes = new Set<EngineType>();
    
    // 1. 根据语言选择主引擎
    const primaryEngine = this.selectPrimaryEngine(analysis, options);
    if (primaryEngine && !selectedTypes.has(primaryEngine)) {
      selectedEngines.push(this.engines[primaryEngine]);
      selectedTypes.add(primaryEngine);
    }
    
    // 2. 根据意图添加辅助引擎
    const secondaryEngines = this.selectSecondaryEngines(analysis, options);
    for (const type of secondaryEngines) {
      if (!selectedTypes.has(type)) {
        selectedEngines.push(this.engines[type]);
        selectedTypes.add(type);
      }
    }
    
    // 3. 添加备用引擎（用于结果融合）
    const fallbackEngines = this.selectFallbackEngines(analysis, selectedTypes);
    for (const type of fallbackEngines) {
      if (!selectedTypes.has(type)) {
        selectedEngines.push(this.engines[type]);
        selectedTypes.add(type);
      }
    }
    
    return selectedEngines;
  }
  
  /**
   * 分析查询
   */
  analyzeQuery(query: string, options: SearchOptions = {}): QueryAnalysis {
    // 语言检测
    const language = options.language || this.detectLanguage(query);
    
    // 提取关键词
    const keywords = this.extractKeywords(query);
    
    // 检测意图
    const hasAcademicKeywords = this.hasKeywords(query, ACADEMIC_KEYWORDS);
    const hasTechnicalKeywords = this.hasKeywords(query, TECHNICAL_KEYWORDS);
    const hasNewsKeywords = this.hasKeywords(query, NEWS_KEYWORDS);
    
    // 确定意图（优先使用用户指定的意图）
    // v1.0.9: 支持深度研究模式
    let intent = options.intent || 'general';
    if (options.deep) {
      intent = 'research';
    } else if (intent === 'general') {
      if (hasAcademicKeywords) {
        intent = 'academic';
      } else if (hasTechnicalKeywords) {
        intent = 'technical';
      } else if (hasNewsKeywords) {
        intent = 'news';
      }
    }
    
    return {
      query: query,
      language: language as 'zh' | 'en' | 'mixed' | 'other',
      intent,
      hasAcademicKeywords,
      hasTechnicalKeywords,
      hasNewsKeywords,
      keywords
    };
  }
  
  /**
   * 检测语言
   */
  detectLanguage(query: string): 'zh' | 'en' | 'mixed' | 'other' {
    const chineseChars = query.match(CHINESE_REGEX);
    const englishChars = query.match(ENGLISH_REGEX);
    
    const chineseCount = chineseChars ? chineseChars.length : 0;
    const englishCount = englishChars ? englishChars.length : 0;
    
    // 中英混合（同时包含中文和英文，且都有一定数量）
    if (chineseCount > 2 && englishCount > 2) {
      return 'mixed';
    }
    
    // 中文为主
    if (chineseCount > englishCount && chineseCount > 0) {
      return 'zh';
    }
    
    // 英文为主
    if (englishCount > chineseCount && englishCount > 0) {
      return 'en';
    }
    
    // 两者都有但数量很少
    if (chineseCount > 0 && englishCount > 0) {
      return 'mixed';
    }
    
    // 其他或无法判断
    return chineseCount > 0 ? 'zh' : 'en';
  }
  
  /**
   * 选择主引擎
   * v1.0.9: 添加场景化引擎选择
   */
  private selectPrimaryEngine(
    analysis: QueryAnalysis,
    options: SearchOptions
  ): EngineType | null {
    const queryLower = analysis.query.toLowerCase();

    console.log('[DEBUG] selectPrimaryEngine:', {
      query: analysis.query,
      keywords: analysis.keywords,
      queryLower
    });

    // 🔥 v1.0.9: 网页抓取场景：优先 Firecrawl
    const isScrape = analysis.keywords.some(k =>
      ['scrape', 'crawl', '抓取', '提取', 'markdown'].includes(k.toLowerCase())
    );
    const isScrapeQuery = (
      isScrape ||
      queryLower.includes('scrape') ||
      queryLower.includes('crawl') ||
      queryLower.includes('网页抓取') ||
      queryLower.includes('内容提取') ||
      queryLower.includes('抓取网站') ||
      queryLower.includes('提取网页')
    );
    
    console.log('[DEBUG] Firecrawl check:', {
      isScrape,
      isScrapeQuery,
      keywordsMatch: analysis.keywords.filter(k => ['scrape', 'crawl', '抓取', '提取', 'markdown'].includes(k.toLowerCase()))
    });

    if (isScrapeQuery) {
      console.log('[DEBUG] Returning firecrawl as primary engine');
      return 'firecrawl';
    }

    // 🔥 v1.0.9: 学术搜索：优先 Exa
    if (analysis.intent === 'academic' || analysis.hasAcademicKeywords) {
      return 'exa';
    }

    // 🔥 v1.0.9: 技术搜索：优先 Exa
    if (analysis.intent === 'technical') {
      return 'exa';
    }

    // 🔥 v1.0.9: 新闻搜索：优先 Tavily
    if (analysis.intent === 'news') {
      return 'tavily';
    }

    // 语言优先
    const language = options.language || analysis.language;

    if (language === 'zh' || language === 'mixed') {
      // 中文查询优先使用百炼
      return 'bailian';
    }

    // 英文查询优先使用 Serper（Google 结果）
    if (language === 'en') {
      return 'serper';
    }

    // 默认使用百炼
    return 'bailian';
  }
  
  /**
   * 选择辅助引擎
   */
  private selectSecondaryEngines(
    analysis: QueryAnalysis,
    options: SearchOptions
  ): EngineType[] {
    const engines: EngineType[] = [];
    
    // 学术查询添加 Exa
    if (analysis.intent === 'academic' || analysis.hasAcademicKeywords) {
      engines.push('exa');
    }
    
    // 技术查询也添加 Exa（学术/技术搜索效果好）
    if (analysis.intent === 'technical' || analysis.hasTechnicalKeywords) {
      if (!engines.includes('exa')) {
        engines.push('exa');
      }
    }
    
    // 新闻查询添加 Tavily（支持时间范围过滤）
    if (analysis.intent === 'news' || analysis.hasNewsKeywords) {
      engines.push('tavily');
    }
    
    return engines;
  }
  
  /**
   * 选择备用引擎
   * v1.0.9: 根据查询复杂度动态决定备用引擎数量
   */
  private selectFallbackEngines(
    analysis: QueryAnalysis,
    alreadySelected: Set<EngineType>
  ): EngineType[] {
    const engines: EngineType[] = [];
    const queryLower = analysis.query.toLowerCase();

    // 🔥 v1.0.9: 根据查询复杂度动态决定备用引擎数量
    let maxFallbackEngines = 2; // 默认 2 个备用引擎

    // 🔥 深度研究场景：使用全部引擎（优先级最高）
    if (analysis.intent === 'research') {
      maxFallbackEngines = 5;
    }
    // 简单查询（<10 字符或<3 关键词）：只选 1 个备用引擎
    else if (analysis.query.length < 10 && analysis.keywords.length < 3) {
      maxFallbackEngines = 1;
    }
    // 🔥 网页抓取场景：优先 Firecrawl
    else if (
      analysis.keywords.some(k =>
        ['scrape', 'crawl', '抓取', '提取', 'markdown', '爬虫', '网页内容'].includes(k.toLowerCase())
      ) ||
      queryLower.includes('scrape') ||
      queryLower.includes('crawl') ||
      queryLower.includes('网页抓取') ||
      queryLower.includes('内容提取') ||
      queryLower.includes('抓取网站') ||
      queryLower.includes('提取网页') ||
      queryLower.includes('爬虫') ||
      queryLower.includes('网页内容')
    ) {
      maxFallbackEngines = 2; // Firecrawl + 1 个备用
      if (!alreadySelected.has('firecrawl')) {
        engines.push('firecrawl');
      }
    }
    // 学术/技术场景：使用 2 个备用引擎（主引擎已经是 Exa）
    else if (
      analysis.intent === 'academic' ||
      analysis.intent === 'technical' ||
      analysis.hasAcademicKeywords ||
      analysis.hasTechnicalKeywords
    ) {
      maxFallbackEngines = 2;
    }

    // 按优先级添加基础备用引擎
    const fallbackOrder: EngineType[] = ['bailian', 'serper', 'tavily', 'exa', 'firecrawl'];

    for (const type of fallbackOrder) {
      if (!alreadySelected.has(type) && !engines.includes(type)) {
        engines.push(type);
      }
    }

    // 🔥 v1.0.9 关键修复：应用数量限制
    return engines.slice(0, maxFallbackEngines);
  }
  
  /**
   * 提取关键词
   */
  private extractKeywords(query: string): string[] {
    // 简单的关键词提取：按空格和标点分割
    return query
      .toLowerCase()
      .split(/[\s,，。！？、;；：:""''【】（）\[\]()]+/)
      .filter(word => word.length > 1)
      .slice(0, 10); // 最多 10 个关键词
  }
  
  /**
   * 检查是否包含关键词
   */
  private hasKeywords(query: string, keywords: string[]): boolean {
    const lowerQuery = query.toLowerCase();
    return keywords.some(keyword => lowerQuery.includes(keyword.toLowerCase()));
  }
  
  /**
   * 获取单个引擎
   */
  getEngine(type: EngineType): SearchEngine {
    return this.engines[type];
  }
  
  /**
   * 获取所有引擎
   */
  getAllEngines(): Record<EngineType, SearchEngine> {
    return this.engines;
  }
  
  /**
   * 获取引擎选择策略说明
   */
  getSelectionStrategy(analysis: QueryAnalysis): string {
    const strategies: string[] = [];
    
    // 语言策略
    if (analysis.language === 'zh') {
      strategies.push('中文查询 → 百炼（中文优化）');
    } else if (analysis.language === 'en') {
      strategies.push('英文查询 → Serper（Google 结果）');
    } else if (analysis.language === 'mixed') {
      strategies.push('中英混合 → 百炼（综合优化）');
    }
    
    // 意图策略
    if (analysis.intent === 'academic') {
      strategies.push('学术意图 → 添加 Exa');
    } else if (analysis.intent === 'technical') {
      strategies.push('技术意图 → 添加 Exa');
    } else if (analysis.intent === 'news') {
      strategies.push('新闻意图 → 添加 Tavily');
    }
    
    // 备用策略
    strategies.push('备用引擎 → Tavily + 其他');
    
    return strategies.join('\n');
  }
}

// 导出单例
export const smartRouter = new SmartRouter();