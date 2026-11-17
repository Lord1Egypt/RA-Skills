## Description:

Use Cronfree through the oo CLI to read and manage schedules connected to your OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Cronfree action schemas and manage recurring webhook schedules through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may persistently install skills across agent apps.

Mitigation: Prefer a verified CLI release, control which skills it installs, and use OO_SKILLS_SYNC_DISABLED=1 when supported to disable startup synchronization.

Risk: Approved schedules send repeated webhook requests until removed, while connected credentials are handled by OOMOL.

Mitigation: Review the connected account and webhook target before approving a schedule, and remove schedules when they are no longer needed.

Risk: The exact remote installer and deployed backend are unverified.

Mitigation: Use a verified CLI release and review its broader effects before installation.

## Reference(s):

- [Cronfree homepage](https://cronfree.com)
- [Cronfree API documentation](https://docs.cronfree.com/api)
- [oo CLI commands and environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Cronfree ClawHub release](https://clawhub.ai/oomol/skills/oo-cronfree)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
