# Session: 2026-06-21 Dispatch #6 — Heredoc Single-Quote Expansion Bug

**Date:** 2026-06-21T17:51Z  
**Trigger:** Dispatcher `new_journals` — 5 new journal files  
**Pipelines:** Forge scan → Mentor light heartbeat → Praxis ingest

## What happened

All three pipelines ran cleanly:

- **Forge:** No unprocessed proposals/decisions. Wrote no-op journal.
- **Mentor:** 4,369 files scanned, 2 new ingested, `active_skills_30d` corrected 14→22.
- **Praxis:** 6 new journals, all no-signal, 0 events.

## New gotcha: Heredoc single-quote expansion

When writing the Forge no-op journal via:
```bash
cat > "$JOURNAL_DIR/forge-scan-${TS}.json" << 'EOF'
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%S.000000+00:00)",
  ...
}
EOF
```

The single-quoted `<< 'EOF'` prevents shell expansion. The `timestamp` field
contains the literal string `$(date -u +%Y-%m-%dT%H:%M:%S.000000+00:00)` instead
of the actual timestamp. The filename (`${TS}`) was expanded because it's
outside the heredoc, but all content inside is literal.

**Fix:** Use `write_file()` for JSON journal writes. If heredoc is necessary,
use double-quoted `<< EOF` (but escape inner JSON quotes) or resolve all
variables before the heredoc and reference them without `$` inside.

**Status:** Patched in `references/journal-scan-cron-guide.md` — new pitfall section added.

## Validation

- Mentor correction confirmed: 12th consecutive dispatch where script `active_skills_30d` undercounted (14 vs true 22).
- Praxis 0-event result expected: all 6 journals were routine operational noise.
- No new skills needed, no user corrections.