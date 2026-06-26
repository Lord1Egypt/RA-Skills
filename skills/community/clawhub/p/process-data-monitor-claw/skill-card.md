## Description: <br>
Helps agents configure business process monitoring, anomaly thresholds, Feishu alert routing, and recurring operational reports for workflows such as fulfillment, inventory, payments, and data pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to turn natural-language monitoring requirements into structured data-source, rule, threshold, cooldown, and notification configurations. It also provides shell helpers for running a monitoring daemon and sending Feishu-based alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Continuous monitoring can access sensitive operational data and distribute alert content outside the source system. <br>
Mitigation: Use dedicated read-only accounts, keep credentials and Feishu tokens in environment variables, and avoid placing secrets or sensitive data in alert messages. <br>
Risk: Misconfigured alert routing can notify the wrong Feishu group or user and expose business incidents unnecessarily. <br>
Mitigation: Confirm webhook destinations, bot tokens, recipient open IDs, and alert severity routing before enabling automated notifications. <br>
Risk: The release declares crypto and purchasing-related capabilities that are not required for normal monitoring use. <br>
Mitigation: Do not grant crypto or purchasing authority unless a separate reviewed workflow explicitly requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/process-data-monitor-claw) <br>
- [Alert rule templates](references/alert-rules.md) <br>
- [Data source integration guide](references/data-sources.md) <br>
- [Monitoring metrics library](references/metrics-library.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML configuration examples and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference environment variables for database credentials, API tokens, Feishu webhooks, and bot tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
