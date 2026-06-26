# Node Cron  --  Full API Reference

## Standalone Functions

### `sendAt(cronExpression: string): DateTime`

Returns a Luxon `DateTime` indicating when the expression will next fire.

```ts
import * as cron from 'cron';
const dt = cron.sendAt('0 0 * * *');
console.log(`Next run: ${dt.toISO()}`);
```

### `timeout(cronExpression: string): number`

Milliseconds until the next execution.

```ts
const ms = cron.timeout('0 0 * * *');
console.log(`Runs in ${ms}ms`);
```

### `validateCronExpression(expr: string): { valid: boolean; error?: string }`

Check if a cron expression is syntactically valid.

```ts
const { valid, error } = cron.validateCronExpression('0 0 * * *');
if (!valid) console.error(error);
```

## CronJob Class

### Constructor

```
new CronJob(
  cronTime,          // string | Date | DateTime  --  REQUIRED
  onTick,            // Function  --  REQUIRED
  onComplete?,       // Function  --  called on job.stop()
  start?,            // boolean  --  auto-start (default false)
  timeZone?,         // string  --  IANA zone
  context?,          // any  --  'this' for onTick
  runOnInit?,        // boolean  --  fire onTick immediately
  utcOffset?,        // number  --  minutes offset (conflicts with timeZone)
  unrefTimeout?,     // boolean  --  unref timer for event loop
  waitForCompletion?,// boolean  --  skip overlapping ticks
  errorHandler?,     // Function  --  catch onTick errors
  name?,             // string  --  job identifier
  threshold?         // number  --  missed deadline tolerance ms (default 250)
)
```

### Static Methods

#### `CronJob.from(options: CronJobOptions): CronJob`

Object-based constructor. All options match the constructor params above.

```ts
const job = CronJob.from({
  cronTime: '*/5 * * * * *',
  onTick: () => console.log('tick'),
  start: true,
  timeZone: 'America/New_York',
  name: 'my-job'
});
```

### Instance Methods

| Method | Description |
|--------|-------------|
| `start()` | Start the job |
| `stop()` | Stop the job, fires `onComplete` |
| `setTime(cronTime: CronTime)` | Change the schedule |
| `lastDate(): DateTime \| undefined` | Last execution as Luxon DateTime |
| `nextDate(): DateTime` | Next execution as Luxon DateTime |
| `nextDates(count?: number): DateTime[]` | Array of next N execution dates (returns empty array if count omitted) |
| `fireOnTick()` | Manually trigger onTick |
| `addCallback(fn: Function)` | Add additional onTick callback |

### Instance Properties

| Property | Type | Description |
|----------|------|-------------|
| `isActive` | `boolean` | Read-only. Whether job is running |
| `isCallbackRunning` | `boolean` | Read-only. Whether onTick is executing |

```ts
const job = new CronJob('* * * * * *', async () => {
  console.log(job.isCallbackRunning); // true during execution
  await someAsyncTask();
});
console.log(job.isCallbackRunning); // false
job.start();
console.log(job.isActive); // true
```

## CronTime Class

### Constructor

```
new CronTime(time: string | Date, zone?: string, utcOffset?: number)
```

- `time`  --  Cron expression string or `Date` object (REQUIRED)
- `zone`  --  IANA timezone string (optional)
- `utcOffset`  --  UTC offset in minutes (optional, conflicts with `zone`)

## Cron Ranges

```
field          allowed values
-----          --------------
second         0-59
minute         0-59
hour           0-23
day of month   1-31
month          1-12 (or JAN-DEC)
day of week    0-7 (0 or 7 = SUN, or names)
```

## Migrating from v2 to v3

- **Month indexing:** Changed from `0-11` to `1-12`. Increment all numeric months by 1.
- **Day-of-Week:** `7` now accepted as Sunday.
- Constructor no longer accepts object as sole param  --  use `CronJob.from()` instead.
- `job()` and `time()` removed  --  use `new CronJob()` / `new CronTime()`.
- `nextDates()` always returns array. Use `nextDate()` for single.

## Migrating from v3 to v4

- **Node v16 dropped.** Requires Node v18+.
- `job.running` renamed to `job.isActive` (read-only). Use `start()`/`stop()` instead.
