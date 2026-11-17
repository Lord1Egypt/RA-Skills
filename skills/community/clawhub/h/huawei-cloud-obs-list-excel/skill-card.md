## Description:

Lists Huawei Cloud OBS buckets and produces a local Excel workbook, table, or JSON report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use the skill to inventory Huawei Cloud OBS buckets and prepare local reports for operations reviews. It supports Excel, table, and JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup weakens download security.

Mitigation: Restore certificate verification before setup and install verified dependencies in an isolated environment.

Risk: Configurable query paths may exceed the advertised endpoint or count restrictions, including through SDK fallback.

Mitigation: Clear executable and extra-argument overrides; do not rely on SDK fallback to enforce endpoint or count restrictions.

Risk: Cloud access uses configured OBS credentials.

Mitigation: Use bucket-list-only credentials with least-privilege IAM permissions.

## Reference(s):

- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [Least-privilege IAM policies](artifact/references/iam-policies.md)
- [Verification method](artifact/references/verification-method.md)
- [Huawei Cloud KooCLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Files, Text, JSON]

**Output Format:** [Excel (.xlsx) workbook, table text, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workbook can include an optional bucket-count summary row and is saved locally.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
