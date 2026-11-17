## Description:

Use AICFO through one bearer API key for session introspection, company selection, connector actions, Company-DB entity and file reads, document workflows, and the included OpenClaw adapter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elvismusli](https://clawhub.ai/user/elvismusli)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to connect OpenClaw to AICFO, inspect API-key session scope, choose an authorized company, and run bounded business operations through the packaged adapter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a sensitive AICFO bearer key that may authorize broad company-data actions.

Mitigation: Use a narrowly scoped API key, inspect session scopes before operating, and avoid actions not granted by the key.

Risk: The adapter can send the bearer key to a caller-configured AICFO endpoint.

Mitigation: Set AICFO_APP_URL explicitly to the intended HTTPS origin and avoid passing keys on the command line.

Risk: Connector and document operations can access raw files or trigger writes, imports, deletes, reprocessing, or clarifications.

Mitigation: Review connector and document actions before execution, and require the documented document scopes before writes or reprocessing.

## Reference(s):

- [AICFO homepage](https://aiceo.city)
- [ClawHub skill page](https://clawhub.ai/elvismusli/skills/openclaw-aicfo-agent)
- [Operations reference](references/operations.md)
- [OpenClaw quickstart](docs/contracts/openclaw-quickstart.md)
- [External agent access](docs/contracts/external-agent-access.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command inputs or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Company-scoped operations require a company_id unless the session provides an implicit company.]

## Skill Version(s):

0.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
