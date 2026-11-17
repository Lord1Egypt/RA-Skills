## Description:

Manage Elastic Kibana for observability and security operations. Query data views, manage alerting rules and detection engine rules, handle Fleet agent policies, manage cases, and interact with the Elastic Security solution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, and security operations teams use this skill to inspect and manage Kibana observability and security resources through ClawLink-connected Kibana tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires enabling an unpinned third-party ClawLink plugin that handles Kibana credentials.

Mitigation: Install only if the publisher is trusted, verify the plugin source and version where possible, and use a dedicated Kibana identity with least-privilege access.

Risk: Kibana write operations can delete or modify alerting rules, connectors, saved objects, Fleet outputs, Fleet proxies, lists, and security monitoring resources.

Mitigation: Review tool previews carefully and approve delete, Fleet, and security changes only after the target resource and intended effect match the user's request.

## Reference(s):

- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Elastic Fleet Documentation](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html)
- [Elastic Security Solution](https://www.elastic.co/security)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Kibana Connection](https://claw-link.dev/dashboard?add=kibana)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation guidance for write and destructive Kibana operations.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
