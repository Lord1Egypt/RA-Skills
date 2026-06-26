## Description: <br>
Manage NetPad forms, submissions, users, and RBAC; use when creating forms with custom fields, submitting data to forms, querying form submissions, managing users/groups/roles, or installing NetPad apps from marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrlynn](https://clawhub.ai/user/mrlynn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, administrators, and operations teams use this skill to manage NetPad forms, submissions, marketplace apps, users, groups, roles, and permissions through documented CLI and REST API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help administer NetPad content and may change, delete, export, publish, or unpublish data and configuration. <br>
Mitigation: Use least-privilege or test API keys when possible, verify the target NetPad base URL, and require explicit confirmation before delete, export, publish, or unpublish actions. <br>
Risk: The skill can guide marketplace installation and RBAC changes that affect access to NetPad resources. <br>
Mitigation: Review proposed marketplace, user, group, role, and permission changes before execution and require explicit confirmation for RBAC updates. <br>
Risk: The skill relies on the external @netpad/cli package for CLI workflows. <br>
Mitigation: Review the external CLI package and its commands before relying on it in a production environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mrlynn/netpad) <br>
- [NetPad API v1 Endpoint Reference](references/api-endpoints.md) <br>
- [NetPad CLI Reference](references/cli-commands.md) <br>
- [Publisher Website](https://mlynn.org) <br>
- [Publisher GitHub Profile](https://github.com/mrlynn) <br>
- [Publisher LinkedIn Profile](https://linkedin.com/in/mlynn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, curl examples, CLI commands, and JSON payload examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NETPAD_API_KEY for REST API workflows or netpad login for CLI workflows; common helper commands depend on curl, jq, and netpad.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
