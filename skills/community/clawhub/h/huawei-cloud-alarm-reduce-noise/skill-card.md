## Description:

Analyzes Huawei Cloud CES and AOM alarm data to identify noise patterns and generate recommendations and an HTML optimization report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations engineers use it to review multi-region CES and AOM alarm trends, prioritize noisy or unresolved alarms, and generate recommendations for alarm governance and convergence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill suspicious because of a reported unsafe remote installer.

Mitigation: Review the installer source and verify it against Huawei Cloud's official installation documentation before running it.

Risk: The security scan reports destructive CLI cleanup instructions.

Mitigation: Review cleanup targets and confirm backups before running any removal command.

Risk: The security scan reports a possible script injection issue in generated HTML reports.

Mitigation: Treat generated reports as untrusted HTML and open them in an isolated browser context until the issue is resolved.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-alarm-reduce-noise)
- [Alarm analysis guide](references/alarm-analysis.md)
- [IAM permissions guide](references/iam-policies.md)
- [Huawei Cloud KooCLI installation guide](references/cli-installation-guide.md)
- [Huawei Cloud KooCLI documentation](https://support.huaweicloud.com/wtsnew-hcli/index.html)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, HTML, JSON]

**Output Format:** [HTML optimization report, JSON data files, and written recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Multi-region alarm analysis with prioritization and a region switcher in the report.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
