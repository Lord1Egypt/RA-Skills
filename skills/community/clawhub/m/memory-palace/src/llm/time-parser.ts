/**
 * Memory Palace v1.1 - TimeParserLLM
 * 
 * Enhanced time parsing using LLM for complex temporal expressions.
 * Target: 10s timeout with optimized prompt.
 */

import type { SubagentClient } from './subagent-client.js';
import type { ParsedTime, TimeParseOptions, LLMResult } from './types.js';
import { defaultClient } from './subagent-client.js';

/**
 * TimeParserLLM - Parse complex time expressions
 * 
 * Features:
 * - Parse relative time ("下周三之前")
 * - Handle fuzzy descriptions ("三天后")
 * - Understand conditional time ("如果明天是周五")
 * - Quick response (target: 10s)
 */
export class TimeParserLLM {
  private client: SubagentClient;

  constructor(client?: SubagentClient) {
    this.client = client ?? defaultClient;
  }

  /**
   * Parse a time expression to a specific date
   * 
   * @param expression Time expression to parse
   * @param options Parse options
   * @returns Parsed date and confidence
   */
  async parse(
    expression: string,
    options?: TimeParseOptions
  ): Promise<LLMResult<ParsedTime>> {
    const referenceDate = options?.referenceDate || this.getToday();
    
    // Check cache for common patterns
    const cached = this.checkCache(expression);
    if (cached) {
      return { success: true, data: cached, duration: 0 };
    }
    
    // Build optimized prompt (minimal for speed)
    const prompt = this.buildPrompt(expression, referenceDate);

    // Call LLM with short timeout
    const result = await this.client.callJSONWithFallback<ParsedTime>(
      {
        task: prompt,
        timeoutSeconds: 10, // Quick task target
        maxRetries: 1, // Fewer retries for speed
      },
      () => this.fallbackParse(expression, referenceDate)
    );

    if (result.success && result.data) {
      // Validate date format
      if (!this.isValidDate(result.data.date)) {
        result.data.date = referenceDate;
        result.data.confidence = 0.3;
      }
    }

    return result;
  }

  /**
   * Build optimized prompt (minimal for speed)
   */
  private buildPrompt(expression: string, referenceDate: string): string {
    return `今日: ${referenceDate}
解析: ${expression}
返回JSON: {"date":"YYYY-MM-DD","confidence":0.9}
仅返回JSON，无解释。`;
  }

  /**
   * Get today's date in YYYY-MM-DD format
   */
  private getToday(): string {
    return new Date().toISOString().split('T')[0];
  }

  /**
   * Check cache for common patterns
   */
  private checkCache(expression: string): ParsedTime | null {
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];
    
    // Common patterns cache (no duplicate keys)
    const cache: Record<string, () => ParsedTime> = {
      '今天': () => ({ date: todayStr, confidence: 1.0 }),
      'today': () => ({ date: todayStr, confidence: 1.0 }),
      '明天': () => {
        const d = new Date(today);
        d.setDate(d.getDate() + 1);
        return { date: d.toISOString().split('T')[0], confidence: 1.0 };
      },
      'tomorrow': () => {
        const d = new Date(today);
        d.setDate(d.getDate() + 1);
        return { date: d.toISOString().split('T')[0], confidence: 1.0 };
      },
      '昨天': () => {
        const d = new Date(today);
        d.setDate(d.getDate() - 1);
        return { date: d.toISOString().split('T')[0], confidence: 1.0 };
      },
      'yesterday': () => {
        const d = new Date(today);
        d.setDate(d.getDate() - 1);
        return { date: d.toISOString().split('T')[0], confidence: 1.0 };
      },
    };

    const normalizer = expression.toLowerCase().trim();
    const fn = cache[normalizer];
    return fn ? fn() : null;
  }

  /**
   * Fallback parse using rule-based engine
   */
  private fallbackParse(expression: string, referenceDate: string): ParsedTime {
    const today = new Date(referenceDate);
    const expr = expression.toLowerCase().trim();
    
    // Relative days (no duplicate keys)
    const dayPatterns: Record<string, number> = {
      '今天': 0, 'today': 0,
      '明天': 1, 'tomorrow': 1,
      '昨天': -1, 'yesterday': -1,
      '后天': 2,
      '前天': -2,
    };

    for (const [pattern, offset] of Object.entries(dayPatterns)) {
      if (expr.includes(pattern)) {
        const result = new Date(today);
        result.setDate(result.getDate() + offset);
        return { date: result.toISOString().split('T')[0], confidence: 0.9 };
      }
    }

    // Weeks
    if (expr.includes('下周') || expr.includes('next week')) {
      const result = new Date(today);
      result.setDate(result.getDate() + 7);
      return { date: result.toISOString().split('T')[0], confidence: 0.8 };
    }
    if (expr.includes('上周') || expr.includes('last week')) {
      const result = new Date(today);
      result.setDate(result.getDate() - 7);
      return { date: result.toISOString().split('T')[0], confidence: 0.8 };
    }

    // Days of week (周一-周日) - no duplicate keys
    const weekDays: Record<string, number> = {
      '周日': 0, '星期日': 0,
      '周一': 1, '星期一': 1,
      '周二': 2, '星期二': 2,
      '周三': 3, '星期三': 3,
      '周四': 4, '星期四': 4,
      '周五': 5, '星期五': 5,
      '周六': 6, '星期六': 6,
    };

    for (const [pattern, dayOfWeek] of Object.entries(weekDays)) {
      if (expr.includes(pattern)) {
        const result = new Date(today);
        const currentDay = result.getDay();
        let daysUntil = dayOfWeek - currentDay;
        
        if (expr.includes('下') || expr.includes('next')) {
          if (daysUntil <= 0) daysUntil += 7;
        } else if (expr.includes('上') || expr.includes('last')) {
          daysUntil = daysUntil - 7;
        } else {
          // This week's
          if (daysUntil < 0) daysUntil += 7;
        }
        
        result.setDate(result.getDate() + daysUntil);
        return { date: result.toISOString().split('T')[0], confidence: 0.85 };
      }
    }

    // Number + day/month patterns
    const daysMatch = expr.match(/(\d+)\s*[天日]/);
    if (daysMatch) {
      const days = parseInt(daysMatch[1], 10);
      const result = new Date(today);
      result.setDate(result.getDate() + days);
      return { date: result.toISOString().split('T')[0], confidence: 0.8 };
    }

    const weeksMatch = expr.match(/(\d+)\s*周/);
    if (weeksMatch) {
      const weeks = parseInt(weeksMatch[1], 10);
      const result = new Date(today);
      result.setDate(result.getDate() + weeks * 7);
      return { date: result.toISOString().split('T')[0], confidence: 0.8 };
    }

    const monthsMatch = expr.match(/(\d+)\s*[个]?月/);
    if (monthsMatch) {
      const months = parseInt(monthsMatch[1], 10);
      const result = new Date(today);
      result.setMonth(result.getMonth() + months);
      return { date: result.toISOString().split('T')[0], confidence: 0.75 };
    }

    // Fallback: return today with low confidence
    return { date: referenceDate, confidence: 0.3 };
  }

  /**
   * Validate date format
   */
  private isValidDate(dateStr: string): boolean {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
    if (!regex.test(dateStr)) return false;
    
    const date = new Date(dateStr);
    return !isNaN(date.getTime());
  }
}

/**
 * Default parser instance
 */
export const defaultTimeParser = new TimeParserLLM();

/**
 * Quick helper for one-off time parsing
 */
export async function parseTime(
  expression: string,
  options?: TimeParseOptions
): Promise<LLMResult<ParsedTime>> {
  return defaultTimeParser.parse(expression, options);
}