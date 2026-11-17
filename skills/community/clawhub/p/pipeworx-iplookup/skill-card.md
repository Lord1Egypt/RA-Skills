## Description:

IP Lookup MCP - ip-api.com (free, no auth for basic usage).

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to connect an MCP client to Pipeworx IP lookup tools for single-IP and batch geolocation lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs a mutable npm package automatically through mcp-remote@latest.

Mitigation: Pin and review the mcp-remote package version before installation or deployment.

Risk: Lookup data is routed through a Pipeworx gateway with limited data-handling disclosure.

Mitigation: Avoid submitting sensitive internal, customer, or investigation IP addresses unless Pipeworx gateway handling and retention practices are acceptable.

## Reference(s):

- [Pipeworx IP Lookup](https://pipeworx.io/packs/iplookup)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-iplookup)
- [Publisher Profile](https://clawhub.ai/user/brucegutman)

## Skill Output:

**Output Type(s):** [text, configuration, API calls]

**Output Format:** [Markdown with JSON configuration and MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides geolocate_ip and batch_geolocate tools through a remote MCP gateway.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
