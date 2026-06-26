## Description: <br>
Manage an executive's schedule, inbox, and communications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or delegated support agents use this persona to review an executive's agenda, prepare for meetings, triage inbox items, and draft or schedule Google Workspace communications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to send email from an executive account without a clear approval step. <br>
Mitigation: Show recipients and the full outbound email body for explicit approval before sending. <br>
Risk: Calendar changes and inbox triage may affect sensitive executive workflows. <br>
Mitigation: Use least-privilege Google Workspace scopes and confirm calendar changes before committing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/persona-exec-assistant) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and the gws-gmail, gws-calendar, gws-drive, and gws-chat utility skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
