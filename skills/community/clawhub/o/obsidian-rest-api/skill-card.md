## Description: <br>
Operate Obsidian via the Local REST API plugin from remote or WSL environments to read, write, search, and manage vault notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jieszs](https://clawhub.ai/user/jieszs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Obsidian users use this skill to operate an Obsidian vault through the Local REST API when direct filesystem access is unavailable or when remote note automation is preferred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a reusable Obsidian REST API key that can read and change vault contents. <br>
Mitigation: Keep the API key private and grant access only when the user is comfortable allowing the agent to read and modify the vault. <br>
Risk: The REST API may be reachable from remote or WSL environments and can perform write, delete, and command-execution operations. <br>
Mitigation: Restrict API and firewall exposure to trusted hosts, and explicitly review write, delete, or command-execution requests before allowing them. <br>


## Reference(s): <br>
- [Obsidian Local REST API Reference](references/api.md) <br>
- [Official Obsidian Local REST API documentation](https://coddingtonbear.github.io/obsidian-local-rest-api/) <br>
- [ClawHub skill page](https://clawhub.ai/jieszs/obsidian-rest-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that read, write, delete, search, or execute actions in an Obsidian vault through a configured API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
