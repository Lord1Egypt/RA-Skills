## Description: <br>
Huawei Cloud SWR Image Governance helps agents guide hcloud CLI workflows for SWR namespace and repository permissions, retention rules, shared download domains, image sharing, agency delegation, and related governance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud platform engineers use this skill to administer Huawei Cloud SWR governance tasks, including permission audits and changes, retention policy management, sharing configuration, and agency delegation checks through the hcloud CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide persistent Huawei Cloud SWR permission, sharing, delegation, and cleanup changes. <br>
Mitigation: Use a dedicated least-privilege IAM user, begin with read-only audits, and require explicit confirmation before write operations. <br>
Risk: Retention rule changes can delete image tags or remove expected artifacts. <br>
Mitigation: Review retention selectors, affected repositories, and deletion scope before running create, update, or delete commands. <br>
Risk: Shared domains and manage/edit grants can broaden access to container images. <br>
Mitigation: Review every proposed access change, prefer read-only access where possible, and audit namespace and repository permissions regularly. <br>


## Reference(s): <br>
- [SWR Governance API Reference Guide](references/swr-governance-api-guide.md) <br>
- [IAM Permission Policies](references/iam-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [SWR Image Governance Output Format](references/output-format.md) <br>
- [Task: Namespace Permissions](references/task-namespace-permissions.md) <br>
- [Task: Repository Permissions](references/task-repository-permissions.md) <br>
- [Task: Retention Management](references/task-retention-management.md) <br>
- [Task: Shared Domains](references/task-shared-domains.md) <br>
- [Task: Image Sharing](references/task-image-sharing.md) <br>
- [Common Pitfalls & Solutions](references/common-pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with hcloud CLI command examples and JSON output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require valid Huawei Cloud credentials, an hcloud CLI installation, and user review before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
