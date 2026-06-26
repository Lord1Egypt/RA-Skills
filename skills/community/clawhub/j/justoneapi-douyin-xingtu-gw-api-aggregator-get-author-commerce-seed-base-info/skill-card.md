## Description: <br>
Call GET /api/douyin-xingtu/gw/api/aggregator/get_author_commerce_seed_base_info/v1 for Douyin Creator Marketplace (Xingtu) Author Commerce Seeding Base Info through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to call a JustOneAPI Douyin Creator Marketplace (Xingtu) endpoint for an author ID and summarize commerce seeding metrics for creator vetting, product seeding analysis, and campaign planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required JustOneAPI token is sent as a query parameter, which can expose it through copied URLs, command lines, or logs. <br>
Mitigation: Use a scoped or revocable token when available, avoid sharing full request URLs or command output that may contain the token, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-aggregator-get-author-commerce-seed-base-info) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_aggregator_get_author_commerce_seed_base_info&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oAuthorId as the required lookup parameter and can include range as DAY_30 or DAY_90.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
