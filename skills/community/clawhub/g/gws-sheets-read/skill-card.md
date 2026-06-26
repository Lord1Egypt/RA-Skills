## Description: <br>
Google Sheets: Read values from a spreadsheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to read values from a specified Google Sheets spreadsheet range through the local gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read spreadsheet data from an unintended Google account, spreadsheet, or range. <br>
Mitigation: Confirm the gws authentication context, spreadsheet ID, and range before execution. <br>
Risk: The skill depends on a local gws CLI installation. <br>
Mitigation: Use only a trusted gws CLI installation and review the gws-shared authentication instructions before use. <br>


## Reference(s): <br>
- [Gws Sheets Read ClawHub release](https://clawhub.ai/googleworkspace-bot/gws-sheets-read) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gws CLI and reads only the spreadsheet range specified by the user.] <br>

## Skill Version(s): <br>
1.0.13 (source: ClawHub release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
