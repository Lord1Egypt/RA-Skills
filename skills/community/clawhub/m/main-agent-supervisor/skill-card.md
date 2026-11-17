## Description:

Supervise a main agent so it defaults to execution, suppresses obvious permission loops, and escalates to the user only for true approvals or critical ambiguity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjingh](https://clawhub.ai/user/sjingh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to design, run, or audit a supervisor layer that reduces unnecessary permission prompts while preserving human confirmation for risky or ambiguous actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to let an agent proceed without asking for low-risk obvious decisions, which could be misapplied if confirmation boundaries are weakened.

Mitigation: Keep confirmation required for publishing, destructive actions, money, accounts, production systems, secrets, and privacy-sensitive tasks.

Risk: Optional cron or hook-pack extensions could add enforcement behavior beyond the reviewed skill text.

Mitigation: Review and scan any cron jobs or hook-pack implementations separately before enabling them.

## Reference(s):

- [Supervisor Design](references/design.md)
- [Comparison: Existing Skills vs Needed Supervisor](references/comparison.md)
- [Workspace Implementation Plan](references/implementation.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with policy labels, checkpoint-file patterns, and optional configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include AUTO, CONFIRM, ESCALATE, and triage classifications for agent supervision.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
