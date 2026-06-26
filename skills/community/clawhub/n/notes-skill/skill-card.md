## Description: <br>
SQLite-based notes management for OpenClaw agents to create, search, list, archive, and back up local notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cocoonovo](https://clawhub.ai/user/cocoonovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to let an agent maintain a persistent local notes database, including note creation, search, listing, archiving, and backup rotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad note-related trigger phrases could cause note actions to happen more easily than intended. <br>
Mitigation: Use clear note-management commands and confirm before listing, searching, archiving, or backing up notes. <br>
Risk: The skill stores notes persistently in a local SQLite database, which may include sensitive user content. <br>
Mitigation: Avoid storing highly sensitive information unless the local environment and backup location are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cocoonovo/notes-skill) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database at ~/.openclaw/workspace/notes/notes.db and backup files under ~/.openclaw/workspace/notes/backups/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
