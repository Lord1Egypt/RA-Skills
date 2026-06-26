## Description: <br>
Life Radar builds a concise daily action brief by aggregating available reminders from email, calendar, SMS/iMessage, weather, and task notes, then prioritizing them into Must-do, Should-do, and Nice-to-have items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YIKAILucas](https://clawhub.ai/user/YIKAILucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users use Life Radar to turn connected calendars, messages, email, billing notices, weather, and task notes into a short daily action digest. It is suited for daily planning, inbox triage, proactive reminders, and role-aware prioritization for executives, team leads, and individual contributors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may summarize sensitive personal or business information from connected calendars, messages, email, billing notices, weather, and notes. <br>
Mitigation: Keep tool permissions scoped to sources the user wants summarized, redact secrets and full account numbers, and avoid collecting unavailable or unnecessary sources. <br>
Risk: Payment, security, deadline, and account-risk items could be incomplete or wrong if source data is missing or ambiguous. <br>
Mitigation: Verify payments, security alerts, deadlines, and account-risk items in the original source before acting, and mark missing dates or amounts as unknown. <br>


## Reference(s): <br>
- [Life Radar Modes](artifact/references/modes.md) <br>
- [Life Radar on ClawHub](https://clawhub.ai/YIKAILucas/life-radar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown action brief with prioritized sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes capped Must-do, Should-do, and Nice-to-have sections plus one-line suggested next actions.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
