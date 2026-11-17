## Description:

Transforms AI agents from task-followers into proactive partners that maintain memory, recover from context loss, use check-ins, and improve with user-approved guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure agents with persistent memory, proactive check-ins, self-improvement routines, onboarding flows, and security-conscious operating patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad personal memory capture with weak consent boundaries.

Mitigation: Review and edit the templates before use, require opt-in before saving personal details, and disable opportunistic profile capture unless explicitly approved.

Risk: Heartbeat and self-improvement routines may lead to background actions or self-modifying workspace guidance.

Mitigation: Make heartbeats report-only by default and require confirmation before file cleanup, app or tab closing, or changes to AGENTS.md and TOOLS.md.

Risk: Autonomous isolated agentTurn cron jobs can perform work outside the user's immediate attention.

Mitigation: Avoid autonomous cron jobs unless they are tightly scoped, preapproved, logged, and easy to disable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andy27725/skills/proactive-agent-andy27725)
- [Onboarding Flow Reference](artifact/references/onboarding-flow.md)
- [Security Patterns Reference](artifact/references/security-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent operating guidance, workspace memory templates, onboarding references, and a local security audit script.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
