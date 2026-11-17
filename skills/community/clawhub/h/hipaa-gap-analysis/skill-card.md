## Description:

Assess compliance documents against HIPAA Security Rule and Privacy Rule requirements. Produces structured findings with evidence, gap descriptions, and remediation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

Apache-2.0

## Use Case:

Compliance, privacy, and security teams use this skill to review policy or procedure documents against HIPAA Security Rule and Privacy Rule requirements and receive structured control findings, evidence, gaps, and remediation recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs access to compliance documents supplied by the user, which may contain sensitive operational, security, or health information.

Mitigation: Use it only in environments where the agent is permitted to read those documents, and limit inputs to materials appropriate for the agent runtime.

Risk: HIPAA findings and remediation recommendations may be mistaken for legal or audit conclusions.

Mitigation: Treat the output as audit support and have qualified reviewers verify quoted evidence, gaps, and recommendations before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dangsllc/skills/hipaa-gap-analysis)
- [Publisher profile](https://clawhub.ai/user/dangsllc)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured HIPAA control findings with document title, analysis date, framework, summary counts, evidence text, gap descriptions, recommendations, confidence scores, and reasoning.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
