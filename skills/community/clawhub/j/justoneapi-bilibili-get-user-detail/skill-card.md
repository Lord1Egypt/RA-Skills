## Description: <br>
Call GET /api/bilibili/get-user-detail/v2 for Bilibili User Profile through JustOneAPI with uid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up Bilibili profile metadata for a specified UID through JustOneAPI, then summarize account, audience, and verification-related fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is used in a query-string based request and could be exposed through shared URLs or logs. <br>
Mitigation: Keep JUST_ONE_API_TOKEN out of chat messages, screenshots, and logs; avoid sharing generated request URLs; rotate the token if exposure is suspected. <br>
Risk: Bilibili profile metadata may be incomplete, stale, or insufficient for identity-sensitive decisions. <br>
Mitigation: Treat returned profile data as informational and corroborate identity or verification decisions with independent evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-bilibili-get-user-detail) <br>
- [JustOneAPI API homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_detail&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summary with raw JSON response data and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Bilibili uid; no request body.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
