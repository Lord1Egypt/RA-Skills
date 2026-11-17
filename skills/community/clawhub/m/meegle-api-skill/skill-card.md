## Description:

Meegle API is an OpenClaw skill pack that helps agents prepare credentials and call Meegle OpenAPI operations for spaces, users, work items, settings, comments, views, and measurement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkycy](https://clawhub.ai/user/pkycy)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to guide Meegle API authentication and API calls for project spaces, users, work items, workflow settings, comments, attachments, views, and reporting operations.

### Deployment Geography for Use:

Global; the artifact documents API hosts for International and China regions.

## Known Risks and Mitigations:

Risk: The skill can guide agents through broad Meegle business-data and administrator-changing operations.

Mitigation: Use least-privilege Meegle plugin scopes and require explicit user confirmation before delete, replace, overwrite, membership, or settings changes.

Risk: Credential and token handling can expose real Meegle project access if secrets are stored or routed unsafely.

Mitigation: Validate the API domain is exactly project.larksuite.com or project.feishu.cn before token requests, and avoid storing long-lived secrets in plain shell files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/pkycy/skills/meegle-api-skill)
- [Artifact README](artifact/README.md)
- [Credentials skill](artifact/meegle-api-credentials/SKILL.md)
- [Server-resolved provenance unavailable](evidence.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with YAML API specifications and request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes valid Meegle credentials, project context, and region-specific API domain.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
