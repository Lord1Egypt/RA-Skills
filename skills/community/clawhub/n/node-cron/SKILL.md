---
name: node-cron
description: Node.js cron job scheduling with the `cron` npm package. Use when the user needs to schedule recurring tasks, create cron jobs, validate cron expressions, set up timed callbacks, or work with cron syntax in a Node.js/TypeScript project. 
---

# Node Cron

Use the `cron` npm package (`npm install cron`) for second-precision scheduled tasks in Node.js.

## Triggers

cron job, node-cron, schedule task, cron expression, cron pattern, scheduled job, npm install cron, CronJob, CronTime.

## Quick Start

```ts
import { CronJob } from 'cron';

const job = new CronJob(
  '0 */5 * * * *',  // every 5 minutes
  () => console.log('Running every 5 minutes'),
  null,             // onComplete
  true,             // start immediately
  'Asia/Shanghai'   // timeZone
);
```

Or use the object form:

```ts
const job = CronJob.from({
  cronTime: '0 0 9 * * 1',    // 9am every Monday
  onTick: () => sendReport(),
  start: true,
  timeZone: 'Asia/Shanghai'
});

job.stop();   // halt
job.start();  // resume
```

## Cron Patterns

The library uses **6 fields** (second-precision), unlike standard 5-field Unix cron:

```
second  minute  hour  day-of-month  month  day-of-week
  0-59   0-59   0-23     1-31       1-12     0-7
```

### Syntax

| Token | Meaning |
|-------|---------|
| `*` | Any value (every second/minute/etc.) |
| `1,3,5` | List of values |
| `1-5` | Range (inclusive) |
| `*/5` | Every N steps |

### Names

Use first 3 letters for month/day-of-week (case-insensitive):
`"jan,mar,dec"`, `"mon,wed,fri"`

Day-of-week: `0` or `7` is Sunday.

### Common Examples

| Expression | Meaning |
|------------|---------|
| `*/10 * * * * *` | Every 10 seconds |
| `0 * * * * *` | Every minute on the second |
| `0 0 * * * *` | Every hour |
| `0 0 9 * * *` | Daily at 9:00 AM |
| `0 30 9 * * 1-5` | 9:30 AM Mon-Fri |
| `0 0 0 1 * *` | Midnight on the 1st of every month |

## CronJob Class

### Constructor Parameters

| Param | Required | Description |
|-------|----------|-------------|
| `cronTime` | [OK] | Cron pattern string, `Date`, or Luxon `DateTime` |
| `onTick` | [OK] | Callback function |
| `onComplete` | | Called when job stops via `job.stop()` |
| `start` | | Auto-start. Default `false` |
| `timeZone` | | IANA zone string (e.g. `'Asia/Shanghai'`) |
| `context` | | `this` context for `onTick` |
| `runOnInit` | | Fire `onTick` immediately on init |
| `waitForCompletion` | | If `true`, skip ticks while callback is still running |
| `errorHandler` | | Catch exceptions in `onTick` |
| `name` | | Job identifier for debugging |
| `threshold` | | Missed-deadline tolerance in ms. Default `250` |

Do NOT pass `utcOffset` together with `timeZone`  --  they conflict.

### Key Methods

- **`CronJob.from(obj)`** (static)  --  Create with named params
- **`job.start()` / `job.stop()`**  --  Start/stop
- **`job.nextDate()`**  --  Next execution as Luxon DateTime
- **`job.nextDates(n)`**  --  Array of next N dates
- **`job.lastDate()`**  --  Last execution date
- **`job.setTime(cronTime)`**  --  Change schedule
- **`job.addCallback(fn)`**  --  Add another onTick callback

### Read-Only Properties

- **`job.isActive`**  --  Whether job is running
- **`job.isCallbackRunning`**  --  Whether onTick is currently executing

## Standalone Utilities

```ts
import * as cron from 'cron';

// When will this cron expression fire next?
const dt = cron.sendAt('0 0 * * *');
console.log(dt.toISO());

// How many ms until next execution?
const ms = cron.timeout('0 0 * * *');

// Validate an expression
const { valid, error } = cron.validateCronExpression('0 0 * * *');
```

## Gotchas

- **Month is 1-12**, not 0-11. Upgrade from v2 needs `+1` on all month values.
- **Day-of-week 0 = Sunday** (7 also works).
- **6 fields** (with seconds) -- unlike standard 5-field Unix cron.
- Use `waitForCompletion: true` for async callbacks to prevent overlap.

## Async onTick

Wrap async work directly  --  `waitForCompletion` prevents overlapping runs:

```ts
const job = CronJob.from({
  cronTime: '*/30 * * * * *',
  onTick: async () => {
    await fetchData();
    await processData();
  },
  waitForCompletion: true,
  start: true
});
```

## Full API Reference

See [references/api_reference.md](references/api_reference.md) for the complete API documentation including `CronTime` class, all method signatures, and migration notes.
