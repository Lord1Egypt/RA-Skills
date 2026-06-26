## Description: <br>
Manage quick notes and time-based reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yusaku-0426](https://clawhub.ai/user/yusaku-0426) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage quick notes and schedule time-based reminders, including listing pending reminders and checking which reminders are due. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references helper scripts that are not included in the artifact. <br>
Mitigation: Review before installing and use it only when the required scripts are available from a trusted source. <br>
Risk: Reminder text can be posted to chat channels without clear safeguards. <br>
Mitigation: Confirm the channel, account, message text, and timezone before any reminder posts into a chat space. <br>
Risk: Natural-language reminder times are interpreted in the Asia/Tokyo timezone. <br>
Mitigation: Confirm the resolved ISO 8601 reminder time with the user before creating or firing a reminder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yusaku-0426/notes-reminders) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires external notes.js and reminders.js helper scripts referenced by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
