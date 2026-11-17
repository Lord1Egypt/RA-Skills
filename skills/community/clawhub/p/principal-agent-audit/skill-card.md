## Description:

Audit a principal AI agent or coordinator bot: review memory, learnings, recent errors, installed skills, operational risks, delegation posture, and propose controlled improvements without autonomous self-modification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanbastias](https://clawhub.ai/user/juanbastias)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review a trusted principal agent's memory, learnings, installed skills, scheduled work, operational risks, and coordination posture. It supports concise operator briefings and proposal-first improvements for reliability, privacy, auditability, and safe delegation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect sensitive local agent memory and operational notes.

Mitigation: Use it only for approved local audits, restrict the review to relevant sources, and summarize sensitive patterns instead of quoting secrets or full private logs.

Risk: Implicit invocation can start an audit without a clear user confirmation step.

Mitigation: Prefer explicit audit requests with an approved source list before use.

Risk: The skill may write durable memories or notes when changes are requested.

Mitigation: Require confirmation before durable writes and prefer reversible edits with written rationale.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juanbastias/skills/principal-agent-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown briefing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed local changes or exact files touched when changes were requested.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
