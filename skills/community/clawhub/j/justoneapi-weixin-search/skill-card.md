## Description:

Call GET /api/weixin/search/v1 for WeChat Official Accounts Keyword Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to search WeChat Official Accounts content by keyword through JustOneAPI and summarize account, title, publish-time, and related result data for content discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token is passed in process arguments and sent to api.justoneapi.com as a URL query parameter.

Mitigation: Use a limited, rotatable token; avoid shell tracing or logging full commands and URLs; rotate the token if it may have appeared in process monitoring or server logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-weixin-search)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_search&utm_content=project_link)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_search&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with optional raw JSON from the API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the operation ID and endpoint path used; backend errors include the backend payload and exact operation ID.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
