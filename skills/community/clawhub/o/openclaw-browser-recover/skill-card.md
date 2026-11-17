## Description:

Diagnose and recover OpenClaw browser tool timeouts involving browser.status, browser.tabs, browser.snapshot, gateway ports 18789/18791, and Chrome CDP 9222 conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sajdijjsid](https://clawhub.ai/user/sajdijjsid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when OpenClaw browser control times out, closes its MCP connection, or hits Chrome CDP port conflicts. It provides a concise recovery runbook and optional healthcheck command for restoring browser tool availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recovery flow may ask the agent or user to inspect local ports and restart the OpenClaw gateway.

Mitigation: Limit recovery to the documented checks and a single gateway restart unless the user explicitly approves further actions.

Risk: The skill's built-in user-facing wording is in Chinese.

Mitigation: Adapt the wording to the user's preferred language while preserving the documented recovery steps.

## Reference(s):

- [OpenClaw Browser Recover on ClawHub](https://clawhub.ai/sajdijjsid/skills/openclaw-browser-recover)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a user-facing recovery sequence and an optional shell healthcheck script.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
