/**
 * Temporal Metadata Extractor
 * 
 * Converts natural language time expressions into ISO dates and relative offsets.
 * Ported from Python dateparser approach for Muninn Memory System.
 * 
 * Usage:
 *   extractTemporalMetadata("in a fortnight", new Date()) 
 *   → { eventTime: "2026-03-12", daysOffset: 14, isFuture: true }
 */

import { DateTime, Duration } from 'luxon';

/**
 * Safe DateTime wrapper that never throws
 * Returns null for invalid inputs instead of crashing
 */
function safeDateTimeFromObject(opts: Record<string, number | undefined>, fallback?: DateTime): DateTime | null {
  // Validate all values are valid numbers
  for (const [key, val] of Object.entries(opts)) {
    if (val === undefined || val === null || Number.isNaN(val)) {
      // Invalid value - use fallback or return null
      return fallback || null;
    }
  }
  
  try {
    const dt = DateTime.fromObject(opts as any);
    return dt.isValid ? dt : (fallback || null);
  } catch {
    return fallback || null;
  }
}

/**
 * Safe DateTime from ISO string
 */
function safeDateTimeFromISO(iso: string, fallback?: DateTime): DateTime | null {
  if (!iso || typeof iso !== 'string') return fallback || null;
  
  try {
    const dt = DateTime.fromISO(iso);
    return dt.isValid ? dt : (fallback || null);
  } catch {
    return fallback || null;
  }
}

/**
 * Reference clock - injected into all temporal operations
 * Defaults to now, but can be overridden for testing or context-aware extraction
 */
export function getReferenceClock(): DateTime {
  return DateTime.now();
}

export interface TemporalMetadata {
  /** When this was mentioned */
  mentionTime: string;
  /** The parsed event time (ISO format) */
  eventTime: string | null;
  /** Days from mention to event */
  daysOffset: number | null;
  /** Is this a future event? */
  isFuture: boolean | null;
  /** Granularity of the time expression */
  granularity: 'hour' | 'day' | 'week' | 'month' | 'year' | null;
  /** Original text that was parsed */
  originalText: string;
  /** Confidence level (0-1) */
  confidence: number;
}

// Relative time patterns
const RELATIVE_PATTERNS: Array<{
  pattern: RegExp;
  resolver: (match: RegExpMatchArray, base: DateTime) => DateTime | null;
}> = [
  // "in a fortnight", "in two weeks", "in 3 days"
  {
    pattern: /in\s+(?:a\s+)?(\d+)?\s*(fortnight|week|weeks|day|days|month|months|year|years|hour|hours|minute|minutes)/i,
    resolver: (match, base) => {
      const count = match[1] ? parseInt(match[1]) : 1;
      const unit = match[2].toLowerCase();
      
      if (unit === 'fortnight') {
        return base.plus({ days: 14 * count });
      }
      
      const unitMap: Record<string, string> = {
        'week': 'weeks', 'weeks': 'weeks',
        'day': 'days', 'days': 'days',
        'month': 'months', 'months': 'months',
        'year': 'years', 'years': 'years',
        'hour': 'hours', 'hours': 'hours',
        'minute': 'minutes', 'minutes': 'minutes'
      };
      
      return base.plus({ [unitMap[unit] || unit]: count });
    }
  },
  
  // "next Tuesday", "next week", "next month"
  {
    pattern: /next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|week|month|year)/i,
    resolver: (match, base) => {
      const target = match[1].toLowerCase();
      
      if (target === 'week') return base.plus({ weeks: 1 });
      if (target === 'month') return base.plus({ months: 1 });
      if (target === 'year') return base.plus({ years: 1 });
      
      // Day of week
      const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
      const targetDay = days.indexOf(target);
      const currentDay = base.weekday - 1; // Luxon uses 1-7, we need 0-6
      let diff = targetDay - currentDay;
      if (diff <= 0) diff += 7; // Next occurrence
      
      return base.plus({ days: diff });
    }
  },
  
  // "last Monday", "last week", etc.
  {
    pattern: /last\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|week|month|year)/i,
    resolver: (match, base) => {
      const target = match[1].toLowerCase();
      
      if (target === 'week') return base.minus({ weeks: 1 });
      if (target === 'month') return base.minus({ months: 1 });
      if (target === 'year') return base.minus({ years: 1 });
      
      const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
      const targetDay = days.indexOf(target);
      const currentDay = base.weekday - 1;
      let diff = currentDay - targetDay;
      if (diff <= 0) diff += 7;
      
      return base.minus({ days: diff });
    }
  },
  
  // "tomorrow"
  {
    pattern: /\btomorrow\b/i,
    resolver: (_, base) => base.plus({ days: 1 })
  },

  // "yesterday"
  {
    pattern: /\byesterday\b/i,
    resolver: (_, base) => base.minus({ days: 1 })
  },

  // "today"
  {
    pattern: /\btoday\b/i,
    resolver: (_, base) => base
  },

  // "on Tuesday", "on Monday" - resolve to most recent occurrence
  // If the day hasn't happened yet this week, use last week's occurrence
  // If it has passed, use this week's occurrence
  {
    pattern: /on\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b/i,
    resolver: (match, base) => {
      const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
      const target = match[1].toLowerCase();
      const targetDay = days.indexOf(target);
      const currentDay = base.weekday - 1; // Luxon uses 1-7, we need 0-6

      // Calculate days since that day this week
      let diff = currentDay - targetDay;
      if (diff < 0) diff += 7; // Target is earlier in the week, go back

      // If the day is today, diff is 0 - return today
      // If the day is in the past this week, diff is positive
      // If the day is in the future this week, we wrap around to last week

      return base.minus({ days: diff });
    }
  },

  // Standalone day names "Tuesday", "Monday" (without "on")
  {
    pattern: /\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b(?!\s+(next|last|week|month))/i,
    resolver: (match, base) => {
      const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
      const target = match[1].toLowerCase();
      const targetDay = days.indexOf(target);
      const currentDay = base.weekday - 1;

      // Most recent occurrence
      let diff = currentDay - targetDay;
      if (diff < 0) diff += 7;

      return base.minus({ days: diff });
    }
  },

  // "X days/weeks/months/years ago" - generic past offset (digits or words)
  {
    pattern: /(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+(day|days|week|weeks|month|months|year|years)\s+ago\b/i,
    resolver: (match, base) => {
      const wordToNum: Record<string, number> = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
      };
      const countRaw = match[1].toLowerCase();
      const count = wordToNum[countRaw] || parseInt(match[1]);
      const unit = match[2].toLowerCase();

      const unitMap: Record<string, string> = {
        'day': 'days', 'days': 'days',
        'week': 'weeks', 'weeks': 'weeks',
        'month': 'months', 'months': 'months',
        'year': 'years', 'years': 'years'
      };

      return base.minus({ [unitMap[unit] || unit]: count });
    }
  },

  // "a day/week/month/year ago"
  {
    pattern: /a\s+(day|week|month|year)\s+ago\b/i,
    resolver: (match, base) => {
      const unit = match[1].toLowerCase();
      const unitMap: Record<string, string> = {
        'day': 'days', 'week': 'weeks', 'month': 'months', 'year': 'years'
      };
      return base.minus({ [unitMap[unit] || unit]: 1 });
    }
  },
  
  // "in 2 weeks time", "3 days time"
  {
    pattern: /(\d+)\s+(week|weeks|day|days|month|months|year|years)\s+time/i,
    resolver: (match, base) => {
      const count = parseInt(match[1]);
      const unit = match[2].toLowerCase();
      
      const unitMap: Record<string, string> = {
        'week': 'weeks', 'weeks': 'weeks',
        'day': 'days', 'days': 'days',
        'month': 'months', 'months': 'months',
        'year': 'years', 'years': 'years'
      };
      
      return base.plus({ [unitMap[unit] || unit]: count });
    }
  },
  
  // "a week from now", "2 days from now"
  {
    pattern: /(?:a|(\d+))\s+(week|weeks|day|days|month|months|year|years)\s+from\s+now/i,
    resolver: (match, base) => {
      const count = match[1] ? parseInt(match[1]) : 1;
      const unit = match[2].toLowerCase();
      
      const unitMap: Record<string, string> = {
        'week': 'weeks', 'weeks': 'weeks',
        'day': 'days', 'days': 'days',
        'month': 'months', 'months': 'months',
        'year': 'years', 'years': 'years'
      };
      
      return base.plus({ [unitMap[unit] || unit]: count });
    }
  },
  
  // "2 weeks after X", "3 days before X" - returns pattern match only, needs context
  {
    pattern: /(\d+)\s+(week|weeks|day|days|month|months|year|years)\s+(after|before)\s+(.+)/i,
    resolver: (match, base) => {
      // This requires context resolution - mark as needing further processing
      return null; // Will be handled by context-aware processor
    }
  }
];

// Absolute date patterns
const ABSOLUTE_PATTERNS: Array<{
  pattern: RegExp;
  parser: (match: RegExpMatchArray, base: DateTime) => DateTime | null;
}> = [
  // "March 15", "March 15th", "15th March"
  {
    pattern: /(?:on\s+)?(?:(\d{1,2})(?:st|nd|rd|th)?\s+)?(january|february|march|april|may|june|july|august|september|october|november|december)(?:\s+(\d{1,2})(?:st|nd|rd|th)?)?(?:\s+(\d{4}))?/i,
    parser: (match, base) => {
      const monthName = match[2].toLowerCase();
      const months = ['january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december'];
      const month = months.indexOf(monthName) + 1;
      const dayRaw = match[1] || match[3];
      const yearRaw = match[4];
      
      const day = dayRaw ? parseInt(dayRaw) : 1;
      const year = yearRaw ? parseInt(yearRaw) : base.year;
      
      // Use safe wrapper
      return safeDateTimeFromObject({ year, month, day }, base);
    }
  },
  
  // "2026-03-15", "2026/03/15"
  {
    pattern: /(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})/,
    parser: (match, _) => {
      return safeDateTimeFromObject({
        year: parseInt(match[1]),
        month: parseInt(match[2]),
        day: parseInt(match[3])
      }) || getReferenceClock();
    }
  },
  
  // "15/03/2026", "15-03-2026" (day first, common in AU/UK)
  {
    pattern: /(\d{1,2})[-\/](\d{1,2})[-\/](\d{4})/,
    parser: (match, _) => {
      return safeDateTimeFromObject({
        year: parseInt(match[3]),
        month: parseInt(match[2]),
        day: parseInt(match[1])
      }) || getReferenceClock();
    }
  }
];

/**
 * Extract temporal metadata from natural language text
 * 
 * Architecture: Reference Clock Injection
 * - Every extraction call includes Current_Time context
 * - Invalid dates degrade gracefully (return null, not crash)
 * - Reference clock can be overridden for testing or context-aware extraction
 */
export function extractTemporalMetadata(
  text: string,
  referenceDate?: Date | string | null
): TemporalMetadata {
  // Use reference clock with fallback
  let base: DateTime;
  if (referenceDate instanceof Date) {
    const dt = DateTime.fromJSDate(referenceDate);
    base = dt.isValid ? dt : getReferenceClock();
  } else if (typeof referenceDate === 'string') {
    const dt = safeDateTimeFromISO(referenceDate);
    base = dt || getReferenceClock();
  } else {
    base = getReferenceClock();
  }
  
  const result: TemporalMetadata = {
    mentionTime: base.toISO() || base.toFormat('yyyy-MM-dd'),
    eventTime: null,
    daysOffset: null,
    isFuture: null,
    granularity: null,
    originalText: text,
    confidence: 0
  };
  
  // Try relative patterns first
  for (const { pattern, resolver } of RELATIVE_PATTERNS) {
    const match = text.match(pattern);
    if (match) {
      const resolved = resolver(match, base);
      if (resolved) {
        const delta = resolved.diff(base, 'days').days;
        
        result.eventTime = resolved.toISODate() || null;
        result.daysOffset = Math.round(delta);
        result.isFuture = delta > 0;
        result.granularity = determineGranularity(match[0]);
        result.confidence = 0.9;
        
        return result;
      }
    }
  }
  
  // Try absolute patterns
  for (const { pattern, parser } of ABSOLUTE_PATTERNS) {
    const match = text.match(pattern);
    if (match) {
      const parsed = parser(match, base);
      if (parsed && parsed.isValid) {
        const delta = parsed.diff(base, 'days').days;
        
        result.eventTime = parsed.toISODate() || null;
        result.daysOffset = Math.round(delta);
        result.isFuture = delta > 0;
        result.granularity = 'day';
        result.confidence = 0.95;
        
        return result;
      }
    }
  }
  
  // Fallback: try to extract any time-like phrases
  const timePhrase = text.match(/(?:in|after|before|next|last)\s+\d+\s+(?:day|week|month|year|hour|minute)s?/i);
  if (timePhrase) {
    result.confidence = 0.3;
    result.granularity = null;
  }
  
  return result;
}

/**
 * Determine the granularity of a time expression
 */
function determineGranularity(text: string): 'hour' | 'day' | 'week' | 'month' | 'year' {
  const lower = text.toLowerCase();
  
  if (lower.includes('hour') || lower.includes('minute')) return 'hour';
  if (lower.includes('week') || lower.includes('fortnight')) return 'week';
  if (lower.includes('month')) return 'month';
  if (lower.includes('year')) return 'year';
  
  return 'day';
}

/**
 * Batch extract temporal metadata from multiple texts
 */
export function extractTemporalMetadataBatch(
  texts: string[],
  referenceDate: Date = new Date()
): Array<{ text: string; metadata: TemporalMetadata }> {
  return texts.map(text => ({
    text,
    metadata: extractTemporalMetadata(text, referenceDate)
  }));
}

/**
 * Resolve "X days after Y" style expressions with context
 * 
 * Architecture: Multi-Hop Temporal Join
 * 1. Muninn retrieves the date of "Y" (Single-hop factual recall)
 * 2. Feed that date as reference_date into this function
 * 3. Calculate the offset
 * 
 * Example: "Two weeks after the launch"
 * - First: Retrieve "launch" event date from memory store
 * - Then: Calculate launch_date + 14 days
 */
export function resolveRelativeWithContext(
  text: string,
  contextEvents: Map<string, Date>,
  referenceDate?: Date | string | null
): TemporalMetadata {
  // Safe reference clock handling
  let base: DateTime;
  if (referenceDate instanceof Date) {
    const dt = DateTime.fromJSDate(referenceDate);
    base = dt.isValid ? dt : getReferenceClock();
  } else if (typeof referenceDate === 'string') {
    const dt = safeDateTimeFromISO(referenceDate);
    base = dt || getReferenceClock();
  } else {
    base = getReferenceClock();
  }
  
  // Pattern: "X days/weeks/months after/before [event]"
  const match = text.match(/(\d+)\s+(day|days|week|weeks|month|months|year|years)\s+(after|before)\s+(.+)/i);
  
  if (!match) {
    return extractTemporalMetadata(text, referenceDate);
  }
  
  const countRaw = parseInt(match[1]);
  const count = Number.isNaN(countRaw) ? 1 : countRaw;
  const unit = match[2].toLowerCase();
  const direction = match[3].toLowerCase();
  const eventRef = match[4].trim().toLowerCase();
  
  // Look up the referenced event
  const eventDate = contextEvents.get(eventRef);
  if (!eventDate) {
    // Can't resolve without context
    return {
      mentionTime: base.toISO() || base.toFormat('yyyy-MM-dd'),
      eventTime: null,
      daysOffset: null,
      isFuture: null,
      granularity: null,
      originalText: text,
      confidence: 0.1 // Low confidence - needs context
    };
  }
  
  const eventDateTime = DateTime.fromJSDate(eventDate);
  if (!eventDateTime.isValid) {
    return {
      mentionTime: base.toISO() || base.toFormat('yyyy-MM-dd'),
      eventTime: null,
      daysOffset: null,
      isFuture: null,
      granularity: null,
      originalText: text,
      confidence: 0.1
    };
  }
  
  const unitMap: Record<string, string> = {
    'day': 'days', 'days': 'days',
    'week': 'weeks', 'weeks': 'weeks',
    'month': 'months', 'months': 'months',
    'year': 'years', 'years': 'years'
  };
  
  let resolved: DateTime;
  if (direction === 'after') {
    resolved = eventDateTime.plus({ [unitMap[unit] || unit]: count });
  } else {
    resolved = eventDateTime.minus({ [unitMap[unit] || unit]: count });
  }
  
  const delta = resolved.diff(base, 'days').days;
  
  return {
    mentionTime: base.toISO() || base.toFormat('yyyy-MM-dd'),
    eventTime: resolved.toISODate() || null,
    daysOffset: Math.round(delta),
    isFuture: delta > 0,
    granularity: unit.includes('week') ? 'week' : unit.includes('month') ? 'month' : unit.includes('year') ? 'year' : 'day',
    originalText: text,
    confidence: 0.85
  };
}