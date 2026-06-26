## Description: <br>
AI Agent 外卖点餐技能。注册成为 Agent，浏览餐厅，下单点外卖。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forgottener](https://clawhub.ai/user/forgottener) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to register with HungryPanda, browse restaurants and menus, manage delivery details, place food orders, and track order status through the HungryPanda API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent real food-ordering authority, including access to saved delivery data and possible saved-card payment flows. <br>
Mitigation: Require explicit user confirmation for orders, payments, address changes, cancellations, refunds, and owner-console setup; keep HungryPanda API keys scoped to HungryPanda only. <br>
Risk: Recurring remote heartbeat instructions can change outside the reviewed package. <br>
Mitigation: Disable or tightly cap auto-confirmation, and review or version-pin remote HEARTBEAT.md and RULES.md before enabling recurring checks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/forgottener/hungrypandabook) <br>
- [HungryPanda Open Platform](https://open.hungrypanda.vip) <br>
- [HungryPanda API Base](https://open.hungrypanda.vip/api/v1) <br>
- [HungryPanda Skill File](https://open.hungrypanda.vip/skill.md) <br>
- [HungryPanda Heartbeat Instructions](https://open.hungrypanda.vip/heartbeat.md) <br>
- [HungryPanda Rules](https://open.hungrypanda.vip/rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and request examples for HungryPanda agent registration, authentication, browsing, ordering, address management, verification, and order tracking.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
