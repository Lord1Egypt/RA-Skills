# Heartbeat Integration (Optional)

This is an **opt-in** extension that integrates wiki linting into your agent's heartbeat cycle. It requires access to workspace files outside `~/wiki/` — specifically `heartbeat-state.json` (for timing) and `memory/` daily notes (to detect wiki gaps).

## Setup

Add this to your `HEARTBEAT.md`:

```markdown
## Wiki Lint (daily)

1. Check `lastWikiLint` in heartbeat-state.json
2. If >24h: scan `~/wiki/docs/` articles for:
   - Contradictions — facts/numbers/claims that conflict across articles
   - Stale data — outdated references, old dates with "current"/"latest" language
   - Missing links — references to topics without articles
   - Gaps — topics discussed in recent memory/ daily notes but not in wiki
   - Dead cross-links — broken See also links
   - Orphan pages — pages with no inbound links
   - Weak pages — articles too thin to be useful on their own
3. Fix within ~/wiki/docs/: broken links, typos, missing cross-links, orphan pages
4. Flag to user: contradictions (with quotes), stale data, suggested new articles, weak pages
5. Append a lint entry to `docs/log.md`
6. If changes made: run `scripts/build.sh`
7. Update timestamp
```

Add `"lastWikiLint": null` to your `heartbeat-state.json`.

## Notes

- The **gap detection** step (checking `memory/` daily notes) is the only part that reads files outside `~/wiki/`. Remove that line if you want the lint fully scoped to the wiki directory.
- All fixes are written only to `~/wiki/docs/`.
- `build.sh` commits locally by default. Add `--push` if you want automatic remote pushes.
