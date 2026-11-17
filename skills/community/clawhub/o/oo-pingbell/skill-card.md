## Description:

Operate PingBell through an OOMOL-connected account to list available sources and ring a selected source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers with a connected PingBell account can list its available sources and ring a chosen source using the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup uses unverified downloads, and the linked CLI can install additional agent skills during startup synchronization.

Mitigation: Review the CLI installation separately; consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking it.

Risk: Remote installer and hosted connector behavior remain unverified.

Mitigation: Connect only the intended PingBell account and review setup before allowing automatic installation.

Risk: Ringing a source changes its counter, screens, and subscribed devices.

Mitigation: Confirm the exact ring target and effect before running the action.

## Reference(s):

- [PingBell API documentation](https://pingbell.io/docs/)
- [PingBell homepage](https://pingbell.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON connector responses and shell commands, described with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the connected PingBell account and selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
