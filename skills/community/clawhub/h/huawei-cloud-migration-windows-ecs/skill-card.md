## Description:

Automates Huawei Cloud SMS migrations of supported Windows hosts to ECS through public or private networking, including batch orchestration, verification, and cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud and systems administrators use this skill to plan and run public, private, or batch migrations of supported Windows hosts to Huawei Cloud ECS with SMS, then verify the target and clean up migration resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with high confidence, citing serious security and operational risks; some packaged executable behavior remains unverified. Migration workflows also use credentials and can provision or clean cloud resources.

Mitigation: Before use, review the packaged executables' provenance and behavior and determine whether the proxy, storage, credential, cleanup, and provisioning actions are safe for the environment. Review the resources and scope before running migration or cleanup commands; partial scanner coverage does not establish that unreviewed material is safe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-migration-windows-ecs)
- [Migration safety rules](artifact/references/safety-rules.md)
- [Migration workflow](artifact/references/migration-workflow.md)
- [SMS CLI commands](artifact/references/cli-commands.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with shell commands, PowerShell checks, and YAML/JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include migration and cleanup commands that act on Windows hosts and Huawei Cloud resources.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
