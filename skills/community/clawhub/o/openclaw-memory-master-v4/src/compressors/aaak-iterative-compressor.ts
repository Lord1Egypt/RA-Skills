/**
 * AAAK 迭代压缩器 v4.2.0
 * 
 * 基于 Hermes Agent 的"Compression as Consolidation"理念
 * 支持累积式摘要更新，而非每次都重新开始
 * 
 * 核心特性:
 * - 迭代压缩：新内容 + 旧摘要 → 更新后的摘要
 * - 结构化模板：决策/任务/时间线/技术细节
 * - Lineage 追踪：保留压缩历史链
 * 
 * @author 小鬼 👻
 * @date 2026-04-11
 * @version 4.2.0
 */

import type { MemoryOrb, MemoryType } from './types/memory';
import {
  PerformanceMonitor,
  LRUCache,
  ParallelProcessor,
  IncrementalCompressor,
  generateCacheKey,
} from './performance-optimizer';

// ============ 类型定义 ============

/**
 * 压缩结果
 */
export interface CompressionResult {
  summary: string;              // 压缩后的摘要
  compressionRatio: number;     // 压缩率 (0-1)
  isIterative: boolean;         // 是否是迭代压缩
  lineageChain: string[];       // 谱系链 (父记忆 ID 列表)
  metadata: CompressionMetadata;
}

/**
 * 压缩元数据
 */
export interface CompressionMetadata {
  originalLength: number;       // 原始长度
  compressedLength: number;     // 压缩后长度
  tokenCount: number;           // Token 数量
  processingTime: number;       // 处理时间 (ms)
  template: CompressionTemplateType; // 使用的模板类型
  importance: number;           // 重要性评分
  keyPoints: string[];          // 关键点提取
}

/**
 * 压缩模板类型
 */
export type CompressionTemplateType = 
  | 'standard'      // 标准摘要
  | 'structured'    // 结构化摘要 (Hermes 风格)
  | 'iterative'     // 迭代更新
  | 'emergency';   // 紧急压缩 (高压缩率)

/**
 * 结构化摘要模板
 */
export interface StructuredSummary {
  keyDecisions: string[];       // 关键决策
  pendingTasks: string[];       // 未完成事项
  technicalDetails: string[];   // 技术细节
  nextActions: string[];        // 下一步行动
  timeline: TimelineEvent[];    // 时间线
  emotions?: EmotionRecord[];   // 情感记录 (可选)
}

/**
 * 时间线事件
 */
export interface TimelineEvent {
  timestamp: number;
  event: string;
  importance: number;
}

/**
 * 情感记录
 */
export interface EmotionRecord {
  type: 'joy' | 'sadness' | 'fear' | 'anger' | 'disgust' | 'surprise';
  intensity: number;  // 0-1
  trigger?: string;
}

// ============ Prompt 模板 ============

/**
 * 标准压缩 Prompt
 */
const STANDARD_PROMPT = `请总结以下内容，保留核心信息：

{content}

要求:
- 简洁明了
- 保留关键事实
- 去除冗余信息
- 长度控制在 {maxLength} 字以内`;

/**
 * 结构化压缩 Prompt (Hermes 风格)
 */
const STRUCTURED_PROMPT = `请分析以下内容，提取结构化信息：

{content}

请按以下格式输出:

## 关键决策
- 决策 1
- 决策 2

## 未完成事项
- 任务 1
- 任务 2

## 技术细节
- 细节 1
- 细节 2

## 下一步行动
1. 行动 1
2. 行动 2

## 时间线
- [时间] 事件 1
- [时间] 事件 2`;

/**
 * 迭代压缩 Prompt (核心！)
 */
const ITERATIVE_PROMPT = `你是一个记忆压缩专家。你需要更新已有的摘要，而不是重新总结。

【之前的摘要】
{previousSummary}

【新内容】
{newContent}

【任务】
请更新摘要，将新内容整合到之前的摘要中：
1. 保留之前摘要中有价值的信息
2. 添加新内容的关键信息
3. 合并重复内容
4. 更新时间线和状态
5. 保持累积性，不要丢失重要上下文

【输出格式】
请直接输出更新后的完整摘要，不需要解释。`;

/**
 * 紧急压缩 Prompt (高压缩率)
 */
const EMERGENCY_PROMPT = `极度压缩以下内容，只保留最核心的信息：

{content}

要求:
- 只保留最关键的事实
- 压缩到 {maxLength} 字以内
- 可以丢失细节，但必须保留主旨`;

// ============ 核心压缩器 ============

export class AAAKIterativeCompressor {
  private maxLength: number;
  private targetCompressionRatio: number;
  
  // 性能优化组件 (v4.2.0 新增)
  private performanceMonitor: PerformanceMonitor;
  private cache: LRUCache<string>;
  private parallelProcessor: ParallelProcessor<string, CompressionResult>;
  private incrementalCompressor: IncrementalCompressor;
  
  constructor(options?: {
    maxLength?: number;
    targetCompressionRatio?: number;
    enableCache?: boolean;
    cacheSize?: number;
    maxConcurrency?: number;
  }) {
    this.maxLength = options?.maxLength || 2000;
    this.targetCompressionRatio = options?.targetCompressionRatio || 0.6;
    
    // 初始化性能优化组件
    this.performanceMonitor = new PerformanceMonitor();
    this.cache = new LRUCache({
      maxSize: options?.cacheSize || 1000,
      ttlMs: 300000, // 5 分钟
      enableStats: true,
    });
    this.parallelProcessor = new ParallelProcessor({
      maxConcurrency: options?.maxConcurrency || 5,
      timeoutMs: 10000,
      retryCount: 3,
    });
    this.incrementalCompressor = new IncrementalCompressor();
  }

  /**
   * 压缩记忆 (带性能优化 v4.2.0)
   * @param content 要压缩的内容
   * @param previousSummary 之前的摘要 (可选，用于迭代压缩)
   * @param parentMemoryId 父记忆 ID (用于 lineage 追踪)
   */
  async compress(
    content: string,
    previousSummary?: string,
    parentMemoryId?: string
  ): Promise<CompressionResult> {
    const startTime = Date.now();
    const originalLength = content.length;
    
    // 生成缓存 key
    const cacheKey = generateCacheKey(content, 'iterative', parentMemoryId);
    
    // 1. 检查缓存 (v4.2.0 新增)
    const cachedResult = this.cache.get(cacheKey);
    if (cachedResult) {
      this.performanceMonitor.recordCompression(Date.now() - startTime, true);
      return JSON.parse(cachedResult);
    }
    
    // 2. 检查是否需要重新压缩 (增量优化)
    if (!previousSummary && this.incrementalCompressor.needsRecompression(content, cacheKey)) {
      const cachedSummary = this.incrementalCompressor.getCachedSummary(cacheKey);
      if (cachedSummary) {
        this.performanceMonitor.recordCompression(Date.now() - startTime, true);
        return this.createCompressionResult(cachedSummary, originalLength, false, parentMemoryId, Date.now() - startTime);
      }
    }
    
    // 3. 判断是否使用迭代压缩
    const isIterative = !!previousSummary && previousSummary.length > 0;
    
    // 4. 选择 Prompt 模板
    const prompt = this.selectPrompt(content, isIterative);
    
    // 5. 调用 LLM 进行压缩
    const summary = await this.callLLM(prompt, {
      content,
      previousSummary,
      maxLength: this.maxLength,
    });
    
    const compressedLength = summary.length;
    const compressionRatio = compressedLength / originalLength;
    
    // 6. 提取元数据
    const metadata = this.extractMetadata(summary, originalLength, compressedLength);
    metadata.processingTime = Date.now() - startTime;
    
    // 7. 构建谱系链
    const lineageChain = parentMemoryId ? [parentMemoryId] : [];
    
    const result = {
      summary,
      compressionRatio,
      isIterative,
      lineageChain,
      metadata,
    };
    
    // 8. 更新缓存 (v4.2.0 新增)
    this.cache.set(cacheKey, JSON.stringify(result));
    this.incrementalCompressor.updateCache(cacheKey, content, summary);
    
    // 9. 记录性能
    this.performanceMonitor.recordCompression(metadata.processingTime, false);
    
    return result;
  }

  /**
   * 选择 Prompt 模板
   */
  private selectPrompt(content: string, isIterative: boolean): string {
    if (isIterative) {
      return ITERATIVE_PROMPT;
    }
    
    // 根据内容长度选择
    if (content.length > 10000) {
      return STRUCTURED_PROMPT;
    }
    
    return STANDARD_PROMPT;
  }

  /**
   * 调用 LLM 进行压缩
   */
  private async callLLM(
    prompt: string,
    variables: Record<string, any>
  ): Promise<string> {
    // 替换变量
    let filledPrompt = prompt;
    for (const [key, value] of Object.entries(variables)) {
      filledPrompt = filledPrompt.replace(
        new RegExp(`\\{${key}\\}`, 'g'),
        String(value)
      );
    }
    
    // TODO: 实际调用 LLM
    // 这里应该调用 Memory-Master 的 LLM 服务
    // 暂时返回模拟结果
    
    console.log('🔮 AAAK 压缩 Prompt:', filledPrompt.slice(0, 200) + '...');
    
    // 模拟 LLM 响应
    return this.simulateLLMResponse(variables.content, variables.previousSummary);
  }

  /**
   * 模拟 LLM 响应 (用于测试)
   */
  private simulateLLMResponse(content: string, previousSummary?: string): string {
    if (previousSummary) {
      // 迭代压缩：合并旧摘要和新内容
      return `[迭代摘要]\n\n${previousSummary}\n\n【新增】\n${this.extractKeyPoints(content).join('\n')}`;
    }
    
    // 标准压缩：提取关键点
    const keyPoints = this.extractKeyPoints(content);
    return keyPoints.slice(0, 5).join('\n');
  }

  /**
   * 提取关键点
   */
  private extractKeyPoints(content: string): string[] {
    // 简单的关键点提取 (按行分割，过滤空行)
    return content
      .split('\n')
      .filter(line => line.trim().length > 0)
      .filter(line => !line.startsWith('#')) // 过滤标题
      .map(line => line.trim())
      .slice(0, 10);
  }

  /**
   * 提取元数据
   */
  private extractMetadata(
    summary: string,
    originalLength: number,
    compressedLength: number
  ): CompressionMetadata {
    const lines = summary.split('\n').filter(l => l.trim().length > 0);
    
    return {
      originalLength,
      compressedLength,
      tokenCount: Math.ceil(summary.length / 4), // 粗略估算
      processingTime: 0, // 由外部计算
      template: 'standard',
      importance: this.calculateImportance(summary),
      keyPoints: lines.slice(0, 5),
    };
  }

  /**
   * 计算重要性评分
   */
  private calculateImportance(summary: string): number {
    // 简单的重要性评分逻辑
    const indicators = [
      { pattern: /核心|关键|重要/g, weight: 0.3 },
      { pattern: /决策|决定/g, weight: 0.2 },
      { pattern: /完成|成功/g, weight: 0.2 },
      { pattern: /TODO|待办|任务/g, weight: 0.1 },
      { pattern: /错误|问题|Bug/g, weight: 0.2 },
    ];
    
    let score = 0.5; // 基础分
    
    for (const { pattern, weight } of indicators) {
      const matches = summary.match(pattern);
      if (matches) {
        score += weight * Math.min(matches.length, 3) / 3;
      }
    }
    
    return Math.min(score, 1.0);
  }

  /**
   * 批量压缩 (v4.2.0 新增 - 并行处理)
   * @param items 压缩任务列表
   * @returns 压缩结果列表
   */
  async compressBatch(
    items: Array<{
      content: string;
      previousSummary?: string;
      parentMemoryId?: string;
    }>
  ): Promise<CompressionResult[]> {
    return this.parallelProcessor.process(items, async (item) => {
      return this.compress(item.content, item.previousSummary, item.parentMemoryId);
    });
  }

  /**
   * 获取性能报告 (v4.2.0 新增)
   */
  getPerformanceReport() {
    return {
      metrics: this.performanceMonitor.getReport(),
      cache: this.cache.getStats(),
      isPerformanceOk: this.performanceMonitor.isPerformanceOk(100),
    };
  }

  /**
   * 清除缓存 (v4.2.0 新增)
   */
  clearCache(key?: string) {
    if (key) {
      this.cache.delete(key);
    } else {
      this.cache.clear();
    }
  }
}

// ============ 辅助函数 ============

/**
 * 结构化摘要解析器
 */
export function parseStructuredSummary(summary: string): StructuredSummary {
  const result: StructuredSummary = {
    keyDecisions: [],
    pendingTasks: [],
    technicalDetails: [],
    nextActions: [],
    timeline: [],
  };
  
  const sections = summary.split(/##\s*/);
  
  for (const section of sections) {
    if (section.includes('关键决策')) {
      result.keyDecisions = extractListItems(section);
    } else if (section.includes('未完成事项')) {
      result.pendingTasks = extractListItems(section);
    } else if (section.includes('技术细节')) {
      result.technicalDetails = extractListItems(section);
    } else if (section.includes('下一步行动')) {
      result.nextActions = extractListItems(section);
    } else if (section.includes('时间线')) {
      result.timeline = extractTimeline(section);
    }
  }
  
  return result;
}

/**
 * 提取列表项
 */
function extractListItems(section: string): string[] {
  return section
    .split('\n')
    .filter(line => line.match(/^[-*•]\s+/))
    .map(line => line.replace(/^[-*•]\s+/, '').trim());
}

/**
 * 提取时间线
 */
function extractTimeline(section: string): TimelineEvent[] {
  return section
    .split('\n')
    .filter(line => line.match(/\[.*?\]/))
    .map(line => {
      const match = line.match(/\[(.*?)\]\s*(.*)/);
      if (match) {
        return {
          timestamp: Date.parse(match[1]) || Date.now(),
          event: match[2].trim(),
          importance: 0.5,
        };
      }
      return null;
    })
    .filter((e): e is TimelineEvent => e !== null);
}

// ============ 导出 ============

export default AAAKIterativeCompressor;
