## Description:

Monitor package logistics status and identify delivery anomalies such as delays, stalls, returns, failed delivery, customs/security holds, or abnormal signing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Buyers, sellers, support teams, and logistics operators use this skill to classify shipment status, identify delivery anomalies, and decide the next action for refunds, reshipments, carrier escalation, or customer follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shipment IDs, delivery routes, and package names may remain in local plaintext storage.

Mitigation: Review before installing on machines handling sensitive shipment data and remove tracked package data when it is no longer needed.

## Reference(s):

- [ClawHub skill listing: Logistics Watcher](https://clawhub.ai/harrylabsj/skills/logistics-watcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured text or Markdown status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a redacted package identifier, anomaly classification, latest tracking evidence, customer-impact risk, next actions, and watch conditions.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
