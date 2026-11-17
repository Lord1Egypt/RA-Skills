## Description:

Use this skill to read, create, update, and delete Pinecone data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use the skill to inspect, search, create, update, and delete Pinecone indexes and vectors through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback pipes a remote installer into a shell, and the security assessment notes that this path lacks clear user approval.

Mitigation: Review and install the oo CLI separately before allowing the skill to run, and check its automatic skill-installation settings.

Risk: Requests and API credentials pass through OOMOL as the disclosed intermediary.

Mitigation: Use a narrowly scoped Pinecone connection and retain the skill's confirmation requirements for write and delete actions.

## Reference(s):

- [Pinecone API documentation](https://docs.pinecone.io/reference/api/introduction)
- [Pinecone](https://www.pinecone.io/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation; read actions can run directly.]

## Skill Version(s):

1.0.7 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
