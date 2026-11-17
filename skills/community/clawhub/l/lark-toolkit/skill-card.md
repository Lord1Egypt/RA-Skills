## Description:

Lark Toolkit guides OpenClaw agents through Lark/Feishu messaging, workspace operations, bot setup, MCP tools, and direct Open API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengxiao-wang](https://clawhub.ai/user/pengxiao-wang)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect OpenClaw agents with Lark or Feishu workspaces for messaging, group management, contacts, calendars, docs, Bitable, OKR, tasks, webhooks, and direct Open API operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward actions that use powerful Lark credentials and broad workspace permissions.

Mitigation: Review and narrow Lark app permissions before use, and require explicit user confirmation before sending messages, sharing documents, adding members, or modifying calendars, tasks, Bitable records, OKRs, or other workspace data.

Risk: The token helper obtains and prints tenant access tokens and can read credentials from a configurable OpenClaw config path.

Mitigation: Prefer environment variables or a protected secret store, avoid logging printed tokens, and do not run scripts/get_token.sh where OPENCLAW_CONFIG can be influenced by untrusted input.

Risk: Misconfigured webhooks, tunnels, or Lark permissions can cause missed events or unintended workspace access.

Mitigation: Confirm the tenant platform, publish permission and event changes, verify webhook challenge handling, and test tunnel routing before relying on the integration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pengxiao-wang/skills/lark-toolkit)
- [Lark API Reference](references/api-reference.md)
- [Lark Bot Setup Playbook](references/bot-setup.md)
- [Lark MCP Tools](references/mcp-tools.md)
- [Lark API Permissions Reference](references/permissions.md)
- [Lark Troubleshooting](references/troubleshooting.md)
- [Webhook & Tunnel Setup](references/webhook-setup.md)
- [Lark Developer Console](https://open.larksuite.com/app)
- [Feishu Developer Console](https://open.feishu.cn/app)
- [Lark Open API Base](https://open.larksuite.com/open-apis/)
- [Feishu Open API Base](https://open.feishu.cn/open-apis/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential handling guidance, API endpoint examples, MCP tool invocations, webhook setup steps, and troubleshooting checklists.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
