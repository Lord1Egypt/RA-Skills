## Description:

Provides Last.fm API reference guidance for retrieving music data and user information about artists, albums, tracks, charts, tags, libraries, and listening stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyfrog-21k](https://clawhub.ai/user/keyfrog-21k)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill as a Last.fm API reference to construct requests for artists, albums, tracks, users, libraries, charts, and tags. It is most useful when an agent needs concise endpoint guidance and example query formats for Last.fm data retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Last.fm API keys may be exposed if copied into shared prompts, logs, or generated requests.

Mitigation: Use a Last.fm API key intentionally and avoid sharing or storing it unnecessarily.

Risk: Some documented user endpoints can expose profile and listening-history data.

Mitigation: Only request user profile or listening-history data when the affected user expects that data to be queried or displayed.

## Reference(s):

- [Last.fm API documentation](https://www.last.fm/api)
- [Last.fm API root endpoint](https://ws.audioscrobbler.com/2.0/)
- [ClawHub skill page](https://clawhub.ai/keyfrog-21k/skills/last-fm)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, API request examples, Configuration]

**Output Format:** [Markdown with HTTP request examples and query parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Last.fm API key; examples show JSON responses through query parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
