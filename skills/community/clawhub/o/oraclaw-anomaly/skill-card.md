## Description: <br>
Anomaly detection for AI agents. Z-score, IQR, and streaming detection. Find outliers in data instantly. Sub-millisecond response. Works on single values or full datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and monitoring agents use this skill to check abnormal metric values, find dataset outliers, monitor recent data batches, and set up anomaly alerts using Z-score or IQR methods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Data sent for anomaly detection is processed by an external Oraclaw service. <br>
Mitigation: Do not send secrets, regulated data, or sensitive operational metrics unless Oraclaw's privacy and retention terms are acceptable. <br>
Risk: Streaming or alerting workflows can create unexpected paid detection calls after the free tier. <br>
Mitigation: Set explicit usage limits, budgets, and alerting thresholds before enabling continuous monitoring. <br>
Risk: Incorrect method or threshold choices can produce misleading anomaly results. <br>
Mitigation: Use Z-score for roughly normal data, IQR for skewed data, require sufficient sample sizes, and tune thresholds for the monitored metric. <br>


## Reference(s): <br>
- [Oraclaw Anomaly homepage](https://oraclaw.dev/anomaly) <br>
- [ClawHub listing](https://clawhub.ai/whatsonyourmind/oraclaw-anomaly) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with JSON request examples and structured anomaly-detection results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ORACLAW_API_KEY; supports z-score and IQR thresholds; paid per detection call after the free tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
