## Description:

Google Classroom: Manage classes, rosters, and coursework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and agent operators use this skill to inspect and run Google Workspace CLI commands for Google Classroom courses, rosters, coursework, invitations, registrations, and user profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Classroom delete, update, invitation, roster, and registration operations can change courses, membership, notifications, or related Classroom data.

Mitigation: Require explicit user confirmation before write operations and verify target course IDs, user IDs, invitation IDs, and Pub/Sub topics before execution.

Risk: Incorrect parameters or permissions can cause failed Classroom API calls or unintended target selection.

Mitigation: Inspect each method with gws schema classroom.<resource>.<method> and confirm required parameters, types, and defaults before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-classroom)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)
- [Google Classroom grading periods licensing requirements](https://developers.google.com/workspace/classroom/grading-periods/manage-grading-periods#licensing_requirements)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and CLI parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and command inspection with gws classroom --help or gws schema before API calls.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
