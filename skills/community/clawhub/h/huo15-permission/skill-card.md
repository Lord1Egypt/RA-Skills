## Description:

火一五权限 is a permission-control skill that checks user IDs to restrict skill-management and content-change operations, granting global administrator authority to ZhaoBo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace administrators use this skill to classify messages by userid and block non-admin users from installing or uninstalling skills or changing content they do not own.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hard-coded administrator receives broad global authority over skill installation, removal, and cross-user content changes.

Mitigation: Install only when ZhaoBo is intentionally the privileged administrator and the host platform independently authenticates userid metadata and enforces sensitive operations.

Risk: Automatic global interception can affect unrelated messages and skill management actions.

Mitigation: Review the policy before deployment and test admin and non-admin flows in the target workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/huo15-permission)
- [Publisher profile: jobzhao15](https://clawhub.ai/user/jobzhao15)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Plain text permission decisions and denial messages with JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses userid metadata, keyword matching, and a default restricted permission level for non-admin users.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
