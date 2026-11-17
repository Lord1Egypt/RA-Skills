## Description:

Integrates n8n workflow automation into coding tasks for building, executing, modifying, and configuring development workflow automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nelmaz](https://clawhub.ai/user/nelmaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect coding workflows with n8n automation, including CI/CD triggers, workflow execution, API integrations, data processing, scheduled maintenance, and workflow configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an older nested v1.0.0 skill that still directs credentials and workflow operations to a fixed third-party host.

Mitigation: Review before installing, avoid loading the bundled nested v1.0.0 skill unless it is removed or corrected, and use only the current v1.1.0 behavior.

Risk: n8n API keys and workflow operations can expose credentials or trigger unintended automation when configured broadly.

Mitigation: Use only a user-controlled N8N_URL, keep n8n API keys out of OpenClaw config files, prefer read-only or narrowly scoped keys, and require confirmation for workflow-changing operations.

Risk: Workflow execution, cloning, updating, or deletion can change external systems connected to n8n.

Mitigation: Use the lowest permission mode that supports the task, review workflow state and diffs before changes, and keep audit logging and rate limits enabled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nelmaz/skills/n8n-code-automation-nelmaz)
- [n8n Documentation](https://docs.n8n.io)
- [n8n API Reference](https://docs.n8n.io/api/)
- [n8n Webhooks](https://docs.n8n.io/workflows/webhooks/)
- [n8n Community Workflows](https://community.n8n.io/)
- [n8n Node Reference](https://docs.n8n.io/nodes/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JSON, YAML, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose n8n API calls and workflow configuration changes that require review before execution.]

## Skill Version(s):

1.1.0 (source: server release evidence, artifact metadata, and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
