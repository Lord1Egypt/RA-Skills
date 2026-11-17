## Description:

OpenDream adds a scheduled OpenClaw or Hermes dream mode in which the agent reads daily memory notes, generates short private dream thoughts, and writes a morning recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajaylakhani](https://clawhub.ai/user/ajaylakhani)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use OpenDream to give an OpenClaw or Hermes agent a nighttime self-reflection workflow that processes daily notes into local dream-cycle files and a morning recall. It is intended for the agent's own dream state, not for interpreting a user's personal dreams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation changes persistent agent behavior by merging dream instructions into HEARTBEAT.md and SOUL.md and by configuring a recurring nighttime heartbeat.

Mitigation: Review the setup diff before installation, confirm the heartbeat schedule is desired, and keep or restore backups of HEARTBEAT.md, SOUL.md, and openclaw.json.

Risk: Nighttime dream ticks read daily memory notes and store derived dream history in local Markdown files.

Mitigation: Install only when this local memory processing is intended, and delete the dreams/ directory if retained dream records are not wanted.

Risk: The setup process can replace an existing heartbeat configuration.

Mitigation: Check current heartbeat settings before running setup and manually merge the configuration when an existing heartbeat is already in use.

## Reference(s):

- [OpenDream Technical Reference](references/REFERENCE.md)
- [OpenDream Manual Installation](references/INSTALL.md)
- [ClawHub Skill Page](https://clawhub.ai/ajaylakhani/skills/opendream)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets; runtime output is local Markdown dream-cycle and morning-recall files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the agent's configured model, reads daily memory notes when available, and writes retained dream history under dreams/.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; skill frontmatter metadata.version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
