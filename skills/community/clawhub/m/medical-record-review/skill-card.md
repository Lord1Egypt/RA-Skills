## Description:

Reviews personal or family health records across their history, tracks trends and conflicts, grades evidence, and highlights issues for clinician review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals or caregivers use the skill to review one person's health records over time, surface data conflicts, and prepare a sourced draft for clinician review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms and health-record tasks can expose private medical history to the model or a hosted provider.

Mitigation: Invoke the skill explicitly for a medical task and use a dedicated record folder. Choose a local model when records must stay on the machine; a hosted model receives records it reads.

Risk: Conflicting merge and rename rules could lead to unsafe record maintenance.

Mitigation: Resolve the conflicting rules before allowing maintenance, and keep backups of records and source references.

Risk: Generated medical analysis may be wrong or mistaken for medical advice.

Mitigation: Treat the output as a draft for a clinician and do not use it alone to make diagnosis, medication, or treatment decisions.

## Reference(s):

- [Health Records an Agent Can Audit (companion article)](https://github.com/j3ffyang/ai-thoughts/blob/main/docs/261021-medical-record-review.md)
- [Project authority starter](references/AGENTS.example.md)
- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/medical-record-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with tables and sourced review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis is a draft for clinician review; the skill does not diagnose, prescribe, or edit source data.]

## Skill Version(s):

1.5.3 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
