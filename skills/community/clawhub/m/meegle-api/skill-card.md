## Description:

Meegle Open API skills index. Read credentials first; missing credentials → see meegle-api-credentials and remind user where to get them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkycy](https://clawhub.ai/user/pkycy)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill pack to configure credentials and guide Meegle OpenAPI calls for spaces, users, work items, comments, settings, views, and measurements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists high-value Meegle credentials.

Mitigation: Use safer secret injection when available, avoid plaintext plugin secrets, and protect configuration files with owner-only permissions.

Risk: A configurable API domain could send credentials or requests to the wrong host.

Mitigation: Use only exact Meegle domains such as project.larksuite.com or project.feishu.cn before making requests.

Risk: The skill covers broad mutation and deletion operations without consistent safeguards.

Mitigation: Require explicit confirmation before delete, batch update, workflow transition, membership, or settings changes, and restrict plugin scopes to the minimum needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pkycy/skills/meegle-api)
- [Artifact README](artifact/README.md)
- [Meegle API credentials skill](artifact/meegle-api-credentials/SKILL.md)
- [Meegle API index skill](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, API calls]

**Output Format:** [Markdown with API specifications and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Meegle plugin credentials, domain, project key, and user key before API calls.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
