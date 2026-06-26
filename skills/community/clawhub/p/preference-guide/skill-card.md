## Description: <br>
Helps an agent ask one brief, non-sensitive follow-up question to capture reusable user preferences and store confirmed answers for future conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wubin010](https://clawhub.ai/user/wubin010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their users use this skill to convert recurring preferences, work habits, and stable constraints into future defaults without blocking the current task. It is intended for direct main-session conversations where lightweight preference capture can improve later assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change future agent behavior by adding memory rules or hook-based reminders. <br>
Mitigation: Install only when proactive preference capture is desired, and review AGENTS.md or OpenClaw hook entries before and after installation. <br>
Risk: Preference history may be stored locally in memory, state, and log files. <br>
Mitigation: Avoid answering with sensitive information, and periodically review or remove MEMORY.md, atr-state.json, and atr-log.jsonl. <br>
Risk: Users may want to disable or reset the behavior after installation. <br>
Mitigation: Remove the Ask-to-Remember memory section or hook files and delete the related local state/log files to reset behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wubin010/preference-guide) <br>
- [ATR Test Scenarios](artifact/references/test-scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON state and log entries, plus optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace memory, state, log, AGENTS.md, and optional OpenClaw hook files.] <br>

## Skill Version(s): <br>
1.0.5 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
