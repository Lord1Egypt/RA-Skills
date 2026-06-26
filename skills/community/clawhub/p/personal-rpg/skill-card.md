## Description: <br>
个人RPG系统 - 将日常变成游戏，完成任务获得经验值，升级解锁新能力 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yansocool](https://clawhub.ai/user/yansocool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn personal tasks into an RPG-style progress system with tasks, experience points, levels, attributes, achievements, and statistics. It is suited for local personal productivity tracking where the user is comfortable storing task and progress records on disk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task descriptions, completion history, achievements, stats, and character progress are stored as local JSON files. <br>
Mitigation: Avoid entering sensitive personal details unless local retention is acceptable, and delete the local personal-rpg data directory to reset or remove records. <br>
Risk: The skill modifies local progress files as part of normal task tracking behavior. <br>
Mitigation: Review the local workspace path and keep backups if the task history or character progress should be preserved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yansocool/personal-rpg) <br>
- [Project homepage](https://github.com/openclaw/personal-rpg) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON files, guidance] <br>
**Output Format:** [Plain text status messages and local JSON records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists character, task, achievement, and statistics data under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
