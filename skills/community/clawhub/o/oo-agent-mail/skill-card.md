## Description:

AgentMail (agentmail.to). Use this skill for ANY AgentMail request — reading, creating, updating, and deleting data. Whenever a task involves AgentMail, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use the skill to manage AgentMail inboxes, messages, domains, webhooks, and related resources through their connected account. It supports reading and searching as well as creating, updating, sending, and deleting mail resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup can run a downloaded CLI installer whose contents have not been verified.

Mitigation: Prefer a verified, fixed CLI release installed under the user's control, and require approval before any automatic installation.

Risk: The skill can send or change mail and can create or delete AgentMail resources.

Mitigation: Confirm the exact requested change and target before write or destructive actions; grant only the AgentMail access needed.

## Reference(s):

- [AgentMail](https://agentmail.to)
- [AgentMail API Reference](https://docs.agentmail.to/api-reference/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [AgentMail on ClawHub](https://clawhub.ai/oomol/skills/oo-agent-mail)

## Skill Output:

**Output Type(s):** [API calls, JSON, Text, Guidance]

**Output Format:** [AgentMail results as JSON with text summaries and action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected AgentMail account; mail and resource changes may require user confirmation.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
