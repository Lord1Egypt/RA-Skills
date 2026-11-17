## Description: <br>
Key Vault Manager helps agents support local API-key vault workflows, including project-separated vaults, redacted key access, audit logging, key rotation, and team sharing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams can use this skill to ask an agent for help with local key-vault operations, such as separating secrets by project, redacting key reads, planning key rotation, summarizing audit activity, and preparing automation configuration. It is most appropriate in controlled workspaces where proposed file and command actions can be reviewed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle API keys, local configuration files, audit logs, and command execution with insufficiently bounded write, exec, and logging behavior. <br>
Mitigation: Use it only in a controlled workspace, keep explicit file backups, and review each proposed file or shell action before execution. <br>
Risk: The stated key-vault scope is mixed with broader security-audit behavior, which can make expected behavior unclear. <br>
Mitigation: Limit use to explicit vault-management tasks and avoid giving the agent access to unrelated secrets, repositories, or configuration directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/key-vault-manager) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and proposed shell or configuration actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review proposed commands and file changes before execution, especially when secrets or local configuration files are involved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
