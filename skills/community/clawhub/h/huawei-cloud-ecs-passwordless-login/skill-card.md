## Description:

Configures passwordless SSH access to Huawei Cloud ECS instances through COC, including key deployment, connection checks, and scheduled key cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to set up and test temporary SSH key access across one or more Huawei Cloud ECS instances through COC.

### Deployment Geography for Use:

COC endpoints in cn-north-4 (China site) or ap-southeast-3 (international site); target ECS instances may be in other regions.

## Known Risks and Mitigations:

Risk: Authenticated cloud permissions and remote script execution can affect the wrong or overly broad set of instances.

Mitigation: Confirm exact target instances and permissions before execution; avoid root access where possible.

Risk: Reused COC scripts could contain unreviewed commands.

Mitigation: Verify the content of any existing script before reuse.

Risk: Disabling SSH host-key checks makes connections vulnerable to impersonation.

Mitigation: Keep host-key verification enabled when feasible.

Risk: Persistent SSH master sessions can preserve access after temporary keys are deleted.

Mitigation: Explicitly close ControlMaster sessions and remove their sockets and SSH config entries when access should end.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ecs-passwordless-login)
- [IAM policies](references/iam-policies.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides SSH connection checks and cleanup guidance; SSH sessions may persist after keys are removed.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
