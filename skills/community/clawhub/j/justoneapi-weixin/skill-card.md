## Description: <br>
Analyze WeChat Official Accounts workflows with JustOneAPI, including user Published Posts, article Engagement Metrics, and article Comments across 5 operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, analysts, and content operations teams use this skill to retrieve WeChat Official Accounts posts, article details, engagement metrics, article comments, and keyword search results through JustOneAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JustOneAPI receives the WeChat article URLs, account IDs, keywords, and response data requested through the skill. <br>
Mitigation: Install only if you trust JustOneAPI with that data and avoid sending sensitive or unnecessary identifiers. <br>
Risk: The required API token can be exposed through copied commands, logs, screenshots, shell history, process listings, proxy logs, or error output. <br>
Mitigation: Keep JUST_ONE_API_TOKEN private, use a scoped or low-privilege token when available, avoid sharing full request URLs, and rotate the token if exposure is possible. <br>


## Reference(s): <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-weixin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown answer with selected fields and optional raw JSON from JustOneAPI responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, JUST_ONE_API_TOKEN, and operation-specific parameters such as articleUrl, wxid, keyword, offset, searchType, or sortType.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
