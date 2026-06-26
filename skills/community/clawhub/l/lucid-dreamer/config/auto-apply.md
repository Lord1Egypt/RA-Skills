# Auto-Apply Configuration

This file defines which categories Lucid is allowed to auto-apply without human review.

Only changes with **HIGH confidence** are ever auto-applied — regardless of category.
Medium and low confidence always require human approval.

When sectioned memory is enabled, Lucid should apply safe edits directly to the relevant `memory/sections/*.md` file(s) and then update the matching `Last Updated` value in `memory/index.md`.
If `memory/sections/` does not exist yet, fall back to editing `MEMORY.md`.

## ✅ Enabled Categories

Edit this list to match your project's needs.

### Safe (factual, no opinions)
- **Version numbers** — skill/plugin tables clearly outdated
- **Stale Cron IDs** — cron was explicitly removed/replaced in notes
- **Service/port deletions** — clearly documented as removed
- **New project entries** — complete details (URL, repo, path, service) mentioned on 2+ days
- **Infrastructure facts** — new cron IDs, script paths, service names, port assignments
- **Lessons Learned** — purely factual technical lessons (not preferences or opinions)
- **Model Strategy** — agent counts, new agent entries when clearly documented with model + alias
- **Closed Open Loops** — remove resolved items when explicit closure signal exists on 2+ days
- **Stale project status** — update "planning"/"in progress" to "live" when URL + service confirmed on 2+ days
- **Factual contradictions** — objective memory-vs-note conflicts where newer daily note evidence clearly supersedes the old value and is safe to auto-apply

## ❌ Never Auto-Apply (hardcoded)

These are always manual regardless of confidence:

- Belief Updates (opinions, model preferences, strategy changes)
- Key Decisions
- Family/personal facts
- User preferences or communication style
- Judgment contradictions
- Anything you are uncertain about
- Anything with medium or low confidence

## 🗑️ Aggressive Cleanup (opt-in)

When `aggressiveCleanup.enabled` is `true` in `lucid.config.json`, Lucid will also **remove** entries from long-term memory that meet ALL of these criteria:

- The item is an Open Loop, Blocker, or factual entry
- Daily notes from the last 7 days contain **explicit closure signal** (e.g., "done", "fixed", "deployed", "removed", "cancelled", "no longer needed")
- The closure signal appears on **2+ separate days** OR is unambiguously final (e.g., "project deleted", "service decommissioned")
- Confidence is HIGH

**What gets removed:**
- Open Loops with confirmed resolution
- Blockers that are no longer blocking (fix deployed, workaround in place)
- Infrastructure entries for removed services/ports/crons
- Project entries for abandoned/deleted projects (only if explicitly stated)

**What NEVER gets removed (even with aggressive cleanup on):**
- Key Decisions (historical record)
- Belief Updates (trajectory matters)
- Family/personal facts
- Lessons Learned (knowledge is permanent)
- Active projects (even if not mentioned recently)

**Rollback:** Every removal is a separate git commit. Use `git revert <hash>` to restore any removed entry.

## Target Files

When a safe change is accepted, prefer these targets:
- `memory/sections/identity.md`
- `memory/sections/operations.md`
- `memory/sections/projects.md`
- `memory/sections/infrastructure.md`
- `memory/sections/skills.md`
- `memory/sections/decisions.md`
- `memory/sections/lessons.md`
- `memory/sections/models.md`
- `memory/index.md` (timestamp updates only)

Fallback target when sectioned memory is unavailable:
- `MEMORY.md`

## Customization Examples

**Minimal setup** (only version numbers + new projects):
Remove all categories except "Version numbers" and "New project entries".

**Aggressive setup** (trust the AI more):
Add "Open Loops closure", "Stale project status", and "Factual contradictions" — but watch for false positives.

**Conservative setup** (human reviews everything):
Remove all categories. Lucid will still generate suggestions but never apply them.
