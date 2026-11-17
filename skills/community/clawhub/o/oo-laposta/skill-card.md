## Description:

Laposta (laposta.nl). Use this skill for any Laposta request to read, create, and update data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to read Laposta mailing lists and members, or create and update lists and members through their connected OOMOL account. It provides the oo CLI commands and payload guidance for those actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run downloaded software without an explicit approval or integrity check.

Mitigation: Install a verified, fixed CLI version yourself or require approval before setup runs downloaded code.

Risk: The connector processes Laposta data through OOMOL, and remote installer and hosted connector behavior remain unverified.

Mitigation: Confirm OOMOL may process your Laposta data, and review the CLI's automatic agent-skill synchronization and disable unwanted changes.

## Reference(s):

- [Laposta](https://laposta.nl/)
- [Laposta API documentation](https://api.laposta.nl/doc/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with oo CLI commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports read actions and state-changing list or member actions; write actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
