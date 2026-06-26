## Description: <br>
Joplin CLI helper for creating, viewing, editing, and syncing notes from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to operate Joplin through shell commands for notebook management, note creation and editing, sync configuration, import/export, and scripted workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Note edits, notebook deletion, sync, and uninstall commands can change or remove local and remote Joplin data. <br>
Mitigation: Confirm the target notebook or note, verify the configured sync destination, and back up Joplin data before destructive or removal commands. <br>
Risk: Sync configuration examples include command-line password fields that may expose credentials in shell history or process listings. <br>
Mitigation: Avoid putting passwords directly on the command line; use safer credential handling supported by the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/killgfat/joplin-cli) <br>
- [Joplin terminal shell mode documentation](https://joplinapp.org/help/apps/terminal/#shell-mode) <br>
- [Joplin terminal installation documentation](https://joplinapp.org/help/apps/terminal/#installation) <br>
- [COMMANDS.md](references/COMMANDS.md) <br>
- [INSTALL.md](references/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Joplin CLI binary named joplin.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence release.version and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
