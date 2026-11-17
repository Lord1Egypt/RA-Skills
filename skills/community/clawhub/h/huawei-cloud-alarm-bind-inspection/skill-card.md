## Description:

Inspects Huawei Cloud alarm baseline coverage by comparing CES and AOM alarm rules with metric and event baselines, then produces instance-level reports and remediation suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations engineers use this skill to compare Huawei Cloud CES and AOM alarm rules with metric and event baselines, then review instance-level binding reports and remediation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with high confidence, citing insecure CES connections and persistent system DNS changes outside the alarm-inspection purpose; its analysis was incomplete.

Mitigation: Review DNS and TLS behavior, installer and image sources, and removal commands before installation. Use a controlled environment while evaluating it, since scanner coverage did not include every component or executable content in the spreadsheet.

## Reference(s):

- [Verification Method](references/verification-method.md)
- [IAM Policies and Configuration](references/iam-policies.md)
- [KooCLI Installation Guide](references/cli-installation-guide.md)
- [Huawei Cloud IAM Documentation](https://support.huaweicloud.com/usermanual-iam/iam_01_0001.html)
- [Huawei Cloud CES API Documentation](https://support.huaweicloud.com/api-ces/ces_03_0001.html)
- [Huawei Cloud AOM API Documentation](https://support.huaweicloud.com/api-aom/aom_04_0001.html)
- [Huawei Cloud KooCLI Documentation](https://support.huaweicloud.com/wtsnew-hcli/index.html)

## Skill Output:

**Output Type(s):** [JSON files, Excel spreadsheets, HTML report, Shell commands]

**Output Format:** [Intermediate JSON, Excel (.xlsx) reports, and an HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account-specific alarm rules and resource data; requires Huawei Cloud credentials and the hcloud CLI.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
