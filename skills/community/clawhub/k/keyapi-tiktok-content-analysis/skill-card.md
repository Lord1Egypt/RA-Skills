## Description:

Analyze TikTok content at scale, extracting insights from videos, hashtags, music tracks, and live streams, including engagement trends, comment sentiment, caption transcription, and commerce attribution data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, analysts, and marketing teams use this skill to collect and synthesize TikTok video, hashtag, music, live-stream, comment, caption, engagement, and commerce signals for content strategy and audience research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a KeyAPI token and may persist secrets if the interactive .env flow is used.

Mitigation: Set KEYAPI_TOKEN only in the process environment when possible, avoid writing tokens to .env, and remove any unintended .env file after use.

Risk: TikTok and KeyAPI results may be stored on local disk in cache or output files.

Mitigation: Review cached data handling requirements and periodically delete .keyapi-cache and generated output files that should not be retained.

Risk: A custom KEYAPI_SERVER_URL can route authenticated requests to a non-default endpoint.

Mitigation: Leave KEYAPI_SERVER_URL unset unless the endpoint is trusted and approved for the data being processed.

Risk: The server security verdict is suspicious and recommends review before execution.

Mitigation: Review the skill, dependency installation, token handling, and network endpoint configuration before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-tiktok-content-analysis)
- [KeyAPI website](https://keyapi.ai/)
- [KeyAPI MCP server endpoint](https://mcp.keyapi.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON API responses, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache API responses and converted cover-image URLs locally; outputs can include TikTok content metadata, engagement data, comments, captions, and commerce signals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
