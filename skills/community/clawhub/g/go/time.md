# Time — Clocks, Timers, Layouts, and Zones

`time.Time` carries two clocks at once: a wall clock (what the calendar says, subject to NTP steps and DST) and a monotonic reading (what the machine has counted since boot). Which one an operation uses is the source of most time bugs in Go.

## Two Clocks in One Value

- `time.Now()` includes a monotonic reading. `t2.Sub(t1)` and `time.Since(t)` use it when both values have it, so elapsed time is immune to NTP adjustments and clock steps.
- The monotonic reading is **stripped** by: `t.Round`, `t.Truncate`, `t.UTC()`, `t.In(loc)`, `t.AddDate`, marshaling and unmarshaling, and anything that round-trips through a string or a database. After that, `Sub` falls back to wall-clock arithmetic and can return a negative duration when NTP steps the clock backwards.
- Rule: measure durations with `time.Since(start)` on a `time.Time` you have not transformed. Store instants (created_at) as wall time; never store an elapsed measurement as the difference of two persisted timestamps if precision matters.
- `t1 == t2` compares the location pointer and the monotonic reading too, so two values for the same instant can compare unequal. Use `t1.Equal(t2)`.

## Timers and Tickers

| Need | Use | Cleanup |
|---|---|---|
| One deadline in a `select` | `context.WithTimeout` | `defer cancel()` (`context.md`) |
| Repeated timeout inside a loop | One `time.NewTimer`, `Reset` per iteration | `defer t.Stop()` |
| Periodic work | `time.NewTicker` | `defer t.Stop()` — always |
| A single delay, nothing to select on | `time.Sleep` | none |

- `case <-time.After(d)` inside a `for`/`select` allocates a new timer every iteration. On `go <1.23` each one also stayed alive until it fired, so a 1-hour timeout in a loop iterating every millisecond accumulated timers for an hour. From `go >=1.23` unreferenced timers are collectable immediately, but the per-iteration allocation remains — hoist a `Timer` and `Reset` it.
- `Timer.Reset` on a timer that may already have fired is only safe if you have drained its channel. The safe sequence outside a select loop: `if !t.Stop() { <-t.C }; t.Reset(d)`. In `go >=1.23` timer channels are unbuffered, which removes the stale-value class of bug, but the module's `go` directive gates the new behavior (`versions.md`).
- A `Ticker` **drops** ticks when the receiver is slower than the period; it never queues them. Long-running periodic work should time itself and log when a cycle exceeds the period, or the schedule silently halves.
- Never leave a Ticker unstopped in a function that returns — it keeps firing into a channel nobody reads, forever (`concurrency.md`).
- `time.AfterFunc(d, f)` runs `f` in its own goroutine; the returned Timer's `Stop` returns false if `f` already started, and does not wait for it to finish.

## Layouts

Go formats by example, using the reference time `Mon Jan 2 15:04:05 MST 2006` (Unix 1136239445 — the digits run 1 2 3 4 5 6 7 in the order month, day, hour, minute, second, year, zone offset).

| Layout piece | Means |
|---|---|
| `2006` / `06` | Four- / two-digit year |
| `01` / `1` / `Jan` / `January` | Month zero-padded / no padding / short / full |
| `02` / `2` / `_2` | Day zero-padded / no padding / space-padded |
| `15` / `03` / `PM` | 24-hour / 12-hour / meridiem |
| `04`, `05`, `.000`, `.999` | Minute, second, fixed-precision fraction, trailing-zeros-trimmed fraction |
| `MST` / `-0700` / `-07:00` / `Z07:00` | Zone name / numeric offset / colon offset / `Z` for UTC |

- Use the constants when they fit: `time.RFC3339` (`2006-01-02T15:04:05Z07:00`) for APIs, `time.DateOnly`/`time.TimeOnly`/`time.DateTime` (`go >=1.20`) for the common human formats.
- `15` is the only 24-hour hour. Writing `2006-01-02 03:04:05` and getting 1 PM printed as `01` is the classic bug.
- `time.Parse` returns an error on any mismatch, including a shorter fraction than the layout. `time.ParseInLocation` is what you want when the input has no zone and belongs to a known place.
- **`time.Parse` with no zone in the input yields UTC**, not local time. A date typed by a user in Madrid parsed with `time.DateOnly` becomes midnight UTC — an hour or two off, and one day off for anyone east of the line.

## Zones and DST

- `time.Local` depends on `TZ` and on the OS zone database. A `FROM scratch` or distroless container has no `/usr/share/zoneinfo`, so `time.LoadLocation("Europe/Madrid")` fails at runtime with "unknown time zone" — import `_ "time/tzdata"` (`go >=1.15`) to embed the database in the binary, at roughly a few hundred KB (`deployment.md`).
- Store and transport instants in UTC; convert to a location only for display and for calendar arithmetic that must respect DST.
- `t.Add(24 * time.Hour)` adds exactly 24 hours and lands on the wrong wall-clock time across a DST boundary. `t.AddDate(0, 0, 1)` adds a calendar day in `t`'s location. Pick by what the user means: "same time tomorrow" is `AddDate`, "in 24 hours" is `Add`.
- `AddDate` normalizes overflow: January 31 plus one month is March 3 (or 2). If you need end-of-month clamping, compute it explicitly.
- Duration is an int64 of **nanoseconds**, so the maximum representable span is about 292 years. Multiplying two durations, or a duration by a duration-typed constant, produces nonsense units: `d * time.Second` is wrong; `time.Duration(n) * time.Second` is right.
- Printing a `time.Duration` uses `String()` (`1h30m0s`). For seconds as a number, `d.Seconds()`.

## Testing Time

- Never call `time.Now()` directly in code you need to test. Inject a `now func() time.Time` field, or a small `Clock` interface, defaulting to `time.Now` (`testing.md`).
- `testing/synctest` (`go >=1.25`, experimental in 1.24 behind `GOEXPERIMENT=synctest`) runs a goroutine group on a fake clock that advances when every goroutine is blocked — it makes tests of timeouts and retries deterministic and instant instead of sleeping.
- Do not synchronize tests with `time.Sleep`. It is slow when it works and flaky when it does not; wait on a channel, a `sync.WaitGroup`, or a condition with a bounded poll.

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| `time.After` in a select loop | Timer allocation per iteration (and, on `go <1.23`, retention until fire) | Hoisted `Timer` + `Reset` |
| Ticker without `Stop` | Goroutine and timer leak | `defer t.Stop()` |
| Elapsed time from two persisted timestamps | Negative or wrong under NTP steps | `time.Since` on an untouched `time.Time` |
| `t1 == t2` | Compares location and monotonic reading | `t1.Equal(t2)` |
| Parsing a bare date without a location | Silently UTC | `time.ParseInLocation` |
| `Add(24*time.Hour)` for "tomorrow" | Off by an hour twice a year | `AddDate(0, 0, 1)` |
| Scratch/distroless image plus `LoadLocation` | Runtime "unknown time zone" that never appears locally | `import _ "time/tzdata"` |
| `time.Sleep` to wait for a goroutine in a test | Flaky and slow | Channel, WaitGroup, or `synctest` |

## Back To SKILL.md

Cancellation deadlines: `context.md`. Timer-related goroutine leaks: `concurrency.md`. Timestamp columns and driver behavior: `database.md`.
