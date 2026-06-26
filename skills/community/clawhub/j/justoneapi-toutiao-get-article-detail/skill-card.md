## Description: <br>
Call GET /api/toutiao/get-article-detail/v1 for Toutiao Article Details through JustOneAPI with id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use this skill to retrieve Toutiao article details by article ID for content performance analysis, media monitoring, authenticity checks, and metadata review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required JustOneAPI token can be exposed through command-line arguments and URL query logging. <br>
Mitigation: Prefer token handling through environment variables or stdin when available; redact logs and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-toutiao-get-article-detail) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_get_article_detail&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_get_article_detail&utm_content=project_link) <br>
- [Generated operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Short endpoint-specific summary followed by raw JSON when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; the required non-token input is the Toutiao article id.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
