## Description:

MultiDesktop helps agents guide Windows users through managing virtual desktop configurations, switching Desktop folder paths, and configuring per-desktop wallpapers through GUI or CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qibowen2008](https://clawhub.ai/user/qibowen2008)

### License/Terms of Use:

MIT-0

## Use Case:

Windows users and support agents use this skill to manage MultiDesktop workflows for adding, editing, deleting, listing, and switching desktop configurations. It is most relevant when an agent needs to explain or operate Windows Desktop folder redirection and per-desktop wallpaper settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill may lead an agent to redirect the live Windows Desktop folder or update HKCU registry settings.

Mitigation: Confirm the user wants the change, record or back up the current Desktop path first, and require explicit confirmation before switching desktop configurations.

Risk: Desktop deletion guidance could remove a configured desktop entry before the user understands the behavior.

Mitigation: Verify what DeleteDesktop will remove and ask for explicit confirmation before deleting desktop configurations.

## Reference(s):

- [ClawHub MultiDesktop skill page](https://clawhub.ai/qibowen2008/skills/multidesktop)
- [MultiDesktop repository](https://github.com/Qibowen2008/MultiDesktop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline CLI commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Windows-specific operational guidance for Desktop folder paths, wallpaper settings, XML configuration files, and CLI usage.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
