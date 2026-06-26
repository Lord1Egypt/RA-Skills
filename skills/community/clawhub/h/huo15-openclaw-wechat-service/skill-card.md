## Description: <br>
OpenClaw WeChat service-account channel plugin that connects public-account followers to LLM agents and supports messaging, publishing, OAuth, analytics, intelligent recognition, coupons, dynamic per-follower agents, and knowledge synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect a WeChat service account to OpenClaw agents so followers can chat with an LLM agent, receive notifications, trigger business workflows, and allow authorized users to manage WeChat public-account APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can control real WeChat service-account operations and exposes broad account-management tools. <br>
Mitigation: Install only for intended accounts, configure permissionMode as admin-only or role-based, set adminUsers, and review who can invoke each tool before production use. <br>
Risk: The plugin requires sensitive WeChat credentials and may integrate with Odoo credentials. <br>
Mitigation: Treat WeChat and Odoo credentials as high-value secrets, store them in environment variables or a secret manager, and restrict access and retention. <br>
Risk: Conversation transcripts can be persisted locally or synchronized to Odoo knowledge articles. <br>
Mitigation: Disable knowledgeSync unless transcript storage is required, and review retention, access controls, and privacy obligations before enabling synchronization. <br>
Risk: Server security evidence reports a suspicious verdict due to broad account-control powers and transcript persistence behavior. <br>
Mitigation: Review and scan the release before deployment, upgrade flagged dependencies, and validate configuration in a non-production environment first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-wechat-service) <br>
- [npm package](https://www.npmjs.com/package/@huo15/wechat-service) <br>
- [WeChat service-account documentation](https://developers.weixin.qq.com/doc/service/guide/) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/zh-CN) <br>
- [Project homepage](https://cnb.cool/huo15/ai/huo15-openclaw-wechat-service) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code, markdown] <br>
**Output Format:** [Markdown guidance with configuration examples, shell commands, and code-oriented tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce WeChat service-account setup guidance, OpenClaw channel configuration, and agent tool outputs for WeChat public-account operations.] <br>

## Skill Version(s): <br>
2.3.5 (source: server release metadata, SKILL.md frontmatter, package.json, CHANGELOG released 2026-05-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
