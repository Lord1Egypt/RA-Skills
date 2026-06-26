## Description: <br>
Connects an OpenClaw agent to n8n so it can create, trigger, manage, and monitor automation workflows from natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marlowne12](https://clawhub.ai/user/marlowne12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an OpenClaw agent orchestrate n8n automations, including workflow creation, webhook triggering, execution monitoring, retries, and basic workflow administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over n8n workflows, including create, delete, activate, retry, and publish-style actions. <br>
Mitigation: Use a test n8n workspace first and require explicit approval before create, delete, activate, retry, or publish actions. <br>
Risk: n8n API keys and webhook endpoints can expose automation control if stored or shared insecurely. <br>
Mitigation: Use a dedicated least-privilege API key, avoid prompt-visible secret storage, and add authentication or shared-secret validation to webhook templates before exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marlowne12/n8n-openclaw-bridge) <br>
- [n8n](https://n8n.io) <br>
- [Lead notification workflow template](artifact/templates/lead-notification.json) <br>
- [Content publisher workflow template](artifact/templates/content-publisher.json) <br>
- [Website monitor workflow template](artifact/templates/website-monitor.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON workflow templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces n8n API examples, workflow JSON structures, webhook patterns, and operational guidance for agent-controlled automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
