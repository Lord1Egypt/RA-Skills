## Description: <br>
Call GET /api/v1/google/trends/search for Google SERP Trends Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query Just Serp API for Google Trends interest, geography, and related-query data for demand analysis and seasonal trend monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires the sensitive JUST_SERP_API_KEY credential to call the Just Serp API. <br>
Mitigation: Provide the key through the documented environment or command argument only, and avoid pasting credential values into chat messages, screenshots, or logs. <br>
Risk: Requests may fail because of an invalid key, insufficient credits, quota exhaustion, or upstream service errors. <br>
Mitigation: Check the returned status and backend payload before relying on the result, and retry only after resolving authentication, quota, or service issues. <br>


## Reference(s): <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_search&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_search&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-trends-search) <br>
- [Publisher Profile](https://clawhub.ai/user/justserpapi) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the JUST_SERP_API_KEY credential and query parameters for the TrendsSearch operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
