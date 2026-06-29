## Description: <br>
Huawei Cloud AOM alarm correlation analysis skill for CCE operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CCE operators use this skill to query Huawei Cloud AOM active and historical alarms, correlate alarm groups, inspect CCE alarm health, and preview or confirm supported alarm-rule changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged dispatcher exposes broader Huawei Cloud and Kubernetes administration capabilities than the alarm-correlation description suggests. <br>
Mitigation: Install only after reviewing the packaged actions, and remove or avoid out-of-scope dispatcher actions before production use. <br>
Risk: The skill requires sensitive Huawei Cloud credentials and can access cloud alarm and cluster context. <br>
Mitigation: Use least-privilege temporary credentials through environment variables, avoid passing AK/SK as command parameters, and never log or persist credentials. <br>
Risk: Alarm-rule and action-rule mutations can change alerting behavior or suppress future notifications. <br>
Mitigation: Keep the documented preview-first workflow and require explicit user confirmation before adding confirm=true to mutation operations. <br>
Risk: ClawScan guidance flags subagent helpers as unsafe until credential redaction is fixed. <br>
Mitigation: Do not use the subagent helpers until credential redaction has been reviewed and corrected. <br>


## Reference(s): <br>
- [Huawei Cloud CCE event list](https://support.huaweicloud.com/usermanual-cce/cce_10_0902.html) <br>
- [Huawei Cloud API Explorer](https://support.huaweicloud.com/apiexplorer/index.html) <br>
- [Huawei Cloud Python SDK documentation](https://doc.huihua.com/api/sdk/python.html) <br>
- [Alarm correlation workflow](references/workflow.md) <br>
- [Risk rules](references/risk-rules.md) <br>
- [Output schema](references/output-schema.md) <br>
- [CCE event list reference](references/cce-event-list.md) <br>
- [CCE Prometheus metric alarm reference](references/cce-prometheus-metric-alarms.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON-compatible alarm summaries and dispatcher command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include alarm groups, timelines, likely related resources, recommended next skills, and preview/confirmation guidance for mutation operations.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
