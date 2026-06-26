## Description: <br>
Google Workflow: Prepare for your next meeting: agenda, attendees, and linked docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and Google Workspace users use this skill to prepare for the next upcoming meeting by reviewing agenda context, attendees, descriptions, and linked materials. Agents use it to invoke the read-only gws meeting-prep workflow and summarize the returned meeting context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private calendar meeting details, attendees, descriptions, and linked materials to the agent. <br>
Mitigation: Use it only with a trusted gws CLI setup, review the gws-shared authentication guidance, and run it only in contexts where the agent is allowed to view the meeting data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-workflow-meeting-prep) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>
- [gws-shared auth and global flags](../gws-shared/SKILL.md) <br>
- [gws-workflow commands](../gws-workflow/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text, Markdown] <br>
**Output Format:** [Markdown with inline bash commands; the referenced CLI can return json, table, yaml, or csv.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and read access to Google Workspace calendar data.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
