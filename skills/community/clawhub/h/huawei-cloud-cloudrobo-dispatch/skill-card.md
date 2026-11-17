## Description:

Manage CloudRobo robot task dispatch by creating, monitoring, cancelling, and retrieving embodied task results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics operators use this skill to dispatch tasks to a selected robot and execution model, monitor progress, cancel tasks, and retrieve results in a workspace session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The verification helper may trigger robot movement or attempt task cancellation without affirmative confirmation.

Mitigation: Review before use, make the helper read-only or dry-run by default, and require explicit approval of the workspace, robot, action, and task for live operations. Use an isolated test robot or simulator with narrowly scoped credentials.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-dispatch)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [IAM policies](artifact/references/iam-policies.md)
- [Dataflow diagram](artifact/references/dataflow-diagram.md)
- [Validation rules](artifact/references/validation-rules.md)
- [Acceptance criteria](artifact/references/acceptance-criteria.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Task status and result summaries]

**Output Format:** [Markdown guidance with bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create or cancel robot tasks; live operations require explicit user approval.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
