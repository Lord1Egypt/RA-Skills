## Description:

Call GET /api/douyin-xingtu/get-kol-spread-info/v1 for Douyin Creator Marketplace (Xingtu) Spread Metrics through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to query JustOneAPI for Douyin Creator Marketplace (Xingtu) spread metrics for a specified KOL ID, including audience, content performance, and commercial indicators for evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token and query parameters are sent to api.justoneapi.com and may be exposed through command arguments, URL query logs, process listings, or shared debugging output.

Mitigation: Use a narrowly scoped or short-lived token when available, avoid shell tracing and command logging, do not paste token values into chat or screenshots, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_spread_info&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_spread_info&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-spread-info)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary with endpoint details followed by raw JSON response data when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a kolId query parameter; optional query parameters include type, range, flowType, onlyAssign, and acceptCache.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
