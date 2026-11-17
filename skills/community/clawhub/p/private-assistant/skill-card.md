## Description:

Personal bookkeeping, memo/journal, reminder, and spending-insight assistant for Hermes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[askdjoashdasd](https://clawhub.ai/user/askdjoashdasd)

### License/Terms of Use:

MIT-0

## Use Case:

Hermes users use this skill to record income, expenses, notes, reflections, and reminders, then query summaries or receive low-distraction spending insights based on local JSONL records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled reminders can later run agent prompts containing raw memo text.

Mitigation: Review before installing, keep use to a private trusted Hermes profile, and avoid setting reminders from copied or untrusted text until reminder prompt isolation is hardened.

Risk: Finance and journal entries are stored locally.

Mitigation: Use only where local storage is acceptable and protect the Hermes profile data directory according to the user's privacy requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/askdjoashdasd/skills/private-assistant)
- [Data Model](references/data-model.md)
- [Interaction Rules](references/interaction-rules.md)
- [Insight Rules](references/insight-rules.md)
- [Insight Templates](references/insight-templates.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Concise user-facing text with inline shell command guidance and JSON-backed local record operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended as single-message Hermes replies; scheduled insight tasks may intentionally return [SILENT] for low-signal periods.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
