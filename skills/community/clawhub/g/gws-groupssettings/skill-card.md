## Description: <br>
Manage Google Groups settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Workspace administrators and agents use this skill to inspect and manage Google Groups settings through the gws CLI, including get, patch, and update operations after reviewing method schemas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Google Workspace group settings through patch or update operations under the active gws account. <br>
Mitigation: Verify the active gws account and OAuth scopes, limit use to intended groups and settings, and require confirmation of the exact patch or update payload before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-groupssettings) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and CLI payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and shared Google Workspace authentication setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
