## Description:

Search Parseur mailboxes and read mailbox schemas, documents, and parsed document data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to search Parseur mailboxes and retrieve mailbox schemas, document metadata, and parsed document data through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code whose effects have not been inspected.

Mitigation: Review installer contents and verify the CLI separately; require approval for local changes and review or disable automatic additional-skill synchronization.

Risk: Connecting Parseur gives OOMOL access to credentials and Parseur data.

Mitigation: Review the connection and its data access before connecting, and only use an account whose data is appropriate to share with the service.

## Reference(s):

- [Parseur](https://parseur.com)
- [Parseur API documentation](https://developer.parseur.com/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only retrieval; results depend on the connected Parseur account and selected mailbox.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
