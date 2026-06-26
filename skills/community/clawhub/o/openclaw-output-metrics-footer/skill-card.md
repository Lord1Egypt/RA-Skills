## Description: <br>
Install, configure, maintain, or troubleshoot a compact OpenClaw output footer that shows live context usage, output tokens, Codex quota remaining, model used, and optional subagent token aggregate under text responses across Discord, Telegram, Slack, WhatsApp, Signal, Matrix, Mattermost, and other supported providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[udaymanish6](https://clawhub.ai/user/udaymanish6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw workspace operators use this skill to install and configure an extension that appends compact runtime metrics to text channel responses. It helps teams see token usage, context pressure, model selection, quota status, and optional nearby subagent usage without adding those metrics to prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The extension reads a local Codex OAuth token and uses it for outbound quota checks. <br>
Mitigation: Install only from a trusted publisher, review the extension before enabling it, and keep quota checks limited to environments where that OAuth access is acceptable. <br>
Risk: The footer can expose operational metadata such as model, token usage, context pressure, subagent totals, and quota state to channel recipients. <br>
Mitigation: Use enabledChannels and disabledConversations to limit deployment to known internal work channels. <br>
Risk: The default configuration can modify text channel messages broadly. <br>
Mitigation: Start with an explicit enabledChannels allowlist and add disabledChannels or disabledConversations for channels where telemetry would add noise or disclose unnecessary information. <br>


## Reference(s): <br>
- [Implementation Notes](references/implementation.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/udaymanish6/openclaw-output-metrics-footer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, JSON configuration, and TypeScript plugin files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The deployed plugin appends a compact one-line telemetry footer to text channel messages.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence and extension package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
