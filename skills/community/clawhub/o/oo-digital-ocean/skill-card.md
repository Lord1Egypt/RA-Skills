## Description:

DigitalOcean (digitalocean.com). Use this skill for ANY DigitalOcean request — reading, creating, updating, and deleting data. Whenever a task involves DigitalOcean, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect DigitalOcean account resources and manage droplet lifecycle actions through a connected account. It supports account, droplet, app, database, DNS, firewall, load balancer, and VPC operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unverified remote code.

Mitigation: Review and approve the CLI installation separately, and use a verified release where available.

Risk: The required CLI may silently synchronize additional agent skills at startup.

Mitigation: Consider setting OO_SKILLS_SYNC_DISABLED=1 before running the CLI.

Risk: Using the integration means trusting OOMOL with connected DigitalOcean access.

Mitigation: Use the integration only if you trust OOMOL with that access.

## Reference(s):

- [DigitalOcean API documentation](https://docs.digitalocean.com/reference/api/)
- [DigitalOcean](https://www.digitalocean.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON API results with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing droplet lifecycle actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
