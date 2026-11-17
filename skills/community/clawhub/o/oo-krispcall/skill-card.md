## Description:

KrispCall (krispcall.com). Use this skill for ANY KrispCall request — reading, creating, updating, and deleting data. Whenever a task involves KrispCall, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read and manage contacts and workspace members in a connected KrispCall account, including creating, updating, and deleting contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs downloaded installer code without verification or explicit installation approval.

Mitigation: Review the installer before running it, and install and verify the oo CLI separately.

Risk: The skill operates on the user's connected KrispCall account, and the remote installers' full local effects are uncertain.

Mitigation: Review setup before installation, approve additional agent skills that an installer adds or updates, and retain confirmation requirements for contact changes and deletions.

## Reference(s):

- [KrispCall](https://krispcall.com)
- [KrispCall API documentation](https://developer.krispcall.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and concise guidance through the oo CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read workspace data, create or update contacts, or delete contacts.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
