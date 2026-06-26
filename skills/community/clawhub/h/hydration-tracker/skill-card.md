## Description: <br>
Track daily water intake, set hydration goals, and get drink reminders. Use when logging water, setting targets, or reviewing weekly intake trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this local command-line utility to log water intake, set daily hydration targets, check progress during the day, and review recent intake history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores hydration goal and intake history as local wellness records under ~/.water_reminder. <br>
Mitigation: Install only if local storage of these records is acceptable, and delete ~/.water_reminder to remove the saved data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/hydration-tracker) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Hydration Tracker documentation](https://bytesagain.com/skills/hydration-tracker) <br>
- [BytesAgain support](https://bytesagain.com/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output from a Bash utility with local JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores intake history and hydration goals locally under ~/.water_reminder.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
