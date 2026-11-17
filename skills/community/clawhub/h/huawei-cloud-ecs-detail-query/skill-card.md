## Description:

Queries Huawei Cloud ECS instance details and instance lists through the Huawei Cloud KooCLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to inspect Huawei Cloud ECS instances, list ECS resources, and retrieve read-only instance details for operations, troubleshooting, and inventory tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the release suspicious because installation and credential guidance create review-worthy security risk.

Mitigation: Review the skill before installation, use a pinned and verified Huawei Cloud CLI installer when available, and run installers without elevated privileges.

Risk: Huawei Cloud AK/SK credentials may be persisted by hcloud configuration or exposed through shell history when entered directly.

Mitigation: Prefer least-privilege read-only IAM credentials, avoid placing long-lived AK/SK values directly in shell history, and understand where hcloud stores local configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/huawei-cloud-ecs-detail-query)
- [Huawei Cloud KooCLI documentation](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Huawei Cloud KooCLI Linux and macOS installer](https://cn-huaweicloud.obs.cn-north-1.myhuaweicloud.com/cli/latest/hcloud_install.sh)
- [Huawei Cloud KooCLI Windows package](https://cn-huaweicloud.obs.cn-north-1.myhuaweicloud.com/cli/latest/hcloud_windows.zip)
- [IAM permissions evidence](artifact/iam-policies.md)
- [CLI installation and authentication evidence](artifact/cli-installation-guide.md)
- [Dataflow evidence](artifact/dataflow-diagram.md)
- [Verification method evidence](artifact/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and formatted tables from CLI-backed ECS queries, with Markdown documentation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only ECS query output depends on configured Huawei Cloud credentials, region, filters, and KooCLI response data.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
