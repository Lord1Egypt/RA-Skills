## Description: <br>
Analyze Twitter workflows with JustOneAPI, including user Profile and user Published Posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve API-backed Twitter user profile details and published posts through JustOneAPI when they have the required user identifiers and token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token and queried Twitter identifiers are sent to a third-party API provider. <br>
Mitigation: Use a dedicated or limited-scope token where possible and install only when JustOneAPI is trusted for the queried data. <br>
Risk: Request URLs or error traces may expose tokens or Twitter identifiers. <br>
Mitigation: Avoid sharing logs or traces that contain full request URLs, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter&utm_content=project_link) <br>
- [Twitter operations](generated/operations.md) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-twitter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should summarize the most relevant fields before including raw JSON.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
