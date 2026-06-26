/**
 * Temporal Routing Module
 * Detects temporal intent and extracts date ranges from natural language
 */

/**
 * Temporal expression patterns
 */
const TEMPORAL_PATTERNS = {
  // Relative time expressions
  relative: [
    { pattern: /today/i, offset: { days: 0 } },
    { pattern: /yesterday/i, offset: { days: -1 } },
    { pattern: /tomorrow/i, offset: { days: 1 } },
    { pattern: /last\s*week/i, offset: { weeks: -1 } },
    { pattern: /this\s*week/i, offset: { weeks: 0 } },
    { pattern: /next\s*week/i, offset: { weeks: 1 } },
    { pattern: /last\s*month/i, offset: { months: -1 } },
    { pattern: /this\s*month/i, offset: { months: 0 } },
    { pattern: /next\s*month/i, offset: { months: 1 } },
    { pattern: /last\s*year/i, offset: { years: -1 } },
    { pattern: /this\s*year/i, offset: { years: 0 } },
    { pattern: /next\s*year/i, offset: { years: 1 } },
    { pattern: /past\s*(\d+)\s*(day|days)/i, offset: (match) => ({ days: -parseInt(match[1]) }) },
    { pattern: /last\s*(\d+)\s*(day|days)/i, offset: (match) => ({ days: -parseInt(match[1]) }) },
    { pattern: /past\s*(\d+)\s*(week|weeks)/i, offset: (match) => ({ weeks: -parseInt(match[1]) }) },
    { pattern: /last\s*(\d+)\s*(week|weeks)/i, offset: (match) => ({ weeks: -parseInt(match[1]) }) },
    { pattern: /past\s*(\d+)\s*(month|months)/i, offset: (match) => ({ months: -parseInt(match[1]) }) },
    { pattern: /last\s*(\d+)\s*(month|months)/i, offset: (match) => ({ months: -parseInt(match[1]) }) },
    { pattern: /past\s*(\d+)\s*(year|years)/i, offset: (match) => ({ years: -parseInt(match[1]) }) },
    { pattern: /last\s*(\d+)\s*(year|years)/i, offset: (match) => ({ years: -parseInt(match[1]) }) },
    { pattern: /recent/i, offset: { days: -7 } },
    { pattern: /recently/i, offset: { days: -7 } }
  ],
  
  // Absolute date patterns
  absolute: [
    { pattern: /(\d{4})-(\d{1,2})-(\d{1,2})/, type: 'ISO' },
    { pattern: /(\d{1,2})\/(\d{1,2})\/(\d{4})/, type: 'US' },
    { pattern: /(\d{1,2})\.(\d{1,2})\.(\d{4})/, type: 'EU' }
  ],
  
  // Temporal intent keywords
  intent: [
    /when/i,
    /date/i,
    /time/i,
    /period/i,
    /during/i,
    /from.*to/i,
    /between.*and/i,
    /since/i,
    /until/i,
    /before/i,
    /after/i
  ]
};

/**
 * Detect temporal intent in a query
 * @param {string} query - Input query
 * @returns {object} Detection result
 */
function detect_temporal(query) {
  if (!query || typeof query !== 'string') {
    return {
      hasTemporal: false,
      intent: null,
      expressions: []
    };
  }
  
  const expressions = [];
  let hasTemporal = false;
  let intent = null;
  
  // Check for temporal intent keywords
  for (const pattern of TEMPORAL_PATTERNS.intent) {
    if (pattern.test(query)) {
      hasTemporal = true;
      intent = 'explicit';
      break;
    }
  }
  
  // Check for relative time expressions
  for (const { pattern, offset } of TEMPORAL_PATTERNS.relative) {
    const match = query.match(pattern);
    if (match) {
      hasTemporal = true;
      if (!intent) intent = 'relative';
      expressions.push({
        type: 'relative',
        text: match[0],
        offset: typeof offset === 'function' ? offset(match) : offset
      });
    }
  }
  
  // Check for absolute dates
  for (const { pattern, type } of TEMPORAL_PATTERNS.absolute) {
    const match = query.match(pattern);
    if (match) {
      hasTemporal = true;
      if (!intent) intent = 'absolute';
      expressions.push({
        type: 'absolute',
        dateType: type,
        text: match[0],
        raw: match.slice(1)
      });
    }
  }
  
  return {
    hasTemporal,
    intent,
    expressions
  };
}

/**
 * Parse a date range from natural language
 * @param {string} expression - Natural language date expression
 * @param {Date} referenceDate - Reference date (default: now)
 * @returns {object} Date range {start, end}
 */
function get_date_range(expression, referenceDate = new Date()) {
  if (!expression || typeof expression !== 'string') {
    return null;
  }
  
  const now = referenceDate;
  const start = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const end = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  
  // Normalize expression
  const expr = expression.toLowerCase().trim();
  
  // Handle "today"
  if (expr === 'today') {
    start.setHours(0, 0, 0, 0);
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle "yesterday"
  if (expr === 'yesterday') {
    start.setDate(start.getDate() - 1);
    start.setHours(0, 0, 0, 0);
    end.setDate(end.getDate() - 1);
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle "tomorrow"
  if (expr === 'tomorrow') {
    start.setDate(start.getDate() + 1);
    start.setHours(0, 0, 0, 0);
    end.setDate(end.getDate() + 1);
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle "last week"
  if (expr === 'last week') {
    const dayOfWeek = start.getDay();
    start.setDate(start.getDate() - dayOfWeek - 7);
    start.setHours(0, 0, 0, 0);
    end.setDate(start.getDate() + 6);
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle "this week"
  if (expr === 'this week') {
    const dayOfWeek = start.getDay();
    start.setDate(start.getDate() - dayOfWeek);
    start.setHours(0, 0, 0, 0);
    end.setDate(start.getDate() + 6);
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle "next week"
  if (expr === 'next week') {
    const dayOfWeek = start.getDay();
    start.setDate(start.getDate() - dayOfWeek + 7);
    start.setHours(0, 0, 0, 0);
    end.setDate(start.getDate() + 6);
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle "last month"
  if (expr === 'last month') {
    start.setMonth(start.getMonth() - 1);
    start.setDate(1);
    start.setHours(0, 0, 0, 0);
    end.setDate(0); // Last day of previous month
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle "this month"
  if (expr === 'this month') {
    start.setDate(1);
    start.setHours(0, 0, 0, 0);
    end.setMonth(end.getMonth() + 1);
    end.setDate(0);
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle "next month"
  if (expr === 'next month') {
    start.setMonth(start.getMonth() + 1);
    start.setDate(1);
    start.setHours(0, 0, 0, 0);
    end.setMonth(end.getMonth() + 1);
    end.setDate(0);
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle "recent" or "recently"
  if (expr === 'recent' || expr === 'recently') {
    start.setDate(start.getDate() - 7);
    start.setHours(0, 0, 0, 0);
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle "past N days/weeks/months/years"
  const pastMatch = expr.match(/past\s+(\d+)\s*(day|days|week|weeks|month|months|year|years)/);
  if (pastMatch) {
    const amount = parseInt(pastMatch[1]);
    const unit = pastMatch[2];
    
    if (unit.startsWith('day')) {
      start.setDate(start.getDate() - amount);
    } else if (unit.startsWith('week')) {
      start.setDate(start.getDate() - (amount * 7));
    } else if (unit.startsWith('month')) {
      start.setMonth(start.getMonth() - amount);
    } else if (unit.startsWith('year')) {
      start.setFullYear(start.getFullYear() - amount);
    }
    
    start.setHours(0, 0, 0, 0);
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle "last N days/weeks/months/years"
  const lastMatch = expr.match(/last\s+(\d+)\s*(day|days|week|weeks|month|months|year|years)/);
  if (lastMatch) {
    const amount = parseInt(lastMatch[1]);
    const unit = lastMatch[2];
    
    if (unit.startsWith('day')) {
      start.setDate(start.getDate() - amount);
    } else if (unit.startsWith('week')) {
      start.setDate(start.getDate() - (amount * 7));
    } else if (unit.startsWith('month')) {
      start.setMonth(start.getMonth() - amount);
    } else if (unit.startsWith('year')) {
      start.setFullYear(start.getFullYear() - amount);
    }
    
    start.setHours(0, 0, 0, 0);
    end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  
  // Handle ISO date (YYYY-MM-DD)
  const isoMatch = expression.match(/(\d{4})-(\d{1,2})-(\d{1,2})/);
  if (isoMatch) {
    const year = parseInt(isoMatch[1]);
    const month = parseInt(isoMatch[2]) - 1;
    const day = parseInt(isoMatch[3]);
    
    // Use local date construction to avoid timezone issues
    const startDate = new Date(year, month, day);
    const endDate = new Date(year, month, day);
    startDate.setHours(0, 0, 0, 0);
    endDate.setHours(23, 59, 59, 999);
    return { start: startDate, end: endDate };
  }
  
  return null;
}

/**
 * Get relative time description
 * @param {Date} date - Date to describe
 * @param {Date} referenceDate - Reference date
 * @returns {string} Human-readable description
 */
function getRelativeTime(date, referenceDate = new Date()) {
  const diffMs = referenceDate - date;
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) return 'today';
  if (diffDays === 1) return 'yesterday';
  if (diffDays === -1) return 'tomorrow';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
  return `${Math.floor(diffDays / 365)} years ago`;
}

module.exports = {
  detect_temporal,
  get_date_range,
  getRelativeTime,
  TEMPORAL_PATTERNS
};
