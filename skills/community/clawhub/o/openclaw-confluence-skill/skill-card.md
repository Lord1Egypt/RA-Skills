## Description:

Full Confluence Cloud REST API v2 skill for pages, spaces, folders, databases, whiteboards, comments, labels, tasks, properties, and related workflows with Basic or OAuth authentication, pagination, and confluence-cli migration helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pangin](https://clawhub.ai/user/pangin)

### License/Terms of Use:


## Use Case:

Developers and Confluence workspace administrators use this skill to automate Confluence Cloud REST API v2 workflows, including content, spaces, permissions, labels, tasks, properties, and migration-related operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live credentials can authorize broad Confluence read, write, delete, invite, role, admin-key, redaction, and ad-hoc API operations.

Mitigation: Use least-privilege credentials, verify the tenant URL before use, and require separate human review for delete, invite, role, admin-key, redaction, and ad-hoc calls.

Risk: Credential storage and destination safeguards are weak for a skill that can load tokens from environment or local configuration.

Mitigation: Keep tokens out of project .env files, prefer managed secret storage, rotate credentials regularly, and avoid sharing configured workspaces.

Risk: Ad-hoc API calls can target high-impact endpoints when supplied with an arbitrary method, path, and body.

Mitigation: Review the exact HTTP method, endpoint path, payload, and expected tenant impact before running generated ad-hoc commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pangin/skills/openclaw-confluence-skill)
- [OpenAPI spec](refs/openapi-v2.v3.json)
- [Endpoints list](refs/endpoints.md)
- [OAuth scopes](refs/scopes.md)
- [Usage tips](refs/usage.md)
- [Test checklist](refs/tests.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with inline shell commands and JSON API request or response bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Confluence Cloud Basic or OAuth credentials; list commands may follow pagination with --all.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
