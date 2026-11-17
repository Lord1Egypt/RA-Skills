## Description:

Scores Cainiao logistics suppliers and pickup station operators, producing risk levels, issue diagnoses, and recommended actions from KPI, complaint, compliance, and operating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Internal control and supplier management teams use this skill to assess logistics suppliers or pickup station operators, identify risk drivers, and plan review or remediation actions. It is a decision-support template and does not replace human approval for suspension, termination, or other enforcement decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational records may contain customer names, contact details, case IDs, or other unnecessary identifiers.

Mitigation: Redact personal or case-identifying details before pasting records into the agent.

Risk: Risk scores and recommendations could be mistaken for automated enforcement decisions.

Mitigation: Keep suspension, termination, and one-vote veto outcomes under human review.

Risk: The quality of scoring depends on the completeness and reliability of supplied KPI, complaint, and compliance data.

Mitigation: Flag missing data as gaps and reconcile self-reported values against platform or authoritative records before action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/inter-control-02-risk-scoring)
- [Continuation reference](references/continuation.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown risk scoring report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scoring details, risk level, data gaps, issue diagnosis, recommended actions, special warnings, and review timing.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
