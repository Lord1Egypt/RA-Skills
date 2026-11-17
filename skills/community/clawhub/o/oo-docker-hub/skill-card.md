## Description:

Docker Hub (hub.docker.com). Use this skill for ANY Docker Hub request — reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect and manage Docker Hub repositories, tags, images, organization members, teams, and access tokens through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote installer code.

Mitigation: Review installer behavior before enabling the skill, use an independently reviewed CLI release, and disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1 as documented in the oo CLI command reference.

Risk: The CLI can silently install skills into other agent applications, and external installer contents and hosted connector behavior are unverified.

Mitigation: Inspect the bundled artifact, review the CLI and connector behavior before use, and keep startup skill synchronization disabled.

Risk: Docker Hub writes and deletions can change account or organization state.

Mitigation: Connect only the permissions needed and retain user approval for write and destructive actions.

## Reference(s):

- [Docker Hub](https://hub.docker.com)
- [Docker Hub API documentation](https://docs.docker.com/reference/api/hub/latest/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance, Analysis]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples; connector results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation; read actions may be run directly.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
