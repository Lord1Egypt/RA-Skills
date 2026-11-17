## Description:

Automates LinkedIn content creation, posting, scheduling, engagement tracking, content ideation, commenting, and audience growth through a logged-in browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renatomaluhy](https://clawhub.ai/user/renatomaluhy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft, post, schedule, and analyze LinkedIn content through a logged-in browser session. It also provides content strategy and engagement guidance for growing a LinkedIn presence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act through a logged-in LinkedIn browser session and includes posting, article publishing, commenting, liking, and scheduling workflows.

Mitigation: Require explicit manual approval before any public LinkedIn action is executed.

Risk: Analytics extraction targets a hard-coded LinkedIn profile in the artifact scripts.

Mitigation: Replace the hard-coded profile with the current user's profile or an explicit user-supplied target before use.

Risk: The analytics workflow includes an optional Discord webhook alert path.

Mitigation: Document the webhook behavior and keep it opt-in with user-provided configuration.

Risk: The security summary identifies an unsafe shell reporting helper.

Mitigation: Fix or review the eval-based report writer before routine use.

## Reference(s):

- [LinkedIn Content Strategy Guide](references/content-strategy.md)
- [LinkedIn Engagement & Growth Tactics](references/engagement.md)
- [ClawHub Skill Page](https://clawhub.ai/renatomaluhy/skills/linkedin-automation-enhanced)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; analytics workflows may produce JSON and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser access with an active LinkedIn session; some workflows depend on OpenClaw browser and cron tools.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
