## Description: <br>
This skill enables agents to manage Powerdrill datasets, upload files, create analysis sessions, and run natural-language data analysis queries that return insights, tables, and charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javainthinking](https://clawhub.ai/user/javainthinking) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and analysts use this skill to connect an agent to Powerdrill for dataset management, file upload, natural-language data exploration, visualization, and cleanup of analysis resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send arbitrary local files to the external Powerdrill service. <br>
Mitigation: Confirm each upload path with the user and avoid secrets or regulated files unless explicitly approved. <br>
Risk: The skill can delete remote Powerdrill datasets and sessions. <br>
Mitigation: Confirm cleanup and delete actions before execution, especially for datasets that may contain persistent user data. <br>
Risk: Powerdrill credentials grant API access to the user's workspace. <br>
Mitigation: Use a least-privileged Powerdrill API key and keep POWERDRILL_USER_ID and POWERDRILL_PROJECT_API_KEY out of logs and shared artifacts. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/javainthinking/powerdrill-skills) <br>
- [Powerdrill Platform](https://chat.powerdrill.ai/) <br>
- [Powerdrill API Documentation](https://docs.powerdrill.ai/api-reference/v2) <br>
- [Powerdrill Quick Start Guide](https://docs.powerdrill.ai/developer-guides/quick-start-v2) <br>
- [Powerdrill Streaming Response Handling](https://docs.powerdrill.ai/api-reference/v2/streaming#streaming-response) <br>
- [Powerdrill Data Source Status](https://docs.powerdrill.ai/api-reference/v2/how-to-check-data-sources) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, analysis] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, and JSON-like API responses; Powerdrill job results may include text, code, tables, chart images, sources, and suggested questions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POWERDRILL_USER_ID and POWERDRILL_PROJECT_API_KEY environment variables; generated table and image URLs may expire.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
