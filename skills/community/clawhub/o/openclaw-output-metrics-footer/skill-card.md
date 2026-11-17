## Description:

Install, configure, maintain, or troubleshoot a compact OpenClaw output footer that shows live context usage, output tokens, Codex quota remaining, model used, and optional subagent token aggregate under text responses across Discord, Telegram, Slack, WhatsApp, Signal, Matrix, Mattermost, and other supported providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[udaymanish6](https://clawhub.ai/user/udaymanish6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install and configure a channel footer that reports context usage, output tokens, model use, Codex quota remaining, and optional nearby subagent token totals without adding prompt tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The extension reads a local OpenClaw Codex OAuth profile and contacts chatgpt.com to fetch quota data.

Mitigation: Install only in workspaces where this access is acceptable, keep quota caching enabled, and verify that tokens and profile details are not printed in channel output.

Risk: Footer metrics can disclose limited usage metadata across sessions or shared channels.

Mitigation: Restrict enabledChannels and disabledConversations, and disable appendSubagents in shared or multi-user gateways when cross-session usage visibility is not acceptable.

Risk: Subagent accounting is best effort and can be inaccurate when nearby outputs are aggregated by time window rather than exact parent-run metadata.

Mitigation: Treat subagent totals as approximate and disable appendSubagents where exact accounting is required.

## Reference(s):

- [Implementation Reference](references/implementation.md)
- [ClawHub Skill Page](https://clawhub.ai/udaymanish6/skills/openclaw-output-metrics-footer)
- [Codex Usage Endpoint](https://chatgpt.com/backend-api/wham/usage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and bundled TypeScript plugin files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a compact footer for text channel delivery; quota data is omitted when unavailable.]

## Skill Version(s):

0.2.1 (source: server release evidence and extension package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
