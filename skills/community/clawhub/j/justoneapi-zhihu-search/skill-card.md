## Description:

Call GET /api/zhihu/search/v1 for Zhihu Keyword Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Zhihu keyword search endpoint for topic discovery and content research. It accepts a keyword and optional offset, then returns Zhihu search result data, metadata, and ranking signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Zhihu search terms and a JustOneAPI token to JustOneAPI, and the token may be exposed through command-line arguments or query-string logging.

Mitigation: Use a narrowly scoped or disposable token where possible, avoid sharing command logs or process listings, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_search&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_search&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Endpoint-specific summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a keyword query parameter; offset is optional.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
