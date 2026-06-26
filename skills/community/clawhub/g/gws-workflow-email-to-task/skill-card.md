## Description: <br>
Google Workflow: Convert a Gmail message into a Google Tasks entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and productivity operators use this skill to turn a specified Gmail message into a Google Tasks entry through the gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can read email-derived content and create a real Google Tasks item. <br>
Mitigation: Confirm the Gmail message ID, destination task list, and Google account before running the command. <br>
Risk: The workflow depends on the local gws CLI and its Google authorization setup. <br>
Mitigation: Install and run it only when the gws CLI and configured Google account are trusted for the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-workflow-email-to-task) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI, a Gmail message ID, and Google account authorization.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
