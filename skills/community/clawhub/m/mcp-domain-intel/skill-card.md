## Description:

Domain intelligence for WHOIS lookups and domain availability checks via the L402 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haveblue997](https://clawhub.ai/user/haveblue997)

### License/Terms of Use:

MIT

## Use Case:

Developers, security analysts, and brand teams use this skill to gather WHOIS and DNS intelligence, check domain availability, and support domain acquisition, brand monitoring, competitor analysis, and cybersecurity investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review verdict is suspicious because installation instructions run an unpinned npm package and documentation is inconsistent about package name, tool names, and environment variables.

Mitigation: Review carefully before installing, prefer a pinned reviewed package version or a local build from inspected source, confirm the intended package name, and use the correct NAUTDEV_BASE_URL setting when controlling the API endpoint.

Risk: The skill sends domain queries to a configurable external API endpoint.

Mitigation: Confirm the endpoint is trusted for the intended environment and avoid submitting sensitive domain investigation data unless that disclosure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haveblue997/skills/mcp-domain-intel)
- [Publisher profile](https://clawhub.ai/user/haveblue997)
- [NautDev API endpoint](https://api.nautdev.com)
- [Blue-Trianon-Ventures GitHub profile](https://github.com/Blue-Trianon-Ventures)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [MCP tool responses as JSON-formatted text, with setup guidance in Markdown and JSON configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns WHOIS/DNS lookup results or domain availability results for a single domain input.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
