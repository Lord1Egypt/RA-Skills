## Description: <br>
Call GET /api/zhihu/get-column-article-list/v1 for Zhihu Column Article List through JustOneAPI with columnId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's Zhihu column article-list endpoint, retrieve article metadata and ordering for a supplied columnId, and summarize the response before returning raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token may be exposed through command history, process listings, or request URLs. <br>
Mitigation: Use a restricted, rotatable JustOneAPI token; avoid shared or heavily logged environments; prefer an implementation that reads the token directly from the environment and avoids URL-based token transport when supported. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-zhihu-get-column-article-list) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_column_article_list&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_column_article_list&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Short Markdown summary followed by raw JSON from the API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and a JUST_ONE_API_TOKEN; the endpoint requires columnId and accepts optional offset.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
