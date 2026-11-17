## Description:

Log Anomaly Detector analyzes log text to identify error patterns, warning signals, possible performance bottlenecks, security-related indicators, and recommended follow-up actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honestqiao](https://clawhub.ai/user/honestqiao)

### License/Terms of Use:


## Use Case:

Developers, operators, and incident responders can use this skill to triage supplied log text for common error, warning, performance, and security indicators and receive concise recommendations for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on the skill as a complete security monitor or incident-response control.

Mitigation: Treat results as triage guidance and verify important findings with established logging, alerting, and incident-response tools.

Risk: The evidence notes reliability gaps in timestamp handling and warning, performance, and security checks.

Mitigation: Review or improve those checks before using the skill output for alerting, reporting, or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/honestqiao/skills/log-anomaly-detector)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON object containing detected errors, warnings, anomalies, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes a single supplied log string with an optional sensitivity setting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
