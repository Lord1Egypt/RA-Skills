## Description:

N8n Operator helps agents design, create, modify, test, and administer n8n workflows through the n8n REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujun2508](https://clawhub.ai/user/lujun2508)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation engineers, and DevOps users use this skill to plan, create, update, validate, activate, and troubleshoot n8n workflows against an n8n instance they administer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live create, update, delete, activate, deactivate, and execute operations on n8n workflows using an API key.

Mitigation: Use only an n8n instance and API key the operator is comfortable letting the agent administer, and require explicit confirmation before any mutating or execution action.

Risk: The security evidence flags persistent local scheduled jobs and host file write examples as high-impact behavior.

Mitigation: Avoid the direct OpenClaw jobs.json cron approach and do not use the root Desktop bind-mount example on sensitive host data; prefer scoped paths, HTTPS or loopback-only HTTP, and reviewed n8n scheduling.

## Reference(s):

- [n8n API Reference](references/references/api.md)
- [n8n Node Templates](references/node-templates.md)
- [n8n Workflow Patterns](references/workflow-patterns.md)
- [n8n Windows Desktop Write Guidance](references/desktop-write.md)
- [ClawHub skill page](https://clawhub.ai/lujun2508/skills/n8n-operator)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include n8n workflow JSON, REST API calls, validation findings, and operational instructions.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
