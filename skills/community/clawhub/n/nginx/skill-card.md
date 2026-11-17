## Description:

Configures and debugs nginx for reverse proxying, load balancing, SSL/TLS termination, caching, redirects, static file serving, operational tuning, containers, and TCP/UDP proxying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, review, tune, and troubleshoot nginx configurations for web serving, reverse proxying, TLS termination, redirects, caching, rate limiting, and containerized deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested nginx commands may require administrative privileges or affect live traffic if applied without review.

Mitigation: Review commands before running them, test configurations with nginx -t, and prefer graceful reloads for configuration changes.

Risk: The skill reads and may update local preference files under ~/Clawic/data/nginx/.

Mitigation: Keep local preference files free of secrets and review stored deployment details when working on sensitive systems.

Risk: The secure_link example contains a placeholder secret.

Mitigation: Replace placeholder secrets with environment-specific values before using signed URL examples.

## Reference(s):

- [ClawHub Nginx skill page](https://clawhub.ai/ivangdavila/skills/nginx)
- [Clawic Nginx skill page](https://clawic.com/skills/nginx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with nginx configuration blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local nginx preference memory under ~/Clawic/data/nginx/ when present.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
