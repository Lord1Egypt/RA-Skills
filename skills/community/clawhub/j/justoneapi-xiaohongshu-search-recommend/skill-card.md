## Description: <br>
Call GET /api/xiaohongshu/search-recommend/v1 for Xiaohongshu (RedNote) Keyword Suggestions through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request Xiaohongshu (RedNote) keyword suggestions from JustOneAPI for content research, SEO/PSEO keyword expansion, and search coverage analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required JustOneAPI token may be exposed through command arguments or outbound request URLs. <br>
Mitigation: Use a short-lived or low-scope token, run only where process arguments and outbound URLs are not logged, and prefer an implementation that reads JUST_ONE_API_TOKEN directly and uses an Authorization header if the API supports it. <br>
Risk: The security verdict is suspicious because credential handling can expose meaningful account access. <br>
Mitigation: Review the skill before installing when the token has meaningful account access, and limit use to environments where credential exposure is controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-search-recommend) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_recommend&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_recommend&utm_content=project_link) <br>
- [Generated operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; calls searchRecommendV1 with keyword as a query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
