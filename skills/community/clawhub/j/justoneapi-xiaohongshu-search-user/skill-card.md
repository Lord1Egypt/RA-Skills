## Description:

Call GET /api/xiaohongshu/search-user/v2 for Xiaohongshu (RedNote) User Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and creator-discovery teams use this skill to search Xiaohongshu (RedNote) users by keyword through JustOneAPI and summarize profile metadata and public signals for account research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can leak through URLs or process logs.

Mitigation: Use a narrowly scoped and revocable token, avoid shell tracing or command logging when invoking the skill, and rotate the token if it may have appeared in logs or process metadata.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-search-user)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_user&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_user&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summary with endpoint details and raw JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a keyword query; page is optional for pagination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
