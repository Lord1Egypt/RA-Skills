## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/author_link_struct/v1 for Douyin Creator Marketplace (Xingtu) Creator Link Structure through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a JustOneAPI wrapper for Douyin Creator Marketplace (Xingtu) creator link structure data. It supports creator performance analysis by retrieving engagement and conversion metrics for a specified author ID and optional platform type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is supplied to the helper as a command-line argument and is sent as a query parameter.

Mitigation: Use a short-lived or limited-scope token when available, avoid exposing shell history, process listings, logs, screenshots, or shared terminals, and rotate the token if exposure is suspected.

Risk: The skill sends creator lookup parameters and the API token to the JustOneAPI endpoint.

Mitigation: Install and run the skill only if JustOneAPI is trusted for this Douyin Creator Marketplace endpoint and the requested creator data use is appropriate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-sp-author-link-struct)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_link_struct&utm_content=project_link)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_link_struct&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and the oAuthorId query parameter; platform defaults to SHORT_VIDEO when omitted.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
