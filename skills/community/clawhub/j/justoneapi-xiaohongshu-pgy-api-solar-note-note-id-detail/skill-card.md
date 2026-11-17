## Description:

Call GET /api/xiaohongshu-pgy/api/solar/note/noteId/detail/v1 for Xiaohongshu Creator Marketplace (Pugongying) Note Details through JustOneAPI with noteId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call JustOneAPI for Xiaohongshu Creator Marketplace note details by noteId, then review media and engagement data for content analysis, archiving, and campaign review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through process arguments or URL query logging.

Mitigation: Use a narrowly scoped token when available, avoid execution environments that log command arguments or full URLs, and rotate the token if it may have appeared in shell, job, proxy, gateway, or API logs.

Risk: A broad or long-lived JustOneAPI token can increase billing or account impact if exposed.

Mitigation: Review token scope and lifetime before installation, prefer short-lived or limited-access credentials, and monitor API usage after deployment.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_note_note_id_detail&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_note_note_id_detail&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-api-solar-note-note-id-detail)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Endpoint-specific summary followed by raw JSON; shell command examples for execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; required endpoint input is noteId.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
