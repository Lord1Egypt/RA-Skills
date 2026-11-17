## Description:

Improve OpenClaw's Feishu reply experience by customizing streaming cards, raw reasoning visibility, card 2.0 layouts, collapsible panels, titles, colors, and fallback send paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doashoi](https://clawhub.ai/user/doashoi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose and improve OpenClaw's built-in Feishu reply path, especially for streaming cards, visible reasoning, collapsible reasoning panels, titles, colors, and fallback send behavior. It helps decide whether raw reasoning is feasible for the current model/runtime path or whether safer card and streaming UX improvements are the right scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to inspect sensitive OpenClaw configuration, session transcripts, raw reasoning logs, or gateway environment data.

Mitigation: Require user consent before reading those sources, inspect only the current session and necessary fields, redact secrets, and avoid dumping full files or full environments.

Risk: Runtime, session, provider, or Feishu delivery changes can disrupt live Feishu replies or make behavior fail after restart or a new session.

Mitigation: Use phased rollout, start with low-risk card changes where appropriate, create a written change note and file backups before risky edits, and provide exact rollback and restart guidance.

Risk: Card changes alone can falsely imply raw reasoning is available when the active model/runtime path exposes only transcript-only, opaque, or no reasoning data.

Mitigation: Verify the active provider/model, session state, raw-stream logs, and runtime hooks before promising visible live reasoning; otherwise offer ordinary streaming and card UX improvements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/doashoi/skills/openclaw-feishu-reasoning-ux)
- [Feishu Card JSON 2.0 Structure](https://open.feishu.cn/document/feishu-cards/card-json-v2-structure)
- [Feishu Collapsible Panel](https://open.feishu.cn/document/feishu-cards/card-json-v2-components/containers/collapsible-panel)
- [Feishu Card Update Guide](https://open.feishu.cn/document/feishu-cards/update-feishu-card)
- [PATCH Updates for Sent Message Cards](https://open.feishu.cn/document/server-docs/im-v1/message-card/patch)
- [OpenClaw Telegram Channel Docs](https://openclawlab.com/en/docs/channels/telegram/)
- [OpenClaw Upstream Repository](https://github.com/openclaw/openclaw)
- [Proven Case and Pitfalls](references/proven-case-and-pitfalls.md)
- [OpenClaw Feishu Card Customization Reference](references/implementation-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, file paths, configuration notes, and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic conclusions, phased rollout steps, backup and rollback instructions, and verification checklists.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
