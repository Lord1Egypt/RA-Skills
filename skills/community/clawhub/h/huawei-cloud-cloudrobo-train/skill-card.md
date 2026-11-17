## Description:

Manage Huawei Cloud CloudRobo model-training and simulation reinforcement learning tasks from configuration and submission through monitoring and diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure, submit, monitor, and troubleshoot CloudRobo model-training and SimRL tasks in a selected Huawei Cloud workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting training or SimRL tasks can start paid cloud compute jobs.

Mitigation: Require clear user approval before submission and set compute limits for the selected workspace.

Risk: Deleting a task is irreversible.

Mitigation: Confirm the task ID and obtain clear user approval before deletion.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-train)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [Authentication & Access Control](references/iam-policies.md)
- [SDK Quick Start](references/sdk-quickstart.md)
- [API Paths](references/api-paths.md)
- [Task Config Reference](references/task-config-catalog.md)
- [Verification Method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
