## Description: <br>
Huawei Cloud SWR (Software Repository for Container) image automation and operations skill using hcloud CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to generate and review hcloud CLI commands for Huawei Cloud SWR cross-region image replication, sync job checks, and CCE/CCI trigger automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SWR sync, trigger, create, update, delete, syncAuto=true, override=true, and trigger enablement commands can make real cloud changes. <br>
Mitigation: Require explicit human review before running changing commands, start in test namespaces or non-production clusters, and confirm target regions, namespaces, repositories, and trigger settings. <br>
Risk: Broad tag patterns such as .* can cause unintended automatic deployments or image replication in production. <br>
Mitigation: Use narrow tag conditions for production, prefer manual sync when releases need approval, and disable triggers before deleting or reconfiguring them. <br>
Risk: Huawei Cloud AK/SK credentials could be exposed or over-privileged during command execution. <br>
Mitigation: Use least-privilege IAM users, environment variables, MFA for sensitive operations, regular credential rotation, and never print, hardcode, or commit AK/SK values. <br>


## Reference(s): <br>
- [SWR Automation API Reference Guide](references/swr-automation-api-guide.md) <br>
- [Task: Image Sync](references/task-image-sync.md) <br>
- [Task: Trigger Management](references/task-trigger-management.md) <br>
- [IAM Permission Policies](references/iam-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Common Pitfalls & Solutions](references/common-pitfalls.md) <br>
- [Huawei Cloud SWR Documentation](https://support.huaweicloud.com/swr/index.html) <br>
- [hcloud CLI Documentation](https://support.huaweicloud.com/cli/index.html) <br>
- [Huawei Cloud API Explorer](https://apiexplorer.developer.huaweicloud.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with hcloud CLI command examples and JSON policy snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include verification checklists, IAM policy JSON, and cautions for cloud-changing operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
