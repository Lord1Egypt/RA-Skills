## Description:

Diagnoses abnormal 4xx and 5xx responses on Huawei Cloud CDN domains using read-only statistics, configuration queries, and access-log analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

CDN operators and engineers use this skill to investigate abnormal HTTP status codes, distinguish edge-generated from origin-generated errors, and prepare an evidence-based diagnosis without changing CDN configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials may be exposed while querying CDN data.

Mitigation: Use least-privilege read-only IAM and an existing CLI profile; never paste access keys into chat or reports.

Risk: Downloaded access logs and diagnosis outputs can expose client IPs, URLs, user agents, or referers.

Mitigation: Keep query windows narrow and redact or limit sensitive log fields and rows before sharing results.

Risk: Applying configuration changes during troubleshooting can affect production traffic.

Mitigation: Keep skill operations read-only; require a separate, manually authorized workflow for remediation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cdn-abnormal-status-code-analysis)
- [Huawei Cloud CDN access-log format](https://support.huaweicloud.com/intl/zh-cn/bestpractice-cdn/cdn_01_0252.html)
- [Read-only IAM policies](references/iam-policies.md)
- [Diagnosis report template](references/task-report.md)
- [Prohibited CDN operations](references/prohibited-operations.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain-text diagnosis report, JSON log findings, and read-only CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports status-code volume, edge/origin attribution, supporting evidence, and suggested manual remediation.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
