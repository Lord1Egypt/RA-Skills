## Description: <br>
通过 MorphixAI 统一链接和管理第三方账号（GitHub、GitLab、Gmail、Outlook、Jira、Slack 等），并通过代理安全调用第三方 API。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations users can use this skill to check or connect third-party accounts through MorphixAI, then make fallback API calls for platforms that do not already have a dedicated skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can proxy read and write requests across linked third-party services, which may expose or modify account data if a request is too broad or misdirected. <br>
Mitigation: Review the account, endpoint, HTTP method, parameters, and body before proxy calls, especially for requests that post, update, delete, or share data. <br>
Risk: The required MorphixAI API key grants access to connected-account workflows and could be misused if stored in committed files or shared logs. <br>
Mitigation: Store MORPHIXAI_API_KEY in a local environment secret, avoid committing it to configuration files, and use the narrowest available API key scopes. <br>
Risk: Dedicated skills may provide safer account selection, URL construction, and data formatting than the generic proxy path. <br>
Mitigation: Use dedicated skills for supported platforms and reserve the generic proxy for platforms that do not have a dedicated skill. <br>


## Reference(s): <br>
- [Office Link on ClawHub](https://clawhub.ai/paul-leo/mx-link) <br>
- [MorphixAI API Keys](https://morphix.app/api-keys) <br>
- [MorphixAI Connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with tool-call examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and linked third-party accounts for proxy operations.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
