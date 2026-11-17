## Description:

Call GET /api/douyin-xingtu/gw/api/aggregator/get_author_commerce_seed_base_info/v1 for Douyin Creator Marketplace (Xingtu) Author Commerce Seeding Base Info through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call the JustOneAPI Douyin Creator Marketplace (Xingtu) endpoint with an author ID, optionally scoped by range, to retrieve commerce seeding base information for product seeding analysis, creator vetting, and campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sent in the request URL, which can expose credentials through URL logs, shell history, or captured command invocations.

Mitigation: Use a dedicated least-privilege token, avoid logging commands or full request URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-aggregator-get-author-commerce-seed-base-info)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_aggregator_get_author_commerce_seed_base_info&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON]

**Output Format:** [Endpoint-specific Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and oAuthorId; optional range values are DAY_30 and DAY_90.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
