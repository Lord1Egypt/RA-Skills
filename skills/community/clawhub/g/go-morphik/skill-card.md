## Description:

Unofficial Go client for the Morphik API. Package morphik (github.com/psyb0t/go-morphik) covers ingestion, document management, retrieval, queries, models, cloud apps and connectors. Use when Go code needs Morphik document search, retrieval or ingestion, or already imports go-morphik.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill when working in Go projects that need to integrate with Morphik for document ingestion, management, retrieval, queries, models, cloud apps, or connectors. It provides setup guidance and typed Go client examples for calling the Morphik API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is marked partial because an AGENTS.md reference could not be resolved; the security evidence also notes a low-probability tool-misuse flag and residual uncertainty.

Mitigation: Review the complete source and any applicable AGENTS.md guidance before installation; keep credentials out of logs and limit remote changes to task-owned resources when requested.

Risk: Morphik requests can send credentials and selected document content to the configured deployment, while ingestion, updates, deletion, and connector or cloud-app management can change remote state.

Mitigation: Use only the default Morphik host or a deployment selected by the user, provide credentials through MORPHIK_API_KEY without logging them, and perform state-changing operations only on task-owned resources when requested.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-morphik)
- [Declared project homepage](https://github.com/psyb0t/go-morphik)
- [ClawHub release](https://clawhub.ai/psyb0t/skills/go-morphik)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and integration guidance for the Go Morphik client.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
