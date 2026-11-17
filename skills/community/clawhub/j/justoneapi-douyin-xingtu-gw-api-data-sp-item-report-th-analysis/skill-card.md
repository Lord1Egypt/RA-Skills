## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/item_report_th_analysis/v1 for Douyin Creator Marketplace (Xingtu) Item Report Analysis through JustOneAPI with itemId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a JustOneAPI endpoint that retrieves Douyin Creator Marketplace item report analysis by itemId for creator evaluation, campaign planning, and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through process lists, command lines, or full request URLs.

Mitigation: Use a narrowly scoped, revocable token; avoid logging command lines or full request URLs; rotate the token if exposure is suspected.

Risk: The skill depends on an external JustOneAPI endpoint and may return backend error payloads.

Mitigation: Review returned error payloads before sharing them and remove sensitive values such as tokens from logs or chat transcripts.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_item_report_th_analysis&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_item_report_th_analysis&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with endpoint details and raw JSON response output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and itemId; calls a single GET endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
