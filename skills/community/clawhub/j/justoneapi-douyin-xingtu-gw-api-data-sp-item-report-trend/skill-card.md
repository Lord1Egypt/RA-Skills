## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/item_report_trend/v1 for Douyin Creator Marketplace (Xingtu) Item Report Trends through JustOneAPI with itemId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a focused JustOneAPI endpoint for Douyin Creator Marketplace (Xingtu) item report trend data using an itemId. It supports creator evaluation, campaign planning, and marketplace research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token can be exposed through command-line arguments and URL query logging.

Mitigation: Use a narrowly scoped or disposable JustOneAPI token where possible, avoid shared machines where process arguments can be inspected, and rotate tokens if exposure is a concern.

Risk: The security verdict is suspicious even though the skill is narrowly focused on one lookup.

Mitigation: Review and scan the skill before installing, and confirm token handling expectations with JustOneAPI before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-sp-item-report-trend)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_item_report_trend&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_item_report_trend&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, API calls, guidance]

**Output Format:** [Markdown summary with raw JSON response data and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and itemId; backend errors should include the backend payload and operation ID.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
