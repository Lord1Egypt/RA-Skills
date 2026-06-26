/**
 * Extended Time Patterns
 *
 * Additional time expression patterns for complex temporal reasoning.
 * Extends the base TimeReasoningEngine.
 */

/**
 * Chinese number to digit mapping
 */
const CHINESE_NUMBERS: Record<string, number> = {
  '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
  '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
  '十': 10, '十一': 11, '十二': 12, '十三': 13, '十四': 14,
  '十五': 15, '十六': 16, '十七': 17, '十八': 18, '十九': 19,
  '二十': 20, '二十一': 21, '二十二': 22, '二十三': 23,
};

/**
 * Weekday mapping
 */
const WEEKDAY_MAP: Record<string, number> = {
  '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '日': 0, '天': 0,
};

/**
 * Extended time result
 */
export interface ExtendedTimeResult {
  /** Resolved date */
  date?: Date;
  /** Resolved time (HH:MM) */
  time?: string;
  /** Date range if applicable */
  dateRange?: { start: Date; end: Date };
  /** Direction (for expressions like "before X") */
  direction?: 'before' | 'after';
  /** Recurring pattern */
  recurring?: {
    type: 'yearly' | 'monthly' | 'weekly' | 'daily';
    month?: number;
    day?: number;
    weekday?: number[];
    time?: string;
  };
  /** Whether this is an approximate time */
  approximate?: boolean;
  /** Whether parsing succeeded */
  success: boolean;
}

/**
 * Extended Time Pattern Matcher
 */
export class ExtendedTimePatterns {
  private now: Date;

  constructor(now?: Date) {
    this.now = now || new Date();
  }

  /**
   * Parse complex time expression
   */
  parse(expression: string): ExtendedTimeResult {
    // Pattern 1: "这周五下午三点前"
    const weekTimeBefore = this.parseWeekTimeBefore(expression);
    if (weekTimeBefore.success) return weekTimeBefore;

    // Pattern 2: "下个月第一周"
    const monthFirstWeek = this.parseMonthFirstWeek(expression);
    if (monthFirstWeek.success) return monthFirstWeek;

    // Pattern 3: "本季度末"
    const quarterEnd = this.parseQuarterEnd(expression);
    if (quarterEnd.success) return quarterEnd;

    // Pattern 4: "每年3月"
    const yearly = this.parseYearly(expression);
    if (yearly.success) return yearly;

    // Pattern 5: "工作日早上9点"
    const weekdayTime = this.parseWeekdayTime(expression);
    if (weekdayTime.success) return weekdayTime;

    // Pattern 6: "最近" (approximate)
    const recent = this.parseRecent(expression);
    if (recent.success) return recent;

    return { success: false };
  }

  /**
   * Parse "这周五下午三点前" pattern
   */
  private parseWeekTimeBefore(expression: string): ExtendedTimeResult {
    // Pattern: 这/下 + 周/星期 + [一二三四五六日天] + [上午下午早晚] + [时间] + [前后]
    const pattern = /([这下上])?(周|星期)([一二三四五六日天])(上午|下午|早上|晚上|早|晚)?([零一二三四五六七八九十]+)点?([前后])?/;
    const match = expression.match(pattern);

    if (!match) return { success: false };

    const weekOffset = match[1] === '下' ? 1 : 0;
    const weekday = WEEKDAY_MAP[match[3]];
    const period = match[4];
    const hourChinese = match[5];
    const direction = match[6] as '前' | '后' | undefined;

    // Calculate date
    const targetDate = this.getWeekdayDate(weekday, weekOffset);

    // Parse hour
    let hour = CHINESE_NUMBERS[hourChinese] ?? parseInt(hourChinese, 10);
    if (period === '下午' || period === '晚上') {
      hour += 12;
    }

    return {
      date: targetDate,
      time: `${hour.toString().padStart(2, '0')}:00`,
      direction: direction === '前' ? 'before' : direction === '后' ? 'after' : undefined,
      success: true,
    };
  }

  /**
   * Parse "下个月第一周" pattern
   */
  private parseMonthFirstWeek(expression: string): ExtendedTimeResult {
    const pattern = /(下个|本|这)?月(第)?([一二三四]?)周/;
    const match = expression.match(pattern);

    if (!match) return { success: false };

    const monthOffset = match[1] === '下个' ? 1 : 0;
    const weekNum = match[3] ? CHINESE_NUMBERS[match[3]] : 1;

    // Calculate date range
    const startDate = new Date(this.now);
    startDate.setMonth(startDate.getMonth() + monthOffset, 1);
    startDate.setDate((weekNum - 1) * 7 + 1);
    startDate.setHours(0, 0, 0, 0);

    const endDate = new Date(startDate);
    endDate.setDate(startDate.getDate() + 6);
    endDate.setHours(23, 59, 59, 999);

    return {
      dateRange: { start: startDate, end: endDate },
      success: true,
    };
  }

  /**
   * Parse "本季度末" pattern
   */
  private parseQuarterEnd(expression: string): ExtendedTimeResult {
    const pattern = /(本|这|下个)?季度(末|底|结束)/;
    const match = expression.match(pattern);

    if (!match) return { success: false };

    const quarterOffset = match[1] === '下个' ? 1 : 0;
    const currentQuarter = Math.floor(this.now.getMonth() / 3);
    const targetQuarter = (currentQuarter + quarterOffset) % 4;
    const targetYear = this.now.getFullYear() + Math.floor((currentQuarter + quarterOffset) / 4);

    // Last day of quarter
    const endMonth = (targetQuarter + 1) * 3;
    const endDate = new Date(targetYear, endMonth, 0); // Last day of previous month

    return {
      date: endDate,
      success: true,
    };
  }

  /**
   * Parse "每年3月" pattern (recurring)
   */
  private parseYearly(expression: string): ExtendedTimeResult {
    const pattern = /每年(\d{1,2})月(\d{1,2})?[日号]?/;
    const match = expression.match(pattern);

    if (!match) return { success: false };

    const month = parseInt(match[1], 10);
    const day = match[2] ? parseInt(match[2], 10) : undefined;

    return {
      recurring: {
        type: 'yearly',
        month,
        day,
      },
      success: true,
    };
  }

  /**
   * Parse "工作日早上9点" pattern
   */
  private parseWeekdayTime(expression: string): ExtendedTimeResult {
    const pattern = /(工作日|平日)(早上|上午|下午|晚上)?([零一二三四五六七八九十]+)点?/;
    const match = expression.match(pattern);

    if (!match) return { success: false };

    const period = match[2];
    let hour = CHINESE_NUMBERS[match[3]] ?? parseInt(match[3], 10);

    if (period === '下午' || period === '晚上') {
      hour += 12;
    }

    return {
      recurring: {
        type: 'weekly',
        weekday: [1, 2, 3, 4, 5], // Monday to Friday
        time: `${hour.toString().padStart(2, '0')}:00`,
      },
      success: true,
    };
  }

  /**
   * Parse "最近" pattern (approximate)
   */
  private parseRecent(expression: string): ExtendedTimeResult {
    const pattern = /最近|近期|这几天/;
    const match = expression.match(pattern);

    if (!match) return { success: false };

    const start = new Date(this.now);
    start.setHours(0, 0, 0, 0);

    const end = new Date(this.now);
    end.setDate(end.getDate() + 7);
    end.setHours(23, 59, 59, 999);

    return {
      dateRange: { start, end },
      approximate: true,
      success: true,
    };
  }

  /**
   * Get date for a specific weekday
   */
  private getWeekdayDate(weekday: number, weekOffset: number = 0): Date {
    const result = new Date(this.now);
    const currentDay = result.getDay();

    // Calculate days to target weekday
    let daysToTarget = weekday - currentDay;
    if (daysToTarget <= 0 && weekOffset === 0) {
      // If same week and day has passed, assume next week
      daysToTarget += 7;
    }
    if (weekOffset > 0) {
      daysToTarget += weekOffset * 7;
    }

    result.setDate(result.getDate() + daysToTarget);
    result.setHours(0, 0, 0, 0);

    return result;
  }
}

/**
 * Create an ExtendedTimePatterns instance
 */
export function createExtendedTimePatterns(now?: Date): ExtendedTimePatterns {
  return new ExtendedTimePatterns(now);
}