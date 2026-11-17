## Description:

AI Agent 外卖点餐技能。注册成为 Agent，浏览餐厅，下单点外卖。

This skill is ready for commercial/non-commercial use.

## Publisher:

[forgottener](https://clawhub.ai/user/forgottener)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to register a HungryPanda agent, browse restaurant and menu data, manage saved delivery information, place food orders, confirm payments, and track active deliveries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access HungryPanda account data, saved addresses, order history, delivery tracking, API credentials, and saved-card payment flows.

Mitigation: Review the skill before installing, store the API key in a proper secret store or a file with 0600 permissions, and require explicit user approval before paid orders or payment confirmations unless a deliberate spending cap is configured.

Risk: The skill asks agents to install and periodically execute unpinned remote heartbeat and rule files.

Mitigation: Do not enable recurring heartbeat or remote rule-file execution unless the publisher provides pinned, reviewed, and verifiable files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/forgottener/skills/hungrypandabook)
- [HungryPanda Open Homepage](https://open.hungrypanda.vip)
- [HungryPanda API Base](https://open.hungrypanda.vip/api/v1)
- [HungryPanda Skill Source](https://open.hungrypanda.vip/skill.md)
- [HungryPanda Heartbeat Instructions](https://open.hungrypanda.vip/heartbeat.md)
- [HungryPanda Rules](https://open.hungrypanda.vip/rules.md)
- [HungryPanda Skill Metadata](https://open.hungrypanda.vip/skill.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown with inline bash commands and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for calling HungryPanda APIs with an agent API key.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
