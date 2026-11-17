## Description:

Helps manage Huawei Cloud ECS instances, inspect quotas and available resources, and diagnose instance creation failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to query and manage Huawei Cloud ECS instances and diagnose creation failures across quota, flavor, image, network, keypair, and disk checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, change, or delete cloud instances, potentially causing service disruption or data loss.

Mitigation: Use a low-privilege account, omit create/delete permissions unless needed, and confirm each instance change after reviewing its target and command.

Risk: The installed reporting wrapper sends command output and local agent-session metadata with under-disclosed scope.

Mitigation: Review the reporting behavior before installation and set SKILL_QUALITY_REPORT=0 if telemetry is not acceptable.

Risk: The installer modifies shell startup files and places a persistent wrapper in ~/.local/bin.

Mitigation: Review the installer and resulting shell configuration before running the skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ecs-manage)
- [Huawei Cloud KooCLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-privilege IAM policies](references/iam-policies.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with commands, structured JSON summaries, and diagnosis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview and explicit confirmation required before instance changes; deletion requires an irreversible-action warning.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
