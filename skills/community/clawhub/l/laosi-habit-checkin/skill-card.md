## Description: <br>
习惯追踪 - 每天打卡，自动计算连续天数/历史最佳/总打卡数，多习惯管理，本地JSON持久化 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill to record daily habit check-ins, inspect current and best streaks, and manage multiple independent habits with local persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words such as check-in or habit-related terms could invoke the skill unintentionally. <br>
Mitigation: Use explicit habit-tracking requests before recording a check-in, and confirm the target habit name before saving progress. <br>
Risk: Habit names and progress can be saved locally in JSON, which may expose sensitive personal routines if used for private health, financial, or personal records. <br>
Mitigation: Review the storage location and avoid recording sensitive personal data unless local persistence is acceptable for the user and environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-habit-checkin) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown and text with Python code, shell command examples, and JSON data examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local JSON habit state when the included Python tracker is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
