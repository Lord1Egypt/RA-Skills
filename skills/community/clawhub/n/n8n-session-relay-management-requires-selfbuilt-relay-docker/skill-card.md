## Description:

Manage n8n workflows and automations via API for listing workflows, activating or deactivating them, checking execution status, manually triggering workflows, and debugging automation issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[droidhackzor](https://clawhub.ai/user/droidhackzor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to manage, validate, test, monitor, and optimize n8n workflows through API-backed commands and Python helpers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Testing commands can execute real n8n workflows and may affect production automations.

Mitigation: Run dry-run and test-suite workflows against staging workflows with test credentials before using them on production.

Risk: API keys can be exposed or over-privileged if configured carelessly.

Mitigation: Use a trusted HTTPS n8n base URL, store credentials through OpenClaw settings or a secret manager, and use a narrowly scoped API key.

Risk: Create, activate, execute, or delete operations can change live workflow behavior.

Mitigation: Manually confirm each state-changing operation and prefer inactive deployment followed by monitored activation.

## Reference(s):

- [n8n API Reference](references/api.md)
- [n8n API documentation](https://docs.n8n.io/api/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python examples, JSON snippets, and plain-text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include API responses, validation reports, dry-run results, workflow statistics, and optimization suggestions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
