## Description: <br>
个人日程管理 Skill supports natural-language calendar creation, editing, deletion, automatic reminders, recurring events, a local web UI, and .ics import/export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tech-fcc-sys](https://clawhub.ai/user/tech-fcc-sys) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individual users use this skill to manage personal schedules from conversational Chinese commands, local browser views, and calendar import/export workflows. It is intended for personal calendar organization, reminders, and lightweight interoperability with common calendar tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal calendar events, reminders, recipient IDs, backups, and imported or exported calendar files may remain on disk in plaintext. <br>
Mitigation: Use the skill only on a trusted device, review local data and backup files regularly, and avoid storing sensitive calendar details unless the local environment is appropriately protected. <br>
Risk: Reminder delivery can use a configured Feishu recipient value. <br>
Mitigation: Review data/config.json before use and remove or replace any Feishu recipient value so reminders are sent only to the intended account. <br>
Risk: Natural-language delete and reschedule commands can modify stored events when a single match is found. <br>
Mitigation: Use specific event titles or times, review command output, and back up the local calendar before bulk use or importing external calendars. <br>
Risk: The web UI uses port 8080 and should be treated as a local management interface. <br>
Mitigation: Run the web UI only on a trusted machine or network and stop it when calendar management is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tech-fcc-sys/personal-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [CLI text output, local JSON/SQLite/ICS files, and browser-rendered HTML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local calendar data, reminder job files, backups, and imported or exported .ics files.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
