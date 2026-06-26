## Description: <br>
Birthday helps agents manage member profiles, solar and lunar birthdays, anniversaries, and OpenClaw scheduled reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IfeyChan702](https://clawhub.ai/user/IfeyChan702) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to maintain personal or organizational member records, convert lunar birthdays, review upcoming events, and create birthday or anniversary reminders. It is intended for family, colleague, relative, and similar member-management workflows rather than general calendar scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Missing session identifiers can cause different users' member data to be stored in the same local namespace. <br>
Mitigation: Require a real per-user session key in shared OpenClaw or bot deployments and avoid using the shared default namespace. <br>
Risk: Member details, birthdays, notes, and reminder content may be stored as plaintext local JSON or embedded in persistent reminders. <br>
Mitigation: Limit sensitive notes in reminders, restrict local data directory permissions, and use encrypted backups if the data is backed up. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/IfeyChan702/mybirthday) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, API calls, configuration, guidance] <br>
**Output Format:** [Markdown or text responses with JSON file updates and scheduled-task calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local member and reminder JSON files and persistent scheduled reminders.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
