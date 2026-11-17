## Description:

Manage Huawei Cloud ModelArts training jobs and related resources through full lifecycle operations via hcloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud engineers, and ML platform operators use this skill to manage Huawei Cloud ModelArts training jobs, algorithms, experiments, models, events, hyperparameter search, and training image save tasks through guided hcloud CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent-assisted workflow with broad Huawei Cloud ModelArts permissions.

Mitigation: Start with the documented read-only or least-privilege IAM policy and expand permissions only for the specific operation being performed.

Risk: Remote one-line CLI installation can execute downloaded code before the user has reviewed it.

Mitigation: Prefer the step-by-step installation path or verify the downloaded installer source before execution.

Risk: Huawei Cloud AK/SK credentials can be exposed through chat, command history, process listings, or credential files.

Mitigation: Configure credentials outside the agent session, never paste secrets into chat, and use presence-only credential checks such as hcloud configure list.

Risk: Create, delete, stop, agency, scheduled-event, and billable operations can change resources or incur cost.

Mitigation: Require explicit user confirmation, check known issues before write operations, and show pricing estimates for billable training job or experiment creation.

## Reference(s):

- [CLI Command Examples](references/cli-command-examples.md)
- [IAM Policies for ModelArts Training Management](references/iam-policies.md)
- [Known Issues and Workarounds](references/known-issues.md)
- [BSS On-Demand Pricing Inquiry](references/pricing-inquiry.md)
- [Verification Method](references/verification-method.md)
- [API Paths from SDK Source](references/api-paths.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Huawei Cloud hcloud CLI documentation](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Huawei Cloud ModelArts API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi/ModelArts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, checklists, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose hcloud CLI commands and JSON input files; write, delete, stop, agency, scheduled-event, and billable operations require explicit user confirmation.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
