## Description:

Call GET /api/zhihu/get-answer-list/v1 for Zhihu Answer List through JustOneAPI with questionId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call JustOneAPI's Zhihu answer-list endpoint for a specific question ID and retrieve answer content, author profile data, and interaction metrics for question analysis and answer research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed to api.justoneapi.com as a query parameter and supplied to the helper as a command-line argument.

Mitigation: Use a low-scope, revocable token; avoid shell tracing and shared logs; and rotate the token if it may have appeared in process listings, command history, traces, or URL logs.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_answer_list&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_answer_list&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-zhihu-get-answer-list)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON API response with a short endpoint-specific summary when used by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the getAnswerListV1 operation with required questionId and optional cursor, offset, order, and sessionId query parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
