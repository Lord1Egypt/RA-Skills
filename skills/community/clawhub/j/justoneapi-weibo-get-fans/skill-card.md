## Description: <br>
Call GET /api/weibo/get-fans/v1 for Weibo User Fans through JustOneAPI with uid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this skill to call JustOneAPI's Weibo fan lookup endpoint by UID and summarize fan profile metadata and verification signals for audience analysis and influencer research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a JustOneAPI token for Weibo lookups, and evidence.security notes that the token may appear in local command arguments and API request URLs. <br>
Mitigation: Use only with tokens suitable for this lookup, avoid sharing command logs or screenshots that include token-bearing URLs, and prefer an environment-based or header-based token flow if the provider supports it. <br>
Risk: Returned fan profile data can include privacy-sensitive profile metadata and verification signals. <br>
Mitigation: Handle returned JSON according to the user's privacy and data-retention requirements, and summarize only the fields needed for the requested analysis. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_fans&utm_content=project_link) <br>
- [Weibo User Fans Operations](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and a Weibo uid; optional page query parameter defaults to 1.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
