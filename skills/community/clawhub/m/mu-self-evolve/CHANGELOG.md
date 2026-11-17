# Changelog

All notable changes to this project will be documented in this file.

## [3.1.0] - 2026-09-09

### What's New

- 🔗 **Broken-loop protection** — real-world deployment revealed the #1 silent failure: daily cron ran on time but the diary (the sole data source of the whole pipeline) was often missing, so the system "punctually recorded that it did nothing". v3.1 closes the loop at both ends.
- ⚡ **In-session instant sedimentation (IRON LAW #4)** — the moment a trigger signal is detected in conversation (correction, tool failure, feature request, positive feedback, key decision), a one-line timestamped entry is written to the daily diary **immediately**, not batched at session end. The diary is the only input of the daily 6-step workflow — missing it means the evolution loop runs empty.
- 🛟 **Diary backfill on cron (fallback)** — when today's diary doesn't exist, the daily cron no longer skips straight to the summary. It first rebuilds the diary from real traces of the day: cron/automation run logs, same-day entries in long-term memory, and same-day workspace file changes (git status / ls -lt). Strictly no fabrication (IRON LAW #1); skip is only allowed when all three sources are empty.
- ➡️ **Explicit data-flow direction** — trigger signals → daily diary → daily 6-step classification into ledgers. Writing directly into LEARNINGS/ERRORS during a session, bypassing the diary, is now forbidden.

### Upgrade Notes

- No breaking changes. Existing diaries, ledgers, and archive keep working as-is.
- If you already have a daily cron, update its message to the new one in SKILL.md ("定时运转" section) so the backfill fallback takes effect.

## [3.0.0] - 2026-07-21

### What's New

- ✨ VFM deterministic verification — `vfm_verify.py` script validates experience rules with recurrence count, cross-task scope, resolution rate, and pathology concentration before promotion to permanent memory
- ✨ Score + decay eviction — `eviction_score.py` replaces line-count hard truncation with `effective_score = VFM × 0.5^(age/30)` formula (30-day half-life, inspired by CrewAI)
- ✨ WHERE×WHY pathology keys — every error entry tagged with structured WHERE (error stage, 10 tags) and WHY (root cause, 11 tags), both user-customizable
- ✨ Bias audit — `bias_audit.py` uses defect injection testing to verify the eviction mechanism handles entries correctly
- ✨ Active Skill synthesis — when ≥3 entries cluster in the same domain, automatically generates a Skill draft (skeleton + script framework)
- ✨ Conflict resolution on entry — contradict→overwrite, supplement→merge, unrelated→new
- ✨ Environment auto-detection — `env_detect.py` auto-detects OpenClaw, Claude Code, or other environments
- ✨ Bilingual README (English + Chinese) with golden structure
- ✨ Landing Page with warm-paper design, bilingual support

### Full Changelog

Initial public release. See [README.md](README.md) for full feature list.
