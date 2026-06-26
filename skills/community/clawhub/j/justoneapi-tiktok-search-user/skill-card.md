## Description: <br>
Call GET /api/tiktok/search-user/v1 for TikTok User Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to search TikTok users by keyword through JustOneAPI, then summarize returned profile data and inspect raw JSON for influencer discovery, audience research, or competitor research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a query-string credential and may be exposed in server, proxy, or diagnostic logs. <br>
Mitigation: Use a scoped or revocable token where available, avoid sharing token values in chat or screenshots, and rotate the token if exposure is suspected. <br>
Risk: TikTok search terms and returned user data are sent to and processed by the third-party JustOneAPI service. <br>
Mitigation: Use the skill only when JustOneAPI is trusted for the search terms and review returned data before relying on it for business decisions. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_search_user&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_search_user&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-tiktok-search-user) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON] <br>
**Output Format:** [Markdown summary with endpoint details and raw JSON returned by the JustOneAPI endpoint.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and the JUST_ONE_API_TOKEN environment variable; non-token inputs include keyword, cursor, and searchId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
