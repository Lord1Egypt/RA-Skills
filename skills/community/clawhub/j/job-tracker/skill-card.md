## Description: <br>
Track job applications, contacts, deadlines, and follow-up reminders in a local SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mehulupase01](https://clawhub.ai/user/mehulupase01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to log job applications, update statuses after recruiter interactions, find upcoming follow-ups, and summarize an application pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local job-search records, recruiter contact details, and notes may be retained in a SQLite database under the skill directory. <br>
Mitigation: Store only necessary information, avoid using the database on shared, backed-up, or synced devices when sensitive details are present, and remove .runtime/job-tracker.db when records should no longer be retained. <br>
Risk: Unconfirmed application updates or inferred dates could make the tracker inaccurate. <br>
Mitigation: Confirm required fields and tentative dates with the user before writing or updating records. <br>


## Reference(s): <br>
- [Job Tracker source homepage](https://github.com/Mehulupase01/openclaw-skill-suite/tree/main/skills/job-tracker) <br>
- [Status Guide](references/status-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-producing CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database under the skill directory for stored application records.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
