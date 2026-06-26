## Description: <br>
Analyze Social Media workflows with JustOneAPI, including cross-Platform Search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run API-backed social media searches across supported platforms for trend research and monitoring. It helps agents request exact JustOneAPI results with explicit keyword, source, time-range, and pagination parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, filters, time ranges, and the JustOneAPI token are sent to JustOneAPI. <br>
Mitigation: Avoid sensitive, regulated, or confidential monitoring queries unless authorized, and use a limited-scope or revocable token when available. <br>
Risk: API credentials may be exposed if pasted into chat messages, screenshots, or logs. <br>
Mitigation: Keep JUST_ONE_API_TOKEN in the environment and do not include token values in user-facing output. <br>


## Reference(s): <br>
- [JustOneAPI API homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_search&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-search) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and sends selected search parameters to JustOneAPI.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
