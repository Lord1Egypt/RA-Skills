## Description:

哈啰顺风车乘客助手，支持通过对话完成地点搜索、询价比价、运力选择、下单、邀请车主、订单查询、司机位置跟踪、取消订单、确认上车和确认到达等乘客侧顺风车流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhujianjie-kevin](https://clawhub.ai/user/zhujianjie-kevin)

### License/Terms of Use:

MIT-0

## Use Case:

External riders use this skill to coordinate Hello Hitch trips through an agent, including route lookup, price comparison, booking, driver invitation, trip tracking, cancellation, and ride-completion confirmations. Developers or operators can also use it as OpenClaw guidance for configuring the Hello Hitch MCP server.

### Deployment Geography for Use:

Mainland China cities where Hello Hitch operates.

## Known Risks and Mitigations:

Risk: The skill can schedule future automatic ride orders and run cron commands for real-world transportation transactions.

Mitigation: Use a dedicated, revocable API key and avoid enabling cron-based automatic booking unless the user accepts future background order creation.

Risk: Real ride orders, cancellations, driver invitations, and ride-completion confirmations can affect cost, travel, and trip status.

Mitigation: Prefer interactive booking that shows the exact route, price, capacity, wait time, and irreversible trip action before the user confirms.

Risk: API credentials may be exposed if copied into chat or reused broadly.

Mitigation: Configure credentials through the MCP server settings and avoid pasting secrets into agent conversations.

## Reference(s):

- [Hello Hitch Skill on ClawHub](https://clawhub.ai/zhujianjie-kevin/skills/hello-hitch-skill)
- [Hello AI Open Platform](https://aiopen.hellobike.com)
- [API Reference](references/api.md)
- [Operations Guide](references/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with JSON snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide real ride-booking actions and scheduled OpenClaw cron tasks after user confirmation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
