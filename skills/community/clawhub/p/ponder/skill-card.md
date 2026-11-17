## Description:

Convergent multi-pass deliberation and code review ledger that enumerates units, grades every unit against a lens rubric, runs four-perspective deliberation (Skeptic, Builder, Dreamer, Empath), records append-only finding deltas, verifies phantom-unit removals across all historical paths, and enforces 1.00 coverage and zero-churn convergence before stopping. Use when the user says "ponder <anything>" ("ponder the UI", "ponder our error handling", "ponder this PR"), "run a ponder audit", "grade every unit with the ponder ledger", "run four-voice Skeptic/Builder/Dreamer/Empath deliberation", or asks for a coverage-gated multi-pass lens audit across files or screens where stopping early would miss units. Also use to resume or recover a ponder session in flight - "where were we in the ponder", "carry on pondering", or an existing .ponder/ directory - by running ponder status rather than starting over.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quinnod345](https://clawhub.ai/user/quinnod345)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use Ponder to run a multi-pass audit of code, interfaces, files, or other scoped material, capture and revise findings, and determine when coverage and findings have converged. It can also resume an existing audit session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit discussions may be stored and recalled through an optional database without clearly documented project boundaries.

Mitigation: For private projects, set PONDER_OCA=off. Before enabling database memory, check its destination, project separation, access permissions, and retention.

Risk: The external installer and engine were unavailable for verification in this review.

Mitigation: Review and pin the installer and engine before execution, and account for subprocess model usage.

## Reference(s):

- [Ponder ClawHub release](https://clawhub.ai/quinnod345/skills/ponder)
- [Protocol reference](artifact/references/protocol.md)
- [Perspectives reference](artifact/references/perspectives.md)
- [Worked example](artifact/references/worked-example.md)
- [Ponder repository referenced for installation](https://github.com/Quinnod345/ponder)
- [OCA project referenced in the skill documentation](https://github.com/Quinnod345/oneiro-oca)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Audit findings and deliberation records in JSON or JSONL, with exported reports and work plans in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are revised across passes; the process tracks coverage and convergence before stopping.]

## Skill Version(s):

0.1.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
