## Description: <br>
Manages lightweight Microsoft 365 task workflows with Microsoft To Do and Planner for creating, assigning, tracking, and following up operational tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdelkrim](https://clawhub.ai/user/Abdelkrim) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, operators, and developers use this skill to run Microsoft Graph-based Microsoft To Do task workflows with clear owners, due dates, statuses, and reusable task naming guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated Microsoft Graph access can read and modify Microsoft To Do tasks. <br>
Mitigation: Use a least-privilege Entra app registration with only the documented delegated permissions and review the account context before running write operations. <br>
Risk: Reusable Microsoft sign-in tokens are stored in a local cache file. <br>
Mitigation: Keep the token cache private, set M365_TOKEN_CACHE_PATH to a protected location when needed, and delete the cache or revoke app access when finished. <br>
Risk: Update and delete commands act on task IDs and can modify or remove the wrong task. <br>
Mitigation: List tasks first and confirm task IDs carefully before running update or delete commands. <br>


## Reference(s): <br>
- [M365 Task Manager Playbook](artifact/references/playbook.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Abdelkrim/openclaw-skill-m365-task-manager-by-altf1be) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI outputs from Microsoft Graph operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires M365_TENANT_ID and M365_CLIENT_ID; may use M365_TOKEN_CACHE_PATH for the local reusable token cache.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
