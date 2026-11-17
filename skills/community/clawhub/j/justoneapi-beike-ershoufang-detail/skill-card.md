## Description:

Call GET /api/beike/ershoufang/detail/v1 for Beike Resale Housing Details through JustOneAPI with cityId and houseCode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Beike resale housing details through JustOneAPI for a known cityId and houseCode. It helps summarize listing details such as pricing, area, layout, and related property attributes while preserving access to the raw API response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JustOneAPI token for the Beike housing-detail endpoint.

Mitigation: Use a low-scope or revocable token, avoid exposing token values in chat, screenshots, shell history, process listings, proxy logs, or server logs, and rotate the token if exposure is suspected.

Risk: Backend errors may include payloads or request context that could contain sensitive lookup details.

Mitigation: Share backend error details only with audiences authorized to see the cityId, houseCode, and related request information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-beike-ershoufang-detail)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_ershoufang_detail&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_ershoufang_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary with endpoint context and raw JSON response when the API call succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token plus cityId and houseCode query parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
