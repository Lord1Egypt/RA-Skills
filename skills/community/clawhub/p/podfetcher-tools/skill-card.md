## Description:

Search podcasts, browse episodes, and fetch podcast transcripts from Podfetcher using the bundled Node.js CLI, SDK, or MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flohiwg](https://clawhub.ai/user/flohiwg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search podcast shows, inspect episode catalogs, and retrieve transcripts from Podfetcher through a CLI, SDK, or MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Podcast searches, show IDs, episode IDs, transcript requests, and API credentials are sent to Podfetcher or to the configured endpoint.

Mitigation: Use PODFETCHER_API_KEY through a protected environment or secret manager, avoid passing keys with --api-key or checked-in MCP config, and rotate any exposed key.

Risk: Custom base URLs can direct API-key-authenticated requests to an unintended or untrusted service.

Mitigation: Only set PODFETCHER_BASE_URL or --base-url for trusted HTTPS endpoints and keep the default production endpoint for normal use.

## Reference(s):

- [Podfetcher](https://podfetcher.com)
- [Podfetcher Tools on ClawHub](https://clawhub.ai/flohiwg/skills/podfetcher-tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON examples; CLI and MCP operations return text or JSON payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20+ and a Podfetcher API key; transcript fetches may return queued processing status unless waiting is enabled.]

## Skill Version(s):

0.5.1 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
