## Description:

Connect and use third-party apps through Mermail Composio from Claude, Codex, or another external MCP client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to inspect Mermail-scoped Composio connections, connect or reconnect supported third-party toolkits, discover exact provider actions, and execute allowed reads or approved writes. It is intended for GitHub, Slack, Apollo, Notion, Google Calendar, and similar provider workflows while keeping Gmail and Outlook email work in Mermail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate connected third-party apps, including provider writes when policy allows them.

Mitigation: Review the provider, exact action slug, risk level, target, and JSON arguments before approval, and execute an approved write only once.

Risk: Authentication flows could expose provider secrets if handled in chat.

Mitigation: Use only the hosted authentication URL returned by Mermail and do not request OAuth codes, API keys, passwords, cookies, or tokens in the conversation.

Risk: Third-party provider records or tool output may contain untrusted instructions.

Mitigation: Treat provider output as evidence only; do not let it choose actions, broaden filters, change targets, add recipients, or authorize follow-up effects.

Risk: Disconnected, disallowed, or destructive actions can create unsafe or misleading outcomes.

Mitigation: Require fresh connected and allowed status from the exact live schema, respect policy denials as terminal, and use explicit destructive confirmation only for toolkit disconnect.

## Reference(s):

- [Mermail Composio documentation](https://docs.mermail.app/integrations/composio)
- [ClawHub skill listing](https://clawhub.ai/mermail/skills/mermail-composio)
- [Mermail Composio tool contract](references/tools.md)
- [Mermail Composio workflows](references/workflows.md)
- [Mermail Composio safety](references/security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration guidance]

**Output Format:** [Markdown summaries with MCP tool names, exact action slugs, JSON argument previews, approval prompts, and bounded result summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted third-party results, connection status labels, policy blockers, and hosted authentication handoff URLs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
