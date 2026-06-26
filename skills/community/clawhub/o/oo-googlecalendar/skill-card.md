## Description: <br>
Google Calendar (workspace.google.com). Use this skill for ANY Google Calendar request, including reading, creating, updating, and deleting calendar data through the OOMOL Google Calendar connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a connected Google Calendar account through OOMOL. It supports calendar and event lookup, free/busy checks, incremental sync, and confirmed create, update, ACL, and delete workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, move, import, or sync Google Calendar data. <br>
Mitigation: Confirm the exact action, target calendar or event, and JSON payload with the user before running write actions. <br>
Risk: The skill can delete calendar resources, clear calendars, remove attendees, and remove calendars from a list. <br>
Mitigation: Require explicit user approval for destructive actions and verify the target identifier before execution. <br>
Risk: The skill depends on OOMOL account access, OAuth connection state, and optional CLI installation. <br>
Mitigation: Only perform setup or connection steps after an action fails for that reason and only when the user trusts OOMOL for this integration. <br>


## Reference(s): <br>
- [ClawHub Google Calendar skill page](https://clawhub.ai/oomol/oo-googlecalendar) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI repository](https://github.com/oomol-lab/oo-cli) <br>
- [Google Calendar homepage](https://workspace.google.com/products/calendar/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs OOMOL connector actions and expects JSON responses with data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
