## Description: <br>
Personal Nutritionist helps an agent log meals, estimate portions, calculate calories and macros, summarize nutrition trends, and maintain a user nutrition profile through conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javi23ruiz](https://clawhub.ai/user/javi23ruiz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a conversational nutrition tracker for meal logging, calorie and macro estimates, daily or weekly summaries, and optional reminders. It is intended to support personal tracking workflows, not replace medical or dietetic advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and reuse sensitive long-term information about meals, goals, allergies, routines, health context, and possible medication details. <br>
Mitigation: Review the memory behavior before use, share only information suitable for retention, and inspect, edit, or delete saved memory when needed. <br>
Risk: Heartbeat and cron reminders can continue prompting or summarizing based on saved nutrition data. <br>
Mitigation: Enable only the reminders the user explicitly wants, review the scheduled messages, and disable unwanted jobs. <br>
Risk: Nutrition, calorie, macro, and burn calculations are estimates and may be inappropriate for medical dietary decisions. <br>
Mitigation: Confirm uncertain portions, treat outputs as estimates, and use qualified professional advice for medical or clinical nutrition needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/javi23ruiz/nutrition-pro) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Onboarding workflow](artifact/ONBOARDING.md) <br>
- [Memory template](artifact/MEMORY_TEMPLATE.md) <br>
- [Heartbeat snippet](artifact/HEARTBEAT_SNIPPET.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational Markdown with meal summaries, memory-file entries, and optional OpenClaw cron commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update MEMORY.md, memory/YYYY-MM-DD.md, HEARTBEAT.md, and scheduled reminder configuration after user confirmation.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
