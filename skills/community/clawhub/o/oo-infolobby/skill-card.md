## Description:

Operate InfoLobby through the oo CLI for reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can use this skill to inspect InfoLobby workspaces, tables, and records, and to create, update, or delete records through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs a mutable remote installer whose changes, including bundled skills, are unverified.

Mitigation: Review the CLI installer and its changes before installation; restrict the connected InfoLobby account to the access needed.

Risk: Create, update, and delete actions can change or remove InfoLobby data.

Mitigation: Keep the documented approval checks for record changes and deletions.

## Reference(s):

- [InfoLobby](https://infolobby.com/)
- [InfoLobby API documentation](https://infolobby.com/api-docs/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON data, Guidance]

**Output Format:** [Text or Markdown, including structured JSON responses when returned by an action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or change InfoLobby records depending on the requested action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
