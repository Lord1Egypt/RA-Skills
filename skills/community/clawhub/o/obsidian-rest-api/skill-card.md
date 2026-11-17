## Description:

Operate Obsidian via Local REST API plugin from remote/WSL environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jieszs](https://clawhub.ai/user/jieszs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to read, write, search, and manage Obsidian vault notes through the Local REST API when direct filesystem access is blocked or the vault is reachable only from WSL or a remote environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a powerful notes API and stores the Obsidian API key in unsafe ways.

Mitigation: Use a protected secret store or environment variable instead of TOOLS.md, and avoid sharing workspace configuration that contains the API key.

Risk: The documented curl examples use -k, which skips TLS certificate verification.

Mitigation: Trust or pin the Obsidian Local REST API certificate instead of disabling certificate checks.

Risk: Binding the Obsidian REST API broadly and opening firewall access can expose note read, write, delete, and command operations beyond the intended client.

Mitigation: Bind the API only to the needed local interface, restrict firewall access to the WSL source, and require explicit confirmation before delete or command-execution operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jieszs/skills/obsidian-rest-api)
- [Obsidian Local REST API reference](references/api.md)
- [Official Obsidian Local REST API documentation](https://coddingtonbear.github.io/obsidian-local-rest-api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Obsidian Local REST API endpoints, request headers, curl commands, and configuration values for the user's environment.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
