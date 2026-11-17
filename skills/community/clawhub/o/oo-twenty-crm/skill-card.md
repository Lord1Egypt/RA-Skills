## Description:

Connects an agent to Twenty CRM to retrieve, create, update, and delete workspace records through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent with a connected Twenty CRM workspace can look up records and metadata, or manage records through approved CRM actions. The skill is intended for CRM tasks that require the oo CLI and an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup directs the agent to run installers whose remote contents have not been verified.

Mitigation: Review the installer and approve CLI installation separately before allowing setup.

Risk: Connecting Twenty CRM routes requested CRM data through OOMOL, and write or destructive actions can change or remove records.

Mitigation: Review the data being sent through the connection and retain confirmation for edits and deletions.

## Reference(s):

- [Twenty CRM API documentation](https://docs.twenty.com/developers/extend/api)
- [Twenty CRM](https://twenty.com)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON payloads, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read CRM records or propose changes; write and destructive actions require confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
