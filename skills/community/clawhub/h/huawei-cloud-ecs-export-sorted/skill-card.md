## Description:

Lists Huawei Cloud ECS instances, sorts them locally by a selected field, and exports the results as an XLSX workbook, CSV, JSON, or text table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to review ECS inventory for a Huawei Cloud region, sort instances by fields such as name, status, size, or creation time, and create a local report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer disables certificate verification, and telemetry data handling is unverified because the reporting wrapper was unavailable for inspection.

Mitigation: Prefer a corrected release that preserves certificate verification and makes telemetry optional. Review a pinned release and its reporting behavior before enabling telemetry.

Risk: Exported cloud inventory files may contain sensitive infrastructure details.

Mitigation: Use read-only cloud credentials and protect exported inventory files.

## Reference(s):

- [KooCLI installation guide](references/cli-installation-guide.md)
- [Least-privilege IAM policy](references/iam-policies.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Files, JSON, Text]

**Output Format:** [XLSX workbook, UTF-8-BOM CSV, structured JSON, or aligned text table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated locally; sorting is applied to fetched inventory, and missing sort values remain last.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
