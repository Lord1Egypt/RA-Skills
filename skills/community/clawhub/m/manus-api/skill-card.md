## Description: <br>
Manus AI Agent API integration with managed API key authentication for creating and managing AI agent tasks, projects, files, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call the Manus API through Maton, manage Manus connections, create and inspect tasks, manage projects and files, and configure task lifecycle webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Maton and Manus credentials and can expose prompts, files, task metadata, and outputs through the API. <br>
Mitigation: Install only if you trust Maton and Manus, keep MATON_API_KEY secret, and avoid sending data that should not leave the current environment. <br>
Risk: Create, delete, upload, and webhook actions can change resources in the connected Manus account. <br>
Mitigation: Approve write actions only after checking the target account, target resource, and intended effect. <br>
Risk: Requests may target the wrong Manus account when multiple connections are active. <br>
Mitigation: Include the Maton-Connection header when multiple connections exist so each request targets the intended account. <br>
Risk: Webhook setup can send task lifecycle data to an external destination URL. <br>
Mitigation: Use webhook endpoints you control and trust, and verify the destination URL before registering it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/manus-api) <br>
- [Maton Homepage](https://maton.ai) <br>
- [Manus API Overview](https://open.manus.im/docs) <br>
- [Manus API Reference](https://open.manus.im/docs/api-reference) <br>
- [Manus Website](https://manus.im) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API requests that require MATON_API_KEY and explicit user approval for write actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
