## Description:

Anchor Browser (anchorbrowser.io). Use this skill for ANY Anchor Browser request — reading, creating, and updating data. Whenever a task involves Anchor Browser, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to retrieve Anchor Browser project and billing information and to start browser sessions through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded installer code without separate user approval; the installer contents were unavailable for review.

Mitigation: Review before installing, prefer a reviewed version-pinned CLI, and require separate approval for local setup. Review bundled-skill behavior before connecting accounts.

## Reference(s):

- [Anchor Browser homepage](https://anchorbrowser.io)
- [Anchor Browser API documentation](https://docs.anchorbrowser.io/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read-only project and billing lookups and browser session creation, which changes state.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
