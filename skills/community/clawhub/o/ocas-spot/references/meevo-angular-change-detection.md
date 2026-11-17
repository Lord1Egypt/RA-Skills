# Meevo Angular Change Detection Issue

**Status**: Persistent — succeeded once on 2026-05-31 14:46 PT after 9+ failures. Then failed on the next 40+ consecutive sweeps (2026-05-31 21:00 through 2026-06-04 11:45 PT). Cookie consent DOM removal + re-click pattern worked once but has not reproduced since. **Longest-running automation blocker in the Spot system.**

## Cron Mode: Consecutive Failure Threshold

**After 3+ consecutive Meevo deferrals for the same venue/service/date, skip the browser attempt entirely in cron mode.** Use last_known data directly. The Angular change detection issue is persistent — retrying the browser flow after 3 consecutive failures wastes tokens with near-zero success probability.

- Only re-attempt the browser flow after a different venue succeeds on Meevo (indicating the platform is generally functional) or after a skill/platform update note indicates the issue may be resolved.
- In interactive mode (user present), always attempt regardless of consecutive failure count.
- Track consecutive failure count in the watch record note.

## Success Pattern (2026-05-31) — WORKS (but not reproducible since)

On 2026-05-31 at 14:46 PT, the full Meevo flow completed after 9+ consecutive failures.

1. Click "Massages" category via JS dispatchEvent
2. Click service radio via full JS sequence (click + mousedown + mouseup + checked=true + change + input)
3. Add-on dialog appeared, close via "No, thanks"
4. Cookie consent dialog appeared, dismiss via DOM removal
5. Re-click the service radio with the same full JS sequence
6. Add-on dialog appeared again, close via "No, thanks"
7. Selection persisted — proceed to Next

## Failure Mode Summary

| Sweep | Attempt | Result |
|-------|---------|--------|
| May 31 14:46 | Full JS seq x2 + DOM removal | SUCCESS |
| May 31 22:52 | Deferred (4th consecutive) | Skipped |
| May 31 23:05 | Deferred (5th consecutive) | Skipped |
| May 31 23:45 | Deferred (6th consecutive) | Skipped |
| May 31 21:00 | Deferred (7th consecutive) | Skipped |
| May 31 22:00 | Deferred (8th consecutive) | Skipped |
| Jun 01 02:00 | Deferred (9th consecutive) | Skipped |
| Jun 01 03:30 | Deferred (10th consecutive) | Skipped |
| Jun 01 18:00 | Deferred (11th consecutive) | Skipped |
| Jun 01 21:00 | Deferred (12th consecutive) | Skipped |
| Jun 01 23:45 | Deferred (13th consecutive) | Skipped |
| Jun 02 02:00 | Deferred (17th consecutive) | Skipped |

| Jun 01 12:11 | Deferred (14th consecutive) | Skipped |
| Jun 01 15:35 | Deferred (15th consecutive) | Skipped |
| Jun 01 16:26 | Deferred (16th consecutive) | Skipped |
| Jun 01 17:05 | Deferred (17th consecutive) | Skipped |
| Jun 01 20:26 | Deferred (18th consecutive) | Skipped |
| Jun 01 16:47 | Deferred (19th consecutive) | Skipped |
| Jun 01 17:05 (2) | Deferred (20th consecutive) | Skipped |
| Jun 02 03:30–Jun 04 18:00 | Deferred (21st–38th consecutive) | Skipped (cron threshold) |
| Jun 05 02:00 | Deferred (39th consecutive) | Skipped (cron threshold) |
| Jun 04 11:45 | Deferred (40th consecutive) | Skipped (cron threshold) |

## Workaround Strategy
- Cron mode: After 3+ consecutive deferrals, skip browser attempt. Use last_known data.
- Interactive mode: Always attempt regardless of consecutive failure count.
- Do not burn more than 2 attempts per sweep on service selection.
- Data staleness: If last_known data is >7 days old, flag. If >14 days, escalate to user.

## Last Known Data
Rockridge Day Spa, June 19: 5 openings for Massage (10:00 AM, 1:15 PM, 2:00 PM, 2:30 PM, 3:15 PM) — none in 3:30-5:00 PM window. Confirmed fresh 2026-05-31 14:46 PT. Data age as of 2026-06-04 11:45 PT: ~3.7 days old — within acceptable range but monitor for staleness.