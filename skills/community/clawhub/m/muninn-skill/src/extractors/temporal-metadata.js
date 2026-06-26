"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.getReferenceClock = getReferenceClock;
exports.extractTemporalMetadata = extractTemporalMetadata;
exports.extractTemporalMetadataBatch = extractTemporalMetadataBatch;
exports.resolveRelativeWithContext = resolveRelativeWithContext;
var luxon_1 = require("luxon");
/**
 * Safe DateTime wrapper that never throws
 * Returns null for invalid inputs instead of crashing
 */
function safeDateTimeFromObject(opts, fallback) {
    // Validate all values are valid numbers
    for (var _i = 0, _a = Object.entries(opts); _i < _a.length; _i++) {
        var _b = _a[_i], key = _b[0], val = _b[1];
        if (val === undefined || val === null || Number.isNaN(val)) {
            // Invalid value - use fallback or return null
            return fallback || null;
        }
    }
    try {
        var dt = luxon_1.DateTime.fromObject(opts);
        return dt.isValid ? dt : (fallback || null);
    }
    catch (_c) {
        return fallback || null;
    }
}
/**
 * Safe DateTime from ISO string
 */
function safeDateTimeFromISO(iso, fallback) {
    if (!iso || typeof iso !== 'string')
        return fallback || null;
    try {
        var dt = luxon_1.DateTime.fromISO(iso);
        return dt.isValid ? dt : (fallback || null);
    }
    catch (_a) {
        return fallback || null;
    }
}
/**
 * Reference clock - injected into all temporal operations
 * Defaults to now, but can be overridden for testing or context-aware extraction
 */
function getReferenceClock() {
    return luxon_1.DateTime.now();
}
// Relative time patterns
var RELATIVE_PATTERNS = [
    // "in a fortnight", "in two weeks", "in 3 days"
    {
        pattern: /in\s+(?:a\s+)?(\d+)?\s*(fortnight|week|weeks|day|days|month|months|year|years|hour|hours|minute|minutes)/i,
        resolver: function (match, base) {
            var _a;
            var count = match[1] ? parseInt(match[1]) : 1;
            var unit = match[2].toLowerCase();
            if (unit === 'fortnight') {
                return base.plus({ days: 14 * count });
            }
            var unitMap = {
                'week': 'weeks', 'weeks': 'weeks',
                'day': 'days', 'days': 'days',
                'month': 'months', 'months': 'months',
                'year': 'years', 'years': 'years',
                'hour': 'hours', 'hours': 'hours',
                'minute': 'minutes', 'minutes': 'minutes'
            };
            return base.plus((_a = {}, _a[unitMap[unit] || unit] = count, _a));
        }
    },
    // "next Tuesday", "next week", "next month"
    {
        pattern: /next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|week|month|year)/i,
        resolver: function (match, base) {
            var target = match[1].toLowerCase();
            if (target === 'week')
                return base.plus({ weeks: 1 });
            if (target === 'month')
                return base.plus({ months: 1 });
            if (target === 'year')
                return base.plus({ years: 1 });
            // Day of week
            var days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
            var targetDay = days.indexOf(target);
            var currentDay = base.weekday - 1; // Luxon uses 1-7, we need 0-6
            var diff = targetDay - currentDay;
            if (diff <= 0)
                diff += 7; // Next occurrence
            return base.plus({ days: diff });
        }
    },
    // "last Monday", "last week", etc.
    {
        pattern: /last\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|week|month|year)/i,
        resolver: function (match, base) {
            var target = match[1].toLowerCase();
            if (target === 'week')
                return base.minus({ weeks: 1 });
            if (target === 'month')
                return base.minus({ months: 1 });
            if (target === 'year')
                return base.minus({ years: 1 });
            var days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
            var targetDay = days.indexOf(target);
            var currentDay = base.weekday - 1;
            var diff = currentDay - targetDay;
            if (diff <= 0)
                diff += 7;
            return base.minus({ days: diff });
        }
    },
    // "tomorrow"
    {
        pattern: /\btomorrow\b/i,
        resolver: function (_, base) { return base.plus({ days: 1 }); }
    },
    // "yesterday"
    {
        pattern: /\byesterday\b/i,
        resolver: function (_, base) { return base.minus({ days: 1 }); }
    },
    // "today"
    {
        pattern: /\btoday\b/i,
        resolver: function (_, base) { return base; }
    },
    // "in 2 weeks time", "3 days time"
    {
        pattern: /(\d+)\s+(week|weeks|day|days|month|months|year|years)\s+time/i,
        resolver: function (match, base) {
            var _a;
            var count = parseInt(match[1]);
            var unit = match[2].toLowerCase();
            var unitMap = {
                'week': 'weeks', 'weeks': 'weeks',
                'day': 'days', 'days': 'days',
                'month': 'months', 'months': 'months',
                'year': 'years', 'years': 'years'
            };
            return base.plus((_a = {}, _a[unitMap[unit] || unit] = count, _a));
        }
    },
    // "a week from now", "2 days from now"
    {
        pattern: /(?:a|(\d+))\s+(week|weeks|day|days|month|months|year|years)\s+from\s+now/i,
        resolver: function (match, base) {
            var _a;
            var count = match[1] ? parseInt(match[1]) : 1;
            var unit = match[2].toLowerCase();
            var unitMap = {
                'week': 'weeks', 'weeks': 'weeks',
                'day': 'days', 'days': 'days',
                'month': 'months', 'months': 'months',
                'year': 'years', 'years': 'years'
            };
            return base.plus((_a = {}, _a[unitMap[unit] || unit] = count, _a));
        }
    },
    // "2 weeks after X", "3 days before X" - returns pattern match only, needs context
    {
        pattern: /(\d+)\s+(week|weeks|day|days|month|months|year|years)\s+(after|before)\s+(.+)/i,
        resolver: function (match, base) {
            // This requires context resolution - mark as needing further processing
            return null; // Will be handled by context-aware processor
        }
    }
];
// Absolute date patterns
var ABSOLUTE_PATTERNS = [
    // "March 15", "March 15th", "15th March"
    {
        pattern: /(?:on\s+)?(?:(\d{1,2})(?:st|nd|rd|th)?\s+)?(january|february|march|april|may|june|july|august|september|october|november|december)(?:\s+(\d{1,2})(?:st|nd|rd|th)?)?(?:\s+(\d{4}))?/i,
        parser: function (match, base) {
            var monthName = match[2].toLowerCase();
            var months = ['january', 'february', 'march', 'april', 'may', 'june',
                'july', 'august', 'september', 'october', 'november', 'december'];
            var month = months.indexOf(monthName) + 1;
            var dayRaw = match[1] || match[3];
            var yearRaw = match[4];
            var day = dayRaw ? parseInt(dayRaw) : 1;
            var year = yearRaw ? parseInt(yearRaw) : base.year;
            // Use safe wrapper
            return safeDateTimeFromObject({ year: year, month: month, day: day }, base);
        }
    },
    // "2026-03-15", "2026/03/15"
    {
        pattern: /(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})/,
        parser: function (match, _) {
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
        parser: function (match, _) {
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
function extractTemporalMetadata(text, referenceDate) {
    // Use reference clock with fallback
    var base;
    if (referenceDate instanceof Date) {
        var dt = luxon_1.DateTime.fromJSDate(referenceDate);
        base = dt.isValid ? dt : getReferenceClock();
    }
    else if (typeof referenceDate === 'string') {
        var dt = safeDateTimeFromISO(referenceDate);
        base = dt || getReferenceClock();
    }
    else {
        base = getReferenceClock();
    }
    var result = {
        mentionTime: base.toISO() || base.toFormat('yyyy-MM-dd'),
        eventTime: null,
        daysOffset: null,
        isFuture: null,
        granularity: null,
        originalText: text,
        confidence: 0
    };
    // Try relative patterns first
    for (var _i = 0, RELATIVE_PATTERNS_1 = RELATIVE_PATTERNS; _i < RELATIVE_PATTERNS_1.length; _i++) {
        var _a = RELATIVE_PATTERNS_1[_i], pattern = _a.pattern, resolver = _a.resolver;
        var match = text.match(pattern);
        if (match) {
            var resolved = resolver(match, base);
            if (resolved) {
                var delta = resolved.diff(base, 'days').days;
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
    for (var _b = 0, ABSOLUTE_PATTERNS_1 = ABSOLUTE_PATTERNS; _b < ABSOLUTE_PATTERNS_1.length; _b++) {
        var _c = ABSOLUTE_PATTERNS_1[_b], pattern = _c.pattern, parser = _c.parser;
        var match = text.match(pattern);
        if (match) {
            var parsed = parser(match, base);
            if (parsed && parsed.isValid) {
                var delta = parsed.diff(base, 'days').days;
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
    var timePhrase = text.match(/(?:in|after|before|next|last)\s+\d+\s+(?:day|week|month|year|hour|minute)s?/i);
    if (timePhrase) {
        result.confidence = 0.3;
        result.granularity = null;
    }
    return result;
}
/**
 * Determine the granularity of a time expression
 */
function determineGranularity(text) {
    var lower = text.toLowerCase();
    if (lower.includes('hour') || lower.includes('minute'))
        return 'hour';
    if (lower.includes('week') || lower.includes('fortnight'))
        return 'week';
    if (lower.includes('month'))
        return 'month';
    if (lower.includes('year'))
        return 'year';
    return 'day';
}
/**
 * Batch extract temporal metadata from multiple texts
 */
function extractTemporalMetadataBatch(texts, referenceDate) {
    if (referenceDate === void 0) { referenceDate = new Date(); }
    return texts.map(function (text) { return ({
        text: text,
        metadata: extractTemporalMetadata(text, referenceDate)
    }); });
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
function resolveRelativeWithContext(text, contextEvents, referenceDate) {
    var _a, _b;
    // Safe reference clock handling
    var base;
    if (referenceDate instanceof Date) {
        var dt = luxon_1.DateTime.fromJSDate(referenceDate);
        base = dt.isValid ? dt : getReferenceClock();
    }
    else if (typeof referenceDate === 'string') {
        var dt = safeDateTimeFromISO(referenceDate);
        base = dt || getReferenceClock();
    }
    else {
        base = getReferenceClock();
    }
    // Pattern: "X days/weeks/months after/before [event]"
    var match = text.match(/(\d+)\s+(day|days|week|weeks|month|months|year|years)\s+(after|before)\s+(.+)/i);
    if (!match) {
        return extractTemporalMetadata(text, referenceDate);
    }
    var countRaw = parseInt(match[1]);
    var count = Number.isNaN(countRaw) ? 1 : countRaw;
    var unit = match[2].toLowerCase();
    var direction = match[3].toLowerCase();
    var eventRef = match[4].trim().toLowerCase();
    // Look up the referenced event
    var eventDate = contextEvents.get(eventRef);
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
    var eventDateTime = luxon_1.DateTime.fromJSDate(eventDate);
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
    var unitMap = {
        'day': 'days', 'days': 'days',
        'week': 'weeks', 'weeks': 'weeks',
        'month': 'months', 'months': 'months',
        'year': 'years', 'years': 'years'
    };
    var resolved;
    if (direction === 'after') {
        resolved = eventDateTime.plus((_a = {}, _a[unitMap[unit] || unit] = count, _a));
    }
    else {
        resolved = eventDateTime.minus((_b = {}, _b[unitMap[unit] || unit] = count, _b));
    }
    var delta = resolved.diff(base, 'days').days;
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
