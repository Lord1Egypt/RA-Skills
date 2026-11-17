## Description:

Review tool usage patterns, permission configurations, and detect security policy violations in session transcripts and evolution state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers can audit tool activity, environment flags, and tool policy configuration in a workspace to identify suspicious patterns and guide follow-up review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan had partial component coverage, so its benign verdict provides incomplete assurance.

Mitigation: Review the uninspected code and missing local references, and confirm coverage with a complete scan before relying on the verdict.

Risk: Auditing workspace session logs and environment files may expose sensitive information in the report or its surrounding workflow.

Mitigation: Limit audits to authorized workspaces and handle session logs and reports as sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/147258xuan/skills/permission-auditor)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Plain-text audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes usage counts, detected patterns, severity labels, and recommendations.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
