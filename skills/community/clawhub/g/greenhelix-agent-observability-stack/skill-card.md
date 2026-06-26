## Description: <br>
Guides developers through building an agent-commerce observability stack with OpenTelemetry tracing, custom metrics, anomaly detection, dashboards, alerting, SLA monitoring, and cost attribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this guide to design and implement observability for multi-agent commerce systems, including tracing, metrics, alerting, SLA monitoring, and cost attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telemetry, webhook, and API-key examples could expose customer, transaction, escrow, billing, or incident data if copied directly into production. <br>
Mitigation: Replace placeholder keys with secrets from an approved secret manager, use trusted HTTPS webhook destinations, and remove or hash sensitive operational data that is not required for monitoring. <br>
Risk: Production-style observability examples may be incomplete for a specific live agent fleet. <br>
Mitigation: Treat the skill as documentation, review and test the examples in a controlled environment, and scan any implementation before connecting it to live systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-agent-observability-stack) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix agent schema](https://greenhelix.net/schemas/agent/1.0) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guide with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable documentation; examples should be reviewed and adapted before production use.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
