## Description:

Guides migration of vision, detection, and segmentation models to Ascend NPU using torch_npu and msprof for model analysis, migration verification, performance profiling, and optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate encoder-only, detection, and segmentation models such as ResNet, YOLO, and UNet to Ascend NPU, then verify inference behavior and analyze performance bottlenecks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact exposes a root SSH credential for a named server and repeatedly directs root access.

Mitigation: Treat the credential as exposed, rotate it if real, and require users to provide least-privilege SSH credentials through a secret manager or explicit interactive approval.

Risk: The workflow includes package installation, Docker commands, SSH access, and hardware-specific profiling actions that can affect a host environment.

Mitigation: Run migration and profiling steps only in an isolated container or test host, and limit use to explicit Ascend NPU migration tasks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ascend-small-model-migrate)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Verification Method](references/verification-method.md)
- [Troubleshooting](references/troubleshooting.md)
- [Report Template](references/report-template.md)
- [Profiler SQL](references/profiler-sql.md)
- [Migration Scripts](references/migration-scripts.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports with inline Python, SQL, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include migration verification reports, profiling summaries, bottleneck tables, and optimization recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
