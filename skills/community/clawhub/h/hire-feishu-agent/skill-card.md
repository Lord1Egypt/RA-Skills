## Description:

Guides an agent through collecting Feishu bot details and preparing OpenClaw configuration snippets to add a new Feishu-routed agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xrovis](https://clawhub.ai/user/xrovis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add a Feishu bot account, agent entry, and DM binding to openclaw.json without overwriting existing configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app secrets may be exposed if pasted into chat or retained in transcripts.

Mitigation: Use least-privilege Feishu credentials, avoid production secrets in chat, and replace placeholders locally where possible.

Risk: Persistent OpenClaw gateway configuration changes can break routing or expose credentials if the file is edited carelessly.

Mitigation: Back up and validate ~/.openclaw/openclaw.json, append entries without overwriting existing accounts or bindings, restrict file permissions, and restart the gateway only when ready.

## Reference(s):

- [OpenClaw Feishu configuration schema](artifact/schema.md)
- [OpenClaw Feishu configuration template](artifact/template.json)
- [ClawHub skill page](https://clawhub.ai/xrovis/skills/hire-feishu-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON snippets and a shell restart command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for Feishu app credentials and emits copy-ready OpenClaw configuration fragments.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
