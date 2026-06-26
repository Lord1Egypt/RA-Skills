## Description: <br>
Create, list, and manage macOS Calendar events via AppleScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucaperret](https://clawhub.ai/user/lucaperret) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to translate scheduling requests into validated macOS Calendar actions, including listing calendars and creating one-time or recurring events with reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create events in configured macOS calendars. <br>
Mitigation: List calendars first and confirm the calendar, date, time, alarm, and recurrence before creating an event. <br>
Risk: Event titles are saved in a local action log. <br>
Mitigation: Avoid highly sensitive event titles when local logs may be exposed through backups or other local access. <br>


## Reference(s): <br>
- [iCal Recurrence Rules](references/recurrence.md) <br>
- [ClawHub skill page](https://clawhub.ai/lucaperret/macos-calendar) <br>
- [Project homepage](https://github.com/lucaperret/agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS Calendar.app, osascript, and python3; creates events through local AppleScript and writes a local action log.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
