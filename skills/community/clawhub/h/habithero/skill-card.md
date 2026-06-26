## Description: <br>
Habit tracker with streak counting and visual calendars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and productivity-focused agents use Habithero to record habits, plans, reminders, reviews, priorities, and streak-related activity locally, then review recent activity, summary statistics, and exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Habit, planning, reminder, review, and related productivity text is stored locally in plaintext and can be exported. <br>
Mitigation: Use on trusted machines, avoid entering sensitive personal data, and review or remove local logs and exports before sharing or backup. <br>
Risk: The user-facing description does not fully explain the broader planning, reminder, review, archive, timeline, report, and export command set. <br>
Mitigation: Review `habithero help`, the local data directory, and generated export files before relying on or distributing results. <br>


## Reference(s): <br>
- [ClawHub Habithero Skill Page](https://clawhub.ai/bytesagain-lab/habithero) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>
- [BytesAgain Feedback](https://bytesagain.com/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration] <br>
**Output Format:** [Command-line text with local log files and optional JSON, CSV, or TXT exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores plaintext productivity history under ~/.local/share/habithero and can export local history to JSON, CSV, or TXT.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
