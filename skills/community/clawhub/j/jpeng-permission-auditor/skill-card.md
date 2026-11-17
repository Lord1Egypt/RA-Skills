## Description:

Audit tool usage patterns and permissions to identify security risks and excessive access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to analyze agent tool logs, compare required and granted permissions, and produce concise security audit reports with recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rule-based scoring can miss context or overstate risk for unfamiliar tool logs.

Mitigation: Treat reports as advisory and confirm findings against actual authorization records, logs, and deployment policy.

Risk: Example paths may not match a different skills directory layout.

Mitigation: Check import and CLI paths before integrating the helper into another repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-permission-auditor)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [JavaScript objects and formatted text reports, with Markdown and shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include risk distribution, detected patterns, anomalies, and recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
