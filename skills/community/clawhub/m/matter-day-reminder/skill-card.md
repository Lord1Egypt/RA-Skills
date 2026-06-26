## Description: <br>
Matter Day Reminder helps users manage birthdays, anniversaries, and other important dates for family and friends with local contact files, lunar and solar date support, two-stage reminders, and generated wishes and gift suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[norfish](https://clawhub.ai/user/norfish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a personal social assistant to record contact events, check upcoming birthday or anniversary reminders, and draft relationship-aware wishes or gift suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores friends' and family members' dates, relationship details, interests, and notes in readable local Markdown/YAML files. <br>
Mitigation: Keep the reminder data directory private, avoid committing it to shared repositories, and back it up only to trusted locations. <br>
Risk: Email fallback configuration can contain mailbox credentials. <br>
Mitigation: Use an app-specific password and keep config.yml out of shared folders, logs, and Git history. <br>
Risk: Leap-month lunar dates may be scheduled incorrectly. <br>
Mitigation: Review leap-month reminders manually and confirm the converted solar date before acting on the reminder. <br>


## Reference(s): <br>
- [Reminder Data Schema](references/data-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/norfish/matter-day-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with YAML, JSON, JavaScript, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Markdown contact files and local YAML configuration when the user asks to manage reminders.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
