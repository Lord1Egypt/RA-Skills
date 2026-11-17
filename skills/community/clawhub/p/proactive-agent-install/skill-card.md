## Description:

Helps agents install and use a proactive operating pattern with persistent memory files, onboarding, heartbeat checks, security review guidance, and self-improvement routines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makaronz](https://clawhub.ai/user/makaronz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure agents with onboarding, durable memory, proactive check-ins, self-review, and security-audit habits. It is intended for agents that manage workspace files and need clearer continuity and user-control practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and profile files can capture sensitive personal or project context.

Mitigation: Review proposed profile and memory files before use, require approval before writing them, and remove the bundled proposed_USER.md from shared copies.

Risk: Autonomous cron or background-agent examples can cause unexpected monitoring or actions.

Mitigation: Disable autonomous cron and background-agent behavior unless the operator explicitly enables and scopes it.

Risk: Installation steps can overwrite existing agent operating files such as AGENTS.md or SOUL.md.

Mitigation: Inspect and merge assets manually instead of blindly copying them over existing workspace files.

Risk: Desktop or browser cleanup routines could remove user state unexpectedly.

Mitigation: Remove cleanup actions or require explicit human approval before closing apps, changing browser state, or deleting files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/makaronz/skills/proactive-agent-install)
- [Onboarding Flow Reference](artifact/references/onboarding-flow.md)
- [Security Patterns Reference](artifact/references/security-patterns.md)
- [Hal Stack author profile](https://x.com/halthelobster)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with file templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance and workspace file templates for agent behavior, memory, onboarding, heartbeats, and security review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
