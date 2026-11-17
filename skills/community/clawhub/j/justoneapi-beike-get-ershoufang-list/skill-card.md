## Description:

Call GET /api/beike/get-ershoufang-list/v1 for Beike Resale Housing List through JustOneAPI with cityId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to retrieve Beike resale housing listings from JustOneAPI by city ID, with optional condition and offset filters for property search pages or regional housing market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may appear in command-line process data, request URLs, or logs.

Mitigation: Use a low-privilege or disposable token when available, avoid logging commands and URLs that contain the token, monitor usage, and rotate the token after suspected exposure.

Risk: The skill sends housing lookup requests to api.justoneapi.com and depends on that external service.

Mitigation: Use it only when external JustOneAPI calls are acceptable for the workflow and review backend error payloads before sharing them.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_get_ershoufang_list&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-beike-get-ershoufang-list)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with optional raw JSON API response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and cityId; optional filters include condition and offset.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
