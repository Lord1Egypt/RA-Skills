## Description:

Autonomous structured learning for mastering complex topics through cron-based five-session GEARS feedback loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sagarmainkar](https://clawhub.ai/user/sagarmainkar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up a structured learning pipeline for subjects that benefit from repeated study, objective testing, gap analysis, and scheduled follow-up sessions. It is best suited to complex topics with verifiable answers rather than quick summaries or opinion-based learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create durable cron jobs that continue running later.

Mitigation: Confirm the schedule before setup, inspect ~/.openclaw/cron/jobs.json after setup, and disable or remove pending learning jobs when autonomous sessions are no longer wanted.

Risk: Autonomous sessions can continue creating future learning work with limited later user control.

Mitigation: Use explicit topic slugs, clear stop or pause instructions, and the documented pause/resume flow to control whether the pipeline remains active.

Risk: The skill creates local learning files and state that influence later agent behavior.

Mitigation: Review the generated playbook, curriculum, and state.json before allowing scheduled sessions to proceed.

## Reference(s):

- [Learning Loop Methodology - GEARS](references/methodology.md)
- [Learning Playbook Template](references/playbook-template.md)
- [state.json Schema](references/state-schema.md)
- [OpenClaw](https://openclaw.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown learning files, JSON state, shell commands, and cron job configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates topic-specific local learning files and scheduled OpenClaw cron jobs when the user confirms setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
