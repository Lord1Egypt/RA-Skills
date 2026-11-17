## Description:

Audit AWS IAM policies and roles for over-privilege, wildcard permissions, and least-privilege violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Security engineers, cloud engineers, and developers use this skill to review AWS IAM policies and roles for risky permissions, attack paths, and least-privilege remediation options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IAM policy review may involve sensitive policy documents, role details, or account context.

Mitigation: Provide only IAM policy JSON or role details needed for the audit, and avoid unrelated AWS credentials or private account data.

Risk: Least-privilege replacement policies and remediation recommendations may not fully preserve intended production behavior.

Mitigation: Have an AWS security reviewer validate proposed changes before applying them in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anmolnagpal/skills/iam-policy-auditor)
- [ClawHub publisher profile](https://clawhub.ai/user/anmolnagpal)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with findings tables and IAM policy JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk score, MITRE ATT&CK mapping, remediation recommendations, IAM Access Analyzer guidance, and severity summary.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
