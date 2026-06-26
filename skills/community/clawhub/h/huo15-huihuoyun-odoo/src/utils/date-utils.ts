/**
 * 日期工具函数
 *
 * 解析相对日期（今天/明天/后天/下周等）并转换为 Odoo 格式
 */

/** 返回今日日期字符串 YYYY-MM-DD */
export function today(): string {
  return new Date().toISOString().split('T')[0]!;
}

/** 返回明天日期字符串 YYYY-MM-DD */
export function tomorrow(): string {
  const d = new Date();
  d.setDate(d.getDate() + 1);
  return d.toISOString().split('T')[0]!;
}

/** 返回 N 天后的日期字符串 YYYY-MM-DD */
export function daysFromNow(n: number): string {
  const d = new Date();
  d.setDate(d.getDate() + n);
  return d.toISOString().split('T')[0]!;
}

/**
 * 格式化 Date 对象为 Odoo datetime 字符串
 * 格式：YYYY-MM-DD HH:MM:SS
 */
export function formatOdooDatetime(date: Date): string {
  return date.toISOString().replace('T', ' ').substring(0, 19);
}

/**
 * 格式化 Date 对象为 Odoo date 字符串
 * 格式：YYYY-MM-DD
 */
export function formatOdooDate(date: Date): string {
  return date.toISOString().split('T')[0]!;
}

/**
 * 解析相对日期描述，返回 Odoo 格式的 datetime 字符串
 *
 * @param relative  相对词：'tomorrow' | 'day_after_tomorrow' | 'next_week' | null
 * @param explicitDate  显式日期字符串 YYYY-MM-DD，优先于 relative
 * @param slot  'start'（默认09:00）或 'end'（默认18:00）
 */
export function resolveRelativeDate(
  relative: string | null | undefined,
  explicitDate: string | null | undefined,
  slot: 'start' | 'end' = 'start',
): string {
  const now = new Date();

  if (explicitDate) {
    const date = new Date(explicitDate);
    date.setHours(slot === 'start' ? 9 : 18, 0, 0, 0);
    return formatOdooDatetime(date);
  }

  if (relative === 'tomorrow') {
    now.setDate(now.getDate() + 1);
  } else if (relative === 'day_after_tomorrow' || relative === 'day after tomorrow') {
    now.setDate(now.getDate() + 2);
  } else if (relative === 'next_week' || relative === 'next week') {
    now.setDate(now.getDate() + 7);
  } else if (relative === 'this_week' || relative === 'this week') {
    const dayOfWeek = now.getDay();
    const daysUntilFriday = ((5 - dayOfWeek) + 7) % 7 || 7;
    now.setDate(now.getDate() + daysUntilFriday);
  }

  now.setHours(slot === 'start' ? 9 : 18, 0, 0, 0);
  return formatOdooDatetime(now);
}
