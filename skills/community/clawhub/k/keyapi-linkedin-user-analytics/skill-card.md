## Description: <br>
Discovers, profiles, and analyzes LinkedIn users, including professional profiles, contact information, work history, education, skills, publications, certifications, honors, recommendations, interests, posts, comments, and videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to retrieve and synthesize LinkedIn profile, content, contact, career, education, and credential data through KeyAPI for profile research and professional intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve and cache personal LinkedIn profile and contact data. <br>
Mitigation: Use it only for lawful, consented research, collect the minimum data needed, and delete cached profile data when the task is complete. <br>
Risk: The runner depends on KEYAPI_TOKEN and can load credentials from a project .env file. <br>
Mitigation: Keep the token out of source control, confirm .env file permissions and ignore rules, and prefer environment-only secret injection where possible. <br>
Risk: The runner provides broad KeyAPI tool access and a configurable server endpoint. <br>
Mitigation: Review tool schemas before use, keep calls scoped to LinkedIn operations required for the task, and use only trusted KeyAPI server URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lycici/keyapi-linkedin-user-analytics) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI LinkedIn MCP endpoint](https://mcp.keyapi.ai/linkedin/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with JSON API responses and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cache KeyAPI responses locally when the runner is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
