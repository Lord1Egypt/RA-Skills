## Description: <br>
Olympic Alert helps an agent check, list, add, and remove Olympic event reminders from a local schedule, with Korean team defaults for the 2026 Milano Cortina Winter Olympics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garibong-labs](https://clawhub.ai/user/garibong-labs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to maintain a local Olympic event schedule and receive reminder text with broadcast links shortly before configured events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The add and remove commands modify the bundled schedule file, and pattern-based removal may delete more than one matching event. <br>
Mitigation: Review the schedule before and after edits, use specific event-name patterns for removal, and keep a backup of scripts/events.json when maintaining important schedules. <br>
Risk: Reminder checks write local notification state under ~/.config/olympic-alert/state.json, which can suppress repeated alerts for events already marked as notified. <br>
Mitigation: Inspect or reset the local state file when retesting reminders or when a notification should be sent again. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/garibong-labs/olympic-alert) <br>
- [Naver Sports Milano Cortina 2026](https://m.sports.naver.com/milanocortina2026) <br>
- [Chzzk Olympic search](https://chzzk.naver.com/search?query=올림픽) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Plain text or Markdown reminders with inline links; command examples use shell snippets and JSON schedule data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and stores reminder state in ~/.config/olympic-alert/state.json.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
