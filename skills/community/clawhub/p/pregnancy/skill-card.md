## Description:

Track pregnancy routines, symptoms, and clinical signals with flexible logs, weekly summaries, and safety-first triage for medical follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to organize pregnancy tracking, symptom logs, appointment preparation, and clinician-ready weekly summaries while preserving medical decision-making for clinicians and emergency services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pregnancy tracking can create sensitive plaintext health notes under ~/pregnancy/.

Mitigation: Use the skill only on a trusted device or protected storage location and review planned writes before approving them.

Risk: Pregnancy symptoms or warning signs may require urgent medical care.

Mitigation: Rely on clinicians or emergency services for urgent symptoms and medical decisions; use the skill for organization and triage support only.

Risk: Incorrect or ambiguous entries can reduce the usefulness of clinician-facing summaries.

Mitigation: Record timestamps, units, and context, and request clarification before saving incomplete entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/pregnancy)
- [Skill homepage](https://clawic.com/skills/pregnancy)
- [Setup guidance](artifact/setup.md)
- [Memory template](artifact/memory-template.md)
- [Tracking framework](artifact/tracking-framework.md)
- [Metric catalog](artifact/metric-catalog.md)
- [Data quality rules](artifact/data-quality.md)
- [Triage rules](artifact/triage-rules.md)
- [Visit summary template](artifact/visit-summary-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown notes, tracking templates, concise summaries, and triage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local pregnancy notes may be stored under ~/pregnancy/ only after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
