## Description: <br>
Monitor applications, infrastructure, logs, synthetic checks, and cloud services in New Relic, including alerts, dashboards, NRQL telemetry queries, workloads, notification channels, and deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect and manage New Relic telemetry, alerts, dashboards, synthetic monitors, cloud integrations, account settings, and related observability resources through ClawLink-backed tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use ClawLink-connected New Relic credentials to perform account management and observability administration actions. <br>
Mitigation: Use a least-privilege New Relic API key and install only when that level of connected account access is acceptable. <br>
Risk: Write or destructive operations can modify or delete New Relic resources such as dashboards, alert policies, users, monitors, workloads, and API keys. <br>
Mitigation: Review write previews carefully and confirm destructive actions only after the target resource and intended effect are clear. <br>
Risk: Credential exposure or over-broad permissions could expand the impact of an unintended tool call. <br>
Mitigation: Keep API keys out of chat, rely on ClawLink credential handling, and rotate or revoke keys if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/new-relic-observability) <br>
- [New Relic NerdGraph API Reference](https://docs.newrelic.com/docs/apis/nerdgraph/) <br>
- [New Relic NRQL Reference](https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/) <br>
- [New Relic Alert Policies](https://docs.newrelic.com/docs/alerts-applied-intelligence/new-relic-alerts/) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=new-relic-observability) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and tool-call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce previews and confirmations for write or destructive New Relic operations.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
