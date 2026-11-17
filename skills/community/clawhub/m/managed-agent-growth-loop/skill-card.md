## Description:

Helps customer-embedded agents turn usage reviews into state handoffs, proactive watchlists, onboarding gap checks, outcome feedback loops, and multi-agent quality gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Operations leads, customer success teams, and agent operators use this skill to review how embedded agents are being used and convert gaps into repeatable handoff, follow-up, onboarding, feedback, and review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring cron or heartbeat suggestions could create ongoing customer-operations follow-up loops without sufficient approval, ownership, expiry, or access-boundary safeguards.

Mitigation: Require explicit approval, a named owner, a customer-specific data boundary, a verified delivery channel, and an expiration or review date before accepting any scheduled task.

Risk: Branded service-value sections may be inappropriate for neutral reports.

Mitigation: Omit branded service-value language when producing neutral customer or internal reports.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with templates, tables, checklists, and inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose recurring cron or heartbeat operating recipes that require human approval before activation.]

## Skill Version(s):

0.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
