## Description: <br>
习惯养成打卡助手，连续激励、数据统计、陪你养成好习惯。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[786793119](https://clawhub.ai/user/786793119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage habit check-ins, track streaks and completion rates, and provide milestone-based encouragement for personal habit building. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Habit names or descriptions may include sensitive personal or health details that remain on local disk. <br>
Mitigation: Avoid recording secrets or highly sensitive health information, and delete ~/.memory/habits/habits.json when records are no longer needed. <br>
Risk: The examples invoke a Python helper that is not included in the artifact. <br>
Mitigation: Only run the referenced helper if it was obtained from a trusted source and reviewed before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/786793119/habit-tracker-companion) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local habit data stored at ~/.memory/habits/habits.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
