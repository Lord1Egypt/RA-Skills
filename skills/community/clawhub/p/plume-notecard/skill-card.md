## Description:

Plume NoteCard helps agents turn topics, long-form text, reference images, batches, and slide-deck requests into designed notecards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dake6767](https://clawhub.ai/user/dake6767)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan and generate information-rich notecards, infographic-style cards, batch card sets, and image slide decks through the Plume service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-controlled Plume configuration can affect how the skill locates credentials and media storage.

Mitigation: Use the skill only in trusted workspaces, review .plume-notecard/EXTEND.md before execution, and prefer a controlled PLUME_API_KEY configuration.

Risk: Uploaded source images, generated media, and action logs may contain private or sensitive content.

Mitigation: Avoid confidential documents or sensitive images, and review or clear the media and action-log directory after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dake6767/skills/plume-notecard)
- [Plume Notecard Service](https://design.useplume.app/notecard)
- [Plume Template Gallery](https://design.useplume.app/notecard/templates?lang=en)
- [Notecard Modes and Parameters](references/modes.md)
- [Notecard Workflow Examples](references/workflows.md)
- [Error Codes Reference](references/error-codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON command results, generated image files, and optional PDF or ZIP artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PLUME_API_KEY and can write generated media and action logs to the agent media directory.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
