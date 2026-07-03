## Description: <br>
Call GET /api/v1/google/trends/trending-now for Google SERP Trends Trending Now through Just Serp API with geo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, analysts, and editorial teams use this skill to request current Google Trends Trending Now data for a geographic region and optional time window or language through Just Serp API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security review marked this release suspicious and recommends installing only when the publisher is trusted. <br>
Mitigation: Install only if you trust justserpapi, review the command before execution, and limit use to explicit user-provided endpoint parameters. <br>
Risk: The skill requires a Just Serp API key and sends requests to api.justserpapi.com. <br>
Mitigation: Provide the key through JUST_SERP_API_KEY or the helper's --api-key argument, avoid exposing key values in chat or logs, and rotate credentials if disclosure is suspected. <br>


## Reference(s): <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_trending_now&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_trending_now&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON API response when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and JUST_SERP_API_KEY; required query parameter is geo, with optional hours and language.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
