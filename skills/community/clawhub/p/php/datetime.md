# Dates, Times, and Time Zones

## Defaults That Prevent Most Bugs

- `DateTimeImmutable` for everything. `DateTime::modify()`, `add()`, `sub()`, and `setDate()` mutate in place, so a helper that "returns next month" also moves the caller's date — the reference is shared (`oop.md`).
- An explicit IANA zone (`new DateTimeZone('Europe/Madrid')`), never an abbreviation. `EST` is a fixed offset with no DST; `America/New_York` is the actual rule set.
- Set `date.timezone` in php.ini. Unset, PHP uses UTC with no warning, and the CLI and FPM ini files can disagree (`php-ini.md`).
- Store UTC, convert at the edges. `->setTimezone(new DateTimeZone($user->tz))` for display, `->setTimezone(new DateTimeZone('UTC'))` before writing.
- Elapsed time is measured with `hrtime(true)` (monotonic nanoseconds), never by subtracting two wall-clock timestamps — NTP can step the clock backwards and produce a negative duration.

## Parsing

- `strtotime()` returns `false` on failure and guesses formats: `03/04/2026` is read as m/d/Y because of the slashes, while `03-04-2026` is read as d-m-Y because of the dashes. Never parse user or API input with it.
- `DateTimeImmutable::createFromFormat()` fills any field the format does not mention from the CURRENT time. `createFromFormat('Y-m-d', '2026-03-01')` carries today's hours, minutes, and seconds — and around a DST boundary that can shift the day. Prefix the format with `!` to zero every unspecified field: `createFromFormat('!Y-m-d', $s)`.
- `createFromFormat` returns `false` on hard failure and can return an object with WARNINGS on a partially-valid input (`2026-02-31` rolls into March). Validate:

```php
$d = DateTimeImmutable::createFromFormat('!Y-m-d', $input, new DateTimeZone('UTC'));
$e = DateTimeImmutable::getLastErrors();     // php >=8.2 returns false when clean
if ($d === false || ($e !== false && ($e['warning_count'] > 0 || $e['error_count'] > 0))) {
    throw new InvalidArgumentException("not a date: {$input}");
}
```

- ISO 8601 with an offset (`2026-07-25T14:03:00+02:00`) is the only format to accept across a network boundary. The constructor parses it directly and the offset removes all ambiguity.
- A bare timestamp string (`@1770000000`) constructs in UTC and IGNORES any timezone argument — set the zone afterward with `setTimezone`.

## Arithmetic and DST

- `->modify('+1 day')` keeps the WALL-CLOCK time across a DST transition, so the interval can be 23 or 25 hours. `->modify('+86400 seconds')` keeps the absolute duration, so the wall clock shifts by an hour. Both are correct; pick the one your domain means. "Same time tomorrow" is the first; "24 hours of SLA" is the second.
- Month arithmetic overflows rather than clamping: 31 January `+1 month` is 3 March in a non-leap year. Use `modify('first day of next month')` or `modify('last day of next month')`, which are relative formats designed for exactly this.
- A local time that does not exist (the hour skipped at a spring-forward) or exists twice (autumn) is a real input from a real user. Decide the policy explicitly rather than letting PHP's normalization pick.
- `diff()` returns a `DateInterval`; `->days` is populated only on intervals produced by `diff()`, and is `false` on a hand-constructed one. `%a` in `format()` is total days, `%d` is the day component of the y/m/d breakdown — mixing them up is the "1 month and 35 days" bug.
- Comparison operators work directly on date objects and compare the instant, including microseconds. Since `new DateTimeImmutable()` captures microseconds, two objects created in the same second are NOT equal — compare `->getTimestamp()`, or format to the precision you care about.
- `getTimestamp()` is UTC by definition; two objects in different zones representing the same instant return the same integer.

## Formatting

- `format('Y-m-d')` uses PHP's own character set and produces ENGLISH month and day names regardless of locale. Localized output needs `IntlDateFormatter` (`ext-intl`).
- `format('c')` is ISO 8601, `format(DATE_ATOM)` the same — use one of them for machine-readable output, always.
- The ISO week trap: `date('W')` is the ISO week number and must be paired with `date('o')`, the ISO year. Using `Y` with `W` reports week 1 of the wrong year for a few days each January.
- `date('L')` for leap year, `date('t')` for days in the month, `date('N')` for ISO weekday (Monday = 1) versus `date('w')` (Sunday = 0) — off-by-one week starts come from mixing these.

## Storage Decisions

- A past instant (created_at, logged_in_at): store a UTC timestamp. The offset is history and does not change.
- A FUTURE local event (a meeting at 09:00 next March): store the local wall time PLUS the IANA zone, not a UTC instant. Governments change DST rules, and a UTC instant computed under the old rules is simply the wrong hour after the change.
- A date with no time (a birthday, an invoice date): store a `DATE` column, and keep it out of `DateTimeImmutable` arithmetic that could apply a zone conversion and move it by a day.
- A duration: store seconds as an integer, not a `TIME` column and not a formatted string.
- MySQL `DATETIME` stores no zone and `TIMESTAMP` converts using the CONNECTION time zone — a worker with a different `time_zone` setting reads back different values from the same rows (`database.md`).

## Operational Notes

- The timezone database lives in the system (or in the `timezonedb` PECL extension). A container image built a year ago carries year-old DST rules; after a country changes its rules, that image returns wrong offsets until it is rebuilt.
- `date_default_timezone_set()` is global and process-wide: in a test suite or a worker it leaks into every later job. Set it once at bootstrap and pass zones explicitly everywhere else (`testing.md`).
- Cron uses the SYSTEM zone while PHP uses `date.timezone`; a job scheduled "at midnight" can be two different midnights (`cli.md`).
- Inject a clock (PSR-20 `ClockInterface`) instead of calling `new DateTimeImmutable()` inside domain code — otherwise the only way to test a month boundary is to wait for one.

## Related

- Serializing dates in payloads: `json.md`
- Storage columns and connection zones: `database.md`
- Making time testable: `testing.md`
