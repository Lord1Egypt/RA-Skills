## Description:

Guides private-network migration of Linux x86_64 VMware virtual machines to Huawei Cloud ECS over a VPN using a proxy ECS and batch migration tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure engineers use this skill to plan and run batch migrations of Linux x86_64 VMware VMs to Huawei Cloud ECS across VPN-connected private networks, including proxy setup and post-migration checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permanent cloud credentials and root SSH access can expose sensitive systems.

Mitigation: Use narrowly scoped credentials, review credential persistence, and protect access to source and proxy hosts.

Risk: Unsafe SSH host-key handling could permit connecting to an untrusted host.

Mitigation: Review the host-key policy and verify host fingerprints out of band before migration.

Risk: Broad proxy access and permissive network rules could expose migration services.

Mitigation: Review Squid ACLs and restrict source CIDRs and proxy access.

Risk: Command-launch behavior and migration changes can disrupt production hosts.

Mitigation: Review commands before execution and require backups and an explicit rollback plan for production hosts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-migration-vmware-ecs-private)
- [Huawei Cloud hcloud CLI configuration guide](https://support.huaweicloud.com/usermanual-hcli/hcli_03_002.html)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Migration runs can also produce JSON results and logs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
