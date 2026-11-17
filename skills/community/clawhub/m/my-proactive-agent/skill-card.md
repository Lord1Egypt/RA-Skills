## Description:

Transforms AI agents from task-followers into proactive partners that anticipate needs and continuously improve with WAL Protocol, Working Buffer, Autonomous Crons, and reliability patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujiang817](https://clawhub.ai/user/liujiang817)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an agent proactive operating patterns for onboarding, persistent memory, heartbeat checks, security prompts, and self-improvement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to persist broad personal and work context, including names, preferences, decisions, URLs, and sometimes full message text.

Mitigation: Install only when that memory behavior is desired, minimize sensitive content in memory files, and keep generated memory files out of shared repositories and backups.

Risk: Heartbeat cleanup and self-healing patterns may lead to autonomous local changes with weak consent and scoping.

Mitigation: Disable or rewrite those parts unless explicitly wanted, and require human approval for destructive, public, external, or security-sensitive actions.

Risk: The authoritative security verdict is suspicious, even though the scan did not identify clear exfiltration or malicious code.

Mitigation: Review the skill carefully before installing and run the included security audit script in the target workspace.

## Reference(s):

- [My Proactive Agent on ClawHub](https://clawhub.ai/liujiang817/skills/my-proactive-agent)
- [Publisher profile](https://clawhub.ai/user/liujiang817)
- [Onboarding Flow Reference](artifact/references/onboarding-flow.md)
- [Security Patterns Reference](artifact/references/security-patterns.md)
- [Hal the Lobster](https://x.com/halthelobster)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operating instructions, starter markdown files, reference material, and a local audit script.]

## Skill Version(s):

3.1.0 (source: artifact/SKILL.md frontmatter; ClawHub release version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
