## Description: <br>
Call GET /api/toutiao/get-user-detail/v1 for Toutiao User Profile through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to look up Toutiao user profile data through JustOneAPI. It supports influencer profiling, audience analysis, and creator performance monitoring when the caller has a JustOneAPI token and a Toutiao userId. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token can be exposed through command history, process listings, or logged request URLs when passed as a CLI argument or query parameter. <br>
Mitigation: Use a scoped token from a protected environment variable, avoid shared machines and shell logging, and prefer a version that reads the token directly from the environment and sends it in a header if the provider supports it. <br>
Risk: Toutiao user IDs and lookup requests are sent to JustOneAPI for profile retrieval. <br>
Mitigation: Run the skill only when sending the requested userId to JustOneAPI is acceptable for the user's policy and use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-toutiao-get-user-detail) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_get_user_detail&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_get_user_detail&utm_content=project_link) <br>
- [Generated operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JUST_ONE_API_TOKEN credential and a Toutiao userId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
