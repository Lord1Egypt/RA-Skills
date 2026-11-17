## Description:

Performs Microsoft Graph CRUD operations for Microsoft To Do tasks and provides operating guidance for lightweight Microsoft 365 task workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdelkrim](https://clawhub.ai/user/abdelkrim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to authenticate with Microsoft Graph, inspect Microsoft To Do lists, and create, read, update, or delete To Do tasks from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, create, update, and delete Microsoft To Do tasks through delegated Microsoft Graph access.

Mitigation: Install only for tenants and accounts where this delegated access is acceptable, and revoke the app grant if the skill is no longer needed.

Risk: Reusable Microsoft authentication tokens are cached locally without evidence of enforced safe file permissions.

Mitigation: Store the token cache in a protected user-only location, use M365_TOKEN_CACHE_PATH when needed, and remove or revoke cached access on shared or compromised machines.

Risk: Server security evidence says the release overstates Planner, owner assignment, reminder, and assignment capabilities.

Mitigation: Rely on the observed Microsoft To Do CRUD behavior only, and verify any Planner, assignment, owner, or reminder workflow before using it operationally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abdelkrim/skills/m365-task-manager-by-altf1be)
- [M365 Task Manager Playbook](references/playbook.md)
- [ClawHub publisher profile](https://clawhub.ai/user/abdelkrim)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires M365_TENANT_ID and M365_CLIENT_ID; M365_TOKEN_CACHE_PATH is optional.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
