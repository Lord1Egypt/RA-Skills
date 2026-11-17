## Description:

Audit Huawei Cloud skills for quality, security, and compliance, producing structured reports with findings and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to scan one or more Huawei Cloud skills and review a report of security, credential, and runtime-pattern findings with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports weaknesses in audit checks and incomplete scan coverage, so findings may not reveal every problem in a skill.

Mitigation: Treat reports as one input; verify important findings and review coverage independently before relying on a passing result.

Risk: The security review reports possible external sharing of scanned content.

Mitigation: Avoid scanning sensitive source until data handling is verified; disable the skill's quality telemetry report with SKILL_QUALITY_REPORT=0 when appropriate.

Risk: The security review reports cloud operations beyond the stated audit purpose.

Mitigation: Use an isolated environment and least-privilege credentials, and omit cloud credentials when they are not needed.

## Reference(s):

- [Huawei Cloud Skill Audit on ClawHub](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-skill-audit)
- [Verification Method](references/verification-method.md)
- [Security Audit Guide](references/security-audit-guide.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [CLI Installation Guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, Text]

**Output Format:** [Plain-text audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes scan results, issues, and suggested fixes.]

## Skill Version(s):

1.0.11 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
