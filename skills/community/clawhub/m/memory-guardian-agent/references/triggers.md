# triggers.md — Trigger/Anti-Trigger Checklist + Version Change Conditions

> Acceleration-layer reference for Agent readers. Consult on demand; no need to read the full document.

---

## Scenario → Tool Mapping

### Scenario 1: Fresh Installation
- **Signal**: First configuration / MCP server startup / references/ detection
- **Action chain**:
  1. `memory_status()` — Confirm system is healthy
  2. Check references/ integrity (6 files; `memory_status()` returns `references.complete: false` if any file is missing)
  3. `memory_sync(dry_run=true)` — First sync of files to meta.json
  4. Set cron: `run_batch(skip_compact=true, apply=true)` every 3h

### Scenario 2: Routine Maintenance
- **Signal**: cron trigger / heartbeat check
- **Action**: cron calls `run_batch(skip_compact=true)` (automatically includes sync → decay → gate), Agent occasionally calls `memory_status()` to glance at the system
- **Principle**: System handles automatically, Agent intervention not needed

### Scenario 3: Issues Detected → Diagnostic Path

**D1 Memory Bloat:**
- Trigger: `memory_status()` returns `memory_md_kb > 15`
- Action: `memory_compact(dry_run=true)` → confirm → `memory_compact()`

**D2 Quality Anomaly:**
- Trigger: `quality_check()` returns `state != NORMAL`
- WARNING → observe violations
- CRITICAL → `quality_check(layer="L2")` to locate the issue
- CRITICAL persists for 3 rounds (~90min) → auto human-review → L3 queue
- Check `retire_rate > 0.3` → `rule_review_suggested`
- Check `similar_case_signal.all_retired` → system-level audit

**D3 Case Invalidation:**
- Trigger: `case_query(filter="frozen")` or `filter="stale"` returns results
- Action: Check confidence trend → `case_review(action="active"|"retire"|"unfreeze"|"ignore")`
- Check `similar_case_signal` → single anomaly vs. systemic issue

---

## Anti-Trigger Checklist (What NOT to Do)

- ❌ Do NOT manually force-normal in WARNING state (let the system self-heal)
- ❌ Do NOT skip CRITICAL and directly perform memory writes (follow the L3 confirmation flow)
- ❌ Do NOT execute archive/delete on memories in observing state
- ❌ Do NOT enable compact in cron (use `skip_compact=true`)
- ❌ Do NOT modify status of memories with pinned=true
- ❌ Do NOT call `memory_decay()` multiple times in the same session
- ❌ Do NOT repeatedly remind about cases with `ignore_at != null`
- ❌ Do NOT expose MEMORY.md content in group chats

---

## Version Change Trigger Conditions

### v0.4 → v0.4.1
- Gate state migration: `mode` → `state` (2-state → 4-state)
- Auto-migration: auto-converts when old fields detected, marks `migrated_from_v04: true`

### v0.4.1 → v0.4.2
- New anomaly_mode tri-state (normal_decay / anomaly / error_recovery)
- New L2 write queue + L1 pending audit
- New per-type decay parameters (static/derive/absorb)
- New quiet degradation (IQR adaptive)
- New stale_watchdog + similar_case_signal
- No auto-migration: new fields use `.setdefault()` for backward compatibility with old meta.json

### v0.4.3 → v0.4.4
- New `memory_sync` MCP tool (10th tool)
- `run_batch` maintenance flow changed to: sync → decay → compact → gate
- New `last_sync_at` field to record sync time
- 30-minute cooldown mechanism to prevent duplicate syncs
- No auto-migration: new fields use `.setdefault()` for backward compatibility with old meta.json

### Detection Commands
```python
# Check schema version
meta.get("schema_version", "v0.4")  # Expected "v0.4.2"
# Check if gate state has been migrated
meta.get("quality_gate_state", {}).get("migrated_from_v04", False)
# Check anomaly mode
meta.get("anomaly_mode", "normal_decay")
```

---

## Code References

- Tool → script mapping: `mcp_server.py` §Tool-to-Script Mapping
- Trigger logic: `quality_gate.py` → `transition_state()`, `compute_intervention_level()`
- Case triggers: `case_invalidate.py` → `check_invalidations()`
- File sync: `memory_sync.py` → `run()`
- Cron entry point: `mcp_server.py` → `handle_run_batch()` / `cli_batch()`
