## Description:

OpenAuto provides a proactive agent operating architecture for persistent memory, working buffers, compaction recovery, autonomous checks, and security guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danavfrost](https://clawhub.ai/user/danavfrost)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use OpenAuto to add reusable operating guidance, memory templates, onboarding flows, heartbeat routines, and security review patterns to a proactive agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memory and working-buffer routines may retain personal, sensitive, or stale context.

Mitigation: Narrow what the agent may remember, avoid storing credentials or highly sensitive data in workspace notes, and review memory files regularly.

Risk: Background checks and autonomous cron or isolated-agent workflows may act beyond the user's intended scope if approval boundaries are unclear.

Mitigation: Require explicit approval for email, calendar, log, browser, desktop, public, irreversible, or external actions, and only enable autonomous jobs with a specific scope.

Risk: The skill's safety rules are behavioral instructions rather than technical enforcement.

Mitigation: Treat the rules as advisory, review the skill before deployment, run the provided security audit where applicable, and rely on platform-level controls for hard boundaries.

## Reference(s):

- [OpenAuto ClawHub release](https://clawhub.ai/danavfrost/skills/openauto)
- [Original proactive-agent skill](https://clawhub.ai/halthelobster/proactive-agent)
- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with shell command examples and a bash audit script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workspace memory templates, onboarding templates, security checklists, heartbeat routines, and a local security-audit script.]

## Skill Version(s):

1.0.7 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
