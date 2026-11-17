## Description:

Agent-to-agent cloud service: deploys and runs your apps and services -- domains, logs, real status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyxory](https://clawhub.ai/user/nyxory)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect an agent to Nyxory's MCP service, deploy Git repositories to live URLs, manage custom domains and secrets, inspect logs, and check deployment status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects the agent to a persistent third-party MCP service with authority over deployments, secrets, domains, and logs.

Mitigation: Install only after confirming trust in Nyxory and prefer project-scoped configuration where available.

Risk: OAuth or API-token access may expose repository, deployment, secret, domain, or log capabilities beyond the immediate task.

Mitigation: Verify requested scopes, use the narrowest available token or authorization, and confirm revocation procedures before use.

Risk: Production deployments, domain changes, secret changes, and log access can affect live services or expose sensitive information.

Mitigation: Require explicit confirmation before those operations and review the target project, environment, and domain before proceeding.

## Reference(s):

- [Nyxory homepage](https://nyxory.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to configure a third-party MCP service that uses OAuth or an API token.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
