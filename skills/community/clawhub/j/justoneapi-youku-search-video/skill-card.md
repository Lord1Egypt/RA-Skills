## Description:

Call GET /api/youku/search-video/v1 for YOUKU Video Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to query JustOneAPI for YOUKU video search results by keyword, supporting video discovery, topic monitoring, and market research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required JustOneAPI token may be exposed through command-line process metadata or URL logs because it is passed to an API call as a query token.

Mitigation: Use a rotated, low-quota, limited-scope JustOneAPI token and avoid environments that record command arguments or full request URLs.

## Reference(s):

- [YOUKU Video Search API on ClawHub](https://clawhub.ai/justoneapi/skills/justoneapi-youku-search-video)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_search_video&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_search_video&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and raw JSON API output after a short endpoint-specific summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; required query input is keyword, with optional page pagination.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
