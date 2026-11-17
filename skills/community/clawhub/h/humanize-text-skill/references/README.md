# References

Human-readable rule source. The engine (`detector/`) is the executable truth
for the detectable subset; these files are the full rule set the model applies,
including judgment calls a regex can't make.

Migrated from shuorenhua (Chinese completeness) + avoid-ai-writing (English),
with humanize-text-skill-specific additions (voice-contract, translation-tone).

## File index

| File | Purpose | Source |
|---|---|---|
| `protected-spans.md` | What must never drift (numbers, commands, paths, errors, quotes) | shuorenhua |
| `positive-style.md` | Subtraction targets — what "more human" looks like | shuorenhua |
| `voice-contract.md` | ★ Addition targets — idiolect fingerprint dimensions | humanize-text-skill (new) |
| `skill-architecture.md` | Full skill runtime map: mode → scene → protected spans → detector → rewrite/audit → output | humanize-text-skill |
| `translation-tone.md` | Chinese-specific translationese (zh-only types) | humanize-text-skill (new) |
| `phrases-zh.md` | 210+ Chinese phrases, T1/T2/T3 | shuorenhua |
| `phrases-en.md` | English phrases, T1/T2/T3 | shuorenhua |
| `structures.md` | 19 cross-lingual structural anti-patterns (zh/en side by side) | shuorenhua |
| `scene-packs.md` | README / release-note / forum-post / issue-reply sub-scenes | shuorenhua |
| `scene-guardrails.md` | 4 primary scenes — what not to touch | shuorenhua |
| `severity.md` | Tier definitions + false-positive guardrails | shuorenhua |
| `boundary-cases.md` | False-positive regression cases | shuorenhua |
| `operation-manual.md` | Per-issue micro-operations | shuorenhua |
| `examples.md` | rewrite vs annotation mode before/after | shuorenhua |
| `quick-checklist.md` | Fast pre-delivery checklist + second-pass residue scan | humanize-text-skill |
| `human-rubric.md` | Human review rubric for rewrite quality | humanize-text-skill |
| `voice/` | Preset idiolect profiles (reserved for stage 6) | humanize-text-skill |

## Reading order

1. `SKILL.md` — scene + tier + level + output contract (the main judgment).
2. `skill-architecture.md` — the top-level map of who decides what.
3. `protected-spans.md` — fence off what must not change, first.
4. `positive-style.md` (subtract) + `voice-contract.md` (add) — what to aim for.
5. Per-problem-type: `phrases-{zh,en}.md`, `structures.md`, `translation-tone.md`, `operation-manual.md`.
6. Per-scene limits: `scene-guardrails.md`, `scene-packs.md`.
7. Delivery polish: `quick-checklist.md`, `human-rubric.md`.
8. Calibration: `severity.md`, `boundary-cases.md`, `examples.md`.
