## Description:

Personal finance management skill using Maybe Finance OS for tracking expenses, analyzing budgets, monitoring net worth, and managing personal finances through a self-hosted Maybe Finance platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage personal finance workflows around a self-hosted Maybe Finance instance, including transaction review, account summaries, budget checks, net worth snapshots, and cash-flow reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests a Maybe Finance API token and finance API URL.

Mitigation: Protect the token, scope it to the intended self-hosted instance, and bind the Maybe service only where intended.

Risk: Security evidence reports that the included CLI mostly returns mock data and can falsely report that transactions were added.

Mitigation: Do not rely on the CLI for real financial records until it is confirmed to run in demo mode or changed to make verified Maybe API calls.

Risk: Account-management examples include destructive operations such as deleting accounts.

Mitigation: Require explicit confirmation and backups before performing destructive account operations.

## Reference(s):

- [Maybe Finance](https://github.com/maybe-finance/maybe)
- [ClawHub Skill Page](https://clawhub.ai/antonia-sz/skills/maybe-finance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI-style text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account, transaction, budget, net worth, and cash-flow summaries; users should verify results against their Maybe Finance instance.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
