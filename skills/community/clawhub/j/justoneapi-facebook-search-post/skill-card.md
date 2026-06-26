## Description: <br>
Call GET /api/facebook/search-post/v1 for Facebook Post Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to call JustOneAPI's Facebook post search endpoint by keyword, optionally with date range and pagination filters, then summarize and return the response JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent to the service as a URL query parameter. <br>
Mitigation: Use a scoped token if available, avoid sharing request URLs or logs, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-facebook-search-post) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_search_post&utm_content=project_link) <br>
- [Just One API dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_search_post&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown summary followed by raw JSON from the API helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN; keyword is required, while startDate, endDate, and cursor are optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
