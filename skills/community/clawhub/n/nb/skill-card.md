## Description: <br>
Manage notes, bookmarks, and notebooks using the nb CLI. Create, list, search, and organize notes across multiple notebooks with Git-backed versioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjesuiter](https://clawhub.ai/user/bjesuiter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CLI users use this skill to operate the nb note-taking tool through concise command guidance for creating, finding, editing, organizing, syncing, and deleting notes, bookmarks, todos, folders, and notebooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sync, delete, and advanced Git commands can change local notes or remote repositories. <br>
Mitigation: Review the nb Git remote before syncing and confirm destructive or force-delete commands before running them. <br>
Risk: Notes or bookmarks may contain secrets or private information that could be pushed to a remote repository. <br>
Mitigation: Avoid storing secrets in nb unless the configured remote is private and trusted. <br>
Risk: Manual edits inside ~/.nb can bypass nb indexing and expected Git commits. <br>
Mitigation: Use nb CLI commands for changes and rebuild the index only when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bjesuiter/nb) <br>
- [nb Project Homepage](https://github.com/xwmx/nb) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nb CLI on darwin or linux; guidance emphasizes using nb commands instead of manually editing ~/.nb repositories.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
