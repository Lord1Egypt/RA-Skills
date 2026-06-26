## Description: <br>
Analyzes provided log text to identify errors, warnings, performance bottlenecks, security-related patterns, and recommended follow-up actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HonestQiao](https://clawhub.ai/user/HonestQiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to triage application or system logs by surfacing common error, warning, performance, and security indicators with concise recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logs can contain secrets, credentials, or personal data. <br>
Mitigation: Review or redact sensitive log lines before submitting them to an agent workflow. <br>
Risk: Keyword-based log triage can miss subtle incidents or overflag benign entries. <br>
Mitigation: Treat findings as triage guidance and verify important results against source logs and monitoring data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON-like findings with errors, warnings, anomalies, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyzes user-provided log text and an optional sensitivity setting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
