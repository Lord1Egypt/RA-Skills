'use strict';

// meeting-parser.js - Pure JS meeting notes parser
// Extracts action items from text using regex/keyword pattern matching.
// No dependencies on apple-bridge, EventKit, or external libraries.

// ─── Pattern Tables ───────────────────────────────────────────────

const PATTERNS = {
  en: {
    actions: [
      { re: /^TODO:\s*(.+)/i, confidence: 'high' },
      { re: /^action\s*item:\s*(.+)/i, confidence: 'high' },
      { re: /^[-*•]\s+(.+?)\s+by\b/i, confidence: 'high' },
      { re: /deadline:\s*(.+)/i, confidence: 'high' },
      { re: /assigned\s+to\s+\S+[,:]\s*(.+)/i, confidence: 'medium' },
      { re: /(.+?)\s+(?:needs?\s+to|should|must)\s+(.+)/i, confidence: 'medium', groupIdx: 2 },
      { re: /^[-*•]\s+(.+)/i, confidence: 'low' },
    ],
    dates: [
      { re: /by\s+(tomorrow)/i, resolve: 'tomorrow' },
      { re: /by\s+(?:next\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)/i, resolve: 'weekday' },
      { re: /by\s+(?:end\s+of\s+(?:the\s+)?week)/i, resolve: 'endOfWeek' },
      { re: /by\s+(?:end\s+of\s+(?:the\s+)?month)/i, resolve: 'endOfMonth' },
      { re: /by\s+(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+(\d{1,2})/i, resolve: 'monthDay' },
      { re: /(\d{1,2})\/(\d{1,2})(?:\/(\d{2,4}))?/, resolve: 'slashDate' },
      { re: /(tomorrow)/i, resolve: 'tomorrow' },
      { re: /(?:next\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)/i, resolve: 'weekday' },
      { re: /(?:end\s+of\s+(?:the\s+)?week)/i, resolve: 'endOfWeek' },
      { re: /(?:end\s+of\s+(?:the\s+)?month)/i, resolve: 'endOfMonth' },
    ],
    priority: {
      high: /\b(?:urgent|asap|critical|immediate(?:ly)?|must|required|blocking)\b/i,
      medium: /\b(?:important|priority)\b/i,
      low: /\b(?:nice\s+to\s+have|when\s+possible|optional|eventually)\b/i,
    },
  },
  ko: {
    actions: [
      { re: /기한:\s*(.+)/, confidence: 'high' },
      { re: /담당:\s*\S+\s*[-,]\s*(.+)/, confidence: 'high' },
      { re: /^[-*•]\s*(.+?)\s*까지/, confidence: 'high' },
      { re: /(.+?)\s*(?:해야\s*(?:합니다|함|해요|됩니다|된다|할\s*것))/, confidence: 'high' },
      { re: /(.+?)\s*까지\s*(.+)/, confidence: 'high', groupIdx: 2 },
      { re: /(.+?)\s*(?:완료|처리|제출|보고|준비)해야/, confidence: 'medium' },
      { re: /(.+?)\s*(?:할\s*것|하기)/, confidence: 'medium' },
      { re: /^[-*•]\s*(.+)/, confidence: 'low' },
    ],
    dates: [
      { re: /(\d{1,2})월\s*(\d{1,2})일/, resolve: 'monthDayNum' },
      { re: /내일/, resolve: 'tomorrow' },
      { re: /다음\s*주\s*(월|화|수|목|금|토|일)?요?일?/, resolve: 'nextWeekDay_ko' },
      { re: /이번\s*주\s*(월|화|수|목|금|토|일)요?일?/, resolve: 'thisWeekDay_ko' },
      { re: /(\d+)\s*일\s*(?:후|뒤)/, resolve: 'daysLater' },
      { re: /다음\s*주/, resolve: 'nextWeek' },
      { re: /이번\s*주/, resolve: 'endOfWeek' },
    ],
    priority: {
      high: /(?:긴급|즉시|반드시|필수|시급)/,
      medium: /(?:중요|우선)/,
      low: /(?:여유|나중에|가능시|가능하면)/,
    },
  },
  ja: {
    actions: [
      { re: /期限:\s*(.+)/, confidence: 'high' },
      { re: /担当:\s*\S+\s*[-,]\s*(.+)/, confidence: 'high' },
      { re: /(.+?)\s*まで(?:に)?\s*(.+)/, confidence: 'high', groupIdx: 2 },
      { re: /(.+?)\s*(?:する必要がある|しなければ|すべき)/, confidence: 'high' },
      { re: /(.+?)\s*(?:を完了|を提出|を準備|を報告)/, confidence: 'medium' },
      { re: /^[-*•]\s*(.+)/, confidence: 'low' },
    ],
    dates: [
      { re: /(\d{1,2})月\s*(\d{1,2})日/, resolve: 'monthDayNum' },
      { re: /(?:明日|あした)/, resolve: 'tomorrow' },
      { re: /来週\s*(月|火|水|木|金|土|日)?曜?日?/, resolve: 'nextWeekDay_ja' },
      { re: /今週\s*(月|火|水|木|金|土|日)曜?日?/, resolve: 'thisWeekDay_ja' },
      { re: /来週/, resolve: 'nextWeek' },
    ],
    priority: {
      high: /(?:緊急|至急|必須|すぐに|即座)/,
      medium: /(?:重要|優先)/,
      low: /(?:できれば|後で|可能なら)/,
    },
  },
  zh: {
    actions: [
      { re: /截止:\s*(.+)/, confidence: 'high' },
      { re: /负责:\s*\S+\s*[-,]\s*(.+)/, confidence: 'high' },
      { re: /(.+?)\s*之前/, confidence: 'high' },
      { re: /(.+?)\s*(?:需要|必须|应该)/, confidence: 'medium' },
      { re: /^[-*•]\s*(.+)/, confidence: 'low' },
    ],
    dates: [
      { re: /(\d{1,2})月\s*(\d{1,2})[日号]/, resolve: 'monthDayNum' },
      { re: /明天/, resolve: 'tomorrow' },
      { re: /下周\s*([一二三四五六日天])?/, resolve: 'nextWeekDay_zh' },
      { re: /本周\s*([一二三四五六日天])/, resolve: 'thisWeekDay_zh' },
      { re: /下周/, resolve: 'nextWeek' },
    ],
    priority: {
      high: /(?:紧急|立即|必须|马上)/,
      medium: /(?:重要|优先)/,
      low: /(?:如果可以|以后|可选)/,
    },
  },
};

// ─── Weekday Maps ─────────────────────────────────────────────────

const EN_DAYS = { sunday: 0, monday: 1, tuesday: 2, wednesday: 3, thursday: 4, friday: 5, saturday: 6 };
const KO_DAYS = { '일': 0, '월': 1, '화': 2, '수': 3, '목': 4, '금': 5, '토': 6 };
const JA_DAYS = { '日': 0, '月': 1, '火': 2, '水': 3, '木': 4, '金': 5, '土': 6 };
const ZH_DAYS = { '日': 0, '天': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6 };

const EN_MONTHS = {
  jan: 0, january: 0, feb: 1, february: 1, mar: 2, march: 2,
  apr: 3, april: 3, may: 4, jun: 5, june: 5, jul: 6, july: 6,
  aug: 7, august: 7, sep: 8, september: 8, oct: 9, october: 9,
  nov: 10, november: 10, dec: 11, december: 11,
};

// ─── Date Resolver ────────────────────────────────────────────────

function nextWeekdayFrom(ref, targetDay) {
  const diff = (targetDay - ref.getDay() + 7) % 7 || 7;
  const d = new Date(ref);
  d.setDate(d.getDate() + diff);
  d.setHours(17, 0, 0, 0);
  return d;
}

function thisWeekdayFrom(ref, targetDay) {
  const current = ref.getDay();
  const diff = targetDay - current;
  const d = new Date(ref);
  d.setDate(d.getDate() + diff);
  d.setHours(17, 0, 0, 0);
  return d;
}

function resolveDate(line, patterns, ref) {
  for (const pat of patterns) {
    const m = line.match(pat.re);
    if (!m) continue;

    switch (pat.resolve) {
      case 'tomorrow': {
        const d = new Date(ref);
        d.setDate(d.getDate() + 1);
        d.setHours(9, 0, 0, 0);
        return d;
      }
      case 'weekday': {
        const dayName = m[1].toLowerCase();
        const target = EN_DAYS[dayName];
        if (target === undefined) continue;
        return nextWeekdayFrom(ref, target);
      }
      case 'endOfWeek': {
        return thisWeekdayFrom(ref, 5); // Friday
      }
      case 'endOfMonth': {
        const d = new Date(ref.getFullYear(), ref.getMonth() + 1, 0);
        d.setHours(17, 0, 0, 0);
        return d;
      }
      case 'monthDay': {
        const monthStr = m[1].toLowerCase();
        const month = EN_MONTHS[monthStr];
        if (month === undefined) continue;
        const day = parseInt(m[2], 10);
        let year = ref.getFullYear();
        const candidate = new Date(year, month, day, 17, 0, 0, 0);
        if (candidate < ref) candidate.setFullYear(year + 1);
        return candidate;
      }
      case 'monthDayNum': {
        const month = parseInt(m[1], 10) - 1;
        const day = parseInt(m[2], 10);
        let year = ref.getFullYear();
        const candidate = new Date(year, month, day, 17, 0, 0, 0);
        if (candidate < ref) candidate.setFullYear(year + 1);
        return candidate;
      }
      case 'slashDate': {
        const mo = parseInt(m[1], 10) - 1;
        const da = parseInt(m[2], 10);
        let yr = m[3] ? parseInt(m[3], 10) : ref.getFullYear();
        if (yr < 100) yr += 2000;
        return new Date(yr, mo, da, 17, 0, 0, 0);
      }
      case 'daysLater': {
        const n = parseInt(m[1], 10);
        const d = new Date(ref);
        d.setDate(d.getDate() + n);
        d.setHours(17, 0, 0, 0);
        return d;
      }
      case 'nextWeek': {
        const d = new Date(ref);
        const daysUntilMon = (1 - d.getDay() + 7) % 7 || 7;
        d.setDate(d.getDate() + daysUntilMon);
        d.setHours(9, 0, 0, 0);
        return d;
      }
      case 'nextWeekDay_ko': {
        const dayChar = m[1];
        if (!dayChar) {
          const d = new Date(ref);
          const daysUntilMon = (1 - d.getDay() + 7) % 7 || 7;
          d.setDate(d.getDate() + daysUntilMon);
          d.setHours(9, 0, 0, 0);
          return d;
        }
        const target = KO_DAYS[dayChar];
        if (target === undefined) continue;
        const d = new Date(ref);
        const daysUntilMon = (1 - d.getDay() + 7) % 7 || 7;
        d.setDate(d.getDate() + daysUntilMon);
        return thisWeekdayFrom(d, target);
      }
      case 'thisWeekDay_ko': {
        const dayChar = m[1];
        const target = KO_DAYS[dayChar];
        if (target === undefined) continue;
        return thisWeekdayFrom(ref, target);
      }
      case 'nextWeekDay_ja': {
        const dayChar = m[1];
        if (!dayChar) {
          const d = new Date(ref);
          const daysUntilMon = (1 - d.getDay() + 7) % 7 || 7;
          d.setDate(d.getDate() + daysUntilMon);
          d.setHours(9, 0, 0, 0);
          return d;
        }
        const target = JA_DAYS[dayChar];
        if (target === undefined) continue;
        const d = new Date(ref);
        const daysUntilMon = (1 - d.getDay() + 7) % 7 || 7;
        d.setDate(d.getDate() + daysUntilMon);
        return thisWeekdayFrom(d, target);
      }
      case 'thisWeekDay_ja': {
        const dayChar = m[1];
        const target = JA_DAYS[dayChar];
        if (target === undefined) continue;
        return thisWeekdayFrom(ref, target);
      }
      case 'nextWeekDay_zh': {
        const dayChar = m[1];
        if (!dayChar) {
          const d = new Date(ref);
          const daysUntilMon = (1 - d.getDay() + 7) % 7 || 7;
          d.setDate(d.getDate() + daysUntilMon);
          d.setHours(9, 0, 0, 0);
          return d;
        }
        const target = ZH_DAYS[dayChar];
        if (target === undefined) continue;
        const d = new Date(ref);
        const daysUntilMon = (1 - d.getDay() + 7) % 7 || 7;
        d.setDate(d.getDate() + daysUntilMon);
        return thisWeekdayFrom(d, target);
      }
      case 'thisWeekDay_zh': {
        const dayChar = m[1];
        const target = ZH_DAYS[dayChar];
        if (target === undefined) continue;
        return thisWeekdayFrom(ref, target);
      }
    }
  }
  return null;
}

// ─── Language Auto-Detection ──────────────────────────────────────

function detectLocale(text) {
  if (/[\uAC00-\uD7A3]/.test(text)) return 'ko';
  const hasCJK = /[\u4E00-\u9FFF]/.test(text);
  const hasKana = /[\u3040-\u30FF]/.test(text);
  if (hasCJK && hasKana) return 'ja';
  if (hasCJK) return 'zh';
  return 'en';
}

// ─── Title Cleaning ───────────────────────────────────────────────

function cleanTitle(raw) {
  let t = raw.trim();
  t = t.replace(/^[-*•]\s*/, '');
  t = t.replace(/[.,、。;；]+$/, '');
  t = t.replace(/^\s+/, '');
  if (t.length > 120) t = t.substring(0, 120);
  return t;
}

// ─── Priority Detection ──────────────────────────────────────────

function detectPriority(line, priorityPatterns) {
  if (priorityPatterns.high && priorityPatterns.high.test(line)) return 'high';
  if (priorityPatterns.medium && priorityPatterns.medium.test(line)) return 'medium';
  if (priorityPatterns.low && priorityPatterns.low.test(line)) return 'low';
  return 'none';
}

// ─── Per-Line Matcher ─────────────────────────────────────────────

function matchLine(line, langPatterns, ref) {
  let title = null;
  let baseConfidence = null;

  for (const pat of langPatterns.actions) {
    const m = line.match(pat.re);
    if (m) {
      const idx = pat.groupIdx || 1;
      title = cleanTitle(m[idx] || m[1]);
      baseConfidence = pat.confidence;
      break;
    }
  }

  if (!title || baseConfidence === 'low') return null;

  const due = resolveDate(line, langPatterns.dates, ref);
  const priority = detectPriority(line, langPatterns.priority);

  let confidence = baseConfidence;
  if (baseConfidence === 'medium' && due) confidence = 'high';

  return {
    title,
    due: due ? formatISO(due) : null,
    priority,
    confidence,
    source_line: line,
  };
}

// ─── ISO Date Formatter ──────────────────────────────────────────

function formatISO(d) {
  const off = -d.getTimezoneOffset();
  const sign = off >= 0 ? '+' : '-';
  const hh = String(Math.floor(Math.abs(off) / 60)).padStart(2, '0');
  const mm = String(Math.abs(off) % 60).padStart(2, '0');
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}${sign}${hh}:${mm}`;
}

// ─── Main Export ─────────────────────────────────────────────────

function parseMeetingText(text, locale, referenceDate) {
  const ref = referenceDate || new Date();
  const lang = locale || detectLocale(text);
  const langPatterns = PATTERNS[lang] || PATTERNS.en;

  // Split on newlines and sentence-ending punctuation
  const rawLines = text.split(/\n/);
  const lines = [];
  for (const raw of rawLines) {
    const trimmed = raw.trim();
    if (!trimmed) continue;
    // Also split on ". " and "。" for multi-sentence lines
    const parts = trimmed.split(/(?<=\.)\s+|(?<=。)\s*/);
    for (const p of parts) {
      const pt = p.trim();
      if (pt) lines.push(pt);
    }
  }

  const items = [];
  for (const line of lines) {
    const item = matchLine(line, langPatterns, ref);
    if (item) items.push(item);
  }

  return { ok: true, items };
}

module.exports = { parseMeetingText, detectLocale };
