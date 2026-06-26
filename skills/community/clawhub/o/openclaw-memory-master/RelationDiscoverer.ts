/**
 * Auto Tagger - 自动打标器
 * 
 * 智能标签提取系统，支持：
 * 1. 关键词提取（TF-IDF + 规则）
 * 2. 情感标签检测
 * 3. 实体识别（人物、地点、组织等）
 * 4. 主题标签生成
 * 5. 自定义标签规则
 * 
 * @author 小鬼 👻 + Jake
 * @version 4.3.0
 * @module smart
 */

import { TaggerConfig } from './SmartMemoryCurator';

// ============ 类型定义 ============

export interface TaggingResult {
  allTags: string[];
  keywordTags: string[];
  emotionTags: string[];
  entityTags: string[];
  topicTags: string[];
  customTags: string[];
  
  keywordScores: Record<string, number>;
  emotionScores: Record<string, number>;
  entityConfidences: Record<string, number>;
  
  extractedEntities: {
    persons: string[];
    locations: string[];
    organizations: string[];
    dates: string[];
    numbers: string[];
    urls: string[];
  };
  
  metadata: {
    processingTime: number;
    wordCount: number;
    uniqueWordCount: number;
    tagDensity: number;
    emotionDominance?: string;
  };
}

export interface Keyword {
  word: string;
  score: number;
  frequency: number;
  position: number;
}

export interface EmotionAnalysis {
  primary: string;
  secondary: string[];
  intensity: number; // 0-100
  scores: Record<string, number>;
  triggers: string[];
}

export interface Entity {
  text: string;
  type: 'person' | 'location' | 'organization' | 'date' | 'number' | 'url' | 'other';
  confidence: number;
  start: number;
  end: number;
}

export interface TaggerRule {
  name: string;
  pattern: RegExp | string;
  tag: string;
  weight: number;
  description: string;
}

// ============ 常量定义 ============

/**
 * 情感词典
 */
export const EMOTION_DICTIONARY: Record<string, string[]> = {
  // 正面情感
  'joy': ['开心', '快乐', '高兴', '喜悦', '兴奋', '愉快', '欢乐', '幸福', '满足', '欣慰'],
  'love': ['爱', '喜欢', '热爱', '喜爱', '钟情', '倾心', '迷恋', '疼爱', '宠爱'],
  'surprise': ['惊讶', '惊奇', '吃惊', '震惊', '意外', '惊喜', '诧异', '愕然'],
  'pride': ['骄傲', '自豪', '得意', '荣耀', '荣誉', '成就感', '自尊'],
  'hope': ['希望', '期望', '期待', '盼望', '憧憬', '向往', '展望'],
  'gratitude': ['感谢', '感激', '感恩', '谢意', '多谢', '谢谢', '致谢'],
  
  // 负面情感
  'sadness': ['悲伤', '伤心', '难过', '悲哀', '悲痛', '沮丧', '消沉', '忧郁'],
  'anger': ['愤怒', '生气', '发怒', '气愤', '怒火', '恼火', '愤慨', '暴怒'],
  'fear': ['害怕', '恐惧', '担心', '忧虑', '惊恐', '畏惧', '恐慌', '不安'],
  'disgust': ['厌恶', '讨厌', '反感', '恶心', '嫌弃', '憎恶', '厌烦'],
  'shame': ['羞耻', '羞愧', '惭愧', '丢脸', '难为情', '不好意思'],
  'guilt': ['内疚', '愧疚', '自责', '悔恨', '懊悔', '后悔'],
  
  // 中性情感
  'neutral': ['一般', '普通', '平常', '正常', '平淡', '无感', '无所谓'],
  'confusion': ['困惑', '迷茫', '疑惑', '不解', '糊涂', '不清楚', '不确定'],
  'curiosity': ['好奇', '感兴趣', '想知道', '探究', '探索', '询问'],
};

/**
 * 常用停用词
 */
export const STOP_WORDS = new Set([
  '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你',
  '会', '着', '没有', '看', '好', '自己', '这', '那', '里', '来', '把', '又', '什么', '呢', '得', '过', '啊', '个', '我们', '他',
  '对', '下', '给', '而', '与', '之', '或', '且', '但', '并', '而且', '然而', '因此', '所以', '因为', '如果', '虽然', '但是',
  'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be',
  'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must',
]);

/**
 * 默认打标规则
 */
export const DEFAULT_TAGGER_RULES: TaggerRule[] = [
  // 技术相关
  {
    name: 'technical-code',
    pattern: /代码|编程|算法|API|数据库|服务器|前端|后端/i,
    tag: '技术',
    weight: 1.0,
    description: '技术开发标签',
  },
  {
    name: 'technical-ai',
    pattern: /人工智能|AI|机器学习|深度学习|神经网络|大模型/i,
    tag: 'AI',
    weight: 1.0,
    description: '人工智能标签',
  },
  {
    name: 'technical-openclaw',
    pattern: /OpenClaw|技能|插件|扩展|配置|记忆系统/i,
    tag: 'OpenClaw',
    weight: 1.0,
    description: 'OpenClaw相关标签',
  },
  
  // 项目相关
  {
    name: 'project-management',
    pattern: /项目|任务|里程碑|进度|计划|时间表/i,
    tag: '项目',
    weight: 1.0,
    description: '项目管理标签',
  },
  {
    name: 'project-meeting',
    pattern: /会议|讨论|评审|反馈|沟通|协作/i,
    tag: '会议',
    weight: 1.0,
    description: '会议相关标签',
  },
  
  // 时间相关
  {
    name: 'time-urgent',
    pattern: /紧急|立刻|马上|尽快|立即|即刻/i,
    tag: '紧急',
    weight: 1.0,
    description: '紧急事项标签',
  },
  {
    name: 'time-future',
    pattern: /明天|后天|下周|下月|明年|未来|计划/i,
    tag: '未来',
    weight: 0.8,
    description: '未来事项标签',
  },
  {
    name: 'time-past',
    pattern: /昨天|前天|上周|上月|去年|过去|以前/i,
    tag: '过去',
    weight: 0.8,
    description: '过去事项标签',
  },
  
  // 重要性相关
  {
    name: 'importance-high',
    pattern: /重要|关键|核心|主要|首要|重点/i,
    tag: '重要',
    weight: 1.0,
    description: '重要事项标签',
  },
  {
    name: 'importance-low',
    pattern: /次要|辅助|额外|补充|可选|非必需/i,
    tag: '次要',
    weight: 0.7,
    description: '次要事项标签',
  },
  
  // 情感强度
  {
    name: 'emotion-strong',
    pattern: /非常|极其|特别|十分|极度|强烈/i,
    tag: '强烈',
    weight: 0.9,
    description: '情感强烈标签',
  },
  {
    name: 'emotion-weak',
    pattern: /稍微|有点|一些|些许|略微|稍稍/i,
    tag: '轻微',
    weight: 0.6,
    description: '情感轻微标签',
  },
];

// ============ 自动打标器 ============

/**
 * 自动打标器
 * 
 * 实现多维度标签提取和分析
 */
export class AutoTagger {
  private config: TaggerConfig;
  private rules: TaggerRule[];
  private emotionDictionary: Record<string, string[]>;
  private stopWords: Set<string>;
  private tagCache: Map<string, TaggingResult>;
  
  constructor(config: TaggerConfig) {
    this.config = config;
    this.rules = DEFAULT_TAGGER_RULES;
    this.emotionDictionary = EMOTION_DICTIONARY;
    this.stopWords = STOP_WORDS;
    this.tagCache = new Map();
    
    console.log(`[AutoTagger] 初始化完成，使用 ${this.rules.length} 条打标规则`);
  }

  /**
   * 打标主方法
   */
  async tag(content: string): Promise<TaggingResult> {
    const startTime = Date.now();
    const cacheKey = this.generateCacheKey(content);
    
    // 检查缓存
    const cached = this.tagCache.get(cacheKey);
    if (cached) {
      console.log(`[AutoTagger] 缓存命中: ${cached.allTags.length} 个标签`);
      return cached;
    }
    
    try {
      console.log(`[AutoTagger] 开始打标: ${content.substring(0, 50)}${content.length > 50 ? '...' : ''}`);
      
      // 并行执行各种标签提取
      const [
        keywords,
        emotions,
        entities,
        ruleTags,
      ] = await Promise.all([
        this.extractKeywords(content),
        this.analyzeEmotions(content),
        this.extractEntities(content),
        this.applyRules(content),
      ]);
      
      // 合并所有标签
      const allTags = this.mergeTags(keywords, emotions, entities, ruleTags);
      
      // 计算元数据
      const wordCount = this.countWords(content);
      const uniqueWordCount = this.countUniqueWords(content);
      const tagDensity = allTags.allTags.length / Math.max(wordCount, 1);
      const emotionDominance = this.getDominantEmotion(emotions);
      
      const processingTime = Date.now() - startTime;
      
      const result: TaggingResult = {
        allTags: allTags.allTags,
        keywordTags: keywords.words,
        emotionTags: emotions.tags,
        entityTags: entities.tags,
        topicTags: [], // 主题标签待实现
        customTags: ruleTags,
        
        keywordScores: keywords.scores,
        emotionScores: emotions.scores,
        entityConfidences: entities.confidences,
        
        extractedEntities: {
          persons: entities.persons,
          locations: entities.locations,
          organizations: entities.organizations,
          dates: entities.dates,
          numbers: entities.numbers,
          urls: entities.urls,
        },
        
        metadata: {
          processingTime,
          wordCount,
          uniqueWordCount,
          tagDensity,
          emotionDominance,
        },
      };
      
      // 缓存结果
      this.tagCache.set(cacheKey, result);
      this.cleanCache();
      
      console.log(`[AutoTagger] 打标完成: ${result.allTags.length} 个标签 (${processingTime}ms)`);
      console.log(`  - 关键词: ${result.keywordTags.slice(0, 3).join(', ')}${result.keywordTags.length > 3 ? '...' : ''}`);
      console.log(`  - 情感: ${result.emotionTags.slice(0, 3).join(', ')}${result.emotionTags.length > 3 ? '...' : ''}`);
      console.log(`  - 实体: ${result.entityTags.slice(0, 3).join(', ')}${result.entityTags.length > 3 ? '...' : ''}`);
      
      return result;
      
    } catch (error) {
      console.error('[AutoTagger] 打标失败:', error);
      
      // 返回降级结果
      const fallbackResult: TaggingResult = {
        allTags: ['unprocessed'],
        keywordTags: [],
        emotionTags: [],
        entityTags: [],
        topicTags: [],
        customTags: [],
        
        keywordScores: {},
        emotionScores: {},
        entityConfidences: {},
        
        extractedEntities: {
          persons: [],
          locations: [],
          organizations: [],
          dates: [],
          numbers: [],
          urls: [],
        },
        
        metadata: {
          processingTime: Date.now() - startTime,
          wordCount: this.countWords(content),
          uniqueWordCount: this.countUniqueWords(content),
          tagDensity: 0,
          emotionDominance: undefined,
        },
      };
      
      return fallbackResult;
    }
  }

  /**
   * 批量打标
   */
  async batchTag(contents: string[]): Promise<TaggingResult[]> {
    const results: TaggingResult[] = [];
    
    for (let i = 0; i < contents.length; i++) {
      console.log(`[AutoTagger] 批量打标: ${i + 1}/${contents.length}`);
      const result = await this.tag(contents[i]);
      results.push(result);
      
      // 避免过载
      if (i % 10 === 9) {
        await new Promise(resolve => setTimeout(resolve, 50));
      }
    }
    
    return results;
  }

  /**
   * 添加自定义规则
   */
  addRule(rule: TaggerRule): void {
    this.rules.push(rule);
    console.log(`[AutoTagger] 添加打标规则: ${rule.name} -> ${rule.tag}`);
  }

  /**
   * 添加情感词汇
   */
  addEmotionWords(emotion: string, words: string[]): void {
    if (!this.emotionDictionary[emotion]) {
      this.emotionDictionary[emotion] = [];
    }
    this.emotionDictionary[emotion].push(...words);
    console.log(`[AutoTagger] 添加情感词汇: ${emotion} (${words.length} 个)`);
  }

  /**
   * 添加停用词
   */
  addStopWords(words: string[]): void {
    words.forEach(word => this.stopWords.add(word));
    console.log(`[AutoTagger] 添加停用词: ${words.length} 个`);
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    ruleCount: number;
    emotionCategoryCount: number;
    stopWordCount: number;
    cacheSize: number;
    averageProcessingTime: number;
  } {
    // 计算平均处理时间（需要实际数据）
    const avgProcessingTime = 0; // 待实现
    
    return {
      ruleCount: this.rules.length,
      emotionCategoryCount: Object.keys(this.emotionDictionary).length,
      stopWordCount: this.stopWords.size,
      cacheSize: this.tagCache.size,
      averageProcessingTime,
    };
  }

  /**
   * 清除缓存
   */
  clearCache(): void {
    this.tagCache.clear();
    console.log('[AutoTagger] 标签缓存已清除');
  }

  // ============ 私有方法 ============

  /**
   * 提取关键词
   */
  private async extractKeywords(content: string): Promise<{
    words: string[];
    scores: Record<string, number>;
  }> {
    const startTime = Date.now();
    
    // 分词
    const words = this.tokenize(content);
    if (words.length === 0) {
      return { words: [], scores: {} };
    }
    
    // 过滤停用词
    const filteredWords = words.filter(word => 
      word.length >= this.config.minKeywordLength && 
      !this.stopWords.has(word.toLowerCase())
    );
    
    // 计算词频
    const wordFreq: Record<string, number> = {};
    for (const word of filteredWords) {
      wordFreq[word] = (wordFreq[word] || 0) + 1;
    }
    
    // 简单的TF（词频）计算
    const totalWords = filteredWords.length;
    const tfScores: Record<string, number> = {};
    
    for (const [word, freq] of Object.entries(wordFreq)) {
      tfScores[word] = freq / totalWords;
    }
    
    // 选择Top-K关键词
    const sortedWords = Object.entries(tfScores)
      .sort((a, b) => b[1] - a[1])
      .slice(0, this.config.maxKeywords);
    
    const processingTime = Date.now() - startTime;
    console.log(`[AutoTagger] 关键词提取: ${sortedWords.length} 个关键词 (${processingTime}ms)`);
    
    return {
      words: sortedWords.map(([word]) => word),
      scores: Object.fromEntries(sortedWords),
    };
  }

  /**
   * 分析情感
   */
  private async analyzeEmotions(content: string): Promise<{
    tags: string[];
    scores: Record<string, number>;
    analysis?: EmotionAnalysis;
  }> {
    if (!this.config.emotionDetection) {
      return { tags: [], scores: {} };
    }
    
    const startTime = Date.now();
    
    // 分词
    const words = this.tokenize(content);
    const contentLower = content.toLowerCase();
    
    // 情感检测
    const emotionCounts: Record<string, number> = {};
    const emotionTriggers: Record<string, string[]> = {};
    
    for (const [emotion, emotionWords] of Object.entries(this.emotionDictionary)) {
      let count = 0;
      const triggers: string[] = [];
      
      for (const emotionWord of emotionWords) {
        const wordLower = emotionWord.toLowerCase();
        
        // 简单匹配
        if (contentLower.includes(wordLower)) {
          count++;
          triggers.push(emotionWord);
        }
        
        // 边界匹配
        const wordPattern = new RegExp(`\\b${wordLower}\\b`, 'gi');
        const matches = content.match(wordPattern);
        if (matches) {
          count += matches.length;
          triggers.push(...matches);
        }
      }
      
      if (count > 0) {
        emotionCounts[emotion] = count;
        emotionTriggers[emotion] = triggers;
      }
    }
    
    // 计算情感强度
    const totalEmotionWords = Object.values(emotionCounts).reduce((a, b) => a + b, 0);
    const emotionScores: Record<string, number> = {};
    
    for (const [emotion, count] of Object.entries(emotionCounts)) {
      emotionScores[emotion] = totalEmotionWords > 0 ? count / totalEmotionWords : 0;
    }
    
    // 确定主要情感
    let primaryEmotion = 'neutral';
    let maxScore = 0;
    
    for (const [emotion, score] of Object.entries(emotionScores)) {
      if (score > maxScore) {
        maxScore = score;
        primaryEmotion = emotion;
      }
    }
    
    // 确定次要情感（得分 > 0.1）
    const secondaryEmotions = Object.entries(emotionScores)
      .filter(([emotion, score]) => emotion !== primaryEmotion && score > 0.1)
      .map(([emotion]) => emotion);
    
    // 计算情感强度（基于得分和词频）
    const intensity = Math.min(maxScore * 100, 100);
    
    const processingTime = Date.now() - startTime;
    
    // 生成情感标签
    const emotionTags: string[] = [];
    if (primaryEmotion !== 'neutral') {
      emotionTags.push(primaryEmotion);
    }
    emotionTags.push(...secondaryEmotions);
    
    console.log(`[AutoTagger] 情感分析: ${primaryEmotion} (强度: ${intensity.toFixed(1)}) (${processingTime}ms)`);
    
    return {
      tags: emotionTags,
      scores: emotionScores,
      analysis: {
        primary: primaryEmotion,
        secondary: secondaryEmotions,
        intensity,
        scores: emotionScores,
        triggers: emotionTriggers[primaryEmotion] || [],
      },
    };
  }

  /**
   * 提取实体
   */
  private async extractEntities(content: string): Promise<{
    tags: string[];
    confidences: Record<string, number>;
    persons: string[];
    locations: string[];
    organizations: string[];
    dates: string[];
    numbers: string[];
    urls: string[];
  }> {
    if (!this.config.extractEntities) {
      return {
        tags: [],
        confidences: {},
        persons: [],
        locations: [],
        organizations: [],
        dates: [],
        numbers: [],
        urls: [],
      };
    }
    
    const startTime = Date.now();
    
    const entities: Entity[] = [];
    const tags: string[] = [];
    const confidences: Record<string, number> = {};
    
    // 提取URL
    const urlRegex = /(https?:\/\/[^\s]+)/gi;
    const urls: string[] = [];
    let urlMatch;
    
    while ((urlMatch = urlRegex.exec(content)) !== null) {
      const url = urlMatch[0];
      urls.push(url);
      entities.push({
        text: url,
        type: 'url',
        confidence: 0.9,
        start: urlMatch.index,
        end: urlMatch.index + url.length,
      });
      tags.push('url');
      confidences[url] = 0.9;
    }
    
    // 提取日期（简单模式）
    const dateRegex = /\b(\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{4}|\d{1,2}月\d{1,2}日)\b/gi;
    const dates: string[] = [];
    let dateMatch;
    
    while ((dateMatch = dateRegex.exec(content)) !== null) {
      const date = dateMatch[0];
      dates.push(date);
      entities.push({
        text: date,
        type: 'date',
        confidence: 0.8,
        start: dateMatch.index,
        end: dateMatch.index + date.length,
      });
      tags.push('date');
      confidences[date] = 0.8;
    }
    
    // 提取数字（简单模式）
    const numberRegex = /\b\d+(\.\d+)?\b/gi;
    const numbers: string[] = [];
    let numberMatch;
    
    while ((numberMatch = numberRegex.exec(content)) !== null) {
      const number = numberMatch[0];
      numbers.push(number);
      entities.push({
        text: number,
        type: 'number',
        confidence: 0.9,
        start: numberMatch.index,
        end: numberMatch.index + number.length,
      });
      tags.push('number');
      confidences[number] = 0.9;
    }
    
    // 简单的人物/地点/组织识别（基于规则）
    // 这里可以扩展为更复杂的NLP模型
    
    const persons: string[] = [];
    const locations: string[] = [];
    const organizations: string[] = [];
    
    const processingTime = Date.now() - startTime;
    console.log(`[AutoTagger] 实体提取: ${entities.length} 个实体 (${processingTime}ms)`);
    
    return {
      tags: [...new Set(tags)],
      confidences,
      persons,
      locations,
      organizations,
      dates,
      numbers,
      urls,
    };
  }

  /**
   * 应用规则打标
   */
  private applyRules(content: string): string[] {
    const tags: string[] = [];
    const contentLower = content.toLowerCase();
    
    for (const rule of this.rules) {
      let matches = false;
      
      if (typeof rule.pattern === 'string') {
        // 字符串匹配
        if (contentLower.includes(rule.pattern.toLowerCase())) {
          matches = true;
        }
      } else {
        // 正则匹配
        if (rule.pattern.test(content)) {
          matches = true;
        }
      }
      
      if (matches) {
        tags.push(rule.tag);
      }
    }
    
    return [...new Set(tags)]; // 去重
  }

  /**
   * 合并所有标签
   */
  private mergeTags(
    keywords: { words: string[] },
    emotions: { tags: string[] },
    entities: { tags: string[] },
    ruleTags: string[]
  ): { allTags: string[] } {
    const allTags = [
      ...keywords.words,
      ...emotions.tags,
      ...entities.tags,
      ...ruleTags,
    ];
    
    // 去重
    const uniqueTags = [...new Set(allTags)]
      .filter(tag => tag && tag.trim().length > 0)
      .slice(0, 20); // 限制标签数量
    
    return { allTags: uniqueTags };
  }

  /**
   * 获取主导情感
   */
  private getDominantEmotion(emotions: { analysis?: EmotionAnalysis }): string | undefined {
    return emotions.analysis?.primary;
  }

  /**
   * 分词
   */
  private tokenize(text: string): string[] {
    // 简单的中英文分词
    // 中文：按字符分割（可改进为更复杂的分词）
    // 英文：按单词分割
    
    const chineseWords = text.match(/[\u4e00-\u9fa5]/g) || [];
    const englishWords = text.toLowerCase().match(/[a-z]+/g) || [];
    
    return [...chineseWords, ...englishWords];
  }

  /**
   * 统计单词数
   */
  private countWords(text: string): number {
    const words = text.split(/\s+/).filter(word => word.length > 0);
    return words.length;
  }

  /**
   * 统计唯一单词数
   */
  private countUniqueWords(text: string): number {
    const words = text.toLowerCase().split(/\s+/).filter(word => word.length > 0);
    const uniqueWords = new Set(words);
    return uniqueWords.size;
  }

  /**
   * 生成缓存键
   */
  private generateCacheKey(content: string): string {
    // 简单的内容哈希
    const hash = this.simpleHash(content.substring(0, 100));
    const lengthCategory = content.length < 100 ? 'short' : content.length < 500 ? 'medium' : 'long';
    
    return `tag_${hash}_${lengthCategory}`;
  }

  /**
   * 简单哈希函数
   */
  private simpleHash(str: string): string {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash).toString(36).substring(0, 8);
  }

  /**
   * 清理缓存
   */
  private cleanCache(): void {
    const maxCacheSize = 1000;
    
    if (this.tagCache.size > maxCacheSize) {
      const keysToRemove = Array.from(this.tagCache.keys()).slice(0, this.tagCache.size - maxCacheSize);
      for (const key of keysToRemove) {
        this.tagCache.delete(key);
      }
      
      console.log(`[AutoTagger] 清理缓存: 移除了 ${keysToRemove.length} 个条目`);
    }
  }
}

/**
 * 导出工具函数
 */
export function createTagger(config?: Partial<TaggerConfig>): AutoTagger {
  const fullConfig: TaggerConfig = {
    maxKeywords: 10,
    minKeywordLength: 2,
    emotionDetection: true,
    extractEntities: true,
    ...config,
  };
  
  return new AutoTagger(fullConfig);
}

/**
 * 快速打标函数
 */
export async function quickTag(content: string, config?: Partial<TaggerConfig>): Promise<TaggingResult> {
  const tagger = createTagger(config);
  return tagger.tag(content);
}