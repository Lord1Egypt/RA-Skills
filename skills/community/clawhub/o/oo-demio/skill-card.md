## Description:

Use this skill to look up Demio events, sessions, and participants, and to register attendees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Event organizers use this skill to review Demio events, sessions, and participants, and to register attendees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs remote installers that have not been independently verified and may make local changes.

Mitigation: Review the setup path, verify the CLI release independently, and explicitly approve local changes before installing.

Risk: The oo CLI can perform broader skill synchronization, and OOMOL mediates Demio access and related attendee data.

Mitigation: Review and control the CLI's skill synchronization options, and account for OOMOL's role when handling Demio attendee data.

## Reference(s):

- [Demio](https://www.demio.com)
- [Demio API documentation](https://publicdemioapi.docs.apiary.io/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Concise natural-language summaries and oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
