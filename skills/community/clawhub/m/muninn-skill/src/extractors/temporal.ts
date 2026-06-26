/**
 * Temporal Extractor for Muninn Memory System
 * 
 * Extracts dates from text and normalizes to ISO format for efficient temporal queries.
 * Designed to power the LOCOMO benchmark temporal questions like:
 * "When did Caroline go to the LGBTQ support group?"
 * 
 * Handles:
 * - Absolute dates: "May 7, 2023", "7 May 2023", "2023-05-07"
 * - Relative dates: "last Tuesday", "yesterday", "next week"
 * - Relative to reference: "the week before 6 July 2023"
 * - Date ranges: "the week before X", "the month of August 2023"
 * 
 * Returns: Array of { date: Date, text: string, confidence: number }
 */

import { DateTime } from 'luxon';

export interface TemporalExtraction {
  /** Extracted date or start of range */
  date: Date;
  /** End date if range */
  endDate?: Date;
  /** Type of extraction */
  dateType: 'absolute' | 'relative' | 'range';
  /** Granularity */
  granularity: 'hour' | 'day' | 'week' | 'month' | 'year';
  /** Original text that was parsed */
  originalText: string;
  /** Confidence level (0-1) */
  confidence: number;
}

/**
 * Get reference clock - can be overridden for testing
 */
function getReferenceDate(): Date {
  return new Date();
}

/**
 * Day name to index (0 = Monday)
 */
const DAY_NAMES: Record<string, number> = {
  monday: 0, tuesday: 1, wednesday: 2, thursday: 3,
  friday: 4, saturday: 5, sunday: 6
};

/**
 * Month name to number (1-12)
 */
const MONTH_NAMES: Record<string, number> = {
  january: 1, february: 2, march: 3, april: 4, may: 5, june: 6,
  july: 7, august: 8, september: 9, october: 10, november: 11, december: 12
};

/**
 * Extract all dates from text
 * 
 * @param text - Input text containing date mentions
 * @param referenceDate - Optional reference date for relative calculations (defaults to now)
 * @returns Array of temporal extractions
 */
export function extractDates(
  text: string,
  referenceDate?: Date
): TemporalExtraction[] {
  const results: TemporalExtraction[] = [];
  const ref = referenceDate ? DateTime.fromJSDate(referenceDate) : DateTime.now();
  
  // Track what we've matched to avoid duplicates
  const matchedSpans = new Set<string>();
  
  // Helper to add result if not duplicate
  const addResult = (extraction: TemporalExtraction) => {
    // Skip invalid dates
    if (!extraction.date || !(extraction.date instanceof Date) || isNaN(extraction.date.getTime())) {
      return;
    }
    const dateISO = extraction.date.toISOString ? extraction.date.toISOString() : String(extraction.date);
    const spanKey = `${extraction.originalText}-${dateISO}`;
    if (!matchedSpans.has(spanKey)) {
      matchedSpans.add(spanKey);
      results.push(extraction);
    }
  };
  
  // ==========================================================================
  // 1. ABSOLUTE DATE PATTERNS
  // ==========================================================================
  
  // Pattern: "7 May 2023", "7th May 2023", "May 7, 2023", "May 7th 2023", "May 7th, 2023"
  // Also handles "May 2023" (month only) and "2023" (year only)
  const monthDayYearPattern = /(?:(\d{1,2})(?:st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december)(?:\s*,?\s*(\d{4}))?)|(?:(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})(?:st|nd|rd|th)?(?:,?\s*(\d{4}))?)|(\d{4})(?=\s|$|[,.])/gi;
  
  let match;
  while ((match = monthDayYearPattern.exec(text)) !== null) {
    const fullMatch = match[0];
    
    try {
      let year = ref.year;
      let month = 1;
      let day = 1;
      let granularity: 'day' | 'month' | 'year' = 'day';
      
      // Case 1: "7 May 2023" format - match[1]=day, match[2]=month, match[3]=year
      if (match[1] && match[2] && !/^\d+$/.test(match[2])) {
        day = parseInt(match[1]);
        month = MONTH_NAMES[match[2].toLowerCase()];
        if (match[3]) year = parseInt(match[3]);
      }
      // Case 2: "May 7, 2023" format - match[4]=month, match[5]=day, match[6]=year
      else if (match[4] && match[5]) {
        month = MONTH_NAMES[match[4].toLowerCase()];
        day = parseInt(match[5]);
        if (match[6]) year = parseInt(match[6]);
      }
      // Case 3: "May 2023" (month + year, no day) - match[4]=month only
      else if (match[4] && !match[5]) {
        month = MONTH_NAMES[match[4].toLowerCase()];
        day = 1;
        granularity = 'month';
        if (match[6]) year = parseInt(match[6]);
      }
      // Case 4: "2023" (year only)
      else if (match[7]) {
        year = parseInt(match[7]);
        month = 1;
        day = 1;
        granularity = 'year';
      }
      
      if (year >= 1900 && year <= 2100) {
        const dt = DateTime.fromObject({ year, month, day });
        if (dt.isValid) {
          addResult({
            date: dt.toJSDate(),
            dateType: 'absolute',
            granularity,
            originalText: fullMatch,
            confidence: granularity === 'day' ? 0.95 : granularity === 'month' ? 0.8 : 0.7
          });
        }
      }
    } catch (e) {
      // Skip invalid dates
    }
  }
  
  // Pattern: ISO format "2023-05-07", "2023/05/07"
  const isoPattern = /(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})/g;
  while ((match = isoPattern.exec(text)) !== null) {
    const fullMatch = match[0];
    try {
      const year = parseInt(match[1]);
      const month = parseInt(match[2]);
      const day = parseInt(match[3]);
      
      const dt = DateTime.fromObject({ year, month, day });
      if (dt.isValid && year >= 1900 && year <= 2100) {
        addResult({
          date: dt.toJSDate(),
          dateType: 'absolute',
          granularity: 'day',
          originalText: fullMatch,
          confidence: 0.98
        });
      }
    } catch (e) {
      // Skip
    }
  }
  
  // Pattern: US format "03/07/2023" or "03-07-2023"
  const usPattern = /(\d{1,2})[-\/](\d{1,2})[-\/](\d{4})/g;
  while ((match = usPattern.exec(text)) !== null) {
    const fullMatch = match[0];
    // Skip if it looks like ISO (first part > 12)
    if (parseInt(match[1]) > 12) continue;
    
    try {
      const month = parseInt(match[1]);
      const day = parseInt(match[2]);
      const year = parseInt(match[3]);
      
      const dt = DateTime.fromObject({ year, month, day });
      if (dt.isValid) {
        addResult({
          date: dt.toJSDate(),
          dateType: 'absolute',
          granularity: 'day',
          originalText: fullMatch,
          confidence: 0.9
        });
      }
    } catch (e) {
      // Skip
    }
  }
  
  // ==========================================================================
  // 2. RELATIVE DATE PATTERNS
  // ==========================================================================
  
  // "yesterday"
  const yesterdayMatch = text.match(/\byesterday\b/i);
  if (yesterdayMatch) {
    const dt = ref.minus({ days: 1 });
    addResult({
      date: dt.toJSDate(),
      dateType: 'relative',
      granularity: 'day',
      originalText: 'yesterday',
      confidence: 0.95
    });
  }
  
  // "tomorrow"
  const tomorrowMatch = text.match(/\btomorrow\b/i);
  if (tomorrowMatch) {
    const dt = ref.plus({ days: 1 });
    addResult({
      date: dt.toJSDate(),
      dateType: 'relative',
      granularity: 'day',
      originalText: 'tomorrow',
      confidence: 0.95
    });
  }
  
  // "last Monday", "last Tuesday", etc.
  const lastDayMatch = text.match(/last\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)/i);
  if (lastDayMatch) {
    const targetDay = DAY_NAMES[lastDayMatch[1].toLowerCase()];
    let diff = ref.weekday - 1 - targetDay;
    if (diff <= 0) diff += 7;
    const dt = ref.minus({ days: diff });
    addResult({
      date: dt.toJSDate(),
      dateType: 'relative',
      granularity: 'day',
      originalText: lastDayMatch[0],
      confidence: 0.9
    });
  }
  
  // "next Monday", "next Tuesday", etc.
  const nextDayMatch = text.match(/next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)/i);
  if (nextDayMatch) {
    const targetDay = DAY_NAMES[nextDayMatch[1].toLowerCase()];
    let diff = targetDay - (ref.weekday - 1);
    if (diff <= 0) diff += 7;
    const dt = ref.plus({ days: diff });
    addResult({
      date: dt.toJSDate(),
      dateType: 'relative',
      granularity: 'day',
      originalText: nextDayMatch[0],
      confidence: 0.9
    });
  }
  
  // "Monday", "Tuesday" without next/last (assume past occurrence)
  const standaloneDayMatch = text.match(/\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b(?!\s+(next|last|week|month))/i);
  if (standaloneDayMatch && !text.match(/\b(next|last)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)/i)) {
    const targetDay = DAY_NAMES[standaloneDayMatch[1].toLowerCase()];
    let diff = ref.weekday - 1 - targetDay;
    if (diff < 0) diff += 7; // Target is earlier this week, go back
    const dt = ref.minus({ days: diff });
    addResult({
      date: dt.toJSDate(),
      dateType: 'relative',
      granularity: 'day',
      originalText: standaloneDayMatch[0],
      confidence: 0.7
    });
  }
  
  // "X days ago", "two weeks ago"
  const agoPattern = /(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+(day|days|week|weeks|month|months|year|years)\s+ago\b/i;
  const agoMatch = text.match(agoPattern);
  if (agoMatch) {
    const wordToNum: Record<string, number> = {
      one: 1, two: 2, three: 3, four: 4, five: 5,
      six: 6, seven: 7, eight: 8, nine: 9, ten: 10
    };
    const countStr = agoMatch[1].toLowerCase();
    const count = wordToNum[countStr] || parseInt(countStr);
    const unit = agoMatch[2].toLowerCase();
    
    const unitMap: Record<string, string> = {
      day: 'days', days: 'days', week: 'weeks', weeks: 'weeks',
      month: 'months', months: 'months', year: 'years', years: 'years'
    };
    
    const dt = ref.minus({ [unitMap[unit]]: count });
    const granularity = unit.includes('week') ? 'week' : unit.includes('month') ? 'month' : unit.includes('year') ? 'year' : 'day';
    
    addResult({
      date: dt.toJSDate(),
      dateType: 'relative',
      granularity,
      originalText: agoMatch[0],
      confidence: 0.9
    });
  }
  
  // "in X days/weeks/months"
  const inFuturePattern = /in\s+(?:a\s+)?(\d+)?\s*(day|days|week|weeks|month|months|year|years)\b/i;
  const inFutureMatch = text.match(inFuturePattern);
  if (inFutureMatch) {
    const count = inFutureMatch[1] ? parseInt(inFutureMatch[1]) : 1;
    const unit = inFutureMatch[2].toLowerCase();
    
    const unitMap: Record<string, string> = {
      day: 'days', days: 'days', week: 'weeks', weeks: 'weeks',
      month: 'months', months: 'months', year: 'years', years: 'years'
    };
    
    const dt = ref.plus({ [unitMap[unit]]: count });
    const granularity = unit.includes('week') ? 'week' : unit.includes('month') ? 'month' : unit.includes('year') ? 'year' : 'day';
    
    addResult({
      date: dt.toJSDate(),
      dateType: 'relative',
      granularity,
      originalText: inFutureMatch[0],
      confidence: 0.85
    });
  }
  
  // ==========================================================================
  // 3. DATE RANGE PATTERNS
  // ==========================================================================
  
  // "the week before X" - need to find X first
  const weekBeforeMatch = text.match(/the\s+week\s+before\s+(\d{1,2}\s+\w+\s+\d{4}|\w+\s+\d{1,2},?\s+\d{4}|\d{4}-\d{2}-\d{2})/i);
  if (weekBeforeMatch) {
    // Extract the reference date from the match
    const refDateStr = weekBeforeMatch[1];
    const refDate = parseExplicitDate(refDateStr, ref);
    if (refDate) {
      const start = refDate.minus({ days: 7 });
      addResult({
        date: start.toJSDate(),
        endDate: refDate.minus({ days: 1 }).toJSDate(),
        dateType: 'range',
        granularity: 'week',
        originalText: weekBeforeMatch[0],
        confidence: 0.85
      });
    }
  }
  
  // "the week after X"
  const weekAfterMatch = text.match(/the\s+week\s+after\s+(\d{1,2}\s+\w+\s+\d{4}|\w+\s+\d{1,2},?\s+\d{4}|\d{4}-\d{2}-\d{2})/i);
  if (weekAfterMatch) {
    const refDateStr = weekAfterMatch[1];
    const refDate = parseExplicitDate(refDateStr, ref);
    if (refDate) {
      const end = refDate.plus({ days: 7 });
      addResult({
        date: refDate.plus({ days: 1 }).toJSDate(),
        endDate: end.toJSDate(),
        dateType: 'range',
        granularity: 'week',
        originalText: weekAfterMatch[0],
        confidence: 0.85
      });
    }
  }
  
  // "last week", "this week", "next week"
  const weekRangeMatch = text.match(/\b(last|this|next)\s+week\b/i);
  if (weekRangeMatch) {
    const weekType = weekRangeMatch[1].toLowerCase();
    let start: DateTime;
    let end: DateTime;
    
    const monday = ref.startOf('week');
    
    if (weekType === 'last') {
      start = monday.minus({ weeks: 1 });
      end = monday.minus({ days: 1 });
    } else if (weekType === 'this') {
      start = monday;
      end = monday.plus({ days: 6 });
    } else {
      start = monday.plus({ weeks: 1 });
      end = monday.plus({ days: 13 });
    }
    
    addResult({
      date: start.toJSDate(),
      endDate: end.toJSDate(),
      dateType: 'range',
      granularity: 'week',
      originalText: weekRangeMatch[0],
      confidence: 0.85
    });
  }
  
  // "last month", "this month", "next month"
  const monthRangeMatch = text.match(/\b(last|this|next)\s+month\b/i);
  if (monthRangeMatch) {
    const monthType = monthRangeMatch[1].toLowerCase();
    let start: DateTime;
    let end: DateTime;
    
    const monthStart = ref.startOf('month');
    
    if (monthType === 'last') {
      start = monthStart.minus({ months: 1 });
      end = monthStart.minus({ days: 1 });
    } else if (monthType === 'this') {
      start = monthStart;
      end = monthStart.plus({ months: 1 }).minus({ days: 1 });
    } else {
      start = monthStart.plus({ months: 1 });
      end = monthStart.plus({ months: 2 }).minus({ days: 1 });
    }
    
    addResult({
      date: start.toJSDate(),
      endDate: end.toJSDate(),
      dateType: 'range',
      granularity: 'month',
      originalText: monthRangeMatch[0],
      confidence: 0.85
    });
  }
  
  // "August 2023" - month + year range
  const monthYearMatch = text.match(/\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})\b/i);
  if (monthYearMatch) {
    const month = MONTH_NAMES[monthYearMatch[1].toLowerCase()];
    const year = parseInt(monthYearMatch[2]);
    const start = DateTime.fromObject({ year, month, day: 1 });
    const end = start.endOf('month');
    
    addResult({
      date: start.toJSDate(),
      endDate: end.toJSDate(),
      dateType: 'range',
      granularity: 'month',
      originalText: monthYearMatch[0],
      confidence: 0.9
    });
  }
  
  return results;
}

/**
 * Parse an explicit date string (like "6 July 2023")
 */
function parseExplicitDate(dateStr: string, ref: DateTime): DateTime | null {
  // Try ISO format first
  const isoMatch = dateStr.match(/(\d{4})-(\d{2})-(\d{2})/);
  if (isoMatch) {
    return DateTime.fromObject({
      year: parseInt(isoMatch[1]),
      month: parseInt(isoMatch[2]),
      day: parseInt(isoMatch[3])
    });
  }
  
  // Try "6 July 2023" format
  const dayMonthYearMatch = dateStr.match(/(\d{1,2})\s+(\w+)\s+(\d{4})/);
  if (dayMonthYearMatch) {
    const day = parseInt(dayMonthYearMatch[1]);
    const month = MONTH_NAMES[dayMonthYearMatch[2].toLowerCase()];
    const year = parseInt(dayMonthYearMatch[3]);
    return DateTime.fromObject({ year, month, day });
  }
  
  // Try "July 6, 2023" format
  const monthDayYearMatch = dateStr.match(/(\w+)\s+(\d{1,2}),?\s+(\d{4})/);
  if (monthDayYearMatch) {
    const month = MONTH_NAMES[monthDayYearMatch[1].toLowerCase()];
    const day = parseInt(monthDayYearMatch[2]);
    const year = parseInt(monthDayYearMatch[3]);
    return DateTime.fromObject({ year, month, day });
  }
  
  return null;
}

/**
 * Detect if a query is asking about a temporal relationship
 * Common patterns: "When did...", "What day...", "What time..."
 */
export function detectTemporalQuery(query: string): {
  isTemporal: boolean;
  temporalType: 'when' | 'what_day' | 'what_time' | 'duration' | 'frequency' | null;
  extractedDates: TemporalExtraction[];
} {
  const lowerQuery = query.toLowerCase();
  
  // "When did X..." or "When was..."
  if (lowerQuery.startsWith('when did') || lowerQuery.startsWith('when was') || lowerQuery.startsWith('when is')) {
    return {
      isTemporal: true,
      temporalType: 'when',
      extractedDates: extractDates(query)
    };
  }
  
  // "What day..."
  if (lowerQuery.startsWith('what day')) {
    return {
      isTemporal: true,
      temporalType: 'what_day',
      extractedDates: extractDates(query)
    };
  }
  
  // "What time..."
  if (lowerQuery.startsWith('what time')) {
    return {
      isTemporal: true,
      temporalType: 'what_time',
      extractedDates: extractDates(query)
    };
  }
  
  // "How long..." / "How often..."
  if (lowerQuery.startsWith('how long') || lowerQuery.startsWith('how often')) {
    return {
      isTemporal: true,
      temporalType: lowerQuery.startsWith('how long') ? 'duration' : 'frequency',
      extractedDates: extractDates(query)
    };
  }
  
  return {
    isTemporal: false,
    temporalType: null,
    extractedDates: []
  };
}

/**
 * Format a date for display
 */
export function formatDate(date: Date, format: 'iso' | 'readable' | 'relative' = 'readable'): string {
  const dt = DateTime.fromJSDate(date);
  
  switch (format) {
    case 'iso':
      return dt.toISODate() || date.toISOString();
    case 'relative':
      return dt.toRelative() || dt.toFormat('MMM dd, yyyy');
    default:
      return dt.toFormat('MMMM dd, yyyy');
  }
}

/**
 * Format a date range for display
 */
export function formatDateRange(start: Date, end: Date, format: 'iso' | 'readable' = 'readable'): string {
  const startDt = DateTime.fromJSDate(start);
  const endDt = DateTime.fromJSDate(end);
  
  if (format === 'iso') {
    return `${startDt.toISODate()}/${endDt.toISODate()}`;
  }
  
  // Same month
  if (startDt.month === endDt.month && startDt.year === endDt.year) {
    return `${startDt.toFormat('MMMM d')} - ${endDt.toFormat('d, yyyy')}`;
  }
  
  // Same year
  if (startDt.year === endDt.year) {
    return `${startDt.toFormat('MMM d')} - ${endDt.toFormat('MMM d, yyyy')}`;
  }
  
  return `${startDt.toFormat('MMM d, yyyy')} - ${endDt.toFormat('MMM d, yyyy')}`;
}
