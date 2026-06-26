/**
 * Lightweight local calendar fallback — no external dependency.
 * Provides season, approximate solar term, lunar info for solar term insight generation
 * when L1 CalendarSvc is unavailable.
 */

// ── 2026 二十四节气日期 (简化，仅2026年) ──
const TERMS_2026 = [
  { name: '小寒', date: '2026-01-05' }, { name: '大寒', date: '2026-01-20' },
  { name: '立春', date: '2026-02-04' }, { name: '雨水', date: '2026-02-19' },
  { name: '惊蛰', date: '2026-03-06' }, { name: '春分', date: '2026-03-21' },
  { name: '清明', date: '2026-04-05' }, { name: '谷雨', date: '2026-04-20' },
  { name: '立夏', date: '2026-05-05' }, { name: '小满', date: '2026-05-21' },
  { name: '芒种', date: '2026-06-05' }, { name: '夏至', date: '2026-06-21' },
  { name: '小暑', date: '2026-07-07' }, { name: '大暑', date: '2026-07-22' },
  { name: '立秋', date: '2026-08-07' }, { name: '处暑', date: '2026-08-23' },
  { name: '白露', date: '2026-09-07' }, { name: '秋分', date: '2026-09-23' },
  { name: '寒露', date: '2026-10-08' }, { name: '霜降', date: '2026-10-23' },
  { name: '立冬', date: '2026-11-07' }, { name: '小雪', date: '2026-11-22' },
  { name: '大雪', date: '2026-12-07' }, { name: '冬至', date: '2026-12-22' },
];

/** Get season from month — uses solar term boundaries, approximate */
function getSeason(dateStr) {
  const m = parseInt(dateStr.slice(5, 7));
  const d = parseInt(dateStr.slice(8, 10));
  // Approximate solar term boundaries
  if (m === 2 && d >= 4) return { name: '春', emoji: '🌸' };
  if (m === 3 || m === 4) return { name: '春', emoji: '🌸' };
  if (m === 5 && d < 5) return { name: '春', emoji: '🌸' };
  if (m === 5 && d >= 5) return { name: '夏', emoji: '☀️' };
  if (m === 6 || m === 7) return { name: '夏', emoji: '☀️' };
  if (m === 8 && d < 7) return { name: '夏', emoji: '☀️' };
  if (m === 8 && d >= 7) return { name: '秋', emoji: '🍂' };
  if (m === 9 || m === 10) return { name: '秋', emoji: '🍂' };
  if (m === 11 && d < 7) return { name: '秋', emoji: '🍂' };
  return { name: '冬', emoji: '❄️' };
}

/** Get season label for display */
function getSeasonLabel(dateStr) {
  const m = parseInt(dateStr.slice(5, 7));
  if (m >= 3 && m <= 5) return '春';
  if (m >= 6 && m <= 8) return '夏';
  if (m >= 9 && m <= 11) return '秋';
  return '冬';
}

/** Find current solar term (most recent before/on date) */
function getCurrentTerm(dateStr) {
  let current = TERMS_2026[0];
  for (const t of TERMS_2026) {
    if (t.date <= dateStr) current = t;
    else break;
  }
  // Calculate which day of the term
  const termDate = new Date(current.date + 'T00:00:00+08:00');
  const queryDate = new Date(dateStr + 'T00:00:00+08:00');
  const dayOffset = Math.floor((queryDate - termDate) / 86400000);
  const termDay = dayOffset + 1;

  return {
    name: current.name,
    day: termDay,
    pentad: Math.min(3, Math.floor(dayOffset / 5) + 1), // 1=初候 2=二候 3=三候
  };
}

/** Get next solar term */
function getNextTerm(dateStr) {
  for (const t of TERMS_2026) {
    if (t.date > dateStr) return t;
  }
  return TERMS_2026[0]; // wrap to next year
}

/** Weekday in Chinese */
function getWeekday(dateStr) {
  const d = new Date(dateStr + 'T00:00:00+08:00');
  return ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][d.getDay()];
}

/** Full local calendar data — matches CalendarSvc response shape */
export function getLocalCalendar(dateStr) {
  const today = dateStr || new Date().toISOString().slice(0, 10);
  const term = getCurrentTerm(today);
  const nextTerm = getNextTerm(today);
  const season = getSeason(today);
  const pentadSuffix = ['初候', '二候', '三候'][term.pentad - 1];

  return {
    _fallback: true,
    lunar: null, // no lunar without lunisolar, but not needed for Aha
    solar_term: {
      name: term.name,
      day: term.day,
      next: nextTerm.name,
    },
    season_phenology: {
      pentad: `${term.name}${pentadSuffix}`,
    },
    season,
    weekday: getWeekday(today),
    date_display: `${today.slice(0,4)}年${parseInt(today.slice(5,7))}月${parseInt(today.slice(8,10))}日 ${getWeekday(today)}`,
  };
}

export { getSeason, getSeasonLabel, getCurrentTerm, getNextTerm };
