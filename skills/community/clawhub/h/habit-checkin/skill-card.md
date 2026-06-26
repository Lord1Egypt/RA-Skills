## Description: <br>
Tracks daily habit check-ins and reports current streak, best streak, and total check-in days. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill with an agent to record daily habit check-ins and monitor streak progress over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases such as "check in", "打卡", or "签到" could cause an unintended habit check-in. <br>
Mitigation: Use explicit habit-related prompts and confirm intent before recording ambiguous check-ins. <br>
Risk: Habit streak data is stored locally and may reflect personal routine information. <br>
Mitigation: Store the JSON file in a user-controlled location and avoid sharing or syncing it unless the user intends to. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/534422530/habit-checkin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown or plain-text agent responses with local JSON state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records check-in state in a local habit_streaks.json file when the host agent implements the skill behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
