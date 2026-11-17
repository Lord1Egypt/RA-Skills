## Description:

Connects a personal WeChat account, not enterprise WeChat or WeCom, by guiding an agent through OpenClaw setup, QR-code login, credential confirmation, and gateway restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oreoandyuumi](https://clawhub.ai/user/oreoandyuumi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when they need an agent to connect a personal WeChat account through OpenClaw using QR-code authentication. The skill is not intended for enterprise WeChat or WeCom connection flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install or update npm packages, including global OpenClaw changes, from external package sources.

Mitigation: Review package provenance before use, prefer pinned package versions, and ask the user clearly before global installs or persistent toolchain changes.

Risk: The flow handles personal WeChat QR codes and can optionally expose a one-time authorization QR code through CDN upload.

Mitigation: Keep QR-code images local by default and use external upload only after explicit user request and disclosure of exposure risk.

Risk: The flow writes account tokens and local credential files after successful QR confirmation.

Mitigation: Show redacted credential details before writing, require user confirmation, write data-only JSON, and restrict credential file permissions.

Risk: The skill changes OpenClaw gateway state and depends on responses from Tencent WeChat endpoints.

Mitigation: Validate API responses, preserve normal agent discretion for error handling, and confirm operational changes before restarting the gateway.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oreoandyuumi/skills/mmxagent-skill-wechat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON credential data, and local QR-code file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a stepwise account-linking flow that may install npm packages, call Tencent WeChat endpoints, save a QR-code image, write local credentials, and restart the OpenClaw gateway.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
