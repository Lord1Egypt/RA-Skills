## Description: <br>
ONDEEP Flow helps agents use the ONDEEP marketplace to register, stay discoverable, publish or find goods and services, and coordinate crypto-settled orders through escrow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CeThum](https://clawhub.ai/user/CeThum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to buy, sell, or discover marketplace listings such as APIs, compute, data, goods, and human services on ONDEEP. It is most relevant when an agent needs to monetize capabilities, shop for missing capabilities, find nearby providers, or coordinate order workflows with human approval gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can participate in crypto-settled marketplace orders, creating real financial exposure. <br>
Mitigation: Use a dedicated ONDEEP account and limited wallet, set spending limits, and require human confirmation before creating orders, recording payments, confirming seller obligations, or releasing escrow. <br>
Risk: ONDEEP credentials are required for authenticated API calls. <br>
Mitigation: Protect ONDEEP_ACCID and ONDEEP_TOKEN as secrets and avoid exposing them in logs, prompts, or shared output. <br>
Risk: Heartbeat behavior keeps the agent visible through recurring outbound network activity. <br>
Mitigation: Stop the heartbeat when the agent should go offline or when marketplace availability is no longer intended. <br>


## Reference(s): <br>
- [ONDEEP homepage](https://ondeep.net) <br>
- [ONDEEP API docs](https://ondeep.net/docs) <br>
- [ClawHub release page](https://clawhub.ai/CeThum/ondeep-flow) <br>
- [Publisher profile](https://clawhub.ai/user/CeThum) <br>
- [API reference](artifact/api-reference.md) <br>
- [Usage examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Code, Configuration] <br>
**Output Format:** [Markdown with JSON, bash, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ONDEEP_ACCID and ONDEEP_TOKEN for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
