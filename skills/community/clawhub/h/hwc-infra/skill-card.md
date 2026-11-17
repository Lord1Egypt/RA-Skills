## Description:

Huawei Cloud Infra helps agents use KooCLI (hcloud) to query, audit, monitor, and perform explicitly confirmed changes for Huawei Cloud ECS, VPC, and RDS resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5xuanwen](https://clawhub.ai/user/5xuanwen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and cloud administrators use this skill to inspect Huawei Cloud infrastructure state, review ECS, VPC, and RDS resources, and prepare cloud management commands with explicit confirmation for changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide installation of a local KooCLI binary and configure persistent Huawei Cloud credentials.

Mitigation: Review the installer before use, prefer verified Huawei Cloud installation instructions, and configure least-privilege AK/SK credentials.

Risk: The skill can prepare cloud-admin commands, including stop, restart, delete, and other write operations.

Mitigation: Require explicit user confirmation and show the exact command before any write or destructive operation.

Risk: Credential exposure would create cloud account risk.

Mitigation: Do not print, store in transcripts, or otherwise expose AK/SK values; use existing local KooCLI configuration when available.

## Reference(s):

- [KooCLI (hcloud) common commands](references/hcloud-queries.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Huawei Cloud KooCLI download source](https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/)
- [ClawHub skill page](https://clawhub.ai/5xuanwen/skills/hwc-infra)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid exposing AK/SK credentials and should request explicit confirmation before write or destructive cloud operations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
