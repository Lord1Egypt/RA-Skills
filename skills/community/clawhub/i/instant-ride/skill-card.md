## Description: <br>
企业用车服务助手，支持即时用车、预约用车、接送机、包车等多种用车场景，提供车型选择、费用预估、订单管理等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fbt](https://clawhub.ai/user/fbt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business travelers use this skill to estimate ride costs, request immediate or scheduled car service, arrange airport transfers, and manage ride orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can present simulated ride bookings, prices, and driver details as if they were real. <br>
Mitigation: Treat booking, cancellation, driver, and price outputs as unconfirmed unless the publisher provides a real authenticated integration and the agent labels mock versus live results clearly. <br>
Risk: A user may rely on generated ride details for time-sensitive travel without an actual car-service transaction. <br>
Mitigation: Require explicit user confirmation before any transaction and verify the booking through the connected provider or publisher-supported channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fbt/instant-ride) <br>
- [Publisher profile](https://clawhub.ai/user/fbt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Markdown and JSON objects containing ride estimates, order status, vehicle details, driver details, and cancellation results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include simulated prices, order identifiers, and driver or vehicle details; users should confirm whether a real authenticated ride-service integration is present before acting on bookings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
