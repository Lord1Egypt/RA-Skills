## Description: <br>
Google Classroom: Manage classes, rosters, and coursework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Google Workspace administrators use this skill to inspect and run gws CLI commands for Google Classroom courses, rosters, coursework, invitations, registrations, and user profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated gws Classroom commands can create, update, patch, delete, invite, grade, or registration changes in Google Classroom. <br>
Mitigation: Before running mutating commands, inspect the schema, verify the target course, user, topic, coursework, or registration, and require explicit confirmation. <br>
Risk: The skill depends on the local gws CLI and shared Google Workspace authentication behavior. <br>
Mitigation: Install only when the gws CLI is trusted and review the shared auth and security guidance before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-classroom) <br>
- [Google Classroom grading periods licensing requirements](https://developers.google.com/workspace/classroom/grading-periods/manage-grading-periods#licensing_requirements) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown reference with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and Google Workspace authentication configured by the shared gws skill.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release evidence; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
