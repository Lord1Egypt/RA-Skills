## Description:

Call GET /api/douyin-xingtu/get-author-content-hot-keywords/v1 for Douyin Creator Marketplace (Xingtu) KOL Content Keyword Analysis through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call JustOneAPI's Douyin Xingtu endpoint for KOL content keyword analysis by KOL ID, then summarize returned metrics, trend signals, and performance indicators for content theme analysis and creator positioning research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required JustOneAPI token can be exposed through process arguments and URL query strings.

Mitigation: Use a short-lived or low-scope token, avoid shared machines where process arguments may be inspected, and rotate the token if exposed.

Risk: URL query tokens may appear in service or proxy logs.

Mitigation: Avoid pasting token values into chat messages or logs, limit token scope, and review logging paths before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-author-content-hot-keywords)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_author_content_hot_keywords&utm_content=project_link)
- [Generated operations reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON]

**Output Format:** [Markdown summary with endpoint details and raw JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, JUST_ONE_API_TOKEN, and the kolId query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
