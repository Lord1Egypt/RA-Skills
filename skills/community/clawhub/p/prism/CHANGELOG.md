## v2.0.1 (2026-03-13)

### Fixes
- Removed internal `SKILL-v1.md` archive from published package

## v2.0.0 (2026-03-08)

**"PRISM That Remembers"** — validated through 19 PRISM reviews across 3 rounds (eating our own cooking).

### New Features
- **Memory:** Prior Review Search — reviewers see what previous reviews found
- **Evidence rules:** Mandatory file citations in every finding (inline in each prompt)
- **Devil's Advocate independence:** Structurally blind to prior findings; spawns first
- **New verdict:** NEEDS WORK — between AWC and REJECT
- **Evidence hierarchy:** Tier 1/2/3 ranking (cross-validated > cited > uncited)
- **Actionability requirement:** Shell command or file path required per finding
- **Synthesis upgrade:** New Findings first, conditional history sections, Limitations section
- **Archive protocol:** Searchable review history in `analysis/prism/archive/<slug>/`
- **Governance mode:** `--governance` flag for stuck findings tracking
- **Verification Auditor:** New Extended mode role — verifies claims exist on disk
- **Orchestrator Checklist:** Mechanical step-by-step, no ambiguity
- **Timeout policy:** 10-minute reviewer timeout with partial synthesis
- **Archive safety:** `mkdir -p` + write-failure warning
- **Brief injection delimiters:** `--- BEGIN/END PRIOR FINDINGS ---` for prompt injection protection
- **DA early spawn:** Step 3b spawns DA immediately, saves 25-90s per review

### Breaking Changes
- Synthesis template format changed (new sections, conditional rendering)
- Archive path convention: `analysis/prism/archive/<kebab-slug>/YYYY-MM-DD-review.md`

### Validation
- Round 1: 5 specialists on the plan (4 AWC, 1 NEEDS WORK)
- Round 2: 5 specialists reframed for "just works" UX (2 NEEDS WORK, 2 AWC, 1 AWC upgraded from NW)
- Round 3: 9-agent Extended PRISM on the implementation (3 NEEDS WORK, 1 SIMPLIFY, 4 AWC, 7/7 verification pass)
- All findings applied before release

## v1.0.0

- Initial release: parallel subagent spawning, 5 specialist roles, synthesis protocol
- Severity normalization, cost estimates, model selection
- Two-round audit workflow
