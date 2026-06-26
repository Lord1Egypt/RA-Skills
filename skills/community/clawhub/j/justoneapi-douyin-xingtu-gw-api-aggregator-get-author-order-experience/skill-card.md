## Description: <br>
Call GET /api/douyin-xingtu/gw/api/aggregator/get_author_order_experience/v1 for Douyin Creator Marketplace (Xingtu) Creator Order Experience through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a JustOneAPI wrapper for Douyin Creator Marketplace (Xingtu) creator order-experience data. It supports creator evaluation, campaign planning, and marketplace research using an oAuthorId lookup and optional reporting period. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper sends JUST_ONE_API_TOKEN as a URL query parameter. <br>
Mitigation: Use a scoped or revocable token, avoid sharing command output or network traces, and rotate the token if it may have been exposed. <br>
Risk: The skill returns creator marketplace data and may include backend error payloads. <br>
Mitigation: Review results before sharing them outside the intended workflow and avoid pasting sensitive output into public channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-aggregator-get-author-order-experience) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_aggregator_get_author_order_experience&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_aggregator_get_author_order_experience&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with an executable Node command and JSON API response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and JUST_ONE_API_TOKEN; uses oAuthorId and optional period query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
