## Description:

Unofficial Go client for the Morphik API covering ingestion, document management, retrieval, queries, models, cloud apps, and connectors for Go projects that need Morphik document search, retrieval, or ingestion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add and use the unofficial Morphik Go client for document ingestion, search, retrieval, and queries, or to work in projects that already import it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration uses an unofficial Go dependency.

Mitigation: Review and pin the dependency before use.

Risk: API credentials and selected document content are sent to the configured Morphik server.

Mitigation: Use a limited-permission API key and verify the destination server and documents before uploading.

Risk: Document and account operations can change remote state.

Mitigation: Make remote changes only when requested and on task-owned resources.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-morphik)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Go code examples, shell commands, and API usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
