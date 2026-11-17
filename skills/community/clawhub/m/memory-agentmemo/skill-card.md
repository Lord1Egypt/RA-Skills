## Description:

Memory (AgentMemo) connects OpenClaw to a self-hosted AgentMemo server for semantic memory search, auto-recall, and optional auto-capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxjsxy](https://clawhub.ai/user/yxjsxy)

### License/Terms of Use:

MIT

## Use Case:

Developers and external OpenClaw users use this plugin to connect agent memory workflows to a self-hosted AgentMemo service for semantic recall and optional memory capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optionally captured user messages are sent to the configured AgentMemo server.

Mitigation: Use a local or trusted HTTPS AgentMemo server and enable auto-capture only with user consent.

Risk: API keys protect authenticated AgentMemo instances.

Mitigation: Store API keys in environment variables or another secret manager and avoid committing them in configuration.

Risk: A compromised or unverified AgentMemo server package could expose memory content.

Mitigation: Pin or otherwise verify the AgentMemo server package before running it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yxjsxy/skills/memory-agentmemo)
- [AgentMemo Project](https://github.com/yxjsxy/agentMemo)
- [AgentMemo Server](https://github.com/agentmemo/agentmemo)

## Skill Output:

**Output Type(s):** [text, API calls, configuration]

**Output Format:** [Plain text context blocks with JSON HTTP requests to the configured AgentMemo service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the configured server URL, optional bearer token, optional user namespace, auto-recall, and auto-capture settings.]

## Skill Version(s):

0.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
