## Description:

Anomaly detection for AI agents. Z-score, IQR, and streaming detection. Find outliers in data instantly. Sub-millisecond response. Works on single values or full datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and monitoring agents use this skill to check metrics, datasets, and recent data batches for anomalies with Z-score or IQR methods and to support alerting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted metrics or datasets may be sent to the external OraClaw anomaly-detection service.

Mitigation: Confirm the provider's privacy and retention terms fit the data before submitting sensitive datasets.

Risk: Use requires an ORACLAW_API_KEY and may incur per-call billing.

Mitigation: Confirm API key ownership, pricing, and billing expectations before enabling the skill in an agent workflow.

## Reference(s):

- [OraClaw Anomaly homepage](https://oraclaw.dev/anomaly)
- [ClawHub skill page](https://clawhub.ai/whatsonyourmind/skills/oraclaw-anomaly)

## Skill Output:

**Output Type(s):** [guidance, JSON]

**Output Format:** [Markdown guidance with JSON request and result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ORACLAW_API_KEY and may use a paid external OraClaw anomaly-detection service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
