## Description: <br>
Huawei Cloud SWR image lifecycle management skill using the hcloud CLI for namespaces, repositories, tags, authentication, and quota checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Huawei Cloud SWR container image resources, including namespaces, repositories, image tags, Docker login credentials, and quota usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports sensitive cloud operations, including deletion of namespaces, repositories, and tags. <br>
Mitigation: Use least-privilege Huawei Cloud IAM permissions and require explicit confirmation before destructive operations. <br>
Risk: The skill handles Docker login credentials and Huawei Cloud AK/SK configuration. <br>
Mitigation: Prefer temporary tokens, store long-term credentials only in a secret manager, and avoid exposing credential values in commands, code, or conversation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/huawei-cloud-swr-image-management) <br>
- [SWR API Reference Guide](references/swr-api-guide.md) <br>
- [IAM Permission Policies](references/iam-policies.md) <br>
- [Task: Namespace Management](references/task-namespace-management.md) <br>
- [Task: Repository Management](references/task-repository-management.md) <br>
- [Task: Tag Management](references/task-tag-management.md) <br>
- [Task: Auth Management](references/task-auth-management.md) <br>
- [Task: Quota Management](references/task-quota-management.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Common Pitfalls & Solutions](references/common-pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with hcloud CLI command examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include destructive-operation checklists and credential-handling guidance for Huawei Cloud SWR workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
