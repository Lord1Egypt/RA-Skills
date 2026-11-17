## Description:

Call GET /api/douyin-xingtu/gw/api/aggregator/get_author_order_experience/v1 for Douyin Creator Marketplace (Xingtu) Creator Order Experience through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to call JustOneAPI's Douyin Creator Marketplace (Xingtu) creator order experience endpoint. It supports creator evaluation, campaign planning, and marketplace research using commercial history and transaction-related indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command lines, request URLs, logs, or command traces.

Mitigation: Use a narrowly scoped, revocable token when available and avoid sharing logs, screenshots, chat messages, or command traces from runs.

Risk: Returned creator commercial history and transaction-related indicators may be sensitive.

Mitigation: Treat returned creator and transaction data as sensitive and share it only with authorized users.

## Reference(s):

- [Operation documentation](artifact/generated/operations.md)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_aggregator_get_author_order_experience&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with raw JSON returned by the API helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and the oAuthorId query parameter; period is optional with DAY_30 as the documented default.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
