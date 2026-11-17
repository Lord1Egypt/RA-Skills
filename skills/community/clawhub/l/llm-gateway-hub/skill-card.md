## Description:

Helps developers connect OpenAI-compatible model providers through a local gateway, manage API keys and budgets, and track usage costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT (Python code only); all rights reserved (documentation and theory)

## Use Case:

Developers and teams use this skill to configure and call multiple model providers from one local interface, monitor spending, and manage provider credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Locally stored provider API keys or synced gateway files may expose credentials.

Mitigation: Keep gateway configuration out of cloud sync, repositories, shared folders, and chats; restrict file permissions and rotate exposed keys.

Risk: Prompts may be sent to an unintended provider, and incorrect pricing can distort budget tracking.

Mitigation: Verify configured provider URLs and current prices before use, and start with a small budget.

Risk: Generated images may lack provenance marking if watermark settings are unsuitable.

Mitigation: Review the image watermark setting when provenance marking matters.

## Reference(s):

- [ClawHub release](https://clawhub.ai/zhaoxinghua09-cell/skills/llm-gateway-hub)
- [Publisher homepage](https://nomos.ai)
- [Gateway configuration template](references/gateway_config.template.json)
- [New provider setup guide](references/接入新平台指引.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provider calls can produce model responses and local usage records.]

## Skill Version(s):

1.0.8 (source: server-resolved ClawHub release; bundled files identify 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
