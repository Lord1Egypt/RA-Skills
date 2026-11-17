# Memory Template — ~/Clawic/data/learning/memory.md

Copy this structure on first write. Keep entries compact — keywords and dates, not prose.

```markdown
# Learner Profile

confirmed:            # explicit statement, or 2+ consistent signals (SKILL.md Rule 8)
- code-first examples (declared)
- avoid extended metaphors (re-asked 2x)

hypotheses:           # 1 signal — test deliberately at the next opportunity
- diagrams for architecture topics (1x, 2026-07-12)

context_qualifiers:   # preferences that hold only in a context
- urgent: answer first, teach after
- new languages: SRS handoff for vocab

# Topic: sql

level: intermediate          # from the Diagnostic Probes grid
horizon: exam 2026-09-15     # or "open"
live:                        # concept — last correct recall — spaced successes toward retirement
- joins — 2026-07-20 — 2/3
- indexes — 2026-07-20 — 1/3
queued_misses:               # the next session opens with these
- why a covering index avoids the table lookup
- misconception re-test: NULL = 0 (surfaced 2026-07-20, new surface needed)
retired:                     # correct recall in 3 separate sessions (retention.md)
- SELECT basics — 2026-07-18
```

## Rules

- One `# Topic:` block per topic. The block is the session opener's source (SKILL.md Session Structure) and the progress evidence used for motivation (`learner-states.md`).
- Spaced successes count only recalls in separate sessions — never same-session repeats; `2/3` means two sessions down, one to go against the retirement criterion in `retention.md`.
- Misconception re-tests are queued like misses, tagged with the date surfaced and a note that the check needs a new surface (`misconceptions.md`).
- Preferences follow the config/memory split: declared → `config.yaml`; observed → this file. An observation never overwrites a declaration without the user confirming.
- Prune: drop a hypothesis that goes 5+ sessions without a second signal (stale hypotheses are noise); move topics untouched for months to an `# Archived` section instead of deleting — returning learners keep their history.
