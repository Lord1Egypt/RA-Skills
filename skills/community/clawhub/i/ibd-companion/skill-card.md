## Description:

Private IBD logging, plans, and evidence-bounded reviews in the local SQLite tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[denniscriss](https://clawhub.ai/user/denniscriss)

### License/Terms of Use:

MIT

## Use Case:

People living with Crohn's disease or ulcerative colitis use this skill to privately record symptoms, tests, and clinician-confirmed plans and prepare descriptive summaries for clinical visits. It does not diagnose or prescribe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health records are stored locally without encryption.

Mitigation: Keep the database and backups private in a dedicated 0700 directory and understand that filesystem permissions do not provide encryption.

Risk: Enabling an external reminder integration may expose reminder metadata to other apps or synced services.

Mitigation: Leave reminders off unless explicitly authorized after reviewing what metadata the integration shares.

Risk: Unverified report extraction or pattern summaries may be mistaken for clinical conclusions.

Mitigation: Confirm source values and plans before recording them, treat trends as exploratory, and seek professional care for medical decisions or urgent symptoms.

## Reference(s):

- [Data entry workflow](references/data-entry.md)
- [IBD Companion schema](references/schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language confirmations and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Confirmed records persist in a private local SQLite database; external reminders are off by default.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
