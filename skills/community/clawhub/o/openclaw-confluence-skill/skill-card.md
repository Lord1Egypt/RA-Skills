## Description: <br>
Full Confluence Cloud REST API v2 skill for pages, spaces, folders, databases, whiteboards, comments, labels, tasks, properties, authentication, pagination, and migration from confluence-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pangin](https://clawhub.ai/user/pangin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Confluence administrators use this skill to let an agent work with Confluence Cloud REST API v2 resources, including content, spaces, permissions, labels, tasks, and administrative endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use broad Confluence credentials for creating, updating, deleting, inviting users, redacting content, and admin-key actions. <br>
Mitigation: Use least-privilege tokens or OAuth scopes and require explicit human review before destructive, invite, redaction, or admin-key commands. <br>
Risk: Credential configuration may expose Confluence email, API token, OAuth token, or admin-key settings if stored carelessly. <br>
Mitigation: Keep local .env files out of source control and restrict file permissions for credential files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pangin/openclaw-confluence-skill) <br>
- [OpenAPI spec](refs/openapi-v2.v3.json) <br>
- [Endpoints list](refs/endpoints.md) <br>
- [OAuth scopes](refs/scopes.md) <br>
- [Usage tips](refs/usage.md) <br>
- [Quick test checklist](refs/tests.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports paginated Confluence API calls and Basic or OAuth authentication through environment configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
