## Description:

Google Docs (workspace.google.com). Use this skill for ANY Google Docs request — reading, creating, updating, and deleting data. Whenever a task involves Google Docs, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with Google Docs use this skill to search, read, create, copy, export, format, update, and delete documents through their connected Google Docs account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can run downloaded software without an explicit approval step, and the remote installer and hosted connector implementation were unavailable for verification.

Mitigation: Review and install the CLI yourself, and require approval before any installer fallback runs.

Risk: Document requests and connected-account credentials are handled through OOMOL.

Mitigation: Assess whether you trust OOMOL to process document requests and manage connected-account credentials; review Google permissions and retain document-change confirmations.

## Reference(s):

- [Google Docs](https://workspace.google.com/products/docs/)
- [Google Docs API reference](https://developers.google.com/workspace/docs/api/reference/rest)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, PDF files]

**Output Format:** [oo CLI commands with JSON payloads and connector responses, including text or document metadata and optional PDF exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document-changing actions require user confirmation; destructive actions require explicit approval.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
