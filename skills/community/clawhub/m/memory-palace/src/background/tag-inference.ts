/**
 * Tag Inference Engine
 *
 * Automatically infers tags from memory content using TF-IDF and rule mapping.
 */

import { TopicCluster } from '../cognitive/cluster.js';

/**
 * Rule mapping: keyword pattern -> tag
 */
const TAG_RULES: Array<{ patterns: RegExp[]; tag: string }> = [
  // Project-related
  { patterns: [/项目|project|工程|代码|code|模块|module/i], tag: '项目' },
  // Decision
  { patterns: [/决定|决策|选择|方案|确定|选了|决定用/i], tag: '决策' },
  // Preference
  { patterns: [/偏好|喜欢|习惯|倾向|偏好|prefer|like/i], tag: '偏好' },
  // Problem/Bug
  { patterns: [/bug|错误|问题|异常|报错|error|issue|故障/i], tag: '问题' },
  // Experience/Lesson
  { patterns: [/经验|教训|注意|记得|记住|要点|总结/i], tag: '经验' },
  // Technical
  { patterns: [/api|接口|数据库|database|redis|服务|server|架构/i], tag: '技术' },
  // User info
  { patterns: [/用户名|我叫|我的名字|名字是|username/i], tag: '用户' },
  // Schedule/Time
  { patterns: [/会议|日程|安排|schedule|meeting|周会/i], tag: '日程' },
  // Document
  { patterns: [/文档|doc|readme|说明|指南/i], tag: '文档' },
  // Config
  { patterns: [/配置|config|设置|setting|环境变量/i], tag: '配置' },
];

/**
 * Inference options
 */
export interface TagInferenceOptions {
  /** Maximum tags to infer (default: 3) */
  maxTags?: number;
  /** Minimum content length for inference (default: 20) */
  minLength?: number;
  /** Whether to merge with existing tags */
  mergeExisting?: boolean;
}

/**
 * Inference result
 */
export interface TagInferenceResult {
  /** Inferred tags */
  tags: string[];
  /** Whether inference was performed */
  inferred: boolean;
  /** Source of tags: 'rules' | 'keywords' | 'default' */
  source: 'rules' | 'keywords' | 'default';
}

/**
 * Tag Inference Engine
 */
export class TagInferenceEngine {
  private cluster: TopicCluster;

  constructor() {
    this.cluster = new TopicCluster();
  }

  /**
   * Infer tags from content
   */
  infer(content: string, options: TagInferenceOptions = {}): TagInferenceResult {
    const maxTags = options.maxTags ?? 3;
    const minLength = options.minLength ?? 20;

    // Skip if content too short
    if (content.length < minLength) {
      return {
        tags: ['未分类'],
        inferred: false,
        source: 'default',
      };
    }

    // Step 1: Try rule-based inference
    const ruleTags = this.inferByRules(content);
    if (ruleTags.length > 0) {
      return {
        tags: ruleTags.slice(0, maxTags),
        inferred: true,
        source: 'rules',
      };
    }

    // Step 2: Fall back to keyword-based inference
    const keywords = this.cluster.extractKeywordsFromContent(content, maxTags);
    if (keywords.length > 0) {
      return {
        tags: keywords,
        inferred: true,
        source: 'keywords',
      };
    }

    // Step 3: Default tag
    return {
      tags: ['未分类'],
      inferred: false,
      source: 'default',
    };
  }

  /**
   * Infer tags using rule patterns
   */
  private inferByRules(content: string): string[] {
    const tags: string[] = [];
    const matchedPatterns = new Set<string>();

    for (const rule of TAG_RULES) {
      for (const pattern of rule.patterns) {
        if (pattern.test(content)) {
          // Avoid duplicate tags from different patterns
          const tagKey = rule.tag;
          if (!matchedPatterns.has(tagKey)) {
            tags.push(rule.tag);
            matchedPatterns.add(tagKey);
          }
          break; // Only match first pattern per rule
        }
      }
    }

    return tags;
  }

  /**
   * Merge inferred tags with existing tags
   */
  merge(inferredTags: string[], existingTags: string[]): string[] {
    const merged = new Set([...existingTags, ...inferredTags]);
    return Array.from(merged);
  }
}

/**
 * Create a TagInferenceEngine instance
 */
export function createTagInferenceEngine(): TagInferenceEngine {
  return new TagInferenceEngine();
}