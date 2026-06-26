## Description: <br>
Scans a local GOG library for installed games not played in 30 or more days, then can email a summary through himalaya and add per-game Apple Reminders through remindctl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to review dormant installed GOG games, generate a cleanup report, and optionally create email and Apple Reminders follow-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal execution can email reports and create Apple Reminders. <br>
Mitigation: Run with --dry-run first, confirm the recipient email, himalaya account, and Reminders list, or use --no-email and --no-reminders for a local scan only. <br>
Risk: Emailed reports can include local install paths and play-history metadata. <br>
Mitigation: Review report content before sending and avoid sending it to recipients who should not receive local library details. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and plain-text report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke himalaya for email and remindctl for Apple Reminders unless dry-run or skip flags are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
