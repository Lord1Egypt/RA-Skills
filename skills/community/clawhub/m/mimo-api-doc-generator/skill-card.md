## Description:

Generates OpenAPI 3.0/Swagger API documentation from code, URLs, OpenAPI files, or interface descriptions, with SDK examples, mock server configuration, and integration test examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn API source code, endpoint URLs, OpenAPI files, or natural-language interface descriptions into complete API reference material. It is aimed at producing Chinese API docs with OpenAPI output, SDK examples, mock server setup, and integration test examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated examples may contain placeholder package names, URLs, bearer tokens, or global install commands that are unsafe to reuse directly.

Mitigation: Replace placeholders with verified official packages and endpoints, avoid global installs where possible, pin versions, and keep real tokens out of docs, logs, shell history, and shared files.

Risk: Generated DELETE examples or other mutating requests could affect real resources if copied into a live environment.

Mitigation: Confirm destructive examples target test resources before running them and review generated API operations before publication or execution.

## Reference(s):

- [details.md](references/details.md)
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/mimo-api-doc-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with OpenAPI YAML, SDK code blocks, cURL examples, mock server configuration, and test examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary documentation language is Chinese; code examples use English comments where specified by the artifact.]

## Skill Version(s):

1.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
