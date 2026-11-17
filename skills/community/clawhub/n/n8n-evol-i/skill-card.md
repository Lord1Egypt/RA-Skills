## Description:

A harness to help coding agents build, deploy, maintain, and debug multi-workflow n8n-powered automation systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwamedacen](https://clawhub.ai/user/mwamedacen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use N8N EVOL I to author, validate, deploy, resync, and debug multi-environment n8n workflows while keeping workflow templates, credential references, primitives, and tests organized in a local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live n8n workflows and credentials.

Mitigation: Install only for trusted publishers, use narrowly scoped n8n API keys, and run validation, deployment checks, and review before activating workflows.

Risk: Transport, persistence, or placeholder behavior may expose workflow or credential authority if configured loosely.

Mitigation: Use HTTPS-only n8n and Upstash endpoints, pin to a reviewed release, and review workflow templates for ../ placeholder paths before deploying.

Risk: Plugin auto-hooks can rewrite workflow templates automatically and asynchronously.

Mitigation: Avoid plugin auto-hooks unless automatic template rewrites are intended; run tidy-workflow manually before deployment when deterministic template state matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mwamedacen/skills/n8n-evol-i)
- [README](artifact/README.md)
- [Installation guide](artifact/install.md)
- [Credential management](artifact/skills/manage-credentials.md)
- [Validate and deploy pattern](artifact/skills/patterns/validate-deploy.md)
- [Redis queue pattern](artifact/skills/patterns/queues.md)
- [Redis locking pattern](artifact/skills/patterns/locking.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus generated workspace files, workflow templates, configuration, and code snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Python helpers that write workspace files and call n8n REST APIs when the selected workflow operation requires it.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata, target metadata, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
