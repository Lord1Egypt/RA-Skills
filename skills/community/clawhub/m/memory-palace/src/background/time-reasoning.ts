/**
 * Time Reasoning Engine
 * 
 * Parses temporal expressions in queries and converts them to search keywords
 * for better memory retrieval.
 */

/**
 * Parsed time context from a query
 */
export interface TimeContext {
  /** Original query string */
  originalQuery: string;
  /** Parsed specific date if mentioned */
  parsedDate?: Date;
  /** Day of week if mentioned */
  dayOfWeek?: '周一' | '周二' | '周三' | '周四' | '周五' | '周六' | '周日' |
              '星期一' | '星期二' | '星期三' | '星期四' | '星期五' | '星期六' | '星期日';
  /** Relative time expression */
  relativeTime?: 'today' | 'tomorrow' | 'yesterday' | 'next_week' | 'last_week' | 
                 'next_month' | 'last_month' | 'this_week' | 'this_month';
  /** Time range if applicable */
  timeRange?: { start: Date; end: Date };
  /** Extracted keywords for search */
  keywords: string[];
  /** Whether time reasoning was applied */
  hasTimeReasoning: boolean;
}

/**
 * Day of week mapping
 */
const DAY_OF_WEEK_MAP: Record<string, number> = {
  '周日': 0, '星期日': 0, '星期天': 0, '周天': 0,
  '周一': 1, '星期一': 1,
  '周二': 2, '星期二': 2,
  '周三': 3, '星期三': 3,
  '周四': 4, '星期四': 4,
  '周五': 5, '星期五': 5,
  '周六': 6, '星期六': 6,
};

/**
 * Time Reasoning Engine
 * 
 * Analyzes queries for temporal expressions and generates search keywords.
 */
export class TimeReasoningEngine {
  private now: Date;
  
  constructor(now?: Date) {
    this.now = now || new Date();
  }
  
  /**
   * Parse a query for temporal expressions
   */
  parseTimeQuery(query: string): TimeContext {
    const context: TimeContext = {
      originalQuery: query,
      keywords: [],
      hasTimeReasoning: false,
    };
    
    // Extract relative time expressions
    const relativeTime = this.extractRelativeTime(query);
    if (relativeTime) {
      context.relativeTime = relativeTime;
      context.hasTimeReasoning = true;
      context.timeRange = this.calculateTimeRange(relativeTime);
    }
    
    // Extract day of week
    const dayOfWeek = this.extractDayOfWeek(query);
    if (dayOfWeek) {
      context.dayOfWeek = dayOfWeek;
      context.hasTimeReasoning = true;
    }
    
    // Extract specific dates
    const parsedDate = this.extractSpecificDate(query);
    if (parsedDate) {
      context.parsedDate = parsedDate;
      context.hasTimeReasoning = true;
    }
    
    // Generate keywords based on time context
    context.keywords = this.generateKeywords(context, query);
    
    return context;
  }
  
  /**
   * Convert time context to search keywords
   */
  timeToKeywords(context: TimeContext): string[] {
    return context.keywords;
  }
  
  /**
   * Extract relative time expressions
   */
  private extractRelativeTime(query: string): TimeContext['relativeTime'] | null {
    const lower = query.toLowerCase();
    
    // Check for relative time patterns
    if (/今[天日]/.test(query) || /today/.test(lower)) {
      return 'today';
    }
    if (/明[天日]/.test(query) || /tomorrow/.test(lower)) {
      return 'tomorrow';
    }
    if (/昨[天日]/.test(query) || /yesterday/.test(lower)) {
      return 'yesterday';
    }
    if (/下[个星期周]/.test(query) || /next\s*week/.test(lower)) {
      return 'next_week';
    }
    if (/上[个星期周]/.test(query) || /last\s*week/.test(lower)) {
      return 'last_week';
    }
    if (/这[个星期周]/.test(query) || /this\s*week/.test(lower)) {
      return 'this_week';
    }
    if (/下[个]?月/.test(query) || /next\s*month/.test(lower)) {
      return 'next_month';
    }
    if (/上[个]?月/.test(query) || /last\s*month/.test(lower)) {
      return 'last_month';
    }
    if (/本[个]?月/.test(query) || /this\s*month/.test(lower)) {
      return 'this_month';
    }
    
    return null;
  }
  
  /**
   * Extract day of week from query
   */
  private extractDayOfWeek(query: string): TimeContext['dayOfWeek'] | null {
    const dayPattern = /(周[一二三四五六日天]|星期[一二三四五六日天])/g;
    const match = query.match(dayPattern);
    if (match) {
      const found = match[0];
      // Validate it's a proper day string
      if (DAY_OF_WEEK_MAP[found] !== undefined) {
        return found as TimeContext['dayOfWeek'];
      }
    }
    
    return null;
  }
  
  /**
   * Extract specific date from query (e.g., "3月15日", "2024-03-15")
   */
  private extractSpecificDate(query: string): Date | null {
    // Match patterns like "3月15日", "3月15", "03-15"
    const monthDayPattern = /(\d{1,2})月(\d{1,2})[日号]?/;
    const match = query.match(monthDayPattern);
    if (match) {
      const month = parseInt(match[1], 10) - 1; // JavaScript months are 0-indexed
      const day = parseInt(match[2], 10);
      const year = this.now.getFullYear();
      return new Date(year, month, day);
    }
    
    // Match patterns like "2024年3月15日", "2024-03-15"
    const fullDatePattern = /(\d{4})[年\-\/](\d{1,2})[月\-\/](\d{1,2})[日号]?/;
    const fullMatch = query.match(fullDatePattern);
    if (fullMatch) {
      const year = parseInt(fullMatch[1], 10);
      const month = parseInt(fullMatch[2], 10) - 1;
      const day = parseInt(fullMatch[3], 10);
      return new Date(year, month, day);
    }
    
    return null;
  }
  
  /**
   * Calculate time range for relative time expressions
   */
  private calculateTimeRange(relativeTime: NonNullable<TimeContext['relativeTime']>): { start: Date; end: Date } {
    const start = new Date(this.now);
    const end = new Date(this.now);
    
    switch (relativeTime) {
      case 'today':
        start.setHours(0, 0, 0, 0);
        end.setHours(23, 59, 59, 999);
        break;
        
      case 'tomorrow':
        start.setDate(start.getDate() + 1);
        start.setHours(0, 0, 0, 0);
        end.setDate(end.getDate() + 1);
        end.setHours(23, 59, 59, 999);
        break;
        
      case 'yesterday':
        start.setDate(start.getDate() - 1);
        start.setHours(0, 0, 0, 0);
        end.setDate(end.getDate() - 1);
        end.setHours(23, 59, 59, 999);
        break;
        
      case 'this_week':
        // Start from Monday of this week
        const dayOfWeek = start.getDay() || 7; // Convert Sunday from 0 to 7
        start.setDate(start.getDate() - dayOfWeek + 1);
        start.setHours(0, 0, 0, 0);
        end.setDate(start.getDate() + 6);
        end.setHours(23, 59, 59, 999);
        break;
        
      case 'next_week':
        // Start from Monday of next week
        const nextWeekDay = start.getDay() || 7;
        start.setDate(start.getDate() - nextWeekDay + 8);
        start.setHours(0, 0, 0, 0);
        end.setDate(start.getDate() + 6);
        end.setHours(23, 59, 59, 999);
        break;
        
      case 'last_week':
        // Start from Monday of last week
        const lastWeekDay = start.getDay() || 7;
        start.setDate(start.getDate() - lastWeekDay - 6);
        start.setHours(0, 0, 0, 0);
        end.setDate(start.getDate() + 6);
        end.setHours(23, 59, 59, 999);
        break;
        
      case 'this_month':
        start.setDate(1);
        start.setHours(0, 0, 0, 0);
        end.setMonth(end.getMonth() + 1);
        end.setDate(0); // Last day of current month
        end.setHours(23, 59, 59, 999);
        break;
        
      case 'next_month':
        start.setMonth(start.getMonth() + 1);
        start.setDate(1);
        start.setHours(0, 0, 0, 0);
        end.setMonth(end.getMonth() + 2);
        end.setDate(0);
        end.setHours(23, 59, 59, 999);
        break;
        
      case 'last_month':
        start.setMonth(start.getMonth() - 1);
        start.setDate(1);
        start.setHours(0, 0, 0, 0);
        end.setMonth(end.getMonth());
        end.setDate(0);
        end.setHours(23, 59, 59, 999);
        break;
    }
    
    return { start, end };
  }
  
  /**
   * Generate search keywords from time context
   */
  private generateKeywords(context: TimeContext, originalQuery: string): string[] {
    const keywords: string[] = [];
    
    // Add day of week
    if (context.dayOfWeek) {
      keywords.push(context.dayOfWeek);
      // Also add short form
      if (context.dayOfWeek.startsWith('星期')) {
        keywords.push(context.dayOfWeek.replace('星期', '周'));
      }
    }
    
    // Add date-related keywords
    if (context.parsedDate) {
      const month = context.parsedDate.getMonth() + 1;
      const day = context.parsedDate.getDate();
      keywords.push(`${month}月${day}日`);
      keywords.push(`${month}月${day}`);
      keywords.push(`${month}月${day}号`);
    }
    
    // Add range-based keywords
    if (context.timeRange) {
      const formatDate = (d: Date): string => `${d.getMonth() + 1}月${d.getDate()}日`;
      
      if (context.relativeTime === 'next_week' || context.relativeTime === 'this_week') {
        keywords.push(`${formatDate(context.timeRange.start)}-${formatDate(context.timeRange.end)}`);
        // Add individual days of the week
        const dayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
        const startDay = context.timeRange.start.getDay();
        for (let i = 0; i < 7; i++) {
          keywords.push(dayNames[(startDay + i) % 7]);
        }
      }
      
      if (context.relativeTime === 'this_month' || context.relativeTime === 'next_month') {
        keywords.push(`${context.timeRange.start.getMonth() + 1}月`);
      }
    }
    
    // Add contextual keywords based on time expression
    if (context.relativeTime === 'tomorrow') {
      keywords.push('明天');
    } else if (context.relativeTime === 'today') {
      keywords.push('今天');
    }
    
    // Add event-related keywords from context
    if (/准备|安排|计划|会议|重要|截止|deadline/i.test(originalQuery)) {
      if (/准备/.test(originalQuery)) keywords.push('准备');
      if (/安排/.test(originalQuery)) keywords.push('安排');
      if (/计划/.test(originalQuery)) keywords.push('计划');
      if (/会议/.test(originalQuery)) keywords.push('会议');
      if (/重要/.test(originalQuery)) keywords.push('重要');
      if (/截止|deadline/i.test(originalQuery)) keywords.push('截止');
    }
    
    return [...new Set(keywords)]; // Remove duplicates
  }
  
  /**
   * Get current date info for context
   */
  getCurrentDateInfo(): { 
    today: Date;
    dayOfWeek: string;
    month: number;
    year: number;
    weekRange: { start: Date; end: Date };
  } {
    const dayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    const dayOfWeek = dayNames[this.now.getDay()];
    
    // Get this week's range
    const weekStart = new Date(this.now);
    const day = weekStart.getDay() || 7;
    weekStart.setDate(weekStart.getDate() - day + 1);
    weekStart.setHours(0, 0, 0, 0);
    
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekEnd.getDate() + 6);
    weekEnd.setHours(23, 59, 59, 999);
    
    return {
      today: this.now,
      dayOfWeek,
      month: this.now.getMonth() + 1,
      year: this.now.getFullYear(),
      weekRange: { start: weekStart, end: weekEnd },
    };
  }
  
  /**
   * Resolve "if tomorrow is X" type conditional queries
   */
  resolveConditionalTime(query: string): { 
    isConditional: boolean;
    condition?: string;
    targetDay?: string;
    keywords: string[];
  } {
    // Match patterns like "如果明天是周三", "假如明天是星期三"
    // Pattern: (如果|假如|假设) + (明天|今天|后天) + 是 + (周X|星期X)
    const conditionalPattern = /(如果|假如|假设).*(明天|今天|后天).*是.*(周[一二三四五六日天]|星期[一二三四五六日天])/;
    const match = query.match(conditionalPattern);
    
    if (match) {
      const relativeDay = match[2];
      const targetDay = match[3];
      
      // Calculate the actual day if the condition were true
      // This is hypothetical reasoning
      const keywords: string[] = [targetDay];
      
      // Add related event keywords
      if (/准备/.test(query)) keywords.push('准备');
      if (/会议/.test(query)) keywords.push('会议');
      if (/安排/.test(query)) keywords.push('安排');
      
      return {
        isConditional: true,
        condition: `${relativeDay}是${targetDay}`,
        targetDay,
        keywords,
      };
    }
    
    return {
      isConditional: false,
      keywords: [],
    };
  }
}

/**
 * Create a TimeReasoningEngine instance
 */
export function createTimeReasoning(now?: Date): TimeReasoningEngine {
  return new TimeReasoningEngine(now);
}