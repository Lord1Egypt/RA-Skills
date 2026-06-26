## Description: <br>
Call GET /api/kuaishou/search-video/v2 for Kuaishou Video Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to search Kuaishou videos by keyword through JustOneAPI. It supports competitive analysis, market trend review, keyword monitoring, and brand tracking by returning Kuaishou video search data such as video IDs, cover images, and descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JUST_ONE_API_TOKEN and sends Kuaishou search keywords to JustOneAPI. <br>
Mitigation: Use a dedicated or low-privilege token when available, avoid exposing full request URLs or logs, and rotate the token after use or suspected exposure. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_search_video&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_search_video&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-kuaishou-search-video) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Shell commands] <br>
**Output Format:** [Markdown summary with JSON response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses keyword as the required lookup scope and page as an optional pagination parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
