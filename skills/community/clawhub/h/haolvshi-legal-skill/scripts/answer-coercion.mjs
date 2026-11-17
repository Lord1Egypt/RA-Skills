// 把宿主大模型提交的自然语言答案转换成后端问答接口真正接受的取值。
//
// 取值契约来自前端项目 new_lvpin 的题目组件，不同 component 差别很大：
//   10 / 11  QDate            value 是 unix 秒字符串；config.dateFormat==='yyyy-MM' 时日固定为 1；
//                             component 11 额外带时分。
//   8        QDateSelect      value 是 { year, month, day, allday, start, end } 对象，start/end 为 unix 秒。
//   17       QArea            value 是地区 id，层级由 config.areaLevel 决定（见 area-resolver.mjs）。
//   25       QInputUnit       value 是 { value, unit } 对象，unit 取自 config.nameUnit。
//   21 / 22  QExchangeRate    value 是 { option, content } 对象。
//            QLiquidatedDamages
//   9/12/13/20 数值            value 是数字。
//
// 只要这里少转一层，后端就会拿到 "1991-11-08" 或 "云南省昆明市" 这样的原文，
// 生成的报告会出现 Invalid Date、未匹配到地区和 NaN 金额。

const DATE_COMPONENTS = new Set(['10', '11']);

const CHINESE_DIGITS = new Map([
  ['〇', '0'], ['零', '0'], ['一', '1'], ['二', '2'], ['三', '3'], ['四', '4'],
  ['五', '5'], ['六', '6'], ['七', '7'], ['八', '8'], ['九', '9']
]);

function componentOf(node) {
  return String(node?.component ?? node?.type ?? '');
}

function configOf(node) {
  return node?.config || {};
}

/** `config.dateFormat === 'yyyy-MM'` 表示只收年月，日固定为 1。 */
export function isMonthOnlyDate(node) {
  return String(configOf(node).dateFormat || '').toLowerCase() === 'yyyy-mm';
}

/** component 11 是带时分的日期。 */
export function isMinuteDate(node) {
  return componentOf(node) === '11';
}

function normalizeChineseNumerals(text) {
  return String(text).replace(/[〇零一二三四五六七八九]/g, char => CHINESE_DIGITS.get(char) ?? char);
}

/**
 * 解析宿主可能给出的各种日期写法，返回 { year, month, day, hour, minute }。
 * 支持 1991-11-08、1991/11/8、1991年11月8日、19911108、1991-11、1991年11月。
 * 无法解析时返回 null，由调用方决定是报错还是把原值透传。
 */
export function parseDateParts(value) {
  if (value === null || value === undefined || value === '') return null;

  // 已经是 unix 时间戳时直接还原，避免二次转换把值改坏。
  // 只有带负号（1970 年之前）或长度为 10/13 位才当作时间戳，
  // 否则 "196905" 这种年月紧凑写法会被误判成秒数。
  const trimmed = String(value).trim();
  const looksLikeTimestamp = typeof value === 'number'
    || /^-\d+$/.test(trimmed)
    || /^\d{10}$|^\d{13}$/.test(trimmed);
  if (looksLikeTimestamp) {
    const raw = Number(value);
    if (!Number.isFinite(raw)) return null;
    const date = new Date(String(raw).length >= 13 ? raw : raw * 1000);
    if (Number.isNaN(date.getTime())) return null;
    return {
      year: date.getFullYear(),
      month: date.getMonth() + 1,
      day: date.getDate(),
      hour: date.getHours(),
      minute: date.getMinutes()
    };
  }

  const text = normalizeChineseNumerals(trimmed);

  const ymd = text.match(/(\d{4})\s*[-/.年]\s*(\d{1,2})(?:\s*[-/.月]\s*(\d{1,2}))?/);
  // 紧凑写法：19911108（年月日）和 199111（年月）都要支持。
  const compact = !ymd && (text.match(/^(\d{4})(\d{2})(\d{2})$/) || text.match(/^(\d{4})(\d{2})$/));
  const matched = ymd || compact;
  if (!matched) return null;

  const year = Number(matched[1]);
  const month = Number(matched[2]);
  const day = matched[3] === undefined ? 1 : Number(matched[3]);
  if (!Number.isFinite(year) || !Number.isFinite(month)) return null;
  if (month < 1 || month > 12) return null;
  if (!Number.isFinite(day) || day < 1 || day > 31) return null;

  const time = text.match(/(\d{1,2})\s*[:时点]\s*(\d{1,2})?/);
  return {
    year,
    month,
    day,
    hour: time ? Number(time[1]) : 0,
    minute: time && time[2] !== undefined ? Number(time[2]) : 0
  };
}

/** 用本地时区构造，和前端 dayjs(`${y}-${m}-${d}`).unix() 的行为保持一致。 */
export function partsToUnixSeconds({ year, month, day, hour = 0, minute = 0 }) {
  const date = new Date(year, month - 1, day, hour, minute, 0, 0);
  if (Number.isNaN(date.getTime())) return null;
  // 前端限制在 1900 到 2200 年之间，超出范围后端会判为非法时间。
  if (year < 1900 || year > 2200) return null;
  return Math.floor(date.getTime() / 1000);
}

/** 日期字段 → unix 秒字符串。无法解析时返回原值，让后端给出可读报错。 */
export function coerceDateValue(node, value) {
  const parts = parseDateParts(value);
  if (!parts) return value;
  if (isMonthOnlyDate(node)) parts.day = 1;
  if (!isMinuteDate(node)) {
    parts.hour = 0;
    parts.minute = 0;
  }
  const seconds = partsToUnixSeconds(parts);
  return seconds === null ? value : String(seconds);
}

/** 日期区间字段 → { year, month, day, allday, start, end }，与前端 calculateDateRange 对齐。 */
export function coerceDateRangeValue(node, value) {
  if (value && typeof value === 'object' && !Array.isArray(value)
    && value.start !== undefined && value.end !== undefined) {
    return value;
  }

  let startRaw;
  let endRaw;
  if (Array.isArray(value)) {
    [startRaw, endRaw] = value;
  } else {
    const dates = String(value).split(/至|到|~|—|–|\s+-\s+/).map(part => part.trim()).filter(Boolean);
    [startRaw, endRaw] = dates;
  }

  const start = parseDateParts(startRaw);
  const end = parseDateParts(endRaw);
  if (!start || !end) return value;

  const startSeconds = partsToUnixSeconds({ ...start, hour: 0, minute: 0 });
  const endSeconds = partsToUnixSeconds({ ...end, hour: 0, minute: 0 });
  if (startSeconds === null || endSeconds === null) return value;

  const startDate = new Date(startSeconds * 1000);
  const endDate = new Date(endSeconds * 1000);
  // 前端把结束日当天也算进去，先加一天再取年月日差。
  const boundary = new Date(endDate.getFullYear(), endDate.getMonth(), endDate.getDate() + 1);

  let year = boundary.getFullYear() - startDate.getFullYear();
  let month = boundary.getMonth() - startDate.getMonth();
  let day = boundary.getDate() - startDate.getDate();
  if (day < 0) {
    month -= 1;
    day += new Date(startDate.getFullYear(), startDate.getMonth() + 1, 0).getDate();
  }
  if (month < 0) {
    year -= 1;
    month += 12;
  }

  const allday = Math.round((endSeconds - startSeconds) / 86400) + 1;
  return { year, month, day, allday, start: startSeconds, end: endSeconds };
}

function firstNumber(value) {
  if (typeof value === 'number') return value;
  const matched = String(value).replace(/,/g, '').match(/-?\d+(?:\.\d+)?/);
  return matched ? Number(matched[0]) : null;
}

/** 数值+单位字段 → { value, unit }，单位必须来自 config.nameUnit。 */
export function coerceNumberUnitValue(node, value) {
  const units = String(configOf(node).nameUnit || '').split(',').map(item => item.trim()).filter(Boolean);
  if (value && typeof value === 'object' && !Array.isArray(value) && 'value' in value) {
    return { value: value.value, unit: value.unit || units[0] || '' };
  }
  const text = String(value);
  const matchedUnit = units.find(unit => unit && text.includes(unit));
  const amount = firstNumber(value);
  return {
    value: amount === null ? value : amount,
    unit: matchedUnit || units[0] || ''
  };
}

/** 汇率、违约金字段 → { option, content }。 */
export function coerceOptionContentValue(node, value) {
  if (value && typeof value === 'object' && !Array.isArray(value)) {
    if ('option' in value || 'content' in value) return value;
  }
  const amount = firstNumber(value);
  return { option: configOf(node).defaultOption || '', content: amount === null ? value : amount };
}

const NUMERIC_TYPES = new Set(['money', 'number']);

/**
 * 按节点的 component 和 config 把答案转换成后端取值。
 * 地区（region）需要查地区表，由 area-resolver.mjs 在调用本函数前解析成 id。
 */
export function coerceNodeValue(node, type, value) {
  if (value === undefined || value === null) return value;
  if (type === 'date') return coerceDateValue(node, value);
  if (type === 'date_range') return coerceDateRangeValue(node, value);
  if (type === 'number_unit') return coerceNumberUnitValue(node, value);
  if (['exchange_rate', 'liquidated_damages'].includes(type)) return coerceOptionContentValue(node, value);
  if (NUMERIC_TYPES.has(type)) {
    const amount = firstNumber(value);
    return amount === null ? value : amount;
  }
  return value;
}

/** 把后端存量的 unix 秒还原成人类可读文本，用于回显和摘要。 */
export function formatDateForDisplay(node, value) {
  const parts = parseDateParts(value);
  if (!parts) return value === undefined || value === null ? '' : String(value);
  const pad = number => String(number).padStart(2, '0');
  if (isMonthOnlyDate(node)) return `${parts.year}-${pad(parts.month)}`;
  const date = `${parts.year}-${pad(parts.month)}-${pad(parts.day)}`;
  return isMinuteDate(node) ? `${date} ${pad(parts.hour)}:${pad(parts.minute)}` : date;
}

export { DATE_COMPONENTS };
