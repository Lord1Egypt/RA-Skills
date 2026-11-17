## Description:

Manage Huawei Cloud ModelArts Notebook instances through hcloud CLI workflows for instance lifecycle, lease, tag, image, flavor, cluster, feature, and dynamic storage operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and platform engineers use this skill to inspect and manage Huawei Cloud ModelArts Notebook instances, including read operations, write operations with confirmation, and pricing checks for chargeable actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags unsafe installer guidance.

Mitigation: Do not run the documented curl-to-bash installer without independently verifying the installer source and integrity; prefer a verified Huawei Cloud CLI installation path.

Risk: The server security guidance flags a credential-handling SDK fallback that needs review.

Mitigation: Use credentials configured outside the agent session through safe local mechanisms, and avoid the SDK fallback unless it is rewritten to avoid direct AK/SK handling by the agent.

Risk: The skill can create, start, stop, update, delete, attach, detach, register, sync, and renew cloud resources.

Mitigation: Use a least-privilege IAM user, require explicit confirmation before write operations, and run pricing inquiry before chargeable CreateNotebook or StartNotebook actions.

## Reference(s):

- [CLI Command Examples](references/cli-command-examples.md)
- [IAM Policies for ModelArts Notebook Management](references/iam-policies.md)
- [Known Issues and Practical Solutions](references/known-issues.md)
- [BSS On-Demand Pricing Inquiry](references/pricing-inquiry.md)
- [API Paths](references/api-paths.md)
- [Verification Method](references/verification-method.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Huawei Cloud hcloud CLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Huawei Cloud ModelArts API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi/ModelArts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require explicit user confirmation; CreateNotebook and StartNotebook require pricing inquiry before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
