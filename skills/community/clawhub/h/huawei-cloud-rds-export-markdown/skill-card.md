## Description:

Lists Huawei Cloud RDS instances in a selected region and exports their inventory details to a local Markdown file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and database engineers use this skill to list Huawei Cloud RDS instances in a selected region and save an inventory, patrol, or handover report as a local Markdown file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags an unrelated CLI dependency and installation downloads whose TLS certificate checks are disabled.

Mitigation: Review the need for the additional CLI before installation, and use independently trusted dependency verification with TLS certificate checks enabled.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-rds-export-markdown)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI installation and credentials guide](artifact/references/cli-installation-guide.md)
- [Least-privilege IAM policy](artifact/references/iam-policies.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Files, Markdown]

**Output Format:** [Local Markdown table file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [RDS instance inventory with optional region, project, name and status filters, and local sorting.]

## Skill Version(s):

1.0.10 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
