## Description:

Use EmailOctopus to read, create, update, and delete data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to inspect EmailOctopus campaigns, mailing lists, and contacts, and to create, update, or remove list contacts through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs a remote installer that has not been verified.

Mitigation: Review the installer and prefer a reviewed, version-pinned CLI installation before setup.

Risk: Startup synchronization may install additional agent skills.

Mitigation: Review synchronization behavior; set OO_SKILLS_SYNC_DISABLED=1 when additional agent skills are unwanted.

Risk: Creating, updating, or deleting contacts changes EmailOctopus data.

Mitigation: Confirm the exact target and payload with the user before write or destructive actions.

## Reference(s):

- [oo CLI command documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [EmailOctopus API documentation](https://emailoctopus.com/api-documentation)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command and JSON examples; API responses in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
