## Description: <br>
Call GET /api/tiktok/search-post/v1 for TikTok Post Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to search TikTok posts through JustOneAPI by keyword, with optional region, sort, pagination, and publish-time filters. It supports trend monitoring, content discovery, keyword-based market analysis, and sentiment tracking workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a request URL query parameter and may be exposed through copied commands, URLs, screenshots, shell history, or logs. <br>
Mitigation: Keep the token in the JUST_ONE_API_TOKEN environment variable, avoid sharing request URLs or command lines containing token values, and rotate the token if exposure is suspected. <br>
Risk: Search terms and filters are sent to JustOneAPI when the endpoint is called. <br>
Mitigation: Use this skill only when the user or deploying organization trusts JustOneAPI with the search terms, filters, and resulting API processing. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_search_post&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-tiktok-search-post) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses operation searchPostV1 against GET /api/tiktok/search-post/v1; returns raw JSON after a short endpoint-specific summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
