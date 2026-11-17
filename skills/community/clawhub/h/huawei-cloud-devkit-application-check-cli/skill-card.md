## Description:

Uses Kunpeng DevKit CLI to collect software inventory, analyze Maven dependency compatibility, manage Huawei Cloud ECS setup, and generate migration assessment reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and migration engineers use this skill to assess application systems for Huawei Kunpeng migration, provision or reuse a DevKit ECS environment, run compatibility scans, and collect reports.

### Deployment Geography for Use:

Huawei Cloud regions supported by the skill: cn-north-4, cn-east-3, cn-south-1, and cn-southwest-2.

## Known Risks and Mitigations:

Risk: The workflow can create or reuse cloud resources, connect over SSH, upload scripts, install dependencies, run scans, and download reports.

Mitigation: Require explicit parameter confirmation before cloud, SSH, upload, install, scan, or report download steps; use least-privileged cloud credentials.

Risk: AK/SK values, DevKit ECS passwords, and target-server passwords may be exposed through chat output, command logs, or node configuration files.

Mitigation: Mask secrets in all user-facing output, avoid plaintext credential display, encrypt nodes.conf passwords before scans, and rotate or remove stored passwords after use.

Risk: Unsafe SSH host verification can connect the agent to an unexpected host.

Mitigation: Verify SSH host fingerprints out of band before SSH, upload, install, scan, or report download operations.

Risk: Retrying non-idempotent create operations can duplicate ECS, VPC, subnet, security group, or EIP resources and incur charges.

Mitigation: Query existing resources first, save create responses before parsing, and query by name after parse failures instead of rerunning create commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-devkit-application-check-cli)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [Prerequisites](references/prerequisites.md)
- [ECS Creation](references/ecs-creation.md)
- [DevKit Operations Guide](references/devkit-operations-guide.md)
- [DevKit Operations Workflow](references/devkit-operations-workflow.md)
- [Security Rules](references/rules.md)
- [IAM Permission Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Troubleshooting](references/troubleshooting.md)
- [Huawei Cloud KooCLI Installer](https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/hcloud_install.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Simplified Chinese Markdown with inline shell commands, parameter confirmations, status summaries, and report download guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Credentials and node configuration secrets should be masked; scan reports may be downloaded as files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists v1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
