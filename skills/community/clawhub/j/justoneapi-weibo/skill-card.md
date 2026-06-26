## Description: <br>
Track Weibo hot search boards, keyword results, creator profiles, fan or follower graphs, and post or video detail endpoints through JustOneAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query JustOneAPI for Weibo trend monitoring, keyword search, account research, post analysis, comments, video details, and audience graph lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens are passed in request URLs and may appear in logs, browser history, proxies, or copied command output. <br>
Mitigation: Use a low-scope, revocable JUST_ONE_API_TOKEN, avoid logging full request URLs, and rotate the token if exposure is possible. <br>
Risk: The skill can collect broad Weibo social-profile, follower, fan, post, comment, and engagement data. <br>
Mitigation: Use these features only for lawful, platform-compliant purposes and avoid storing or sharing unnecessary personal data. <br>
Risk: The security verdict is suspicious and recommends review before installation. <br>
Mitigation: Review the skill before installing and confirm that the requested Weibo data access matches the intended use case. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-weibo) <br>
- [Publisher Profile](https://clawhub.ai/user/justoneapi) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo&utm_content=project_link) <br>
- [Weibo Operations](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN for authenticated JustOneAPI GET requests; outputs should summarize Weibo findings before raw backend payloads.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
