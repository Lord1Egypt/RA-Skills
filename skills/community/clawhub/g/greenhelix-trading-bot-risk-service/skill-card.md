## Description: <br>
A guide for building a cross-exchange, cross-strategy portfolio risk monitoring system with webhooks, an event bus, SLA checks, drawdown alerts, correlation monitoring, liquidation proximity checks, circuit breakers, and production deployment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading bot operators use this skill to design portfolio-level risk monitoring across multiple exchanges and strategies, including alerting, aggregate exposure checks, and circuit-breaker workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live exchange access and order-cancellation examples could affect funds if adapted directly. <br>
Mitigation: Use sandbox or read-only exchange credentials until trading controls are explicitly approved; require audit logging, least-privilege keys, and human approval before enabling order cancellation or position closing. <br>
Risk: The guide references sensitive signing and exchange credentials. <br>
Mitigation: Store secrets in a proper secret manager, avoid hardcoding credentials, and rotate keys when access patterns change. <br>
Risk: Webhook and platform integrations may transmit portfolio or trading data to GreenHelix and operator-controlled endpoints. <br>
Mitigation: Verify what data is sent to each endpoint and confirm endpoint trust, retention, and access controls before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-trading-bot-risk-service) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API reference](https://api.greenhelix.net/v1) <br>
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with inline Python and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; examples reference AGENT_SIGNING_KEY and user-supplied exchange or API credentials.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
