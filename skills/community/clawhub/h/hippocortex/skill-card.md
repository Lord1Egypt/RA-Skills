## Description:

Gives an OpenClaw agent persistent long-term memory powered by Hippocortex so it can remember and recall conversations, facts, preferences, and procedures across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vmaiops-alt](https://clawhub.ai/user/vmaiops-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add persistent memory to an agent, including recalling prior conversations and storing useful facts, preferences, procedures, and project context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived queries, selected exchanges, and extracted facts may be sent to and retained by an external persistent memory service.

Mitigation: Install only when that data handling is acceptable; avoid storing secrets or regulated data in conversations and review available memory controls before using it for sensitive work.

Risk: A misconfigured or untrusted base URL can route memory content to the wrong endpoint.

Mitigation: Verify HIPPOCORTEX_BASE_URL or the .hippocortex.json baseUrl before enabling the skill, and prefer a trusted cloud or self-hosted endpoint.

Risk: Local .hippocortex.json files can contain API keys and session configuration.

Mitigation: Prefer environment variables where possible, use a dedicated low-privilege API key, and protect or exclude .hippocortex.json from sharing and source control.

## Reference(s):

- [Hippocortex Setup Guide](references/setup-guide.md)
- [Hippocortex dashboard](https://dashboard.hippocortex.dev)
- [Hippocortex API endpoint](https://api.hippocortex.dev)
- [ClawHub skill page](https://clawhub.ai/vmaiops-alt/skills/hippocortex)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to issue memory API calls and use retrieved memory as supporting context; memory failures should not block normal responses.]

## Skill Version(s):

2.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
