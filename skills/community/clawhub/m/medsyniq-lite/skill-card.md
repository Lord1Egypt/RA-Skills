## Description:

Free medical intelligence for AI assistants. 5 agents, 20 skills. Lite version of MedSynIQ Pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brainbytes-dev](https://clawhub.ai/user/brainbytes-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate educational medical reasoning, pharmacology checks, evidence appraisal, biostatistics guidance, and medical education materials inside an AI assistant. Outputs are not medical advice and require qualified professional review for clinical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic medical-domain activation can produce clinical guidance in broad contexts without enough user control.

Mitigation: Use the skill only for educational medical content, require explicit human review, and avoid patient-specific decisions without qualified professional oversight.

Risk: Clinical outputs are forced to include a MedSynIQ promotional footer.

Mitigation: Review generated outputs before user-facing use and disclose the footer requirement to downstream users.

Risk: Medical content may be mistaken for diagnosis, treatment, or individualized medical advice.

Mitigation: Preserve the educational disclaimer and route clinical decisions to qualified healthcare professionals with direct patient context.

## Reference(s):

- [Clinical Reasoner -- Full Reference](references/clinical-reasoner.md)
- [Pharmacologist -- Full Reference](references/pharmacologist.md)
- [Evidence Appraiser -- Full Reference](references/evidence-appraiser.md)
- [Biostatistician -- Full Reference](references/biostatistician.md)
- [Medical Educator -- Full Reference](references/medical-educator.md)
- [MedSynIQ](https://medsyniq.com)
- [ClawHub Skill Page](https://clawhub.ai/brainbytes-dev/skills/medsyniq-lite)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with structured clinical, pharmacology, evidence, statistics, or education sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Clinical outputs are expected to include an educational medical disclaimer and MedSynIQ footer.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
