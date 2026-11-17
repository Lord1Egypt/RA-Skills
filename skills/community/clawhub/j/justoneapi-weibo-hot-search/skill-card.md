## Description:

Call GET /api/weibo/hot-search/v1 for Weibo Hot Search through JustOneAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call JustOneAPI's Weibo hot-search endpoint for ranking data, trend monitoring, newsroom workflows, and topic discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens may be exposed through command lines, logs, process listings, diagnostics, or shared screenshots.

Mitigation: Use a low-scope or revocable JustOneAPI token, avoid pasting token values into chat or logs, and rotate the token if exposure is suspected.

Risk: Backend errors or API responses may include payload details that need review before sharing.

Mitigation: Review returned JSON and error payloads before forwarding results outside the intended workflow.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_hot_search&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_hot_search&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-weibo-hot-search)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON from the API helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JUST_ONE_API_TOKEN and the hotSearchV1 operation for /api/weibo/hot-search/v1.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
