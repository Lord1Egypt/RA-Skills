## Description:

Discover, profile, and analyze YouTube channels - retrieve channel metadata, video libraries, convert between channel IDs and URLs, search channels by keyword, and explore advanced search with filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and channel researchers use this skill to resolve YouTube channel identities, retrieve channel metadata, enumerate video libraries, search within channels, and perform filtered YouTube discovery through KeyAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a KeyAPI token for live MCP calls.

Mitigation: Set KEYAPI_TOKEN only for the current shell session when possible and avoid storing tokens in shared, synced, or source-controlled directories.

Risk: The runner supports overriding the KeyAPI MCP server URL.

Mitigation: Use the default KeyAPI endpoint unless the alternate KEYAPI_SERVER_URL is fully trusted.

Risk: Local cache and output files may contain API response data.

Mitigation: Keep .keyapi-cache and generated output files out of shared locations and source control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lycici/skills/keyapi-youtube-channel-analysis)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI YouTube MCP Endpoint](https://mcp.keyapi.ai/youtube/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON output files and cache API responses when users run the bundled Node.js runner.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
