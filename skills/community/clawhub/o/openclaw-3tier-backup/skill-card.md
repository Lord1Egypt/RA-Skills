## Description:

Automated backup in 3 layers: daily timestamped snapshots, secondary drive mirror, and emergency conversation export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI workspace users use this skill to set up layered local backups, mirror a workspace to secondary storage, and keep a standalone local emergency chat file available for recovery scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The mirror restore command uses `robocopy /MIR`, which can delete destination files that are not present in the mirror.

Mitigation: Restore into a new empty directory or run a dry run before pointing the mirror command at a live workspace.

Risk: Backup and restore paths are placeholders and must be adapted to the user's local Windows environment.

Mitigation: Review and customize workspace, backup, and mirror paths before registering scheduled tasks or running restore commands.

Risk: The emergency chat sends prompts to a local Ollama service.

Mitigation: Avoid sensitive prompts unless the local Ollama instance is trusted and controlled by the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/openclaw-3tier-backup)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown guidance with PowerShell commands and a standalone HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local backup setup instructions, restore commands, retention guidance, and an emergency Ollama chat HTML artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
