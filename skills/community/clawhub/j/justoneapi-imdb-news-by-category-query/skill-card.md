## Description: <br>
Call GET /api/imdb/news-by-category-query/v1 for IMDb News by Category through JustOneAPI with category. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch IMDb news by category through JustOneAPI, then summarize headlines, summaries, and source metadata for media monitoring or news research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is sent in the URL query string and may appear in request URLs, command output, shell history, or logs. <br>
Mitigation: Use a limited-scope token if available, avoid sharing logs or screenshots that may include request URLs, and rotate the token if exposure is suspected. <br>
Risk: The skill depends on an external JustOneAPI service and will fail if the service, token, network, or endpoint contract is unavailable. <br>
Mitigation: Check backend error payloads, keep the token current, and treat returned IMDb news data as service-provided content that may need verification before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-imdb-news-by-category-query) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_news_by_category_query&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_news_by_category_query&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN value supplied at runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
