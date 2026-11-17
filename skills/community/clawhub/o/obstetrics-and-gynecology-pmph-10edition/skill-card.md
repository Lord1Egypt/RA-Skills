## Description:

A registry of 187 obstetrics and gynecology clinical skills based on PMPH Obstetrics and Gynecology, 10th edition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xllgreen](https://clawhub.ai/user/xllgreen)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, midwives, reproductive medicine specialists, medical students, and residents use this skill to retrieve structured, textbook-aligned obstetrics and gynecology guidance for education and clinician-supervised professional decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-stakes obstetrics and gynecology guidance may be outdated, incomplete, or inappropriate for a specific patient.

Mitigation: Use only under qualified clinician supervision and verify recommendations against current local guidelines, patient history, contraindications, and available diagnostics before action.

Risk: Dosing, surgery, emergency, and pregnancy-related content can cause harm if used for self-diagnosis, self-medication, emergency self-management, or standalone treatment decisions.

Mitigation: Add global and per-skill guardrails that prohibit standalone clinical decision-making and escalate urgent symptoms or emergencies to immediate in-person medical care.

Risk: Textbook-aligned material may not reflect jurisdiction-specific protocols or recent changes in standards of care.

Mitigation: Require clinician review against local institutional protocols and current specialty guidance before using outputs in care planning or teaching.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xllgreen/skills/obstetrics-and-gynecology-pmph-10edition)
- [Artifact README](README.md)
- [Skill Registry](SKILL.md)
- [Skill Configuration](config/skill-config.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown guidance with structured clinical steps, cautions, reference pointers, and occasional shell command snippets for registry search/report scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for clinician-supervised education or professional decision support and require review against current local clinical guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
