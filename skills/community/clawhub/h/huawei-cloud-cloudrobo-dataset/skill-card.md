## Description:

Manage CloudRobo processing and evaluation tasks, including task lifecycle operations, logs and output review, processing-to-evaluation workflows, custom operator onboarding, and ROS2 bag-to-LeRobot manifest preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics or data engineers use this skill to manage CloudRobo processing and evaluation jobs, diagnose results, onboard custom operators, and prepare ROS2 bag manifests for LeRobot conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unauthenticated web preview may expose local recording details.

Mitigation: Review the preview's exposure before use, keep it limited to trusted local access, and avoid using sensitive recordings until its handling is understood.

Risk: The security review reports unsafe command execution patterns and calls out the shell-based test runner.

Mitigation: Inspect shell commands and scripts before running them, especially commands that install software, change group membership, or clean up files.

Risk: The security review calls out broad privilege guidance, cleanup commands, and credential handling.

Mitigation: Review elevated and cleanup commands for their targets and scope, and protect CloudRobo credentials while following the documented credential-handling guidance.

Risk: ClawScan inspected 47 of 56 components fully and 9 partially.

Mitigation: Resolve the incomplete scan coverage and review the identified areas before installing or relying on the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-dataset)
- [Interactive workflow](references/interactive-workflow.md)
- [Task configuration catalog](references/task-config-catalog.md)
- [Custom operator workflow](references/custom-operator/custom-operator-workflow.md)
- [IAM policies](references/iam-policies.md)
- [Bag to manifest](references/bag2manifest.md)
- [Huawei Cloud API Explorer](https://console.huaweicloud.com/apiexplorer/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Analysis]

**Output Format:** [Markdown guidance, shell commands, code, JSON or YAML task configuration, and ROS manifest.yaml files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task status and log summaries, output previews, and configuration files for downstream processing.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
