## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/item_report_detail/v1 for Douyin Creator Marketplace (Xingtu) Item Report Details through JustOneAPI with itemId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve Douyin Creator Marketplace (Xingtu) item report details through JustOneAPI for a specific itemId, then summarize item performance fields before returning the backend JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is placed in the request URL, where logs or process tooling may retain it.

Mitigation: Use a least-privilege, revocable token, avoid sharing command output or logs, and rotate the token if URLs or process arguments may have been captured.

Risk: The endpoint can return Douyin Creator Marketplace item analytics for a requested itemId.

Mitigation: Confirm the requester is authorized for the itemId and share summarized or raw backend output only with the intended audience.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_item_report_detail&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-sp-item-report-detail)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and itemId; backend errors should include the operation ID and backend payload.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
