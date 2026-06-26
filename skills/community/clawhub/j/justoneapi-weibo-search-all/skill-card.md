## Description: <br>
Call GET /api/weibo/search-all/v2 for Weibo Keyword Search through JustOneAPI with endDay, endHour, q, startDay, and startHour. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query Weibo keyword search data through JustOneAPI for trend monitoring, including authors, publish times, and engagement signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and the security evidence flags token handling in leak-prone places. <br>
Mitigation: Use a scoped token when available, avoid sharing command history or logs that may contain tokens, and rotate the token if exposure is suspected. <br>
Risk: Search requests send the provided keyword and date window to the JustOneAPI service. <br>
Mitigation: Review queries before execution and avoid sending sensitive or restricted keywords unless that service is approved for the use case. <br>


## Reference(s): <br>
- [Generated Weibo Keyword Search operations](artifact/generated/operations.md) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_search_all&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON from the API helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and a JUST_ONE_API_TOKEN; required endpoint inputs are q, startDay, startHour, endDay, and endHour.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
