## Description:

Call GET /api/douyin-xingtu/gw/api/author/get_author_base_info/v1 for Douyin Creator Marketplace (Xingtu) Creator Profile through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call the JustOneAPI Douyin Creator Marketplace creator profile endpoint for influencer vetting, benchmark analysis, and campaign planning. It requires an API token and an oAuthorId value, with an optional platform selector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token can be exposed through process arguments or URL query logs.

Mitigation: Use a narrowly scoped, revocable token, avoid logging commands or request URLs, and rotate the token if logs or process metadata may have captured it.

Risk: The skill depends on paid or account-scoped JustOneAPI access.

Mitigation: Review the token's quota and permissions before installation, especially where the token has meaningful account access.

## Reference(s):

- [JustOneAPI API homepage](https://api.justoneapi.com)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-author-get-author-base-info)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_author_get_author_base_info&utm_content=project_link)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes the endpoint-specific result before returning raw JSON; reports operation ID and backend error payloads when calls fail.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
