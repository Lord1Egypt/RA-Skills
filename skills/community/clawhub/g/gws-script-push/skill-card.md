## Description: <br>
Google Apps Script: Upload local files to an Apps Script project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace administrators use this skill to prepare `gws script +push` commands that upload local Google Apps Script files to a target Apps Script project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the push command can overwrite every file in the target Apps Script project. <br>
Mitigation: Confirm the script ID, source directory, active Google/GWS account, and recovery plan before execution. <br>
Risk: The skill depends on the local `gws` CLI and its authenticated account context. <br>
Mitigation: Install and use it only when the local `gws` CLI is trusted and authenticated to the intended Google account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-script-push) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command flags such as `--script` and `--dir`; the resulting command can replace all files in the target Apps Script project.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; skill metadata: 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
