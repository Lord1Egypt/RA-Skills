## Description: <br>
Decision framework for deciding whether a task should be automated in n8n or handled by an OpenClaw agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route scheduled, deterministic pipelines to n8n and keep judgment-heavy or workspace-aware work with OpenClaw agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references local n8n access and a secret-manager credential path. <br>
Mitigation: Use it only in an authorized environment, and require explicit approval before accessing credentials or local n8n services. <br>
Risk: The skill can guide an agent toward creating and activating active automations. <br>
Mitigation: Review and manually test each workflow before activation, and keep workflow changes scoped to approved operational tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/n8n-task-router) <br>
- [Publisher profile](https://clawhub.ai/user/nissan) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklist items and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes routing criteria for n8n versus OpenClaw and operational setup notes for local n8n workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
