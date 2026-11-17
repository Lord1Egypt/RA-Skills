## Description:

Split group expenses fairly (equal or weighted shares) and compute the minimum number of money transfers to settle up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to settle shared expenses for trips, roommates, clubs, and other group pools. It reads a simple ledger, computes each person's fair share and net position, and produces a compact settlement plan plus audit output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented ledger format can silently produce incorrect payment instructions.

Mitigation: Review the ledger carefully, avoid inline comments in ledger lines, run with --show-items to verify parsed participants, and double-check settlement lines before sending money.

Risk: Ledgers from untrusted people may contain misleading amounts, participants, or weights.

Mitigation: Use trusted ledger inputs where possible and compare the audit output with receipts before relying on the settlement plan.

## Reference(s):

- [Fair Splitting & Minimum-Transfer Settlement](references/settlement-theory.md)
- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/group-expense-settler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; terminal text tables and optional JSON from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline Python output based on a user-supplied ledger; settlement lines should be reviewed before money is sent.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
