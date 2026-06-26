## Description: <br>
Call GET /api/reddit/search/v1 for Reddit Keyword Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Reddit by keyword through JustOneAPI, then review titles, authors, and subreddit context for topic discovery and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a URL query parameter and may be exposed by systems that log full URLs. <br>
Mitigation: Use a limited-scope, revocable token, avoid environments that log full URLs, and rotate the token if exposure is suspected. <br>
Risk: The skill sends search requests and credentials to the third-party service api.justoneapi.com. <br>
Mitigation: Install and use the skill only when the user trusts JustOneAPI for the intended Reddit search workflow. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_search&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_search&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-reddit-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON response and inline shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses operation searchRedditV1 with required keyword and optional after pagination token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
