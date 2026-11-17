## Description:

Call GET /api/douyin-xingtu/gw/api/aggregator/get_author_commerce_spread_info/v1 for Douyin Creator Marketplace (Xingtu) Author Commerce Spread Info through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a focused JustOneAPI endpoint for Douyin Creator Marketplace (Xingtu) author commerce spread metrics using an author ID. The results support creator evaluation for campaign planning and media buying.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token is passed through command-line arguments and the request URL, which can expose it through shell tracing, process telemetry, CI logs, or URL logs.

Mitigation: Use a scoped or short-lived JustOneAPI token when possible, avoid shell tracing and CI log capture for invocations, and rotate the token if it may have been exposed.

Risk: The requested author ID and API token are sent to api.justoneapi.com.

Mitigation: Install and run this skill only when JustOneAPI is an approved service for the intended data and workflow.

## Reference(s):

- [JustOneAPI API homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_aggregator_get_author_commerce_spread_info&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_aggregator_get_author_commerce_spread_info&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-aggregator-get-author-commerce-spread-info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples and endpoint JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the gwApiAggregatorGetAuthorCommerceSpreadInfoV1 operation and returns a short endpoint-specific summary before raw JSON when results are available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
