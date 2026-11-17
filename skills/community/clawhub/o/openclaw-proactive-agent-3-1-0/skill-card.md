## Description:

Transforms AI agents from task-followers into proactive partners that anticipate needs, preserve working context, harden against unsafe instructions, and improve over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q262045312-ui](https://clawhub.ai/user/q262045312-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure proactive agent behavior, durable memory files, onboarding flow, heartbeat checks, self-healing practices, and security review habits for OpenClaw-style agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files may capture broad personal, conversation, or project context.

Mitigation: Require opt-in memory categories, exclude secrets and regulated data, and disable automatic transcript logging unless the user explicitly enables it.

Risk: Proactive background behaviors and autonomous crons may act with too little user control.

Mitigation: Disable autonomous crons by default and require approval before changing AGENTS.md, TOOLS.md, skill files, or other persistent operating rules.

Risk: System hygiene guidance can involve disruptive local actions such as closing apps, tabs, or moving files.

Mitigation: Require confirmation before closing applications or browser tabs, moving files, deleting files, sending messages, publishing content, or making purchases.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/q262045312-ui/skills/openclaw-proactive-agent-3-1-0)
- [Publisher profile](https://clawhub.ai/user/q262045312-ui)
- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)
- [Hal profile](https://x.com/halthelobster)
- [Clawdbot](https://github.com/clawdbot/clawdbot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, workspace file templates, and a shell audit script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance and local artifacts for an agent; proactive actions and persistent memory behavior depend on host-agent configuration and user approval.]

## Skill Version(s):

3.1.0 (source: artifact/SKILL.md frontmatter; ClawHub release package version: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
