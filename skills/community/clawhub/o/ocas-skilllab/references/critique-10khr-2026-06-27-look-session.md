# 10khr Session — June 27, 2026 (Look)

## Target: ocas-look (heuristic 46/50 → manual 40/50 → 50/50)

### Dimensions Fixed
- **D1 (4→5):** Added `metadata.hermes.category: ocas-look`, moved `tags` from top-level frontmatter into `metadata.hermes.tags` (was incorrectly placed outside the hermes block)
- **D3 (4→5):** Removed 7-line redundant "What this skill does not do" section (duplicated "When NOT to Use" bullets). Skill improved from 241 to 235 lines.
- **D5 (4→5):** Added `- [ ]` checkbox checklists to the 10-step workflow, added concrete I/O examples (event flyer → calendar draft, meal photo → health_macros draft), added 4-item validation step before execution
- **D6 (3→5):** Added "why" explanations for all 3 risk tiers and confirmation-token requirement. Added rationale paragraph to No-Hallucination Policy explaining downstream error propagation.
- **D7 (4→5):** Added pre-execution validation step (4 concrete checks: non-empty fields, risk tier, confirmation token, evidence refs)
- **D9 (2→5):** Rewrote `update.sh` from 5-line bare script to 50-line agentic script with `--help`, `--check` mode, `set -euo pipefail`, git/repo existence checks, structured update messages, meaningful error messages to stderr
- **D10 (4→5):** Metadata fixes (D1) resolved the last spec-coverage gap. All description capabilities now have corresponding reference files.

### Already-Perfect Dimensions
D2 (5), D4 (5), D8 (5), D9 was N/A in some dimensions but the script now exists in improved form.

### Score impact
| Dim | Before | After | Delta |
|-----|--------|-------|-------|
| D1 | 4 | 5 | +1 |
| D3 | 4 | 5 | +1 |
| D5 | 4 | 5 | +1 |
| D6 | 3 | 5 | +2 |
| D7 | 4 | 5 | +1 |
| D9 | 2 | 5 | +3 |
| D10 | 4 | 5 | +1 |
| **Total** | **40** | **50** | **+10** |

### Key Observations
- **Heuristic over-scored by 6 points** (reported 46, actual 40) — the largest gap in recent sessions. The heuristic was fooled by:
  - "error handling" phrase in a pointer sentence ("See workflow.md for error handling table") without detecting that the SKILL.md body itself had no table
  - "why" not present in the SKILL.md body — the heuristic only checks the SKILL.md file, not reference files
- **D9=2 was the worst script score in recent memory** — `update.sh` was 5 lines with `2>/dev/null` on every line (silent failures), no `--help`, no validation. This is the most common failure mode for git-backed skills.
- **The D6 fix was entirely in a reference file** (decision_policy.md), not the SKILL.md body. This confirms that manual assessment must read ALL reference files, not just SKILL.md.

### Key learning: `--check` mode for update/version scripts
For version-update scripts (self-update), a valuable sub-pattern is `--check` mode:
```bash
if [ "${1:-}" = "--check" ]; then
  # Only check for updates, don't apply
  LOCAL=$(git rev-parse HEAD)
  REMOTE=$(git rev-parse origin/main)
  if [ "$LOCAL" = "$REMOTE" ]; then exit 0; fi
  echo "Update available: ${LOCAL:0:8} → ${REMOTE:0:8}"
  exit 1  # signal update available
fi
```
This enables agent probing ("is there an update?") without side effects.

### Key learning: `tags:` at top-level vs `metadata.hermes.tags`
Some older skills place `tags:` at top-level frontmatter instead of under `metadata.hermes.tags`. The heuristic runner does NOT penalize this (since it checks for `tags` presence, not location). But D1=5 requires the tags under `metadata.hermes` for proper Hermes grouping. Heuristic misses this — always check `metadata.hermes.tags` specifically.

### Next target
Re-run `critique_10khr_runner.py --report-only` to re-rank. Expected next targets: ocas-usercontext, ocas-10xeng-audit, ocas-10xeng-review, util-buy (all at heuristic 46/50).