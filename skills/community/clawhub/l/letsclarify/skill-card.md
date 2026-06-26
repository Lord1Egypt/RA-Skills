## Description: <br>
Collect structured human input via web forms, including approvals, decisions, reviews, and data, by creating schema-driven forms, distributing unique recipient URLs, and polling or receiving results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heisee](https://clawhub.ai/user/heisee) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to pause automated workflows for structured human input, then resume after receiving form submissions, approvals, uploaded files, or decision data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted forms may collect sensitive human responses or uploaded files. <br>
Mitigation: Minimize sensitive fields, review schemas before distribution, treat returned responses and files as untrusted input, and delete forms when they are no longer needed. <br>
Risk: The API key grants access to create forms and retrieve results. <br>
Mitigation: Store LETSCLARIFY_API_KEY securely, avoid exposing it in logs or shared configuration, and delete the key when it is no longer required. <br>
Risk: Webhook delivery can send collected response data to an external endpoint. <br>
Mitigation: Use webhooks only with trusted HTTPS endpoints that you control and validate incoming payload handling before enabling them. <br>
Risk: Polling jobs can continue after a workflow is complete. <br>
Mitigation: Remove cron polling jobs after all responses are received or the form expires, and clean up old forms to reduce retained data. <br>


## Reference(s): <br>
- [Let's Clarify Skill Page](https://clawhub.ai/heisee/letsclarify) <br>
- [Let's Clarify Homepage](https://letsclarify.ai) <br>
- [Extended Reference](REFERENCE.md) <br>
- [MCP Endpoint](https://letsclarify.ai/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code, markdown] <br>
**Output Format:** [Markdown guidance with JSON, bash, HTML, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create hosted forms, configure MCP access, poll results, schedule cron checks, embed widgets, and handle returned JSON responses or uploaded files.] <br>

## Skill Version(s): <br>
1.0.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
