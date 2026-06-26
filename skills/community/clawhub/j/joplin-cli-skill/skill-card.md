## Description: <br>
Interact with Joplin notes via the Joplin CLI for reading, creating, editing notes, managing todos, WebDAV sync, and kanban-formatted notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davek-dev](https://clawhub.ai/user/davek-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent operate a local Joplin CLI for note reading, creation, editing, todo management, notebook management, WebDAV sync, imports, exports, and kanban-note maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect note or notebook identifiers could cause unintended edits or deletion. <br>
Mitigation: Confirm note IDs before edits or deletion and verify changes with Joplin CLI commands such as listing notes and reading note content. <br>
Risk: WebDAV sync configuration can expose credentials or sync notes to an untrusted server. <br>
Mitigation: Protect WebDAV passwords and sync only to a trusted server. <br>
Risk: Direct database edits can cause sync conflicts or data loss. <br>
Mitigation: Use the Joplin CLI for note operations and avoid modifying the SQLite database directly. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/davek-dev/joplin-cli-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include Joplin CLI commands that read, create, edit, delete, sync, import, export, or verify notes and notebooks.] <br>

## Skill Version(s): <br>
1.3.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
