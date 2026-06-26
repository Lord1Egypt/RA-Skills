## Description: <br>
Pilot Alert provides configurable alerting on event patterns and thresholds with webhook delivery and direct agent messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to subscribe to Pilot events, trigger alerts from patterns or thresholds, and notify on-call agents or approved webhook destinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive alert contents may be sent to configured webhooks or agents. <br>
Mitigation: Use only trusted destinations and redact secrets, customer data, stack traces, and internal identifiers before sending alerts. <br>
Risk: Broad event subscriptions can expose more operational data than intended. <br>
Mitigation: Use narrow Pilot topics and explicit event patterns or thresholds for each alert workflow. <br>
Risk: Unvalidated webhook URLs can route alerts outside approved systems. <br>
Mitigation: Validate webhook URLs against approved Slack, Discord, PagerDuty, or internal endpoints before deployment. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-alert) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON payload snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, curl, a running Pilot daemon, and trusted event sources or webhook destinations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
