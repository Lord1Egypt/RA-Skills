## Description:

Personal Health Journal helps agents record daily symptoms and vital signs, generate structured health summaries, analyze recent trends, and surface tiered care reminders without replacing clinical diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangforsix](https://clawhub.ai/user/yangforsix)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to keep a local Markdown health journal, summarize daily symptoms and vital signs, review 7-14 day trends, and identify when home observation, follow-up, or urgent in-person care may be appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Markdown health notes may contain sensitive medical information.

Mitigation: Store records in a private, access-restricted folder and avoid syncing, sharing, or committing the journal files.

Risk: Symptom-based directory names may reveal private health details.

Mitigation: Use neutral directory names or another naming scheme that does not expose symptoms.

Risk: Health summaries and risk tiers could be mistaken for a clinical diagnosis.

Mitigation: Keep outputs framed as health management and risk reminders, and seek timely in-person care for urgent symptoms.

## Reference(s):

- [Symptom Record Template](references/symptom-template.md)
- [Daily Health Summary Template](references/daily-summary-template.md)
- [Risk Classification and Care Guidance](references/risk-flags.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Analysis, Guidance]

**Output Format:** [Markdown health records, daily summaries, trend analysis, and tiered care reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local daily health-journal files and mirrors a concise summary in chat.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
