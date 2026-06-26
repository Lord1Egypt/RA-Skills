## Description: <br>
Call GET /api/twitter/get-user-detail/v1 for Twitter User Profile through JustOneAPI with restId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's Twitter user profile endpoint for a supplied X/Twitter restId and summarize profile metadata, audience metrics, and verification-related fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is passed as a command argument and then added to the request URL, which can expose it through shell history, process listings, logs, or URL capture. <br>
Mitigation: Run only in a trusted local environment, avoid command logging, rotate any exposed token, and prefer a version that reads the token from the environment internally without placing it in command arguments or URLs. <br>
Risk: The skill sends a Twitter/X user restId to an external JustOneAPI endpoint. <br>
Mitigation: Use only identifiers the user intends to look up and review the returned data before relying on or sharing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-twitter-get-user-detail) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter_get_user_detail&utm_content=project_link) <br>
- [Generated Operation Reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; non-token input is restId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
