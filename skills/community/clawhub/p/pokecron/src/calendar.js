import os from "node:os";

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const WEEKDAY_INDEX = new Map(
  WEEKDAYS.flatMap((name, index) => [
    [name.toLowerCase(), index],
    [name.toLowerCase().slice(0, 2), index]
  ])
);

const SHORTHANDS = new Set([
  "minutely",
  "hourly",
  "daily",
  "weekly",
  "monthly",
  "quarterly",
  "semiannually",
  "yearly"
]);

function pad(value, width = 2) {
  return String(value).padStart(width, "0");
}

function startOfLocalDay(date) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0, 0);
}

function addLocalDays(date, days) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate() + days, 0, 0, 0, 0);
}

function toInteger(value, label) {
  const parsed = Number.parseInt(String(value), 10);
  if (!Number.isFinite(parsed)) {
    throw new Error(`Invalid ${label}: ${value}`);
  }
  return parsed;
}

function addRangeValues(values, start, end, min, max, step) {
  if (step <= 0) {
    throw new Error(`Invalid step: ${step}`);
  }
  if (start < min || start > max || end < min || end > max) {
    throw new Error(`Range outside bounds: ${start}..${end}`);
  }
  if (start <= end) {
    for (let current = start; current <= end; current += step) values.add(current);
    return;
  }
  for (let current = start; current <= max; current += step) values.add(current);
  for (let current = min; current <= end; current += step) values.add(current);
}

function parseFieldToken(token, min, max, label) {
  const trimmed = String(token).trim();
  if (!trimmed) {
    throw new Error(`Invalid ${label}: empty token`);
  }

  const stepMatch = trimmed.match(/^(.+?)\/(\d+)$/);
  const base = stepMatch ? stepMatch[1] : trimmed;
  const step = stepMatch ? toInteger(stepMatch[2], `${label} step`) : 1;
  const values = new Set();

  if (base === "*") {
    addRangeValues(values, min, max, min, max, step);
    return { any: step === 1, values };
  }

  const rangeMatch = base.match(/^(\d+)(?:\.\.|-)(\d+)$/);
  if (rangeMatch) {
    addRangeValues(values, toInteger(rangeMatch[1], label), toInteger(rangeMatch[2], label), min, max, step);
    return { any: false, values };
  }

  if (/^\d+$/.test(base)) {
    const numeric = toInteger(base, label);
    if (numeric < min || numeric > max) {
      throw new Error(`Invalid ${label}: ${base}`);
    }
    if (stepMatch) {
      addRangeValues(values, numeric, max, min, max, step);
    } else {
      values.add(numeric);
    }
    return { any: false, values };
  }

  throw new Error(`Invalid ${label}: ${token}`);
}

function parseFieldSpec(spec, min, max, label) {
  const trimmed = String(spec).trim();
  if (!trimmed) {
    throw new Error(`Invalid ${label}: empty spec`);
  }
  if (trimmed === "*") {
    return { any: true, values: new Set() };
  }

  const values = new Set();
  for (const part of trimmed.split(",")) {
    const token = part.trim();
    if (!token) continue;
    const parsed = parseFieldToken(token, min, max, label);
    if (parsed.any) {
      for (let current = min; current <= max; current += 1) values.add(current);
      continue;
    }
    for (const value of parsed.values) values.add(value);
  }
  return { any: values.size === max - min + 1, values };
}

function matchesField(field, value) {
  return field.any || field.values.has(value);
}

function expandField(field, min, max) {
  if (field.any) {
    return Array.from({ length: max - min + 1 }, (_, index) => min + index);
  }
  return [...field.values].sort((left, right) => left - right);
}

function parseWeekdayToken(token) {
  const lower = String(token).trim().toLowerCase();
  if (!lower) return null;
  if (!WEEKDAY_INDEX.has(lower)) {
    throw new Error(`Invalid weekday token: ${token}`);
  }
  return WEEKDAY_INDEX.get(lower);
}

function parseWeekdaySpec(spec) {
  const trimmed = String(spec).trim();
  if (!trimmed || trimmed === "*") {
    return { any: true, values: new Set() };
  }
  const values = new Set();
  for (const part of trimmed.split(",")) {
    const token = part.trim();
    if (!token) continue;
    const rangeMatch = token.match(/^([A-Za-z]+)\.\.([A-Za-z]+)$/);
    if (rangeMatch) {
      addRangeValues(values, parseWeekdayToken(rangeMatch[1]), parseWeekdayToken(rangeMatch[2]), 0, 6, 1);
      continue;
    }
    values.add(parseWeekdayToken(token));
  }
  return { any: values.size === 7, values };
}

function parseSingleTimePattern(token) {
  const parts = String(token).trim().split(":");
  if (parts.length !== 2 && parts.length !== 3) {
    throw new Error(`Invalid time token: ${token}`);
  }

  const hourField = parseFieldSpec(parts[0], 0, 23, "hour");
  const minuteField = parseFieldSpec(parts[1], 0, 59, "minute");
  const secondField = parseFieldSpec(parts[2] ?? "0", 0, 59, "second");
  const hours = expandField(hourField, 0, 23);
  const minutes = expandField(minuteField, 0, 59);
  const seconds = expandField(secondField, 0, 59);
  const times = [];

  for (const hour of hours) {
    for (const minute of minutes) {
      for (const second of seconds) {
        times.push({
          hour,
          minute,
          second,
          sortKey: hour * 3600 + minute * 60 + second
        });
      }
    }
  }

  return times;
}

function parseTimeSpec(spec) {
  const trimmed = String(spec).trim();
  if (!trimmed) {
    throw new Error("Invalid time token: empty spec");
  }

  const csvParts = trimmed.split(",").map((part) => part.trim()).filter(Boolean);
  const patterns =
    csvParts.length > 1 && csvParts.every((part) => part.includes(":")) ? csvParts : [trimmed];

  const deduped = new Map();
  for (const pattern of patterns) {
    for (const time of parseSingleTimePattern(pattern)) {
      deduped.set(time.sortKey, time);
    }
  }
  return [...deduped.values()].sort((left, right) => left.sortKey - right.sortKey);
}

function parseGeneralCalendarExpression(expression) {
  const tokens = String(expression).trim().split(/\s+/).filter(Boolean);
  if (tokens.length !== 2 && tokens.length !== 3) {
    throw new Error(`Unsupported OnCalendar expression: ${expression}`);
  }

  const [weekdayToken, dateToken, timeToken] = tokens.length === 3 ? tokens : ["*", tokens[0], tokens[1]];
  const dateParts = dateToken.split("-");
  if (dateParts.length !== 3) {
    throw new Error(`Invalid date token in OnCalendar expression: ${expression}`);
  }

  return {
    kind: "calendar",
    expression,
    weekday: parseWeekdaySpec(weekdayToken),
    year: parseFieldSpec(dateParts[0], 1970, 2500, "year"),
    month: parseFieldSpec(dateParts[1], 1, 12, "month"),
    day: parseFieldSpec(dateParts[2], 1, 31, "day"),
    times: parseTimeSpec(timeToken)
  };
}

export function parseOnCalendarExpression(expression) {
  const trimmed = String(expression || "").trim();
  if (!trimmed) {
    throw new Error("Empty OnCalendar expression");
  }

  const lower = trimmed.toLowerCase();
  if (SHORTHANDS.has(lower)) {
    return {
      kind: "shorthand",
      expression: trimmed,
      value: lower
    };
  }

  return parseGeneralCalendarExpression(trimmed);
}

function matchesCalendarDate(parsed, date) {
  return (
    matchesField(parsed.year, date.getFullYear()) &&
    matchesField(parsed.month, date.getMonth() + 1) &&
    matchesField(parsed.day, date.getDate()) &&
    (parsed.weekday.any || parsed.weekday.values.has(date.getDay()))
  );
}

function nextShorthandOccurrence(parsed, afterDate) {
  const date = new Date(afterDate.getTime() + 1000);
  switch (parsed.value) {
    case "minutely":
      return new Date(
        date.getFullYear(),
        date.getMonth(),
        date.getDate(),
        date.getHours(),
        date.getMinutes() + 1,
        0,
        0
      );
    case "hourly":
      return new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours() + 1, 0, 0, 0);
    case "daily":
      return new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1, 0, 0, 0, 0);
    case "weekly": {
      const result = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0, 0);
      const day = result.getDay();
      const delta = day === 0 ? 1 : 8 - day;
      result.setDate(result.getDate() + delta);
      return result;
    }
    case "monthly":
      return new Date(date.getFullYear(), date.getMonth() + 1, 1, 0, 0, 0, 0);
    case "quarterly": {
      const quarter = Math.floor(date.getMonth() / 3);
      const month = (quarter + 1) * 3;
      return new Date(date.getFullYear(), month, 1, 0, 0, 0, 0);
    }
    case "semiannually": {
      const month = date.getMonth() < 6 ? 6 : 12;
      return new Date(date.getFullYear(), month, 1, 0, 0, 0, 0);
    }
    case "yearly":
      return new Date(date.getFullYear() + 1, 0, 1, 0, 0, 0, 0);
    default:
      throw new Error(`Unsupported OnCalendar shorthand: ${parsed.value}`);
  }
}

export function nextOccurrenceForCalendar(parsedExpression, afterDate) {
  const parsed =
    typeof parsedExpression === "string" ? parseOnCalendarExpression(parsedExpression) : parsedExpression;
  const after = afterDate instanceof Date ? afterDate : new Date(afterDate);
  if (Number.isNaN(after.getTime())) {
    throw new Error(`Invalid date for calendar lookup: ${afterDate}`);
  }

  if (parsed.kind === "shorthand") {
    return nextShorthandOccurrence(parsed, after);
  }

  const start = startOfLocalDay(after);
  for (let dayOffset = 0; dayOffset < 3660; dayOffset += 1) {
    const day = addLocalDays(start, dayOffset);
    if (!matchesCalendarDate(parsed, day)) continue;
    for (const time of parsed.times) {
      const candidate = new Date(
        day.getFullYear(),
        day.getMonth(),
        day.getDate(),
        time.hour,
        time.minute,
        time.second,
        0
      );
      if (candidate.getTime() > after.getTime()) {
        return candidate;
      }
    }
  }

  throw new Error(`Unable to compute next occurrence for expression: ${parsed.expression}`);
}

export function occurrencesBetween(parsedExpression, afterDate, untilDate, limit = 1024) {
  const parsed =
    typeof parsedExpression === "string" ? parseOnCalendarExpression(parsedExpression) : parsedExpression;
  const after = afterDate instanceof Date ? afterDate : new Date(afterDate);
  const until = untilDate instanceof Date ? untilDate : new Date(untilDate);
  const occurrences = [];
  let cursor = after;

  while (occurrences.length < limit) {
    const next = nextOccurrenceForCalendar(parsed, cursor);
    if (next.getTime() > until.getTime()) break;
    occurrences.push(next);
    cursor = new Date(next.getTime());
  }

  return occurrences;
}

export function formatLocalTimestamp(date) {
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(
    date.getMinutes()
  )}:${pad(date.getSeconds())}`;
}

export function formatSystemdExactCalendar(date) {
  return `${WEEKDAYS[date.getDay()]} ${formatLocalTimestamp(date)}`;
}

export function buildLaunchdCalendarParts(date) {
  return {
    Month: date.getMonth() + 1,
    Day: date.getDate(),
    Hour: date.getHours(),
    Minute: date.getMinutes()
  };
}

export function formatIsoLocal(date) {
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(
    date.getMinutes()
  )}:${pad(date.getSeconds())}`;
}

export function describeLocalTimezone() {
  return Intl.DateTimeFormat(undefined, { timeZoneName: "short" })
    .formatToParts(new Date())
    .find((part) => part.type === "timeZoneName")?.value || os.userInfo().username;
}
