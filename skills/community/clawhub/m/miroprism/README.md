# MiroPRISM — Adversarial Two-Round Review Protocol

> A finding that survives explicit challenge is more reliable than one that was never challenged.

MiroPRISM is a standalone fork of [PRISM](https://github.com/jeremyknows/PRISM) that adds a mandatory second debate round. Where PRISM runs reviewers in isolation and merges at the end, MiroPRISM broadcasts a sanitized digest of all R1 findings and requires every reviewer to respond with AGREE, DISAGREE, or UNCERTAIN — with independent evidence required for each stance.

**The problem it solves:** PRISM reviewers converge toward consensus without genuine disagreement. The first voice anchors everything. MiroPRISM breaks that pattern by forcing explicit engagement with opposing findings before synthesis.

## What it does

- **R1** — 5 specialist reviewers run in complete isolation (identical to PRISM)
- **Phase 2** — Orchestrator sanitizes all R1 findings (strips code, URLs, JSON; enforces structured templates to block prompt injection) and broadcasts a randomized digest
- **R2** — Every reviewer responds to every finding: AGREE (cite evidence), DISAGREE (cite contradiction), or UNCERTAIN (state what would resolve it)
- **Synthesis** — Findings labeled `[HIGH]` (challenged + survived), `[STANDARD: VALIDATION REQUIRED]` (unchallenged), or `[FLAGGED]` (drift, unvalidated citation). Unresolved Disagreements surfaced as the primary output.

## Install

**Claude Code / OpenClaw:**
```bash
git clone https://github.com/jeremyknows/MiroPRISM ~/.openclaw/skills/miroprism
# or SSH:
git clone git@github.com:jeremyknows/MiroPRISM.git ~/.openclaw/skills/miroprism
```

**Cursor / Windsurf / other:**
```bash
git clone https://github.com/jeremyknows/MiroPRISM /path/to/your/skills/miroprism
```

Then restart your agent or reload skills.

## Quick Start

1. **Have your artifact ready** — design doc, PR, architecture decision, code file, or any text you need reviewed
2. Say: `"MiroPRISM this"` and provide the artifact inline or as a file path
3. Wait ~20 min (Standard) or ~5 min (Budget)
4. Read synthesis at `analysis/miroprism/archive/<slug>/YYYY-MM-DD-review-1.md`

**Reading the output:**
- **`[HIGH]`** findings — challenged by another reviewer and survived. Act on these.
- **`[STANDARD: VALIDATION REQUIRED]`** — not challenged. May be correct, but not confirmed under adversarial conditions. Verify independently.
- **Unresolved Disagreements** — genuine expert split on the same evidence. Use these for your final call.
- **Final Verdict** — APPROVE / APPROVE WITH CONDITIONS / NEEDS WORK / REJECT

That's it. MiroPRISM handles the rest.

## Usage

```
"MiroPRISM this"                              → Standard (5 reviewers, 2 rounds, Sonnet ~$0.70)
"Budget MiroPRISM"                            → 3 reviewers, 2 rounds, Haiku (~$0.08)
"Budget MiroPRISM with Performance"           → Security + DA + Performance
"MiroPRISM this, max 3 rounds"                → Auto-triggers R3 if R2 delta >20%
"MiroPRISM this, review digest log before R2" → Pause for manual digest approval
```

## When to use MiroPRISM vs PRISM

| Situation | Use |
|-----------|-----|
| Architecture decisions, major forks, things living 6+ months | MiroPRISM |
| Security-sensitive changes, open source releases | MiroPRISM |
| High-stakes decisions where consensus drift is a real risk | MiroPRISM |
| Bug fixes, minor refactors, reversible decisions | PRISM |
| Fast checks, urgent reviews | PRISM (or Budget PRISM) |

## Variants & Cost

> Pricing current as of 2026-03-15 (Claude Sonnet 4.6 / Haiku 3.5, Anthropic rates).

| Variant | Reviewers | Rounds | Model | Tokens | Est. Cost |
|---------|-----------|--------|-------|--------|-----------|
| Standard | 5 | 2 | Sonnet | ~120K | ~$0.65–1.00 |
| Standard + large artifact (>5K tokens) | 5 | 2 | Sonnet | ~150K+ | ~$1.00–1.50 |
| Budget | 3 | 2 | Haiku | ~40K | ~$0.08 |
| Extended | 5 | 2–3 | Sonnet | ~170K | ~$1.10–1.60 |

Token breakdown (Standard, small artifact): R1×5 ~35K · Phase 2 ~500 · R2×5 ~42.5K · Synthesis ~20–22K

**Large artifact:** R2 sends the original artifact to every reviewer. If >5K tokens (~20KB), multiply R2 cost by reviewer count.

## File structure

```
analysis/miroprism/
  runs/<slug>/
    .lock               # concurrent run guard
    r1-outputs/         # blind R1 reviewer outputs
    R1-digest-log.md    # transparency log (SHA256, sanitization counts)
    r1-digest.md        # sanitized, randomized digest sent to R2
    r2-outputs/         # R2 response outputs
  archive/<slug>/
    YYYY-MM-DD-review-N.md   # final synthesis
```

## Security

MiroPRISM's digest pipeline sanitizes R1 findings before broadcast:
- Strips all code blocks, URLs, JSON, and structured data
- Enforces a structured finding template with allowlisted `FINDING_TYPE` values — no freeform narrative
- Randomizes finding order to remove implicit vote-count signal
- Strips all reviewer identity signals

The transparency log (`R1-digest-log.md`) records SHA256 of every R1 input and sanitization counts for post-hoc verification.

## Limitations

- Requires an agent capable of spawning 5+ parallel subagents
- R2 token cost is ~2.5–3x PRISM — not appropriate for quick checks
- Reviewer count (5) is a starting point, not a validated optimum — see [Post-Launch Metrics](references/post-launch-metrics.md) after 10 runs
- Extended mode (3 rounds) adds cost; only use when R2 delta is high
- Reduces cascade sycophancy — does not eliminate it; the shared digest can still anchor R2 reviewers

## Relationship to PRISM

MiroPRISM is a **standalone fork**, not a PRISM extension. The execution model (feedback loop) is fundamentally different. R1 reviewer prompts are identical to PRISM; everything else is new. Do not try to bolt MiroPRISM's R2 onto an existing PRISM run.

## License

MIT — see [LICENSE.txt](LICENSE.txt)
