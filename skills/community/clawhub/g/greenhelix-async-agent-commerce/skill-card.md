## Description: <br>
A guide for building event-driven agent commerce systems with saga patterns, compensating transactions, dead letter handling, exactly-once processing, backpressure, async escrow settlement, event bus architecture, and webhook integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design asynchronous commerce workflows for autonomous transactions, including event buses, webhooks, saga orchestration, backpressure, and escrow settlement patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial workflow examples may be unsafe if copied into production without controls. <br>
Mitigation: Use sandbox mode first, set spending and counterparty limits, maintain audit logs, and require human or policy approval for high-value escrow releases or disputes. <br>
Risk: Event-driven and webhook-driven transaction handlers can process duplicate or unauthenticated state-changing events. <br>
Mitigation: Verify event and webhook authenticity, add idempotency to every state-changing call, and test failure handling before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-async-agent-commerce) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint](https://api.greenhelix.net/v1) <br>
- [GreenHelix Agent Production Hardening](https://clawhub.ai/skills/greenhelix-agent-production-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guide with Python code examples and architecture patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable educational content; review examples before adapting them for production.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
