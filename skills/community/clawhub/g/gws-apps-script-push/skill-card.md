## Description: <br>
Google Apps Script: Upload local files to an Apps Script project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to prepare shell commands for uploading local Google Apps Script source files to a selected Apps Script project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The push command replaces all files in the target Apps Script project. <br>
Mitigation: Confirm the project ID, source directory, and user intent before executing the command. <br>
Risk: The command depends on the local gws CLI and Google account authentication. <br>
Mitigation: Use a trusted gws CLI installation and verify it is authenticated to the intended Google account before use. <br>


## Reference(s): <br>
- [Gws Apps Script Push on ClawHub](https://clawhub.ai/googleworkspace-bot/gws-apps-script-push) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and a target Apps Script project ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
