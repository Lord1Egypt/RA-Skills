## Description:

Connects WeChat Official Accounts to OpenClaw agents for follower chat, notifications, content publishing, OAuth, analytics, intelligent recognition, card/coupon operations, multi-account routing, and knowledge synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect a WeChat Official Account to OpenClaw agents so followers can chat with an agent, receive notifications, and trigger official-account workflows. It is intended for configured OpenClaw deployments with WeChat account credentials and appropriate channel permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default dynamic-agent settings can expose powerful account-management tools to public follower agents.

Mitigation: Before production use, set dynamicAgents.permissionMode to admin-only or role-based and configure adminUsers, roles, or rolePermissions.

Risk: Default instructions may include Huo15-branded or lead-capture behavior that is not appropriate for every account.

Mitigation: Review defaultInstructionsPreset and set it to none/off or replace it with account-specific instructions when needed.

Risk: Conversation synchronization to local files or Odoo can retain follower conversations outside the chat channel.

Mitigation: Enable knowledgeSync or Odoo synchronization only when retention, access control, and privacy requirements are acceptable.

Risk: Using the skill on a production WeChat Official Account without review can affect follower-facing messaging and account resources.

Mitigation: Review configuration and permissions before installing on a production official account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-wechat-service)
- [npm package @huo15/wechat-service](https://www.npmjs.com/package/@huo15/wechat-service)
- [WeChat Official Account Platform documentation](https://developers.weixin.qq.com/doc/service/guide/)
- [OpenClaw documentation](https://docs.openclaw.ai/zh-CN)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown, text replies, JSON-style tool results, and WeChat Official Account API effects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send messages or change WeChat account resources when configured with credentials and authorized permissions.]

## Skill Version(s):

2.3.5 (source: frontmatter, package.json, changelog, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
