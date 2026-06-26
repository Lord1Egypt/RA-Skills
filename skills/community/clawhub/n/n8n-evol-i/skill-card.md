## Description: <br>
A harness that helps coding agents build, deploy, maintain, and debug multi-workflow n8n automation systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mwamedacen](https://clawhub.ai/user/mwamedacen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to let an agent scaffold, validate, deploy, resync, debug, and maintain n8n workflows across environments. It is especially suited to projects that need template-stable round trips between agent-authored files and the n8n UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent modify a real n8n workspace and call the n8n API. <br>
Mitigation: Use a development environment first, review generated workflow changes, and prefer non-activating or dry-run style workflows where available. <br>
Risk: The skill uses sensitive credentials and OAuth-capable integrations. <br>
Mitigation: Keep .env files out of source control, use scoped credentials, and review credential references before deploy. <br>
Risk: Workflow templates and hydration can involve placeholder file paths that may read unintended local content. <br>
Mitigation: Review templates for parent-directory placeholder paths before hydration or deploy. <br>
Risk: Error and observability flows may send operational payloads to Datadog, Sentry, Slack, or Redis. <br>
Mitigation: Sanitize error payloads and confirm each destination is appropriate before enabling those integrations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mwamedacen/n8n-evol-i) <br>
- [README](artifact/README.md) <br>
- [Install guide](artifact/install.md) <br>
- [Skill router](artifact/SKILL.md) <br>
- [Queue pattern](artifact/skills/patterns/queues.md) <br>
- [Locking pattern](artifact/skills/patterns/locking.md) <br>
- [Validate and deploy pattern](artifact/skills/patterns/validate-deploy.md) <br>
- [Agent API discipline pattern](artifact/skills/patterns/agent-api-discipline.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, workflow templates, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call n8n APIs and helper scripts when the host agent follows the skill instructions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
