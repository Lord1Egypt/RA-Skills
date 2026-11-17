## Description:

OpenClaw plugin that prepends configured text to every user message before it reaches the agent across configured workspace channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harukaon](https://clawhub.ai/user/harukaon)

### License/Terms of Use:


## Use Case:

Workspace administrators and developers use this plugin to apply a consistent prompt prefix, such as persistent project context, safety reminders, or required retrieval steps, before user messages reach the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured prompt prefixes affect every user prompt in configured channels and can persistently steer agent behavior.

Mitigation: Install only when a trusted workspace administrator intentionally wants a shared visible policy or context, and disclose the behavior to affected users.

Risk: Broad prompt rewriting can be inappropriate for sensitive workspaces if configuration changes are not controlled.

Mitigation: Restrict who can edit prependText and prefer narrower scoping or audit logs before deployment in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harukaon/skills/message-injector)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Markdown instructions with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces configured prompt-prefix text that OpenClaw prepends to user messages when enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
