## Description:

Builds, previews, schedules, monitors, and revises multi-channel B2B outreach campaigns using the user's knowledge base and learned writing style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milstan](https://clawhub.ai/user/milstan)

### License/Terms of Use:

MIT-0

## Use Case:

Sales users and operators use this skill to plan, approve, send, monitor, pause, resume, and revise outbound B2B outreach across connected channels. It is intended to keep outreach grounded in available prospect, company, style, opt-out, and campaign-state evidence before any live contact action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read sales knowledge-base and style data and poll connected messaging accounts.

Mitigation: Review connected account permissions before installation and grant only the accounts and channels needed for the intended outreach workflow.

Risk: The skill can persist scheduled outreach and automate external account actions.

Mitigation: Require visible confirmation for prerequisite research and every live account action, especially sending, queueing, pausing, resuming, or canceling campaign touchpoints.

Risk: Sensitive outreach drafts may be stored in predictable temporary files.

Mitigation: Avoid shared machines and shared temporary directories until the file handling is replaced with secure per-run temporary files.

## Reference(s):

- [Campaign Engine Reference](references/campaign-engine.md)
- [Channel Adapters Reference](references/channel-adapters.md)
- [Response Listener Reference](references/response-listener.md)
- [Outclaw homepage](https://github.com/leadbay/outclaw)
- [ClawHub skill page](https://clawhub.ai/milstan/skills/outclaw-plan)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown outreach plans, structured JSON campaign or response records, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-visible approval gates before live outreach actions; may produce campaign state, draft messages, dashboard summaries, and response classifications.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter declares 2.1.33)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
