## Description: <br>
Call GET /api/amazon/get-best-sellers/v1 for Amazon Best Sellers through JustOneAPI with category. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query JustOneAPI for Amazon Best Sellers data by category, with optional country and page parameters. It supports product trend review, category research, market analysis, and sales-rank tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends category lookups to JustOneAPI and requires an API token. <br>
Mitigation: Install only when JustOneAPI is trusted for the intended lookup data, keep JUST_ONE_API_TOKEN secret, and avoid sharing command output or URLs that may expose it. <br>
Risk: Provider pricing, quotas, or rate limits may affect repeated endpoint use. <br>
Mitigation: Review the provider's pricing and rate-limit terms before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-amazon-get-best-sellers) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_best_sellers&utm_content=project_link) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_best_sellers&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a category query value; country defaults to US and page defaults to 1.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
