## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/check_author_display/v1 for Douyin Creator Marketplace (Xingtu) Creator Visibility Status through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can call a focused JustOneAPI wrapper to retrieve Douyin Creator Marketplace (Xingtu) creator visibility status, discovery eligibility, and campaign display signals for a supplied author ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sent as a query parameter and may appear in shell history, process telemetry, proxy logs, or API logs.

Mitigation: Use a narrowly scoped or short-lived token where possible, avoid logging full request URLs, and rotate the token if exposure is suspected.

Risk: The skill requires a network call to JustOneAPI and depends on the token's account, quota, billing, and data access permissions.

Mitigation: Review token scope and account impact before installation or execution, especially for tokens with meaningful quota, billing, or data access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-sp-check-author-display)
- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_check_author_display&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper returns parsed JSON from the selected JustOneAPI operation after required parameters are provided.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
