## Description:

Call GET /api/bilibili/search-video/v2 for Bilibili Video Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Bilibili videos by keyword through JustOneAPI, then summarize matched videos, creators, and engagement metrics for topic research and content discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and the JustOneAPI token are sent to api.justoneapi.com.

Mitigation: Use the skill only when that data sharing is acceptable, and prefer a restricted, low-quota, rotatable token.

Risk: The token can be exposed through command lines, request URLs, process listings, shell history, telemetry, or URL logs.

Mitigation: Avoid sharing command logs or screenshots, keep tokens out of chat, and rotate the token if exposure is possible.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_search_video&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Short Markdown summary followed by raw JSON from the API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a keyword; optional query parameters include page and order.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
