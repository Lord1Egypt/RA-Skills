## Description: <br>
Calendar synchronization skill. Sync events between Google Calendar, Outlook, and local storage. Supports CRUD operations and reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and scheduling-focused users use this skill to guide calendar event creation, listing, deletion, availability checks, reminders, recurring events, and synchronization across Google Calendar, Outlook, and local storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth client secrets and calendar permissions can expose access to personal or organizational calendar data. <br>
Mitigation: Protect OAuth secrets, use the narrowest calendar permissions available, and avoid storing credentials where unrelated agents or users can read them. <br>
Risk: Create, edit, and delete operations can change or remove real calendar events. <br>
Mitigation: Manually confirm the target account, calendar, event ID, event details, and operation type before applying changes. <br>
Risk: The referenced calendar.py provider implementation may be supplied separately from this artifact. <br>
Mitigation: Inspect the implementation before installing or running it, especially any provider authentication, sync, and deletion logic. <br>


## Reference(s): <br>
- [Calendar Sync on ClawHub](https://clawhub.ai/jpengcheng523-netizen/jpeng-calendar-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell command snippets, environment variable configuration, and JSON result examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calendar operations may affect connected Google Calendar or Outlook data when a provider implementation is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: metadata, release evidence, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
