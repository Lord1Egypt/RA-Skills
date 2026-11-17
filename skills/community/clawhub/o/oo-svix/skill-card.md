## Description:

Use this skill to read, create, update, and delete Svix data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage Svix applications, endpoints, event types, and messages through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup runs a remote installer whose code has not been verified.

Mitigation: Install a verified CLI release yourself and inspect its agent-skill synchronization settings before enabling the skill.

Risk: The connector implementation and its handling of mediated credentials have not been verified.

Mitigation: Connect only the Svix account you intend to use.

## Reference(s):

- [Svix documentation](https://docs.svix.com/)
- [Svix homepage](https://www.svix.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions are identified as reads, writes, or destructive operations; writes and destructive actions require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
