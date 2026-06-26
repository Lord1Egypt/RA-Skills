## Description: <br>
Builds a concise "what needs action now" daily brief by aggregating reminders from email, calendar, SMS/iMessage, weather, and task notes, then prioritizing them into Must-do, Should-do, and Nice-to-have items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YIKAILucas](https://clawhub.ai/user/YIKAILucas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and business leaders use this skill to turn connected personal and work signals into a short action brief for today or the next 72 hours. It adapts priorities for CEO, department lead, or individual contributor planning when the user provides a role. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may summarize sensitive personal sources such as calendars, messages, email, notes, tasks, weather, and billing notifications. <br>
Mitigation: Use specific accounts, channels, and time windows, keep redaction enabled for secrets and account numbers, and review the brief before acting. <br>
Risk: Missing or ambiguous dates, amounts, or source availability can make priorities incomplete or uncertain. <br>
Mitigation: Downgrade uncertain items, mark unknown details explicitly, and prefer fewer high-confidence actions over a noisy list. <br>


## Reference(s): <br>
- [Life Radar Modes](references/modes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/YIKAILucas/life-radar-repo) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown daily brief with prioritized action lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits Must-do to 3 items, Should-do to 5 items, and Nice-to-have to 3 items; marks missing deadlines or uncertainty explicitly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
