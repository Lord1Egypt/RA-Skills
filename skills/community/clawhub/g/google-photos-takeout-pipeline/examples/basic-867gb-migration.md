# Example: 867 GB library, 18 parts, real-world run (Aug 2026)

Starting point: Takeout export finished (867.3 GB in 18 x 50 GB zips),
Chromium browser (Comet) running with --remote-debugging-port=9222,
Google session established by one manual login.

## Timeline (real run)

| Time | Step |
|---|---|
| 11:19 | First browser download started manually to discover the final URL |
| 11:24 | URL ripped from chrome://downloads → pattern recognized → all URLs constructed |
| 11:26 | aria2c resume of part 1 (24.6 GB migrated from browser download, 0 bytes lost) |
| 12:05 | FULL cookie jar via Storage.getCookies (317 cookies) → first CLI download success (HTTP 206, PK magic) |
| 12:33 | Runner v2 with per-part cookie refresh live (earlier static-jar run had produced 17 x 1.2 MB HTML files) |
| 13:18 | Part 1 complete (53.7 GB real ZIP), unpack watchdog already extracting |
| +2.7h/part | Parts 2-18 at 5 MB/s soft throttle, self-healing Comet relaunches |

## Failure modes actually hit during this run

1. 17 HTML garbage zips from a stale jar (→ per-part refresh + PK check)
2. Comet closed by user mid-run (→ runner relaunches browser automatically)
3. Chromium ate 3.8 GB of .crdownload bytes on cancel (→ rename before cancel rule)
4. Time Machine started and threatened the SSD mount during download (→ stopbackup watchdog)

## Final verification

- Part 1: 53,699,761,942 bytes, PK magic, unzip -t clean
- Throttle test: SIGSTOP → 0 bytes in 15 s window, SIGCONT → instant 4 MB/s+
- Cookie freshness: 331-346 cookies harvested per refresh, rotation observed ~every 15-30 min
