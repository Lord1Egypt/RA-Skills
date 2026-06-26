## Description: <br>
Call GET /api/douyin-xingtu/gw/api/author/get_author_show_items_v2/v1 for Douyin Creator Marketplace (Xingtu) Showcase Items through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a focused JustOneAPI endpoint for Douyin Creator Marketplace showcase item data by creator author ID, supporting creator evaluation, campaign planning, and marketplace research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is passed in the URL query string and may be exposed through shell history, command logs, full request URLs, screenshots, or error traces. <br>
Mitigation: Pass the token from JUST_ONE_API_TOKEN, avoid sharing logs or request URLs, and use a limited-scope or revocable token when available. <br>
Risk: Endpoint calls send creator lookup parameters and authentication to the JustOneAPI service. <br>
Mitigation: Only submit IDs and filters that are appropriate for the user's account, policy, and data-sharing requirements. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_author_get_author_show_items_v2&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-author-get-author-show-items-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; required endpoint input is oAuthorId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
