# Position Tracker — Known Limitations

This document outlines the current limitations of Position Tracker and workarounds where available.

---

## 1. API Rate Limits

### Problem
External APIs have rate limits. Frequent reconciliation can trigger throttling.

### Impact
- Reconciliation failures during high-frequency trading/monitoring
- Delayed orphan detection if polling is throttled

### Workarounds
- **Adjust reconcile_interval:** Increase from 300s (5 min) to fit API limits
- **Batch API calls:** If your adapter can fetch all positions in one call, use it
- **Caching:** Implement short-term caching in your adapter (30-60s)

### Future Fix
WebSocket support for real-time updates (no polling needed)

---

## 2. Race Conditions During Reconciliation

### Problem
External state can change between:
1. Fetching positions from API
2. Comparing against local state
3. Taking corrective action

Example: Position closes externally between steps 1 and 3, causing false positive.

### Impact
- Rare false orphan/phantom detection
- Unnecessary cleanup attempts (usually harmless, but creates noise)

### Workarounds
- **Verify before cleanup:** Call `get_all_positions()` again before closing orphans
- **Disable auto-reconcile:** Use `enable_auto_reconcile=False` and review manually
- **Dust threshold:** Set `min_position_value` high enough to ignore churn

### Future Fix
Two-phase commit pattern: detect → verify → act (with retry logic)

---

## 3. Dust Threshold Calibration

### Problem
`min_position_value` is global, but different positions may have different "dust" levels.

Example:
- Crypto: $5 is reasonable (filters rewards, rounding)
- Cloud instances: $5/month might be too low (misses small VMs)
- Stock trading: $5 might be too high (misses fractional shares)

### Impact
- Too low: Noise from sub-dollar positions (rewards, rounding errors)
- Too high: Miss real positions that should be tracked

### Workarounds
- **Calibrate per use case:** Test with real data to find the right threshold
- **Per-position metadata:** Store `min_value` in metadata and filter manually
- **Custom adapter logic:** Implement domain-specific filtering in `get_all_positions()`

### Future Fix
Per-position or per-asset-class dust thresholds

---

## 4. State File Corruption

### Problem
If the process crashes during state save, the state file can be corrupted or incomplete.

### Impact
- Loss of position tracking data
- Need to rebuild state from external API

### Workarounds
- **Atomic writes:** Already implemented (write to `.tmp`, then `os.replace()`)
- **Backups:** Periodically copy `state/positions.json` to versioned backups
- **Reconciliation:** Run `reconcile()` after restart to rebuild from external API

### Current Status
Atomic writes + fsync minimize risk, but not 100% guaranteed on all filesystems.

---

## 5. No Multi-Process Support

### Problem
Position Tracker uses local file-based state. Multiple processes accessing the same state file will conflict.

### Impact
- Cannot run multiple tracker instances in parallel
- Cannot distribute tracking across worker processes

### Workarounds
- **Single process only:** Run one tracker instance per state directory
- **Separate state files:** Use different `state_file` per process (but requires manual reconciliation)
- **Process-level locking:** Implement file locking in your code (not built-in)

### Future Fix
Redis or database backend for distributed state

---

## 6. External API Failures

### Problem
If external API is unreachable, reconciliation fails and orphan detection stops.

### Impact
- Blind to external state during API downtime
- Orphans can accumulate undetected

### Workarounds
- **Retry logic:** Implement retries in your adapter (exponential backoff)
- **Fallback to local state:** Continue tracking based on last known state
- **Alert on API failures:** Use `alert_callback` to notify when API is down

### Current Status
Tracker logs API errors but doesn't retry automatically — add retry logic in your adapter.

---

## 7. No Built-In Logging

### Problem
Position Tracker uses `print()` for logging. Not configurable, no log levels, no rotation.

### Impact
- Limited integration with existing logging frameworks
- No control over verbosity
- Logs mix with stdout

### Workarounds
- **Override `_log()`:** Subclass `PositionTracker` and replace `_log()` with your logger
- **Redirect stdout:** Pipe to log file at OS level

### Example Override
```python
import logging

class MyTracker(PositionTracker):
    def _log(self, message: str):
        logging.info(f"[PositionTracker] {message}")
```

### Future Fix
Configurable logger (pass `logging.Logger` instance)

---

## 8. No Transaction History

### Problem
Position Tracker stores current state only. No historical record of past positions or state changes.

### Impact
- Cannot audit past positions
- Cannot analyze position lifetime or performance
- Cannot replay state changes

### Workarounds
- **Separate history log:** Write position updates to append-only log file
- **Database integration:** Store positions in DB alongside tracker state
- **Snapshot backups:** Periodically save state file with timestamps

### Future Fix
Built-in transaction log (JSONL append-only history)

---

## 9. Memory Usage Scales with Position Count

### Problem
All positions are held in memory. Large position counts (1000+) increase memory footprint.

### Impact
- ~1KB per position → 1000 positions ≈ 1MB memory
- Not a problem for most use cases, but limits scalability

### Workarounds
- **Cleanup aggressively:** Lower `exited_cleanup_seconds` to remove old positions faster
- **Archive old positions:** Move EXITED positions to separate file after N days
- **Database backend:** Store positions in DB, load only active ones

### Future Fix
Lazy loading with database backend

---

## 10. No Built-In Alerting

### Problem
`alert_callback` is basic — just a function call. No retry, no delivery guarantees, no multi-channel support.

### Impact
- Alerts can be lost if callback fails
- Cannot send to multiple channels (Slack + email + Discord)
- No rate limiting on alerts

### Workarounds
- **External alerting service:** Pass alerts to a queue (Redis, SQS, etc.)
- **Retry logic in callback:** Implement retries in your callback function
- **Multi-channel wrapper:** Write a callback that fans out to multiple services

### Future Fix
Built-in alert queue with retry logic and multi-channel support

---

## 11. Timezone Handling

### Problem
Timestamps are stored in ISO format with UTC timezone, but comparison logic doesn't enforce timezone awareness.

### Impact
- Potential issues if external API returns local time instead of UTC
- Cleanup timeouts may be inaccurate if system clock changes

### Workarounds
- **Force UTC in adapter:** Convert all timestamps to UTC in `get_all_positions()`
- **Use epoch time:** Store `time.time()` instead of ISO strings for comparisons

### Current Status
Uses `datetime.now(timezone.utc)` for new entries, but doesn't validate loaded state.

---

## 12. No Web UI

### Problem
Position Tracker is code-only. No dashboard, no visualization, no GUI.

### Impact
- Must read state file or logs to see current positions
- No real-time monitoring view
- Not accessible to non-technical users

### Workarounds
- **Custom dashboard:** Build web UI that reads `state/positions.json`
- **CLI tool:** Write a simple CLI to query tracker state
- **Log parsing:** Parse logs for monitoring

### Future Fix
Built-in web dashboard (Flask/FastAPI)

---

## 13. Performance with Large Position Counts

### Problem
`reconcile()` is O(N) where N = position count. Slow for 10,000+ positions.

### Impact
- Reconciliation takes >1 second for very large portfolios
- Blocks main thread during reconciliation

### Workarounds
- **Run reconciliation in background:** Use threading or async
- **Partition positions:** Run multiple trackers with different subsets
- **Database queries:** Use indexed database instead of in-memory dict

### Current Status
Not optimized for >1000 positions.

---

## 14. No Support for Partial Positions

### Problem
Tracker assumes positions are all-or-nothing (ENTER → EXIT). No support for partial closes.

Example: Enter 100 shares, exit 50 shares, still holding 50.

### Impact
- Cannot track partial exits accurately
- Workaround requires creating separate position IDs for each lot

### Workarounds
- **Lot-based tracking:** Create one position per lot (e.g., `AAPL-lot1`, `AAPL-lot2`)
- **Metadata tracking:** Store `remaining_quantity` in metadata, update manually
- **Custom state machine:** Add `PARTIAL_EXIT` state in your code

### Future Fix
Built-in support for quantity tracking and partial exits

---

## Summary Table

| Limitation | Severity | Workaround Available? | Planned Fix |
|------------|----------|----------------------|-------------|
| API rate limits | Medium | Yes (adjust interval) | WebSocket support |
| Race conditions | Low | Yes (verify before act) | Two-phase commit |
| Dust threshold | Low | Yes (calibrate) | Per-position thresholds |
| State corruption | Low | Yes (atomic writes) | Already mitigated |
| Multi-process | Medium | No (single process only) | Redis backend |
| API failures | Medium | Yes (retry in adapter) | Built-in retry logic |
| No logging | Low | Yes (override `_log()`) | Configurable logger |
| No history | Medium | Yes (separate log) | Transaction log |
| Memory scaling | Low | Yes (cleanup) | Database backend |
| No alerting | Medium | Yes (external service) | Alert queue |
| Timezone | Low | Yes (force UTC) | Timezone validation |
| No web UI | Low | Yes (custom dashboard) | Built-in dashboard |
| Performance | Low | Yes (partition) | Optimize for 10K+ |
| Partial exits | Medium | Yes (lot-based) | Quantity tracking |

---

## Contributing Fixes

If you have solutions to any of these limitations, we'd love to hear from you!

- 🐛 **Report issues:** GitHub issues
- 💡 **Suggest improvements:** Discord or Twitter
- 🔧 **Submit PRs:** We review everything

---

## Philosophy

Position Tracker is **production-ready for most use cases**, but not perfect. We document limitations honestly so you can make informed decisions.

**Use it if:**
- You need reliable position tracking with self-healing
- You can work within the limitations (or implement workarounds)
- You value simplicity over feature completeness

**Don't use it if:**
- You need real-time WebSocket updates (use native exchange SDKs)
- You need multi-process distributed state (use Redis/database)
- You need sub-second reconciliation for 10,000+ positions

---

**Questions? Found a limitation we missed?**

💬 Discord: https://discord.com/invite/clawd  
🐦 Twitter: https://x.com/TheShadowyRose
