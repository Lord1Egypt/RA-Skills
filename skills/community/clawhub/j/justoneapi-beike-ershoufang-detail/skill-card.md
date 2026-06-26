## Description: <br>
Call GET /api/beike/ershoufang/detail/v1 for Beike Resale Housing Details through JustOneAPI with cityId and houseCode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's Beike resale housing detail endpoint with a city ID and house code, then summarize listing pricing, unit price, area, and layout details before returning raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a JustOneAPI token with endpoint requests. <br>
Mitigation: Use a low-scope or disposable token, avoid exposing token values in chat or logs, and rotate the token if command output, URLs, or debug logs may have exposed it. <br>
Risk: Returned housing details may be stale, incomplete, or affected by backend/API errors. <br>
Mitigation: Review the endpoint response and backend error payloads before using the data for user-facing property comparisons or decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-beike-ershoufang-detail) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_ershoufang_detail&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_ershoufang_detail&utm_content=project_link) <br>
- [Generated operation documentation](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN plus cityId and houseCode query parameters; backend errors include the operation ID and response payload when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
