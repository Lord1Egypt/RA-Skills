## Description: <br>
Call 2 get-user versions for Xiaohongshu (RedNote) User Profile through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to look up Xiaohongshu (RedNote) user profile data through JustOneAPI for creator research, account analysis, and competitor monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Xiaohongshu userIds and the JustOneAPI token to api.justoneapi.com. <br>
Mitigation: Install only if that data flow is acceptable, use a scoped or low-privilege token when available, monitor API usage, and rotate the token if exposure is suspected. <br>
Risk: Tokens may appear in command lines, full URLs, logs, screenshots, or terminal history during use. <br>
Mitigation: Pass the token through the documented environment variable, avoid logging full commands or URLs, and do not paste token values into chat messages or screenshots. <br>


## Reference(s): <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Shell commands] <br>
**Output Format:** [Markdown summary with raw JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and a Xiaohongshu userId; supports getUserV3 and getUserV4.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
