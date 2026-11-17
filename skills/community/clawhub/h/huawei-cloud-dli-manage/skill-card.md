## Description:

Guides Huawei Cloud DLI resource management, job troubleshooting, and inspections through hcloud CLI, producing reports and change snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inspect and manage DLI queues, jobs, databases, tables, connections, and resource usage, and to troubleshoot failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DLI administration permissions can enable destructive changes or unexpected cloud costs.

Mitigation: Begin with read-only or narrowly scoped IAM permissions and review each destructive or cost-changing command before execution.

Risk: Execution-quality reports are sent to Huawei Cloud endpoints by default when credentials are available.

Mitigation: Disable telemetry unless the reporting and its destination are approved.

Risk: Installing hcloud from an unverified installer may expose the host to unsafe code.

Mitigation: Verify the installer source before running it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-dli-manage)
- [DLI operation catalog](references/dli-operation-catalog.md)
- [Common workflows](references/common-workflows.md)
- [IAM policies](references/iam-policies.md)
- [hcloud CLI installation guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Markdown reports, Shell commands, Operational guidance]

**Output Format:** [Markdown with hcloud CLI commands and structured inspection reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes change snapshots, cleanup proposals, and risk alerts.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
