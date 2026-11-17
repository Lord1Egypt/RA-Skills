## Description:

Diagnoses Huawei Cloud CDN HTTPS certificate configuration and expiry by comparing configured details with the certificate served at the edge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

CDN operators and engineers use this skill to diagnose certificate configuration, deployment, and expiration problems on authorized Huawei Cloud CDN domains without changing CDN settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports and API responses can reveal CDN domain and certificate metadata.

Mitigation: Redact domain and certificate details before sharing raw responses or generated reports.

Risk: Overprivileged access or exposed cloud credentials can put the account at risk.

Mitigation: Use a least-privilege read-only IAM user on authorized domains and never paste AK/SK credentials into chat.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cdn-certificate-diagnosis)
- [Certificate verification method](artifact/references/verification-method.md)
- [Diagnosis report format](artifact/references/task-report-generation.md)
- [Read-only operation boundaries](artifact/references/prohibited-operations.md)
- [Huawei Cloud CLI documentation](https://support.huaweicloud.com/hcloudcli/index.html)

## Skill Output:

**Output Type(s):** [Text, Guidance, JSON diagnostic results]

**Output Format:** [Structured text diagnosis report with JSON probe results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes certificate status, validity dates, days remaining, and recommended next steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; source frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
