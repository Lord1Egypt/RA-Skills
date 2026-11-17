## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/get_author_convert_ability/v1 for Douyin Creator Marketplace (Xingtu) Conversion Analysis through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a focused JustOneAPI endpoint for Douyin Creator Marketplace creator conversion analysis. It supports creator evaluation, campaign planning, and marketplace research using an author ID plus optional platform and date-range filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token may be exposed through request URLs or process arguments.

Mitigation: Use a narrowly scoped JustOneAPI token where available, avoid logging full URLs or command lines, and rotate the token if it may have appeared in logs.

Risk: The skill consumes JustOneAPI quota or billing capacity when called.

Mitigation: Review the skill before installation when the token has meaningful quota, billing, or data access, and run it only with the required author ID and filters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-sp-get-author-convert-ability)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_ability&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_ability&utm_content=project_link)
- [Generated Operations Reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown summary followed by raw JSON when results are available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; endpoint inputs include oAuthorId with optional platform and range query parameters.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
