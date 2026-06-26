## Description: <br>
Search and debug production logs via Graylog - absolute/relative time queries, stream filtering, system health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pranavj17](https://clawhub.ai/user/pranavj17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and support engineers use this skill to search Graylog logs, filter by streams and time windows, inspect recent errors, and check Graylog system health during production debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production log searches can expose sensitive operational data, and broad log-related prompts may activate the skill. <br>
Mitigation: Install only for users who need Graylog access, use a least-privilege read-only Graylog token, and avoid broad production credentials. <br>
Risk: The skill uses an external npm runtime to connect to Graylog with an API token. <br>
Mitigation: Pin the runtime to the reviewed package version and install only when the npm package publisher is trusted. <br>
Risk: Credential mishandling could expose the Graylog API token. <br>
Mitigation: Provide the token through environment variables, keep it out of prompts and logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pranavj17/graylog-log-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BASE_URL and API_TOKEN; Graylog access is read-only, with documented request timeouts, result limits, and relative time bounds.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
