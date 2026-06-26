## Description: <br>
Expert n8n workflow builder that creates, deploys, and manages n8n workflows programmatically via the n8n REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kassimisai](https://clawhub.ai/user/kassimisai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to design, deploy, activate, verify, and manage n8n workflows through workflow JSON and the n8n REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A powerful n8n API key can let the agent change live automations and connected services. <br>
Mitigation: Use a test instance or a least-privileged API key where possible, and review generated workflow JSON plus workflow IDs before create, update, delete, execute, or activate actions. <br>
Risk: Generated workflows may expose secrets or regulated data through examples, node parameters, or downstream services. <br>
Mitigation: Avoid placing secrets or regulated data in generated workflow examples and review workflows before deployment. <br>
Risk: Activated workflows can continue running after deployment. <br>
Mitigation: Monitor deployed workflows and deactivate workflows that should not remain active. <br>


## Reference(s): <br>
- [Workflow Patterns](references/workflow-patterns.md) <br>
- [Workflow Schema](references/workflow-schema.md) <br>
- [n8n Builder on ClawHub](https://clawhub.ai/kassimisai/n8n-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON workflow definitions and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, activate, deactivate, delete, or execute n8n workflows when used with a configured n8n API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
