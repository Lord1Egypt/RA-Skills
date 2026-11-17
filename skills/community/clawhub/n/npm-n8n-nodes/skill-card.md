## Description:

Build, structure, test, and publish npm packages for custom n8n community nodes, including credentials, HTTP handling, triggers, webhooks, errors, versioning, and local publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold and implement n8n community node packages, wire credentials and node behavior, test locally, and prepare npm releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example-derived debug logging can expose credentials or workflow data when adapted into real node projects.

Mitigation: Remove full credential and object logging, and avoid logging workflow data before using generated code with real services.

Risk: Loose dependency ranges can introduce unstable or vulnerable packages into n8n community node releases.

Mitigation: Use bounded dependency versions, commit lockfiles, and review generated node code before publishing to npm or connecting production credentials.

## Reference(s):

- [Data Flow and pairedItem Tracking](references/concepts/data-and-pairing.md)
- [Error Handling](references/concepts/error-handling.md)
- [HTTP Requests and Binary Data](references/concepts/http-and-binary.md)
- [Node Properties and UI Fields](references/concepts/node-properties.md)
- [Node Versioning](references/concepts/node-versioning.md)
- [Credential Patterns: API Key / Token Auth](references/examples/credentials/api-key-patterns.md)
- [Credential Patterns: OAuth2](references/examples/credentials/oauth2-patterns.md)
- [Credential Patterns: Other Auth](references/examples/credentials/other-patterns.md)
- [Declarative Node Example](references/examples/nodes/declarative-node.md)
- [Programmatic Node Example](references/examples/nodes/programmatic-node.md)
- [Trigger Node Example](references/examples/nodes/trigger-node.md)
- [Webhook Node Example](references/examples/nodes/webhook-node.md)
- [Common Gotchas](references/gotchas/common-gotchas.md)
- [Local Testing](references/templates/local-testing.md)
- [Project Files](references/templates/project-files.md)
- [Publishing](references/templates/publishing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
