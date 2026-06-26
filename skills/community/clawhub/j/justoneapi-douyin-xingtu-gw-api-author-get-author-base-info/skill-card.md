## Description: <br>
Call GET /api/douyin-xingtu/gw/api/author/get_author_base_info/v1 for Douyin Creator Marketplace (Xingtu) Creator Profile through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and campaign planners use this skill to retrieve a Douyin Creator Marketplace creator profile by oAuthorId for influencer vetting, benchmark analysis, and campaign planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent in the URL query string. <br>
Mitigation: Treat JUST_ONE_API_TOKEN as a secret, avoid logging full request URLs, and rotate the token if it is exposed. <br>
Risk: Creator audience and pricing data may be sensitive business information. <br>
Mitigation: Share and store returned profile data only where it is needed for the campaign or analysis workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-author-get-author-base-info) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_author_get_author_base_info&utm_content=project_link) <br>
- [Generated operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Endpoint-specific summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and oAuthorId; sends the token to api.justoneapi.com as a query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
