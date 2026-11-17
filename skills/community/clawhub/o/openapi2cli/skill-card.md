## Description:

Generate CLI tools from OpenAPI specs. Built for AI agents who hate writing curl commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awlevin](https://clawhub.ai/user/awlevin)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to generate Python command-line clients from OpenAPI or Swagger specifications so agents can call APIs through discoverable CLI commands instead of hand-written HTTP requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages unpinned runtime package execution through uvx, so the executed package version can change over time.

Mitigation: Pin and verify uv and openapi2cli versions before use, and install only from trusted package indexes.

Risk: Generated API clients can perform real authenticated write operations against external services.

Mitigation: Inspect generated Python files, test against sandbox endpoints first, use dry-run for new commands, and provide only short-lived least-privilege credentials.

## Reference(s):

- [OpenAPI to CLI on ClawHub](https://clawhub.ai/awlevin/skills/openapi2cli)
- [openapi2cli on PyPI](https://pypi.org/project/openapi2cli/)
- [openapi2cli project homepage](https://github.com/Olafs-World/openapi2cli)
- [GitHub REST API OpenAPI description](https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and generated Python CLI usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and guidance for generating API-specific Python CLI files from OpenAPI specifications.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
