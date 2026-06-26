## Description: <br>
Call GET /api/imdb/title-more-like-this-query/v1 for IMDb Recommendations through JustOneAPI with id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch IMDb title recommendations from JustOneAPI for content discovery and recommendation analysis. It requires an IMDb title id and can optionally apply a language-country preference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user's JustOneAPI token and IMDb lookup request to JustOneAPI. <br>
Mitigation: Install only when the user trusts JustOneAPI, pass the token through JUST_ONE_API_TOKEN, and avoid sharing token values in chat, screenshots, or logs. <br>
Risk: The API token is transmitted as a query-string parameter and may appear in proxy, gateway, or error logs outside the skill. <br>
Mitigation: Use a scoped token when available, rotate credentials if exposed, and review surrounding infrastructure logs and retention policies before production use. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_more_like_this_query&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-imdb-title-more-like-this-query) <br>
- [Generated Operation Reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and an IMDb title id; languageCountry is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
