## Description: <br>
Call GET /api/kuaishou/search-user/v2 for Kuaishou User Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Kuaishou users through JustOneAPI by keyword and summarize profile-oriented results such as names, avatars, and follower counts for creator discovery or account research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and places it in the request URL query string. <br>
Mitigation: Use a scoped, revocable token, avoid sharing it in prompts or logs, and rotate it if exposure is suspected. <br>
Risk: Requests and returned Kuaishou profile data are handled through a third-party API service. <br>
Mitigation: Install only when the JustOneAPI service is trusted for the intended workflow and data handling requirements. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_search_user&utm_content=project_link) <br>
- [Kuaishou User Search operations](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON response data when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the searchKuaishouUserV2 operation and requires JUST_ONE_API_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
