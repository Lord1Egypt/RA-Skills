## Description: <br>
Google Tasks: Manage task lists and tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect Google Tasks commands and operate on authenticated task lists and tasks through the gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide delete, clear, patch, update, and assigned-task operations that may remove, hide, or alter Google Tasks data. <br>
Mitigation: Require explicit user confirmation before destructive or mutating commands and review generated parameters before execution. <br>
Risk: Commands operate on the currently authenticated Google account. <br>
Mitigation: Verify the authenticated Google account before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-tasks) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and an authenticated Google account; users should inspect command schemas before invoking API methods.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
