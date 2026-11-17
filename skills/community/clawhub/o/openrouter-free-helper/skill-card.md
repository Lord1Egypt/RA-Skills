## Description:

Monitors free OpenRouter models for expiration notices and newly available free models, with optional scheduled Feishu notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suidge](https://clawhub.ai/user/suidge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor configured OpenRouter free models, detect model expiration notices, discover new free models, and produce concise notification summaries for manual or scheduled workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may start Chrome with DevTools debugging on port 9222 and invoke bb-browser for browser-assisted model discovery.

Mitigation: Review this behavior before installation and prefer API-only execution when browser automation is not required.

Risk: Notifications may include model names, OpenRouter links, and check timestamps.

Mitigation: Confirm the Feishu recipient and notification policy before enabling scheduled or direct notification delivery.

Risk: Global or unpinned installs of browser automation dependencies can change runtime behavior over time.

Mitigation: Pin dependencies where possible and review installed bb-browser adapters before scheduled use.

## Reference(s):

- [Openrouter Free Helper on ClawHub](https://clawhub.ai/suidge/skills/openrouter-free-helper)
- [Cron Task Reference](references/cron-task.md)
- [OpenRouter Page Structure Reference](references/openrouter-structure.md)
- [OpenRouter frontend models endpoint](https://openrouter.ai/api/frontend/models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands, JSON configuration snippets, and notification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON status data and may send Feishu messages when notification mode is enabled.]

## Skill Version(s):

1.0.10 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
