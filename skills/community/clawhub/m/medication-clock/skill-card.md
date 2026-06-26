## Description: <br>
优甲乐智能服药提醒系统 - 每日6:30提醒，智能统计，数据导出。适合甲状腺疾病患者建立规律服药习惯。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbingithub](https://clawhub.ai/user/robbingithub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who take levothyroxine use this skill to receive medication reminders, record doses, review adherence statistics, and export local medication history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medication history is sensitive and is stored locally under ~/.openclaw/medication_data. <br>
Mitigation: Review local file permissions and keep exported CSV files out of shared or synced folders unless that sharing is intended. <br>
Risk: Included scripts can modify medication records, and test_system.py includes cleanup behavior that can reset records. <br>
Mitigation: Avoid running test_system.py with --cleanup against real records unless a backup has been verified and record reset is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robbingithub/medication-clock) <br>
- [Publisher profile](https://clawhub.ai/user/robbingithub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown-style text responses, local JSON records, and CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores medication records locally under ~/.openclaw/medication_data and can export CSV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
