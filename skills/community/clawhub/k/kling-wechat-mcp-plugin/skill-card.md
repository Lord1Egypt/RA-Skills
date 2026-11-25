## Description:

Connect Kling AI's official MCP to OpenClaw and use it through Tencent's Weixin channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klingai-dev](https://clawhub.ai/user/klingai-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can configure and troubleshoot a WeChat-to-OpenClaw-to-Kling MCP path, including region-specific OAuth setup and connectivity checks that avoid using generation credits.

### Deployment Geography for Use:

Global and China

## Known Risks and Mitigations:

Risk: The security scan reported no findings but was partial because a local reference could not be resolved.

Mitigation: Review the skill and unresolved reference before installation, and confirm the stated OpenClaw and Node.js requirements.

Risk: OAuth credentials or Weixin session credentials could be exposed if copied into chat or configuration files.

Mitigation: Complete authorization as the account holder, scan and confirm the login QR code directly, and do not paste tokens or session credentials into chat or config.

Risk: Generation, upload, or task creation actions can consume Kling credits, and messages from unknown senders may reach the agent if access controls are open.

Mitigation: Use connectivity probes for checks, obtain an explicit generation request before credit-consuming actions, and configure pairing or an allowlist for senders.

## Reference(s):

- [ClawHub release](https://clawhub.ai/klingai-dev/skills/kling-wechat-mcp-plugin)
- [Tencent Weixin channel plugin](https://github.com/Tencent/openclaw-weixin)
- [OpenClaw WeChat channel guide](https://docs.openclaw.ai/zh-CN/channels/wechat)
- [OpenClaw MCP connection guide](https://docs.openclaw.ai/tools/mcp)
- [OpenClaw MCP configuration reference](https://docs.openclaw.ai/gateway/config-extensions)
- [Kling Global MCP](https://kling.ai/mcp/plugin)
- [Kling China MCP](https://klingai.com/mcp/plugin)
- [Kling OpenClaw Global plugin](https://hub.openclaw.ai/klingai-dev/plugins/kling-ai-global-openclaw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup and troubleshooting guidance varies by Kling account region and existing OpenClaw configuration.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
