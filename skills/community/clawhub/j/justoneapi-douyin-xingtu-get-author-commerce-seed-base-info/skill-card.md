## Description:

Call GET /api/douyin-xingtu/get-author-commerce-seed-base-info/v1 for Douyin Creator Marketplace (Xingtu) Author Commerce Seeding Base Info through JustOneAPI with kolId and range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Douyin Creator Marketplace (Xingtu) creator commerce seeding base information for product seeding analysis, creator vetting, and campaign planning. The required lookup scope is a KOL ID and time range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command lines, process telemetry, shell history, proxy logs, or API URL logs.

Mitigation: Use a low-privilege, rotateable token; avoid logging command lines or full request URLs; rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-author-commerce-seed-base-info)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_author_commerce_seed_base_info&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_author_commerce_seed_base_info&utm_content=project_link)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summary with endpoint details, followed by raw JSON when the API call succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN. Required non-token query inputs are kolId and range; acceptCache is optional.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
