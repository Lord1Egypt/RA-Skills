## Description: <br>
Analyze Beike workflows with JustOneAPI, including resale Housing Details, resale Housing List, and community List. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve API-backed Beike resale housing details, resale housing lists, and community list data through JustOneAPI when they can provide the required city, listing, or filter parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent to api.justoneapi.com in URL query parameters for authenticated requests. <br>
Mitigation: Use this skill only when JustOneAPI is trusted, avoid logging full request URLs or command output, prefer limited-scope tokens when available, and rotate the token if it may have appeared in logs or debugging traces. <br>


## Reference(s): <br>
- [ClawHub Beike API Skill](https://clawhub.ai/justoneapi/justoneapi-beike) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and operation-specific Beike parameters.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
