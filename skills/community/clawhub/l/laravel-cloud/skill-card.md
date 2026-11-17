## Description:

Manage Laravel Cloud infrastructure via API: apps, environments, deployments, databases, caches, domains, scaling, commands, storage, and WebSockets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[florianbeer](https://clawhub.ai/user/florianbeer)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage Laravel Cloud applications and related infrastructure from an agent workflow. It supports operational tasks such as creating resources, inspecting metrics and logs, changing environment settings, running commands, and initiating deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant an agent broad authority to change Laravel Cloud resources.

Mitigation: Install only when agent-managed Laravel Cloud operations are intended, use the narrowest available token scope, and require human confirmation for delete, restore, stop, deployment, variable replacement, bucket-key, and remote command operations.

Risk: Plaintext credential-file storage can expose the Laravel Cloud API token if file permissions are weak.

Mitigation: Prefer an environment variable or secret manager, and set any credential file to owner-only permissions.

## Reference(s):

- [Laravel Cloud Documentation](https://cloud.laravel.com/docs)
- [Laravel Cloud API Introduction](https://cloud.laravel.com/docs/api/introduction)
- [ClawHub Skill Release](https://clawhub.ai/florianbeer/skills/laravel-cloud)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and LARAVEL_CLOUD_API_TOKEN.]

## Skill Version(s):

1.2.2 (source: server-resolved release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
