## Description: <br>
卖家之家(跨境电商)平台一体化服务助手（服务商、物流、服务产品、技能商城、货盘、资讯、问答、供需、私信、全球开店、活动） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjzj-tec](https://clawhub.ai/user/mjzj-tec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External cross-border e-commerce sellers and service providers use this skill to query MJZJ providers, logistics, service products, skills, pallets, articles, Q&A, supply-demand posts, messages, global shop-opening platforms, and events, and to prepare authenticated MJZJ account actions when the user authorizes them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MJZJ_API_KEY and can let an agent act through the user's MJZJ account. <br>
Mitigation: Install only when account access is intended, keep the key scoped and private, and rotate or revoke it when the skill is no longer needed. <br>
Risk: Authenticated actions can publish, upload, send private messages, refresh posts, or delete content without built-in confirmation safeguards. <br>
Mitigation: Before any account-changing action, require the agent to show the exact target, content, and consequence, then wait for explicit user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjzj-tec/mjzj) <br>
- [Publisher profile](https://clawhub.ai/user/mjzj-tec) <br>
- [MJZJ homepage](https://mjzj.com) <br>
- [MJZJ API endpoint](https://data.mjzj.com) <br>
- [MJZJ agent API key page](https://mjzj.com/user/agentapikey) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with HTTP API endpoint details and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MJZJ_API_KEY for account-specific publish, upload, messaging, refresh, delete, and private-data actions.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
