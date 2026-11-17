## Description:

Manage CloudRobo workspaces, workspace members, workspace overview statistics, and active workspace context for other CloudRobo skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to administer CloudRobo workspace resources, manage workspace membership, inspect quota and overview information, and set the active workspace context used by related CloudRobo workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace and member operations can create, update, transfer, or delete CloudRobo resources.

Mitigation: Confirm exact workspace and user IDs before mutating operations, prefer dry-run first, and require explicit user confirmation before deletes or role changes.

Risk: CloudRobo administration uses AK/SK credentials for signed API access.

Mitigation: Use least-privilege credentials, keep secrets in environment variables or protected config, and avoid logging credentials or signed traffic in production.

Risk: Switching workspaces writes persistent local context consumed by other CloudRobo skills.

Mitigation: Run `cloudrobo workspace current` after switching and verify `~/.cloudrobo/workspace.json` points to the intended workspace before running related workflows.

Risk: Disabling TLS verification weakens protection for signed CloudRobo requests.

Mitigation: Keep TLS verification enabled except for controlled local debugging against trusted endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-workspace)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [API Paths](references/api-paths.md)
- [Workspace Config Reference](references/workspace-config-catalog.md)
- [Dataflow Diagram](references/dataflow-diagram.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Huawei Cloud API Explorer](https://console.huaweicloud.com/apiexplorer/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose CloudRobo CLI or SDK operations that affect workspace resources, membership, quotas, and local workspace context.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
