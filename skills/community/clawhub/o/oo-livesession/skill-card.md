## Description:

List LiveSession session replays through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can list LiveSession session replays with pagination and common filters, then use the returned data to find relevant sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup can automatically execute unverified remote code without clear user approval.

Mitigation: Review the CLI and installer, check installation effects including bundled-skill synchronization, and confirm OOMOL access to LiveSession data before setup.

## Reference(s):

- [LiveSession](https://livesession.io)
- [LiveSession API authentication documentation](https://livesession.dev/docs/api/authentication)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Text or Markdown summaries with inline shell commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session data depends on the connected LiveSession account; the listed action supports pagination and common filters.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
