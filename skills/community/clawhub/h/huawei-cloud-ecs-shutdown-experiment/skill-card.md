## Description:

Full lifecycle ECS shutdown fault injection experiment for Huawei Cloud chaos engineering, covering preparation, execution with rollback, and post-experiment CES and LTS analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud reliability engineers, and SRE teams use this skill to plan and run controlled Huawei Cloud ECS shutdown experiments, then collect monitoring metrics and logs to assess service impact and recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real ECS shutdown operations can interrupt services and cause downtime.

Mitigation: Run dry-runs first, confirm the exact target instance IDs and maintenance window, require explicit execution confirmation, and keep rollback access ready.

Risk: Incorrect or non-resilient targets can increase outage or rollback risk.

Mitigation: Use the prepare-phase discovery and validation checks before execution, review validation warnings, and avoid targets that cannot tolerate interruption.

Risk: Overbroad Huawei Cloud credentials could expand the impact of misuse or mistakes.

Mitigation: Use least-privilege, resource-scoped credentials and the documented phase-specific IAM permissions.

Risk: The documented /etc/hosts workaround can affect local networking if applied incorrectly.

Mitigation: Avoid the workaround unless an administrator explicitly approves it, back up the hosts file before changes, and verify rollback afterward.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ecs-shutdown-experiment)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [ECS Validation Rules](references/ecs-validation-rules.md)
- [Experiment Template Guide](references/experiment-template-guide.md)
- [Execution Workflow](references/execution-workflow.md)
- [Analysis Workflow](references/analysis-workflow.md)
- [Verification Method](references/verification-method.md)
- [Huawei Cloud KooCLI Documentation](https://support.huaweicloud.com/developer-hcli/hcli_01_0001.html)
- [Huawei Cloud KooCLI Download](https://support.huaweicloud.com/developer-hcli/hcli_02_0001.html)
- [Huawei Cloud ECS BatchStopServers API](https://support.huaweicloud.com/api-ecs/ecs_02_0302.html)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with bash commands plus JSON configuration and log files and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce experiment.json, rollback scripts, execution-log.json, log-analysis-result.json, execution-report.md, and log-analysis-report.md when the workflows are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
