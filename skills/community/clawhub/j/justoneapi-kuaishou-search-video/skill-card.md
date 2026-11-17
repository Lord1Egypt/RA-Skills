## Description:

Call GET /api/kuaishou/search-video/v2 for Kuaishou Video Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and analysts use this skill to search Kuaishou videos by keyword through JustOneAPI. It supports competitive analysis, market trend review, keyword monitoring, and brand tracking with a short result summary and raw JSON when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and the JustOneAPI token are sent to JustOneAPI.

Mitigation: Install only if that data sharing is acceptable; use a narrowly scoped token when available and avoid sensitive search terms.

Risk: Token values may appear in command-line telemetry or full request URL logs.

Mitigation: Avoid logging commands or full request URLs, and rotate the token if it may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-kuaishou-search-video)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_search_video&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_search_video&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summary with command guidance and raw JSON when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a keyword; page is optional and defaults to 1.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
