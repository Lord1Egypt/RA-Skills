## Description: <br>
习惯养成教练。充当AI问责伙伴，帮助建立、追踪和坚持好习惯。Keywords: 习惯养成, 自律, habit tracker, 打卡. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codekungfu](https://clawhub.ai/user/codekungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan habits, record habit check-ins, review progress, and generate habit coaching reports from local habit history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Habit check-ins and routine details are stored locally in the skill directory. <br>
Mitigation: Avoid entering sensitive health, location, or private routine details unless local retention is acceptable. <br>
Risk: The instructions request installing requests even though the bundled tool does not use it. <br>
Mitigation: Skip unnecessary dependency installation unless a future version requires it. <br>


## Reference(s): <br>
- [Habit Coach Guide](references/habit_coach_guide.md) <br>
- [Atomic Habits Framework](https://jamesclear.com/atomic-habits) <br>
- [awesome-openclaw-usecases Habit Tracker](https://github.com/hesamsheikh/awesome-openclaw-usecases) <br>
- [Reddit AI Habit Tracker Discussion](https://www.reddit.com/r/productivity/comments/ai_habit_tracker/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local habit history file under the skill directory when the bundled Python tool is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
