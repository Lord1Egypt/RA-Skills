## Description:

Lists Huawei Cloud SCM certificates for one region with filters, expiry details, pagination, and compact, table, or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and security or operations teams use the skill to inventory Huawei Cloud SCM certificates, review expiry dates, and check certificate coverage before deployment or compliance reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags the additional quality and telemetry CLI, which may download and install executable software and make persistent local changes.

Mitigation: Review the quality CLI before running its installer; use the documented SDK backend if you do not want to install it, and set SKILL_QUALITY_REPORT=0 to disable telemetry reporting when using it.

## Reference(s):

- [KooCLI installation and configuration guide](references/cli-installation-guide.md)
- [Read-only SCM IAM policy](references/iam-policies.md)
- [Huawei Cloud KooCLI download guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text certificate list or table, or JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One region per run; certificate records include identity, domain, type, status, expiry, remaining days, and region.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
