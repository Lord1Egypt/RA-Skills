## Description: <br>
Analyze Facebook workflows with JustOneAPI, including post Search, get Profile ID, and get Profile Posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search public Facebook posts, resolve profile IDs from Facebook profile paths, and retrieve public profile posts through JustOneAPI when a task needs API-backed Facebook data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token and Facebook search or profile inputs are sent to JustOneAPI, and the token can be exposed if shared through chat, screenshots, logs, or command history. <br>
Mitigation: Use a scoped or disposable token if available, pass it through JUST_ONE_API_TOKEN, avoid sharing logs or command lines that contain it, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-facebook) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook&utm_content=project_link) <br>
- [Just One API dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown answer with selected fields and optional raw JSON from JustOneAPI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; operations are GET requests with query parameters.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
