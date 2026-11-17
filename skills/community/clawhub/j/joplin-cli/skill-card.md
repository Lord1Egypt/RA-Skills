## Description:

Joplin Cli helps agents use the Joplin terminal app to create, view, edit, organize, and sync notes from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killgfat](https://clawhub.ai/user/killgfat)

### License/Terms of Use:


## Use Case:

Developers, technical note-takers, and automation agents use this skill to operate a local Joplin CLI profile for notebook and note management, including creation, editing, search-oriented listing, import/export, and sync workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes broad note-changing workflows, including commands that can create, edit, move, delete, import, export, and sync Joplin data.

Mitigation: Confirm the active Joplin profile and notebook before write operations, and require explicit review before delete, import/export, or sync commands are run.

Risk: Force-delete and uninstall examples can remove notebooks, notes, or local Joplin data.

Mitigation: Back up notes before using force-delete or uninstall commands, and avoid automated execution of destructive examples without human confirmation.

Risk: Sync configuration examples include password-style values and can point the profile at a remote target.

Mitigation: Do not place real sync passwords directly in shell commands; use safer secret handling where available and confirm the remote target before running `joplin sync`.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/killgfat/skills/joplin-cli)
- [Joplin Terminal Shell Mode](https://joplinapp.org/help/apps/terminal/#shell-mode)
- [Joplin Terminal Installation](https://joplinapp.org/help/apps/terminal/#installation)
- [Joplin CLI Complete Command Reference](references/COMMANDS.md)
- [Joplin Terminal Installation Guide](references/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local joplin CLI binary; generated commands can modify, delete, export, import, or sync notes in the active Joplin profile.]

## Skill Version(s):

0.1.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
