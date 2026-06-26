## Description: <br>
Reading intelligence that helps an agent log books, capture quotes, and surface relevant reading context from local markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilyabelikin](https://clawhub.ai/user/ilyabelikin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Pages to give an agent a private, searchable reading memory: books, quotes, notes, ratings, recommendations, and topic-based recall stored as local markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local book notes, ratings, quotes, and recommendation trails can contain sensitive personal reflections that may be resurfaced in later conversations. <br>
Mitigation: Keep sensitive reflections out of Pages unless the user is comfortable with future recall, and review local files before sharing or syncing the workspace. <br>
Risk: Optional web lookups and cover-image fetching can disclose reading interests or spend extra tokens. <br>
Mitigation: Ask before web or image lookups and keep the default image setting disabled unless the user explicitly enables it. <br>
Risk: Heartbeat or cron reminders can create recurring agent activity that the user may not expect. <br>
Mitigation: Confirm before adding Pages checks to HEARTBEAT.md or cron, and make the schedule visible to the user. <br>
Risk: Peeps integration may write recommendation details into personal-network files. <br>
Mitigation: Ask before cross-writing to Peeps files and keep recommendation links limited to information the user provided. <br>
Risk: Replacing the skill from an unpinned GitHub main URL can pull unreviewed changes. <br>
Mitigation: Prefer reviewed ClawHub releases or pinned source revisions when updating the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ilyabelikin/pages) <br>
- [Publisher profile](https://clawhub.ai/user/ilyabelikin) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and concise conversational guidance with optional shell commands and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local files under mind/pages/ and may suggest optional reminder or integration changes when the user approves.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
