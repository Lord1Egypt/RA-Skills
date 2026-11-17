## Description:

Helps an agent guide users through Playtomic padel court search, booking, active match listing, cancellation, and padel-tui installation workflows from a terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipp-eisen](https://clawhub.ai/user/philipp-eisen)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate the padel-tui CLI for Playtomic court discovery, reservation, active match review, and cancellation while preserving explicit user approval for installation and booking actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance depends on trusting upstream padel-tui package or binary sources.

Mitigation: Confirm padel-tui is the intended tool, prefer an official versioned source, and avoid sudo during installation.

Risk: Local Playtomic session material is sensitive.

Mitigation: Treat the session file as private and avoid exposing or sharing its contents.

Risk: Booking and cancellation commands can reserve or cancel courts.

Mitigation: Confirm venue, court, time, duration, player count, and match ID before running book or match-cancel commands.

## Reference(s):

- [Installation Reference](references/INSTALLATION.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require user confirmation before installation, booking, or cancellation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
