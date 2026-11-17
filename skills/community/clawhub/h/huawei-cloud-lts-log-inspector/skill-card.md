## Description:

Huawei Cloud LTS Log Inspector helps agents analyze log traffic, inspect collection health, retrieve concise log context, and manage scoped OBS transfer tasks for batch log export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and cloud support engineers use this skill to troubleshoot Huawei Cloud LTS traffic surges, collection outages, log flooding, and targeted historical log export workflows.

### Deployment Geography for Use:

Global where Huawei Cloud LTS and OBS services are available.

## Known Risks and Mitigations:

Risk: The skill can expose or act on cloud log data from the wrong Huawei Cloud account or region.

Mitigation: Verify the active hcloud profile, target account, and region before running reports or transfer operations.

Risk: OBS transfer creation or deletion can incur cost, alter export configuration, or affect stored log exports.

Mitigation: Use read-only IAM permissions unless export management is required, and require explicit confirmation before CreateTransfer or DeleteTransfer.

Risk: Batch export can create excessive storage or transfer volume if scope is too broad.

Mitigation: Require a specific log group and log stream, show the cost and storage warning before execution, and avoid bulk export of all logs.

Risk: Large or sensitive log context output can be difficult to review safely.

Mitigation: Return concise context fragments within the documented size limits and avoid full-log dumps in diagnostic output.

## Reference(s):

- [hcloud CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [IAM Policies for LTS Log Inspector](artifact/references/iam-policies.md)
- [Verification Method](artifact/references/verification-method.md)
- [LTS API Command Quick Reference](artifact/references/lts-api-reference.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Data Flow Diagram](artifact/references/dataflow-diagram.md)
- [Huawei Cloud hcloud CLI Installer](https://hwcloudcli.obs.cn-north-1.myhuaweicloud.com/cli/latest/hcloud_install.sh)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline hcloud CLI commands and structured diagnostic checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Context log fragments are bounded by documented before/after limits, and OBS transfer actions require confirmation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
