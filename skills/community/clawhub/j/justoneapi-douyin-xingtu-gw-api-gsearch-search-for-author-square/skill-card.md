## Description: <br>
Call the JustOneAPI GET endpoint for Douyin Creator Marketplace (Xingtu) creator search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and creator marketing teams use this skill to query JustOneAPI's Douyin Xingtu creator search endpoint with keyword, follower, content, price, and search-type filters for discovery, comparison, and shortlist building. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a URL query parameter for this endpoint. <br>
Mitigation: Avoid sharing request URLs, logs, screenshots, or command output that could expose JUST_ONE_API_TOKEN, and rotate the token if exposure is suspected. <br>
Risk: The skill makes live outbound requests to JustOneAPI and returns backend payloads or errors. <br>
Mitigation: Use it only when the user intends to query this endpoint, keep search terms appropriate for the workspace, and review backend errors before retrying or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-gsearch-search-for-author-square) <br>
- [Publisher profile](https://clawhub.ai/user/justoneapi) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_gsearch_search_for_author_square&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_gsearch_search_for_author_square&utm_content=project_link) <br>
- [Endpoint operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes the endpoint and operation ID before presenting raw JSON; backend errors include the operation ID and backend payload when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
