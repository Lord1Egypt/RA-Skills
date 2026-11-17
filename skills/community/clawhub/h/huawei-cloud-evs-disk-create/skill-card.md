## Description:

Guides agents through creating Huawei Cloud EVS disks, including disk type, size, availability zone, snapshot, and batch options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to plan, create, and verify individual or multiple Huawei Cloud EVS disks using KooCLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing cloud CLI tooling from an unverified script, especially in silent or root mode, may expose the environment to unsafe software.

Mitigation: Use a verified Huawei Cloud CLI installation source and avoid silent or root installation unless necessary.

Risk: Broad EVS FullAccess permissions grant more cloud access than disk creation requires.

Mitigation: Prefer the documented minimum custom IAM policy over EVS FullAccess.

Risk: Single or batch disk creation can incur cloud costs; batch execution can skip its confirmation prompt.

Mitigation: Require explicit user confirmation of region, zone, size, type, and disk count before any creation, including batch runs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-evs-disk-create)
- [KooCLI installation guide](references/cli-installation-guide.md)
- [IAM permission policies](references/iam-policies.md)
- [Disk verification method](references/verification-method.md)
- [EVS API reference](https://support.huaweicloud.com/api-evs/index.html)
- [KooCLI EVS command help](https://support.huaweicloud.com/cli-koocli/koocli_02_0034.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes disk creation and verification steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
