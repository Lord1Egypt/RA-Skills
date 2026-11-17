## Description:

Assesses Huawei Cloud CCE container environments by collecting metrics and configuration data, then generating scoring tables, reports, and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and cloud operations teams use this skill to assess Huawei Cloud CCE container environments against cloud-native best practices. It collects cluster, workload, Dockerfile, security, observability, elasticity, and resilience signals, then generates scoring tables, charts, reports, and improvement guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Huawei Cloud credentials and can collect sensitive CCE cluster and workload inventory.

Mitigation: Use temporary least-privilege read-only credentials in an isolated workspace, and treat generated data files and reports as sensitive.

Risk: Setup guidance includes remote installers, sudo usage, and cleanup commands that can affect the local system.

Mitigation: Review downloaded installers and any sudo or removal commands before execution; avoid non-interactive installation unless it has been independently verified.

Risk: The security review reports unsafe API practices and says TLS verification must be fixed before production use.

Mitigation: Do not use the skill against production environments until TLS verification and related API handling are reviewed and corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cce-env-assessment)
- [Huawei Cloud KooCLI Installation Guide](references/koocli-installation-guide.md)
- [Cloud-native checklist](references/cloud-native-checklist.xlsx)
- [Python requirements](references/requirements.txt)
- [Huawei Cloud KooCLI release notes](https://support.huaweicloud.com/wtsnew-hcli/index.html)
- [Huawei Cloud CCE version bulletin](https://support.huaweicloud.com/intl/zh-cn/bulletin-cce/cce_bulletin_0033.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown status updates, environment collection Markdown, Excel scoring workbook, SVG charts, and an HTML assessment report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are written under data/ and artifacts/ during the skill workflow.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
