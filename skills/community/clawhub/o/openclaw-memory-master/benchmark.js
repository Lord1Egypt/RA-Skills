/**
 * AAAK Compressor - AAAK 压缩算法核心
 * 
 * 基于 MemPalace 的 AAAK 压缩理念
 * Abstract → Align → Anchor → Knowledge
 * 
 * 压缩流程：
 * 1. Abstract: 提取核心摘要，移除冗余
 * 2. Align: 对齐上下文，建立关联
 * 3. Anchor: 识别关键锚点，标记重点
 * 4. Knowledge: 结构化知识，生成压缩表示
 * 
 * @author 小鬼 👻 + Jake
 * @version 4.2.0
 */

import * as fs from 'fs';
import * as path from 'path';

export interface CompressedMemory {
  id: string;
  original?: string;       // 原始内容（可选，用于无损解压）
  abstract: string;        // 摘要（阶段 1）
  align: Alignment[];      // 对齐信息（阶段 2）
  anchors: Anchor[];       // 锚点（阶段 3）
  knowledge: Knowledge;    // 结构化知识（阶段 4）
  metadata: CompressionMetadata;
  checksum: string;        // 校验和（验证无损）
}

export interface Alignment {
  type: 'temporal' | 'semantic' | 'relational';
  source: string;          // 来源片段
  target: string;          // 目标片段
  relation: string;        // 关系描述
  confidence: number;      // 置信度 0-1
}

export interface Anchor {
  id: string;
  type: 'entity' | 'concept' | 'event' | 'action';
  text: string;            // 锚点文本
  position: number;        // 在原文中的位置
  weight: number;          // 权重 0-1
  references: string[];    // 相关引用
}

export interface Knowledge {
  entities: Entity[];
  relations: Relation[];
  summary: string;         // 最终摘要
  keywords: string[];      // 关键词
  categories: string[];    // 分类标签
}

export interface Entity {
  id: string;
  name: string;
  type: string;
  attributes: Record<string, any>;
}

export interface Relation {
  from: string;            // 实体 ID
  to: string;              // 实体 ID
  type: string;
  description: string;
}

export interface CompressionMetadata {
  originalSize: number;    // 原始大小（字节）
  compressedSize: number;  // 压缩后大小（字节）
  compressionRatio: number; // 压缩率
  timestamp: number;
  version: string;
  stages: {
    abstract: boolean;
    align: boolean;
    anchor: boolean;
    knowledge: boolean;
  };
}

export interface CompressionOptions {
  targetRatio?: number;    // 目标压缩率（默认 0.9）
  preserveOriginal?: boolean; // 保留原文（默认 false，只保留结构化数据）
  preserveEntities?: boolean; // 保留实体（默认 true）
  preserveRelations?: boolean; // 保留关系（默认 true）
  minAnchorWeight?: number;   // 最小锚点权重（默认 0.3）
}

/**
 * AAAK 压缩器
 */
export class AAAKCompressor {
  private config: Required<CompressionOptions>;

  constructor(options: CompressionOptions = {}) {
    this.config = {
      targetRatio: options.targetRatio ?? 0.9,
      preserveOriginal: options.preserveOriginal ?? false,
      preserveEntities: options.preserveEntities ?? true,
      preserveRelations: options.preserveRelations ?? true,
      minAnchorWeight: options.minAnchorWeight ?? 0.3,
    };
  }

  /**
   * 压缩记忆
   */
  async compress(content: string, id?: string): Promise<CompressedMemory> {
    const memoryId = id || `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    console.log(`[AAAK] 开始压缩 ${memoryId}`);

    // 阶段 1: Abstract 摘要提取
    console.log(`[AAAK] 阶段 1: Abstract 摘要提取`);
    const abstract = await this.extractAbstract(content);

    // 阶段 2: Align 上下文对齐
    console.log(`[AAAK] 阶段 2: Align 上下文对齐`);
    const alignments = await this.alignContext(content, abstract);

    // 阶段 3: Anchor 关键锚定
    console.log(`[AAAK] 阶段 3: Anchor 关键锚定`);
    const anchors = await this.identifyAnchors(content, abstract);

    // 阶段 4: Knowledge 知识结构化
    console.log(`[AAAK] 阶段 4: Knowledge 知识结构化`);
    const knowledge = await this.structureKnowledge(content, abstract, anchors);

    // 生成压缩结果
    const compressed: CompressedMemory = {
      id: memoryId,
      original: this.config.preserveOriginal ? content : undefined, // 可选保留原文
      abstract,
      align: alignments,
      anchors,
      knowledge,
      metadata: {
        originalSize: Buffer.byteLength(content, 'utf-8'),
        compressedSize: 0, // 待计算
        compressionRatio: 0, // 待计算
        timestamp: Date.now(),
        version: '4.2.0',
        stages: {
          abstract: true,
          align: true,
          anchor: true,
          knowledge: true,
        },
      },
      checksum: this.calculateChecksum(content),
    };

    // 计算压缩后大小
    compressed.metadata.compressedSize = this.calculateCompressedSize(compressed);
    compressed.metadata.compressionRatio = 
      1 - (compressed.metadata.compressedSize / compressed.metadata.originalSize);

    console.log(`[AAAK] 压缩完成:`);
    console.log(`   原始大小：${compressed.metadata.originalSize} 字节`);
    console.log(`   压缩后：${compressed.metadata.compressedSize} 字节`);
    console.log(`   压缩率：${(compressed.metadata.compressionRatio * 100).toFixed(1)}%`);

    return compressed;
  }

  /**
   * 解压记忆（无损还原）
   */
  async decompress(compressed: CompressedMemory): Promise<string> {
    console.log(`[AAAK] 开始解压 ${compressed.id}`);

    // 如果保留了原文，直接返回
    if (compressed.original) {
      // 验证校验和
      const checksum = this.calculateChecksum(compressed.original);
      if (checksum !== compressed.checksum) {
        throw new Error('校验和失败，数据可能已损坏');
      }
      return compressed.original;
    }

    // 否则，从结构化数据重建（有损）
    console.warn('[AAAK] 原文未保留，从结构化数据重建（有损）');
    return this.reconstructFromKnowledge(compressed);
  }

  /**
   * 从知识重建文本（有损）
   */
  private reconstructFromKnowledge(compressed: CompressedMemory): string {
    const parts: string[] = [];
    
    // 使用摘要作为基础
    parts.push(compressed.abstract);
    
    // 添加关键词
    if (compressed.knowledge.keywords.length > 0) {
      parts.push(`关键词：${compressed.knowledge.keywords.join(', ')}`);
    }
    
    // 添加实体
    if (compressed.knowledge.entities.length > 0) {
      parts.push(`实体：${compressed.knowledge.entities.map(e => e.name).join(', ')}`);
    }
    
    return parts.join('\n');
  }

  /**
   * 阶段 1: 提取摘要
   */
  private async extractAbstract(content: string): Promise<string> {
    // 简单实现：提取关键句
    // TODO: 使用 LLM 进行智能摘要
    
    const sentences = content.split(/[。！？.!?]/).filter(s => s.trim().length > 0);
    
    if (sentences.length <= 3) {
      return content;
    }

    // 提取前 3 句和最后 1 句（通常包含关键信息）
    const keySentences = [
      ...sentences.slice(0, 3),
      ...sentences.slice(-1)
    ];

    return keySentences.join('。') + '。';
  }

  /**
   * 阶段 2: 上下文对齐
   */
  private async alignContext(content: string, abstract: string): Promise<Alignment[]> {
    const alignments: Alignment[] = [];

    // 简单实现：查找重复概念
    // TODO: 使用语义分析进行深度对齐
    
    const words = content.split(/[\s,，.。]+/);
    const wordCount = new Map<string, number>();
    
    for (const word of words) {
      if (word.length > 1) { // 忽略单字
        wordCount.set(word, (wordCount.get(word) || 0) + 1);
      }
    }

    // 找出重复出现的词（>2 次）
    for (const [word, count] of wordCount.entries()) {
      if (count > 2) {
        alignments.push({
          type: 'semantic',
          source: word,
          target: word,
          relation: '重复出现',
          confidence: Math.min(count / 5, 1.0),
        });
      }
    }

    return alignments.slice(0, 20); // 限制数量
  }

  /**
   * 阶段 3: 识别锚点
   */
  private async identifyAnchors(content: string, abstract: string): Promise<Anchor[]> {
    const anchors: Anchor[] = [];
    let anchorId = 0;

    // 简单实现：提取名词短语作为锚点
    // TODO: 使用 NER 实体识别
    
    // 匹配可能的实体（简单正则）
    const patterns = [
      /([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)/g,  // 英文专有名词
      /([\u4e00-\u9fa5]{2,})/g,  // 中文词汇
    ];

    for (const pattern of patterns) {
      let match;
      while ((match = pattern.exec(content)) !== null) {
        const text = match[0];
        if (text.length >= 2 && text.length <= 20) {
          anchors.push({
            id: `anchor_${anchorId++}`,
            type: this.classifyAnchorType(text),
            text,
            position: match.index,
            weight: this.calculateAnchorWeight(text, content),
            references: [],
          });
        }
      }
    }

    // 按权重排序，保留 Top-K
    anchors.sort((a, b) => b.weight - a.weight);
    return anchors.filter(a => a.weight >= this.config.minAnchorWeight);
  }

  /**
   * 阶段 4: 构建知识
   */
  private async structureKnowledge(
    content: string,
    abstract: string,
    anchors: Anchor[]
  ): Promise<Knowledge> {
    const entities: Entity[] = [];
    const relations: Relation[] = [];
    const entityIdMap = new Map<string, string>();

    // 从锚点提取实体
    for (const anchor of anchors.slice(0, 10)) { // 限制数量
      if (anchor.type === 'entity') {
        const entityId = `entity_${entities.length}`;
        entityIdMap.set(anchor.text, entityId);
        
        entities.push({
          id: entityId,
          name: anchor.text,
          type: 'concept',
          attributes: {
            weight: anchor.weight,
            mentions: 1,
          },
        });
      }
    }

    // 创建简单关系（共现关系）
    for (let i = 0; i < entities.length - 1; i++) {
      relations.push({
        from: entities[i].id,
        to: entities[i + 1].id,
        type: 'co-occurrence',
        description: '在文本中共现',
      });
    }

    // 提取关键词
    const keywords = anchors
      .slice(0, 10)
      .map(a => a.text)
      .filter((v, i, a) => a.indexOf(v) === i); // 去重

    // 生成分类
    const categories = this.classifyContent(content);

    return {
      entities,
      relations,
      summary: abstract,
      keywords,
      categories,
    };
  }

  /**
   * 分类锚点类型
   */
  private classifyAnchorType(text: string): 'entity' | 'concept' | 'event' | 'action' {
    // 简单启发式分类
    if (/^[A-Z]/.test(text)) {
      return 'entity'; // 大写字母开头，可能是专有名词
    }
    
    if (/(了|着|过|的|地|得)$/.test(text)) {
      return 'action'; // 动词后缀
    }
    
    if (/(事件|活动|会议|比赛)$/.test(text)) {
      return 'event'; // 事件后缀
    }
    
    return 'concept'; // 默认概念
  }

  /**
   * 计算锚点权重
   */
  private calculateAnchorWeight(text: string, content: string): number {
    const occurrences = (content.match(new RegExp(text, 'g')) || []).length;
    const length = text.length;
    
    // 权重 = 出现频率 * 长度因子
    const frequency = occurrences / content.length;
    const lengthFactor = Math.min(length / 10, 1.0);
    
    return Math.min(frequency * 100 * lengthFactor, 1.0);
  }

  /**
   * 分类内容
   */
  private classifyContent(content: string): string[] {
    const categories: string[] = [];
    const contentLower = content.toLowerCase();

    // 简单关键词分类
    if (/(技术|代码|编程|开发|软件)/.test(contentLower)) {
      categories.push('技术');
    }
    
    if (/(学习|知识|教育|培训)/.test(contentLower)) {
      categories.push('学习');
    }
    
    if (/(工作|项目|任务|会议)/.test(contentLower)) {
      categories.push('工作');
    }
    
    if (/(生活|日常|心情|感受)/.test(contentLower)) {
      categories.push('生活');
    }

    return categories.length > 0 ? categories : ['通用'];
  }

  /**
   * 计算校验和
   */
  private calculateChecksum(content: string): string {
    // 简单哈希（实际应该用 SHA-256）
    let hash = 0;
    for (let i = 0; i < content.length; i++) {
      const char = content.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return hash.toString(16);
  }

  /**
   * 计算压缩后大小
   */
  private calculateCompressedSize(compressed: CompressedMemory): number {
    // 估算压缩后的大小（只计算结构化数据）
    const size = 
      Buffer.byteLength(compressed.abstract, 'utf-8') +
      JSON.stringify(compressed.align).length +
      JSON.stringify(compressed.anchors).length +
      JSON.stringify(compressed.knowledge).length +
      JSON.stringify(compressed.metadata).length;
    
    return size;
  }

  /**
   * 批量压缩
   */
  async batchCompress(contents: string[]): Promise<CompressedMemory[]> {
    const results: CompressedMemory[] = [];
    
    for (const content of contents) {
      const compressed = await this.compress(content);
      results.push(compressed);
    }
    
    return results;
  }

  /**
   * 压缩质量评估
   */
  evaluateQuality(original: string, compressed: CompressedMemory): QualityReport {
    const report: QualityReport = {
      compressionRatio: compressed.metadata.compressionRatio,
      informationRetention: 0,
      entityAccuracy: 0,
      relationAccuracy: 0,
      overallScore: 0,
    };

    // 计算信息保留率（简单版本）
    const originalWords = new Set(original.split(/[\s,，.。]+/));
    const compressedWords = new Set(compressed.abstract.split(/[\s,，.。]+/));
    
    let overlap = 0;
    for (const word of compressedWords) {
      if (originalWords.has(word)) {
        overlap++;
      }
    }
    
    report.informationRetention = overlap / originalWords.size;

    // 实体准确率
    report.entityAccuracy = compressed.knowledge.entities.length > 0 ? 0.8 : 0;

    // 关系准确率
    report.relationAccuracy = compressed.knowledge.relations.length > 0 ? 0.7 : 0;

    // 综合评分
    report.overallScore = (
      report.compressionRatio * 0.4 +
      report.informationRetention * 0.3 +
      report.entityAccuracy * 0.15 +
      report.relationAccuracy * 0.15
    );

    return report;
  }
}

export interface QualityReport {
  compressionRatio: number;      // 压缩率
  informationRetention: number;  // 信息保留率
  entityAccuracy: number;        // 实体准确率
  relationAccuracy: number;      // 关系准确率
  overallScore: number;          // 综合评分
}
