## Description: <br>
Route tasks to verified human workers worldwide via Loopuman for work that needs human verification, translation, moderation, image labeling, local knowledge, or subjective judgment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seesayearn-boop](https://clawhub.ai/user/seesayearn-boop) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create, monitor, list, wait for, and cancel Loopuman tasks when a workflow needs real human judgment, local knowledge, or cultural context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task descriptions and attachments may be sent to Loopuman and external human workers. <br>
Mitigation: Do not submit secrets, credentials, private documents, customer data, regulated personal data, or proprietary material unless it is authorized and redacted. <br>
Risk: Creating tasks can spend account credits and pay workers when tasks complete. <br>
Mitigation: Start with small budgets while testing, review task parameters before submission, and cancel unwanted tasks before workers start. <br>
Risk: The skill stores a long-lived Loopuman API key in a local configuration file. <br>
Mitigation: Protect the local config file, avoid sharing it, and rotate or replace the API key if it may have been exposed. <br>
Risk: Custom apiUrl or webhook settings can send data to endpoints outside the default service. <br>
Mitigation: Use only API and webhook URLs that you control or trust. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/seesayearn-boop/loopuman) <br>
- [Loopuman API Reference](references/api-reference.md) <br>
- [Loopuman website](https://loopuman.com) <br>
- [Loopuman API](https://api.loopuman.com) <br>
- [Loopuman MCP manifest](https://api.loopuman.com/.well-known/mcp.json) <br>
- [Loopuman A2A agent card](https://api.loopuman.com/.well-known/agent-card.json) <br>
- [Loopuman ERC-8004 Agent](https://www.8004scan.io/agents/celo/17) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq; task content is sent to the Loopuman API and may be reviewed by external human workers.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
