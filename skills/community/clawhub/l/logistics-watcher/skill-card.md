## Description: <br>
Logistics Watcher monitors package logistics status and identifies delivery anomalies such as delays, stalls, returns, failed delivery, customs or security holds, and abnormal signing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Buyers, sellers, support teams, and operations teams use this skill to turn carrier tracking events into logistics anomaly classifications, customer-facing next steps, escalation guidance, and watch conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shipment history may be saved locally in plaintext. <br>
Mitigation: Use the skill only on machines where local files are protected, and review how to delete or retain old tracking records before using it with sensitive shipment data. <br>
Risk: Tracking summaries can expose addresses, phone numbers, or full tracking numbers if copied outside the user's private context. <br>
Mitigation: Redact addresses, phone numbers, and full tracking numbers in shared summaries. <br>
Risk: Carrier screenshots or user descriptions may be incomplete or stale. <br>
Mitigation: Treat carrier data as the source of truth and label conclusions as provisional when only user-provided descriptions or screenshots are available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/logistics-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text logistics triage report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a partially redacted tracking identifier, anomaly status, evidence, risk level, next action, and watch condition.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
