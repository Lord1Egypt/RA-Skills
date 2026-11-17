## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve with memory, verification, security, and self-improvement patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp33333333333](https://clawhub.ai/user/cp33333333333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure AI agents with persistent memory, proactive check-ins, reverse prompting, security hardening, and self-improvement routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad persistent personal memory that may capture sensitive user context.

Mitigation: Require explicit opt-in for persistent memory, scope what may be remembered, and keep memory files out of source control or cloud sync unless reviewed.

Risk: Recurring autonomous work and isolated agent turns may operate outside the user's immediate attention.

Mitigation: Disable or review cron jobs and require human approval before external actions or changes with lasting effects.

Risk: Automatic edits to AGENTS.md, TOOLS.md, or skill files can alter future agent behavior.

Mitigation: Prevent automatic edits to persistent operating files unless the user approves and reviews the diff.

## Reference(s):

- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/cp33333333333/skills/proactive-agent1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent operating guidance, starter markdown files, and optional local security audit commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact content version 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
