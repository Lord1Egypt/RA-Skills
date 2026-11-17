## Description:

卖家之家(跨境电商)平台一体化服务助手，帮助代理查询并操作服务商、物流、服务产品、技能商城、货盘、资讯、问答、供需、私信、全球开店和活动相关 MJZJ API。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through MJZJ platform API workflows for cross-border ecommerce discovery, publishing, messaging, uploads, and account-specific management actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated access can send private messages, publish content, upload files, refresh posts, and delete supply-demand items.

Mitigation: Require explicit user confirmation before authenticated write actions, and show the recipient, content, file path, or item id before calling the API.

Risk: Use of MJZJ_API_KEY may expose account data and account-scoped actions to the agent.

Mitigation: Install only with an API key the user is comfortable granting to the agent, and rotate or revoke the key if unintended access is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj)
- [MJZJ homepage](https://mjzj.com)
- [MJZJ API key page](https://mjzj.com/user/agentapikey)
- [MJZJ API base URL](https://data.mjzj.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with API endpoint references, JSON request bodies, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MJZJ_API_KEY for authenticated account data and write actions.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
