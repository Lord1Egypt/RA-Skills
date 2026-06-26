## Description: <br>
Analyze Toutiao workflows with JustOneAPI, including article Details, user Profile, and app Keyword Search across 4 operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Toutiao article details, user profiles, app keyword search results, and web keyword search results through JustOneAPI when they have the required identifiers or keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is included in API request URLs. <br>
Mitigation: Use a limited-scope or easily rotated token, keep it out of chat messages and screenshots, and avoid sharing logs or command output that may contain full request URLs. <br>


## Reference(s): <br>
- [Toutiao operations](generated/operations.md) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-toutiao) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, JSON, Shell commands] <br>
**Output Format:** [Plain-language Markdown with selected JSON API results and optional command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN; authenticated GET requests include the token as a query parameter.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
