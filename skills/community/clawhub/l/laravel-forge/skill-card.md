## Description: <br>
Manage Laravel Forge servers, sites, deployments, databases, integrations, and more via the Forge API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[florianbeer](https://clawhub.ai/user/florianbeer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent administer Laravel Forge infrastructure through the Forge API, including servers, sites, deployments, databases, backups, teams, and integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over Laravel Forge infrastructure, including servers, deployments, credentials, and remote commands. <br>
Mitigation: Install only for intended Forge administration workflows, use the least-privileged Forge token available, and manually confirm production-impacting actions. <br>
Risk: Credential exposure could allow unauthorized Forge administration. <br>
Mitigation: Protect the Laravel Forge API token and credentials file, and set an explicit organization when multiple organizations are available. <br>


## Reference(s): <br>
- [Laravel Forge API Reference](https://forge.laravel.com/docs/api-reference/introduction) <br>
- [Laravel Forge API Documentation](https://forge.laravel.com/api-documentation) <br>
- [ClawHub Laravel Forge release page](https://clawhub.ai/florianbeer/laravel-forge) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a Laravel Forge API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
