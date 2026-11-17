## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve through memory, verification, security, and self-improvement patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makaronz](https://clawhub.ai/user/makaronz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure an AI agent with proactive work habits, persistent memory files, onboarding flow, heartbeat checks, security review patterns, and validation protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent conversation and profile logging can capture sensitive user context.

Mitigation: Disable or narrow raw conversation logging and opportunistic profile updates, and require explicit approval before profile writes.

Risk: Heartbeat checks, autonomous crons, and broad tool access can expand the agent's autonomy beyond the user's intent.

Mitigation: Constrain heartbeat access to email, calendar, browser, apps, and desktop state; require explicit approval for scheduled jobs and external actions.

Risk: Self-updating operating rules can introduce unwanted behavior changes.

Mitigation: Review proposed changes to AGENTS.md or security-related behavior before deployment.

Risk: Deletion or public actions can cause irreversible or external effects.

Mitigation: Require explicit approval for deletions, sends, posts, purchases, and other public or irreversible actions.

## Reference(s):

- [Proactive Skill Page](https://clawhub.ai/makaronz/skills/proactive)
- [Onboarding Flow Reference](artifact/references/onboarding-flow.md)
- [Security Patterns Reference](artifact/references/security-patterns.md)
- [Author Profile](https://x.com/halthelobster)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with configuration files and shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workspace file templates, onboarding and memory protocols, heartbeat guidance, security checks, and helper shell scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md declares 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
