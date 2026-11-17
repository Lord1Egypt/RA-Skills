## Description:

Query Huawei Cloud CCM certificate inventory and details, assess expiry status, and export results as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations and security teams use it to review Huawei Cloud SCM SSL certificate inventory, check expiry status, inspect certificate details, and prepare Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because a custom endpoint could send cloud authentication identifiers and signatures to an arbitrary HTTPS host.

Mitigation: Use the default regional SCM endpoint; configure a custom endpoint only when its host is verified and trusted.

Risk: The Skillspector scan was partial because four local references could not be resolved, leaving the security evidence incomplete.

Mitigation: Review the unresolved references and endpoint configuration before installing or using the skill.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ccm-certificate-query)
- [API reference](references/api.md)
- [Least-privilege IAM policies](references/iam-policies.md)
- [Markdown export guide](references/markdown-export.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Aligned text tables and field lists, structured JSON, and Markdown inventory reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes derived expiry days and grades; Markdown reports are saved locally and echoed to stdout.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
