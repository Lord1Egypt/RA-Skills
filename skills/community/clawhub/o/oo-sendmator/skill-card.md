## Description:

Sendmator (sendmator.com). Use this skill for ANY Sendmator request — reading, creating, updating, and deleting data. Whenever a task involves Sendmator, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read and manage contacts through a connected Sendmator account. It covers contact lookup and listing, creation, updates, and permanent deletion, with confirmation required for changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency may make persistent changes to other local agents through skill synchronization.

Mitigation: Review the CLI setup and control startup synchronization; the publisher documents OO_SKILLS_SYNC_DISABLED.

Risk: The connected service can access contact data, and deleting a contact is permanent.

Mitigation: Review the CLI and connected service setup, confirm contact changes with the user, and require explicit approval for deletion.

Risk: The remote installers and hosted service were not verified.

Mitigation: Prefer an independently reviewed CLI installation before allowing automatic installation.

## Reference(s):

- [Sendmator](https://sendmator.com)
- [Sendmator contacts API documentation](https://docs.sendmator.com/api/contacts/add-contact)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands]

**Output Format:** [JSON action requests and results, with concise text guidance and oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contact writes require confirmation; permanent deletion requires explicit approval.]

## Skill Version(s):

1.0.4 (source: artifact frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
