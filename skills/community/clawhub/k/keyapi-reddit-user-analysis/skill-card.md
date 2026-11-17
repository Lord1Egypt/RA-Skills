## Description:

Discover and analyze Reddit users and subreddits by retrieving public profiles, active communities, public trophies, subreddit rules, settings, post channels, typeahead suggestions, dynamic search results, and trending search intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external agent users can use this skill to collect public Reddit user, subreddit, search, and trend intelligence through KeyAPI MCP and synthesize the results into structured reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner has broader platform and network authority than the Reddit-only description makes clear.

Mitigation: Review the requested platform and tool before use, and keep KEYAPI_SERVER_URL unset or pointed only at the intended KeyAPI host.

Risk: KEYAPI_TOKEN handling can be weaker if the token is entered interactively and written to a local .env file.

Mitigation: Set KEYAPI_TOKEN through a controlled environment variable and avoid entering it into the interactive prompt.

Risk: Reddit results are cached locally by default.

Mitigation: Use no-cache behavior for sensitive lookups or delete the local .keyapi-cache directory after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lycici/skills/keyapi-reddit-user-analysis)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI Reddit MCP Endpoint](https://mcp.keyapi.ai/reddit/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, KEYAPI_TOKEN, and network access to KeyAPI MCP; caches API responses locally unless disabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
