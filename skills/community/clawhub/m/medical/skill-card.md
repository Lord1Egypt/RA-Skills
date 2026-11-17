## Description:

Local-first health record management with strict privacy boundaries for organizing medications, symptoms, vital signs, medical history, emergency summaries, and doctor-visit notes without diagnosis or treatment advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to keep local personal health records, including medications, symptoms, vital signs, medical history, emergency summaries, and doctor-visit preparation. It is for organization and clinician-facing summaries, not diagnosis, treatment advice, medication changes, or emergency-care replacement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores highly sensitive medical information locally in plaintext.

Mitigation: Review before installing with real health data, restrict filesystem access, and avoid storing details that are not needed for the intended personal record workflow.

Risk: Emergency summaries may print or export protected health information into less-protected places.

Mitigation: Review generated cards before sharing or saving, exclude unnecessary identifiers, and regenerate cards when medications, allergies, contacts, or conditions change.

Risk: Medication interaction checks are limited and must not be treated as comprehensive medical advice.

Mitigation: Verify medication questions with a doctor or pharmacist before starting, stopping, or changing any medication.

## Reference(s):

- [Emergency Health Summary](references/emergency-card.md)
- [Personal Medical History](references/medical-history.md)
- [Medication Manager](references/medication-manager.md)
- [Symptom Tracker & Appointment Preparation](references/symptom-tracker.md)
- [Vital Signs & Chronic Condition Monitoring](references/vital-signs.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown or plain text summaries, local JSON record files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores health records locally under ~/.openclaw/workspace/memory/health and can export emergency summaries for phone, wallet, or JSON formats.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
