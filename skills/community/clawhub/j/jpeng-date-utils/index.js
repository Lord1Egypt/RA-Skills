/**
 * Date Utils
 * Provides date and time manipulation operations
 */

/**
 * Format date with pattern
 * Patterns: YYYY (year), MM (month), DD (day), HH (hours), mm (minutes), ss (seconds)
 */
function formatDate(date, pattern = 'YYYY-MM-DD HH:mm:ss') {
  if (!(date instanceof Date) || isNaN(date)) {
    return 'Invalid Date';
  }
  
  const pad = (n) => String(n).padStart(2, '0');
  
  const replacements = {
    'YYYY': date.getFullYear(),
    'YY': String(date.getFullYear()).slice(-2),
    'MM': pad(date.getMonth() + 1),
    'M': date.getMonth() + 1,
    'DD': pad(date.getDate()),
    'D': date.getDate(),
    'HH': pad(date.getHours()),
    'H': date.getHours(),
    'hh': pad(date.getHours() % 12 || 12),
    'h': date.getHours() % 12 || 12,
    'mm': pad(date.getMinutes()),
    'm': date.getMinutes(),
    'ss': pad(date.getSeconds()),
    's': date.getSeconds(),
    'SSS': String(date.getMilliseconds()).padStart(3, '0'),
    'A': date.getHours() >= 12 ? 'PM' : 'AM',
    'a': date.getHours() >= 12 ? 'pm' : 'am'
  };
  
  let result = pattern;
  for (const [key, value] of Object.entries(replacements)) {
    result = result.replace(new RegExp(key, 'g'), value);
  }
  return result;
}

/**
 * Parse date from string with pattern
 */
function parseDate(str, pattern = 'YYYY-MM-DD') {
  if (!str) return null;
  
  const patternParts = pattern.match(/(YYYY|YY|MM|M|DD|D|HH|H|hh|h|mm|m|ss|s|SSS|A|a)/g) || [];
  const regex = pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    .replace(/YYYY/g, '(\\d{4})')
    .replace(/YY/g, '(\\d{2})')
    .replace(/MM/g, '(\\d{2})')
    .replace(/M/g, '(\\d{1,2})')
    .replace(/DD/g, '(\\d{2})')
    .replace(/D/g, '(\\d{1,2})')
    .replace(/HH/g, '(\\d{2})')
    .replace(/H/g, '(\\d{1,2})')
    .replace(/hh/g, '(\\d{2})')
    .replace(/h/g, '(\\d{1,2})')
    .replace(/mm/g, '(\\d{2})')
    .replace(/m/g, '(\\d{1,2})')
    .replace(/ss/g, '(\\d{2})')
    .replace(/s/g, '(\\d{1,2})')
    .replace(/SSS/g, '(\\d{3})')
    .replace(/A/g, '(AM|PM)')
    .replace(/a/g, '(am|pm)');
  
  const match = str.match(new RegExp(regex));
  if (!match) return null;
  
  let year = 0, month = 0, day = 1, hours = 0, minutes = 0, seconds = 0, ms = 0;
  let isPM = false;
  
  patternParts.forEach((part, i) => {
    const value = match[i + 1];
    switch (part) {
      case 'YYYY': year = parseInt(value); break;
      case 'YY': year = parseInt(value) + (parseInt(value) > 50 ? 1900 : 2000); break;
      case 'MM': case 'M': month = parseInt(value) - 1; break;
      case 'DD': case 'D': day = parseInt(value); break;
      case 'HH': case 'H': hours = parseInt(value); break;
      case 'hh': case 'h': hours = parseInt(value); break;
      case 'mm': case 'm': minutes = parseInt(value); break;
      case 'ss': case 's': seconds = parseInt(value); break;
      case 'SSS': ms = parseInt(value); break;
      case 'A': case 'a': isPM = value.toLowerCase() === 'pm'; break;
    }
  });
  
  if (isPM && hours < 12) hours += 12;
  if (!isPM && hours === 12) hours = 0;
  
  return new Date(year, month, day, hours, minutes, seconds, ms);
}

/**
 * Get current timestamp in milliseconds
 */
function now() {
  return Date.now();
}

/**
 * Get current date at start of day
 */
function today() {
  const d = new Date();
  d.setHours(0, 0, 0, 0);
  return d;
}

/**
 * Get tomorrow's date at start of day
 */
function tomorrow() {
  const d = today();
  d.setDate(d.getDate() + 1);
  return d;
}

/**
 * Get yesterday's date at start of day
 */
function yesterday() {
  const d = today();
  d.setDate(d.getDate() - 1);
  return d;
}

/**
 * Add days to date
 */
function addDays(date, days) {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

/**
 * Subtract days from date
 */
function subtractDays(date, days) {
  return addDays(date, -days);
}

/**
 * Add months to date
 */
function addMonths(date, months) {
  const result = new Date(date);
  result.setMonth(result.getMonth() + months);
  return result;
}

/**
 * Add years to date
 */
function addYears(date, years) {
  const result = new Date(date);
  result.setFullYear(result.getFullYear() + years);
  return result;
}

/**
 * Add hours to date
 */
function addHours(date, hours) {
  const result = new Date(date);
  result.setHours(result.getHours() + hours);
  return result;
}

/**
 * Add minutes to date
 */
function addMinutes(date, minutes) {
  const result = new Date(date);
  result.setMinutes(result.getMinutes() + minutes);
  return result;
}

/**
 * Add seconds to date
 */
function addSeconds(date, seconds) {
  const result = new Date(date);
  result.setSeconds(result.getSeconds() + seconds);
  return result;
}

/**
 * Get start of day
 */
function startOfDay(date) {
  const result = new Date(date);
  result.setHours(0, 0, 0, 0);
  return result;
}

/**
 * Get end of day
 */
function endOfDay(date) {
  const result = new Date(date);
  result.setHours(23, 59, 59, 999);
  return result;
}

/**
 * Get start of week (Sunday)
 */
function startOfWeek(date, startOnMonday = false) {
  const result = new Date(date);
  const day = result.getDay();
  const diff = startOnMonday ? (day === 0 ? 6 : day - 1) : day;
  result.setDate(result.getDate() - diff);
  return startOfDay(result);
}

/**
 * Get end of week (Saturday)
 */
function endOfWeek(date, startOnMonday = false) {
  const result = startOfWeek(date, startOnMonday);
  result.setDate(result.getDate() + 6);
  return endOfDay(result);
}

/**
 * Get start of month
 */
function startOfMonth(date) {
  const result = new Date(date);
  result.setDate(1);
  return startOfDay(result);
}

/**
 * Get end of month
 */
function endOfMonth(date) {
  const result = new Date(date);
  result.setMonth(result.getMonth() + 1, 0);
  return endOfDay(result);
}

/**
 * Get start of year
 */
function startOfYear(date) {
  const result = new Date(date);
  result.setMonth(0, 1);
  return startOfDay(result);
}

/**
 * Get end of year
 */
function endOfYear(date) {
  const result = new Date(date);
  result.setMonth(11, 31);
  return endOfDay(result);
}

/**
 * Get difference in milliseconds
 */
function diff(date1, date2) {
  return date1.getTime() - date2.getTime();
}

/**
 * Get difference in seconds
 */
function diffSeconds(date1, date2) {
  return Math.floor(diff(date1, date2) / 1000);
}

/**
 * Get difference in minutes
 */
function diffMinutes(date1, date2) {
  return Math.floor(diffSeconds(date1, date2) / 60);
}

/**
 * Get difference in hours
 */
function diffHours(date1, date2) {
  return Math.floor(diffMinutes(date1, date2) / 60);
}

/**
 * Get difference in days
 */
function diffDays(date1, date2) {
  return Math.floor(diffHours(date1, date2) / 24);
}

/**
 * Get difference in weeks
 */
function diffWeeks(date1, date2) {
  return Math.floor(diffDays(date1, date2) / 7);
}

/**
 * Get difference in months
 */
function diffMonths(date1, date2) {
  const months = (date1.getFullYear() - date2.getFullYear()) * 12;
  return months + date1.getMonth() - date2.getMonth();
}

/**
 * Get difference in years
 */
function diffYears(date1, date2) {
  return date1.getFullYear() - date2.getFullYear();
}

/**
 * Check if date is before another
 */
function isBefore(date1, date2) {
  return date1.getTime() < date2.getTime();
}

/**
 * Check if date is after another
 */
function isAfter(date1, date2) {
  return date1.getTime() > date2.getTime();
}

/**
 * Check if dates are same day
 */
function isSameDay(date1, date2) {
  return date1.getFullYear() === date2.getFullYear() &&
         date1.getMonth() === date2.getMonth() &&
         date1.getDate() === date2.getDate();
}

/**
 * Check if date is today
 */
function isToday(date) {
  return isSameDay(date, new Date());
}

/**
 * Check if date is tomorrow
 */
function isTomorrow(date) {
  return isSameDay(date, tomorrow());
}

/**
 * Check if date is yesterday
 */
function isYesterday(date) {
  return isSameDay(date, yesterday());
}

/**
 * Check if date is weekend
 */
function isWeekend(date) {
  const day = date.getDay();
  return day === 0 || day === 6;
}

/**
 * Check if date is weekday
 */
function isWeekday(date) {
  return !isWeekend(date);
}

/**
 * Check if date is in range
 */
function isInRange(date, start, end) {
  return date.getTime() >= start.getTime() && date.getTime() <= end.getTime();
}

/**
 * Get day of week name
 */
function getDayName(date, short = false) {
  const days = short 
    ? ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    : ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  return days[date.getDay()];
}

/**
 * Get month name
 */
function getMonthName(date, short = false) {
  const months = short
    ? ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  return months[date.getMonth()];
}

/**
 * Get days in month
 */
function getDaysInMonth(date) {
  return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
}

/**
 * Get day of year (1-366)
 */
function getDayOfYear(date) {
  const start = startOfYear(date);
  return Math.floor((date - start) / (24 * 60 * 60 * 1000)) + 1;
}

/**
 * Get week of year
 */
function getWeekOfYear(date) {
  const start = startOfYear(date);
  const firstDay = start.getDay();
  const days = getDayOfYear(date);
  return Math.ceil((days + firstDay) / 7);
}

/**
 * Get quarter (1-4)
 */
function getQuarter(date) {
  return Math.floor(date.getMonth() / 3) + 1;
}

/**
 * Check if year is leap year
 */
function isLeapYear(date) {
  const year = date.getFullYear();
  return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
}

/**
 * Get relative time string (ago)
 */
function timeAgo(date) {
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
  
  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)} minute${seconds >= 120 ? 's' : ''} ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)} hour${seconds >= 7200 ? 's' : ''} ago`;
  if (seconds < 604800) return `${Math.floor(seconds / 86400)} day${seconds >= 172800 ? 's' : ''} ago`;
  if (seconds < 2592000) return `${Math.floor(seconds / 604800)} week${seconds >= 1209600 ? 's' : ''} ago`;
  if (seconds < 31536000) return `${Math.floor(seconds / 2592000)} month${seconds >= 5184000 ? 's' : ''} ago`;
  return `${Math.floor(seconds / 31536000)} year${seconds >= 63072000 ? 's' : ''} ago`;
}

/**
 * Get relative time string (from now)
 */
function timeFromNow(date) {
  const seconds = Math.floor((date.getTime() - Date.now()) / 1000);
  
  if (seconds < 60) return 'in a few seconds';
  if (seconds < 3600) return `in ${Math.floor(seconds / 60)} minute${seconds >= 120 ? 's' : ''}`;
  if (seconds < 86400) return `in ${Math.floor(seconds / 3600)} hour${seconds >= 7200 ? 's' : ''}`;
  if (seconds < 604800) return `in ${Math.floor(seconds / 86400)} day${seconds >= 172800 ? 's' : ''}`;
  if (seconds < 2592000) return `in ${Math.floor(seconds / 604800)} week${seconds >= 1209600 ? 's' : ''}`;
  if (seconds < 31536000) return `in ${Math.floor(seconds / 2592000)} month${seconds >= 5184000 ? 's' : ''}`;
  return `in ${Math.floor(seconds / 31536000)} year${seconds >= 63072000 ? 's' : ''}`;
}

/**
 * Get age from birthdate
 */
function getAge(birthdate) {
  const today = new Date();
  let age = today.getFullYear() - birthdate.getFullYear();
  const monthDiff = today.getMonth() - birthdate.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthdate.getDate())) {
    age--;
  }
  
  return age;
}

/**
 * Create date from parts
 */
function createDate(year, month, day, hours = 0, minutes = 0, seconds = 0, ms = 0) {
  return new Date(year, month - 1, day, hours, minutes, seconds, ms);
}

/**
 * Get calendar month array
 */
function getCalendarMonth(year, month, startOnMonday = false) {
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const days = [];
  
  // Add days from previous month
  let startDay = firstDay.getDay();
  if (startOnMonday) {
    startDay = startDay === 0 ? 6 : startDay - 1;
  }
  
  for (let i = startDay - 1; i >= 0; i--) {
    const date = new Date(year, month, -i);
    days.push({ date, isCurrentMonth: false });
  }
  
  // Add days of current month
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const date = new Date(year, month, i);
    days.push({ date, isCurrentMonth: true });
  }
  
  // Add days from next month
  const remaining = 42 - days.length; // 6 weeks
  for (let i = 1; i <= remaining; i++) {
    const date = new Date(year, month + 1, i);
    days.push({ date, isCurrentMonth: false });
  }
  
  return days;
}

/**
 * Check if valid date
 */
function isValidDate(date) {
  return date instanceof Date && !isNaN(date.getTime());
}

/**
 * Clone date
 */
function cloneDate(date) {
  return new Date(date.getTime());
}

/**
 * Get timezone offset in hours
 */
function getTimezoneOffset() {
  return -new Date().getTimezoneOffset() / 60;
}

/**
 * Convert to ISO string (local time)
 */
function toISOString(date) {
  return formatDate(date, 'YYYY-MM-DDTHH:mm:ss.SSS');
}

/**
 * Get Unix timestamp (seconds)
 */
function toUnix(date) {
  return Math.floor(date.getTime() / 1000);
}

/**
 * Create date from Unix timestamp
 */
function fromUnix(timestamp) {
  return new Date(timestamp * 1000);
}

/**
 * Main entry point for testing
 */
function main() {
  console.log('📅 Date Utils Skill\n');
  
  const now = new Date();
  
  // Test formatting
  console.log('Testing formatting:');
  console.log(`formatDate(now, 'YYYY-MM-DD'): '${formatDate(now, 'YYYY-MM-DD')}'`);
  console.log(`formatDate(now, 'YYYY-MM-DD HH:mm:ss'): '${formatDate(now, 'YYYY-MM-DD HH:mm:ss')}'`);
  console.log(`formatDate(now, 'DD/MM/YYYY'): '${formatDate(now, 'DD/MM/YYYY')}'`);
  
  // Test parsing
  console.log('\nTesting parsing:');
  const parsed = parseDate('2024-03-15', 'YYYY-MM-DD');
  console.log(`parseDate('2024-03-15', 'YYYY-MM-DD'): ${parsed ? formatDate(parsed, 'YYYY-MM-DD') : 'null'}`);
  
  // Test date arithmetic
  console.log('\nTesting date arithmetic:');
  console.log(`addDays(now, 7): ${formatDate(addDays(now, 7), 'YYYY-MM-DD')}`);
  console.log(`subtractDays(now, 7): ${formatDate(subtractDays(now, 7), 'YYYY-MM-DD')}`);
  
  // Test comparisons
  console.log('\nTesting comparisons:');
  console.log(`isToday(now): ${isToday(now)}`);
  console.log(`isWeekend(now): ${isWeekend(now)}`);
  
  // Test relative time
  console.log('\nTesting relative time:');
  const hourAgo = addHours(now, -1);
  console.log(`timeAgo(1 hour ago): ${timeAgo(hourAgo)}`);
  
  // Test utility functions
  console.log('\nTesting utilities:');
  console.log(`getDayName(now): ${getDayName(now)}`);
  console.log(`getMonthName(now): ${getMonthName(now)}`);
  console.log(`getQuarter(now): ${getQuarter(now)}`);
  console.log(`isLeapYear(now): ${isLeapYear(now)}`);
  
  console.log('\n✅ date-utils loaded successfully');
}

module.exports = {
  formatDate,
  parseDate,
  now,
  today,
  tomorrow,
  yesterday,
  addDays,
  subtractDays,
  addMonths,
  addYears,
  addHours,
  addMinutes,
  addSeconds,
  startOfDay,
  endOfDay,
  startOfWeek,
  endOfWeek,
  startOfMonth,
  endOfMonth,
  startOfYear,
  endOfYear,
  diff,
  diffSeconds,
  diffMinutes,
  diffHours,
  diffDays,
  diffWeeks,
  diffMonths,
  diffYears,
  isBefore,
  isAfter,
  isSameDay,
  isToday,
  isTomorrow,
  isYesterday,
  isWeekend,
  isWeekday,
  isInRange,
  getDayName,
  getMonthName,
  getDaysInMonth,
  getDayOfYear,
  getWeekOfYear,
  getQuarter,
  isLeapYear,
  timeAgo,
  timeFromNow,
  getAge,
  createDate,
  getCalendarMonth,
  isValidDate,
  cloneDate,
  getTimezoneOffset,
  toISOString,
  toUnix,
  fromUnix,
  main
};
