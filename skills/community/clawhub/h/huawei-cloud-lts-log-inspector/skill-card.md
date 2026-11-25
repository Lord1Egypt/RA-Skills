## Description:

Analyzes Huawei Cloud LTS traffic and collection health, retrieves bounded log context, and manages scoped OBS transfers for batch export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations engineers use the skill to investigate LTS traffic changes, retrieve relevant log context, and check host collection status. For scoped batch exports, it can create and monitor OBS transfer tasks after a cost warning and user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An OBS transfer can create ongoing log copies and incur LTS transfer and OBS storage charges.

Mitigation: Warn about potential charges, confirm the log group, stream, destination, and transfer scope before creating a task, and require clear confirmation before deleting a transfer.

Risk: The downloaded hcloud installer may access local files and credentials.

Mitigation: Review the installer source and verify its integrity before running it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-lts-log-inspector)
- [hcloud CLI installation guide](references/cli-installation-guide.md)
- [LTS IAM policies](references/iam-policies.md)
- [LTS API command reference](references/lts-api-reference.md)
- [Verification method](references/verification-method.md)
- [Data flow diagram](references/dataflow-diagram.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Huawei Cloud hcloud CLI installer](https://hwcloudcli.obs.cn-north-1.myhuaweicloud.com/cli/latest/hcloud_install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic reports and concise log fragments, with shell command examples and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Log context is bounded to at most 500 lines before and after a target. OBS exports require a specific log group and stream; bulk export of all logs is not supported.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
