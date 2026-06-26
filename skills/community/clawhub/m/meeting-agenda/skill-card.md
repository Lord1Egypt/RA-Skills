## Description: <br>
Meeting Agenda helps agents create Chinese meeting agendas and templates for standups, retrospectives, one-on-ones, decision meetings, and meeting minutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and team leads use this skill to draft Chinese meeting agendas, standup and retrospective formats, one-on-one outlines, decision-meeting agendas, and meeting minutes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting details or task text entered into the task-tracking script can be saved on disk. <br>
Mitigation: Avoid entering sensitive meeting content unless local storage is acceptable; set MEETING_AGENDA_DIR to a controlled location when testing or using task commands. <br>
Risk: Some task-tracking commands may report changes that were not actually persisted. <br>
Mitigation: Treat task-status output as advisory and verify saved data before relying on it for meeting follow-up. <br>


## Reference(s): <br>
- [Meeting Agenda ClawHub page](https://clawhub.ai/bytesagain-lab/meeting-agenda) <br>
- [Meeting Agenda tips](artifact/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plain text with shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agenda prompts and templates are primarily Chinese; the included task-tracking shell script writes local data when its task commands are used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
