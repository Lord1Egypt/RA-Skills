## Description:

Provides bilingual clinical nephrology support for kidney disease questions, including structured reasoning, education, literature-search planning, and guideline-oriented consult-style answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanbastias](https://clawhub.ai/user/juanbastias)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, trainees, and healthcare educators use this skill to structure nephrology differentials, identify red flags, plan literature searches, and draft consult-style educational answers in Spanish or English. It is not a substitute for patient-specific clinical judgment, local protocols, or the treating care team.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical nephrology guidance could be mistaken for patient-specific medical direction.

Mitigation: Use outputs for education and structured reasoning only, and confirm personalized or urgent decisions with the treating team, local protocols, and current guidelines.

Risk: ICU, pregnancy, transplant, oncology, dialysis, procedure, and medication-dosing topics carry elevated patient-safety risk.

Mitigation: Escalate these cases to appropriate clinicians and verify recommendations against specialty guidance, institutional protocols, and pharmacy or multidisciplinary review where relevant.

Risk: Outdated or unsupported thresholds, doses, guideline claims, or citations could lead to unsafe conclusions.

Mitigation: Do not invent clinical values or sources; state uncertainty and use current literature, guidelines, or authoritative references when precision is required.

## Reference(s):

- [Acid-base and electrolytes](references/acid-base.md)
- [Chronic kidney disease](references/ckd.md)
- [CRRT and ICU renal replacement therapy](references/crrt.md)
- [Onconephrology](references/onconephrology.md)
- [Pregnancy and kidney disease](references/pregnancy.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown text with bullets or tables when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Spanish or English clinical reasoning support with explicit safety boundaries.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
