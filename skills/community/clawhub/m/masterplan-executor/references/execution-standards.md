# Execution Standards — verify by doing, not by reading the code back

This mirrors masterplan-builder's production-readiness bar, but every item here is phrased as something to actually verify during execution, not just something to have written. "Looks right" is not the bar; "checked and confirmed" is.

## Universal — check every phase against these before moving on

- **No hardcoded secrets/config** — grep the diff for literals that look like keys, tokens, URLs, or credentials before closing out the phase. Confirm they're sourced from environment variables/secrets manager instead.
- **Real error handling** — for every external call added this phase (network, DB, filesystem, third-party API), actually trigger the failure path (kill the connection, pass invalid input, hit a timeout) and confirm the specified behavior actually happens, not just that the code compiles.
- **Input validation on every boundary** — actually send invalid/boundary input (empty, too long, wrong type, malicious) to anything that accepts external input this phase, and confirm it's rejected the way the plan specifies, not silently accepted or crashing.
- **No debug/dev-only artifacts** — grep for leftover debug prints/console logs, TODO/FIXME markers left in shipped code, mock data reachable from production paths, or auth bypasses before closing the phase.
- **No dead code** — check for unused functions/imports/variables (via linter or manual check), unreachable branches, commented-out blocks, and permanently-off feature flags. If this phase supersedes something from an earlier phase, confirm the superseded code was actually deleted, not left alongside the new version.
- **No silent failures** — check every catch/error-handling path added this phase: does it log/alert/return a real error, or does it swallow the problem? Check every fallback path (retry exhausted, cache miss, degraded mode): is it observable (logged/metriced), or does it look identical to success?
- **Logging is structured and useful** — spot-check that a log line from this phase would actually help debug an incident, without leaking secrets or full PII.
- **AuthN/authZ enforced per resource** — actually attempt an unauthorized action against anything gated this phase and confirm it's rejected.
- **Rate limiting/abuse protection** present on any publicly reachable endpoint added this phase.
- **Dependencies are current** — any new dependency added this phase has its version confirmed current/maintained via research (see SKILL.md Phase 2 step 2), not just pinned to whatever installed by default.
- **Tests actually run and pass** — the test suite (or the relevant subset) is executed, not just written, before the phase is marked done.
- **Docs updated** — README/setup docs/API reference updated to reflect what this phase actually added, if the masterplan named documentation as a deliverable.

## Version control discipline

- Commit at natural phase boundaries with messages that map to the roadmap phase, so the history itself is a traceable record of execution — not one giant undifferentiated commit at the end.
- Never commit a known Blocker/Major gap "to fix in the next commit" — the self-audit in SKILL.md Phase 2 step 5 happens before the commit that closes out the phase, not after.

## Category-specific execution checks

- **Website/Web App**: actually load the page/flow this phase touches, check responsive behavior at real breakpoints, confirm HTTPS/cookie/CSRF/CSP settings are actually in effect, not just configured.
- **Mobile App**: actually run on at least the range of screen sizes/OS versions the plan's support matrix names, or confirm via the platform's official device simulators — don't assume one test device represents the matrix.
- **Local AI Assistant/Agent**: actually verify resource usage (RAM/VRAM) against the plan's stated hardware floor, not just against the dev machine; actually test the degraded/fallback path when resources are constrained, not just the best-case path.
- **Desktop App**: actually test OS-specific behavior (paths, packaging, notifications) on each target OS named in the plan, or via each platform's own toolchain — don't assume parity untested.
- **Backend/API**: actually load-test or at minimum sanity-check behavior under concurrent requests for anything the plan flagged as scale-sensitive; confirm health-check endpoints actually respond correctly.
- **Browser Extension**: actually load the extension unpacked and test against a real page matching the manifest's host permissions; confirm no broader permission is requested than what's actually used.
- **CLI Tool**: actually run it non-interactively/piped as well as interactively; confirm exit codes are correct for both success and failure paths.

## Environment adaptability — verify, don't assume

For anything the masterplan's Adaptive System Design section calls out: actually simulate at least one degraded condition per dimension that applies (throttle network, cap memory/CPU, use a small screen size, force offline) and confirm the stated fallback behavior actually triggers — not just that the best-case path works. A feature that was only ever run under ideal conditions has not actually been verified as adaptive.

## When a check fails

A failed check here mid-phase is a Blocker or Major finding exactly as it would be in masterplan-builder's own review process — fix it in this phase, don't note it and move on. If fixing it requires a decision the masterplan didn't anticipate, that's a plan gap — handle it per SKILL.md Phase 3 (research the correct approach, implement it, log the deviation).
