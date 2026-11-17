## Description:

Use the oo CLI to inspect and manage Neon projects, branches, databases, and operations through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect and manage Neon resources from an agent. It supports read actions and guides users to confirm changes before write or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes unverified remote code, and its resulting changes may not be clearly limited.

Mitigation: Review setup, install a verified oo CLI release yourself, and consider disabling automatic skill synchronization before first launch.

Risk: Write and destructive actions can change or remove Neon resources.

Mitigation: Inspect the live action schema and confirm the exact target and effect with the user before running these actions.

## Reference(s):

- [oo CLI commands](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Neon API documentation](https://api-docs.neon.tech/reference/getting-started-with-neon-api)
- [Neon](https://neon.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text]

**Output Format:** [JSON responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inspects an action's live schema before constructing a request; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
