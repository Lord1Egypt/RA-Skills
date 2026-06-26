## Description: <br>
哈啰顺风车乘客助手覆盖询价比价、下单、邀请车主、行程追踪、确认上车和到达的完整拼车流程，并从日常出行表达中识别真实顺风车需求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhujianjie-kevin](https://clawhub.ai/user/zhujianjie-kevin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External passengers use this skill with OpenClaw to plan and manage Hello Hitch ride-sharing trips, including price checks, order creation, driver invitations, status tracking, cancellation, and trip completion. It is intended for real ride-hailing workflows rather than software development, navigation-app control, or general travel advice. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real ride-hailing actions such as booking, cancellation, driver invitation, and trip-completion confirmation. <br>
Mitigation: Require explicit user confirmation before each real-world state-changing action and present prices, route details, wait time, and driver options before proceeding. <br>
Risk: API credentials are required to connect the OpenClaw MCP server. <br>
Mitigation: Configure the API key through OpenClaw MCP configuration and avoid pasting secrets into ordinary chat messages. <br>
Risk: Cron-based ride tasks can trigger delayed background ride actions. <br>
Mitigation: Create scheduled tasks only when the user clearly requests them, include complete origin and destination details, and review or disable scheduled tasks when automatic execution is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhujianjie-kevin/hello-hitch-skill) <br>
- [哈啰 AI 开放平台](https://aiopen.hellobike.com) <br>
- [API reference](references/api.md) <br>
- [Operations guide](references/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-facing ride status, options, confirmations, links, and configuration guidance; may also instruct the agent to call MCP tools.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
