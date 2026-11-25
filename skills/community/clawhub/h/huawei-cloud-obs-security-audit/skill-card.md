## Description:

Audits Huawei Cloud OBS bucket security settings and produces a scored report with risks and remediation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and security engineers use this skill to review an OBS bucket's access controls and related security settings, then prioritize remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports automatic telemetry with unspecified contents.

Mitigation: Review the telemetry behavior before use; set SKILL_QUALITY_REPORT=0 to disable reporting if it is not acceptable.

Risk: ClawScan flags remote installation of an unauthenticated CLI.

Mitigation: Review the installer and verify the CLI package through a trusted channel before installing it, or use a separately vetted installation.

Risk: ClawScan says replication or logging checks may misrepresent bucket settings, and the scan evidence is incomplete.

Mitigation: Confirm replication and logging settings directly in the Huawei Cloud console or another trusted source before relying on the score or recommendations.

Risk: ClawScan reports a command argument risk.

Mitigation: Review the target bucket and command arguments before execution, and use a least-privilege read-only account.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-obs-security-audit)
- [Huawei Cloud KooCLI documentation](https://support.huaweicloud.com/cli/index.html)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [Least-Privilege IAM Policies](references/iam-policies.md)
- [Security Check Catalog](references/security-check-catalog.md)
- [Verification Method](references/verification-method.md)
- [Related Commands](references/related-commands.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Text or JSON security audit report with a score, findings, risk levels, and remediation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries bucket configuration and object names; intended audit actions are read-only.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
