## Description: <br>
Personal bookkeeping, memo/journal, reminder, and spending-insight assistant for Hermes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askdjoashdasd](https://clawhub.ai/user/askdjoashdasd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this Hermes skill to record income, expenses, notes, reflections, and reminders, then query summaries and spending insights from local records. It is suited for personal productivity workflows that need concise bookkeeping and reminder management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal finance records, notes, and reminder metadata locally in the Hermes data directory. <br>
Mitigation: Install only when local storage of this information is acceptable, and avoid saving secrets or other highly sensitive content. <br>
Risk: Vague update or delete requests such as 'last' can affect the wrong local record. <br>
Mitigation: Review the target record before confirming ambiguous update or delete actions. <br>
Risk: Cron reminders and digest subscriptions can continue running after they are no longer useful. <br>
Mitigation: Periodically review scheduled reminders and digest subscriptions, and disable entries that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/askdjoashdasd/private-assistant) <br>
- [Publisher Profile](https://clawhub.ai/user/askdjoashdasd) <br>
- [Data Model](references/data-model.md) <br>
- [Interaction Rules](references/interaction-rules.md) <br>
- [Insight Rules](references/insight-rules.md) <br>
- [Insight Templates](references/insight-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise text or Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-message responses; helper scripts create or update local JSON and JSONL records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
