## Description:

Connect Lark (Feishu) messaging to OpenClaw via webhook bridge. Supports text, rich text (post), and image messages bidirectionally. Use when setting up Lark/Feishu as a messaging channel, receiving messages with images, sending replies back to Lark, reading Lark documents/wikis/bitables, or troubleshooting Lark integration issues. Covers both Lark International (larksuite.com) and China Feishu (feishu.cn).

This skill is ready for commercial/non-commercial use.

## Publisher:

[boyangwang](https://clawhub.ai/user/boyangwang)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to connect Lark or Feishu messaging with OpenClaw through a webhook bridge, including setup, message handling, image support, document access notes, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A network webhook can pass Lark-originated messages into a privileged OpenClaw agent.

Mitigation: Use HTTPS or a trusted reverse proxy, require webhook token or signature validation, restrict ingress to trusted sources, and use a constrained OpenClaw agent profile.

Risk: Service setup guidance may lead to running the bridge with excessive privileges.

Mitigation: Avoid root services and run the bridge under a dedicated low-privilege account.

Risk: Lark app credentials and OpenClaw gateway tokens are required for operation.

Mitigation: Store secrets in locked-down files and review permissions before installation.

## Reference(s):

- [Lark API Message Formats](references/api-formats.md)
- [Lark Integration Setup Guide](references/setup-guide.md)
- [Lark Developer Console](https://open.larksuite.com/)
- [Feishu Developer Console](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with command, code, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include webhook setup steps, Lark API formats, bridge service guidance, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release evidence, scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
