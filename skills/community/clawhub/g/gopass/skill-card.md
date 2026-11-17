## Description:

Store, retrieve, list, and manage secrets using gopass (the team password manager).

This skill is ready for commercial/non-commercial use.

## Publisher:

[erdgeclaw](https://clawhub.ai/user/erdgeclaw)

### License/Terms of Use:


## Use Case:

Developers, operators, and team members use this skill to guide agent-assisted gopass workflows for saving, retrieving, generating, searching, syncing, and managing password-store entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to expose, copy, edit, delete, sync, or change access to password-store entries.

Mitigation: Require explicit path-by-path approval before any command that shows, copies, modifies, deletes, syncs, or changes recipients.

Risk: Auto-confirmation, warning suppression, recursive deletion, and plaintext output can increase the chance of accidental secret exposure or destructive changes.

Mitigation: Avoid --yes, warning suppression, recursive deletion, and plaintext output unless there is a specific controlled reason.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include commands that access, copy, modify, delete, sync, or administer secrets in a gopass store.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
