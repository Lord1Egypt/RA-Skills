## Description:

Models BMD T-score trajectories and 10-year fracture risk in chronic glucocorticoid users with Monte Carlo uncertainty and ACR 2022 osteoporosis treatment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptoreumd](https://clawhub.ai/user/cryptoreumd)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, clinical researchers, and clinical software developers use this skill to model glucocorticoid-induced osteoporosis trajectories, estimate fracture risk, and draft clinician-reviewed treatment guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Osteoporosis risk estimates and treatment recommendations may be mistaken for standalone medical advice.

Mitigation: Have a licensed clinician review the outputs before using them to start, stop, taper, or choose medication.

Risk: Modeled T-score trajectories and fracture probabilities are simplified estimates and may not match an individual patient's validated clinical risk.

Mitigation: Compare outputs with current DXA results, validated risk tools, guideline updates, and patient-specific clinical judgment.

Risk: Patient inputs can include sensitive health information.

Mitigation: Use the script only in an approved environment and avoid entering unnecessary direct identifiers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptoreumd/skills/osteo-gc)
- [Skill documentation](artifact/SKILL.md)
- [OSTEO-GC implementation](artifact/osteo_gc.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Python data structures and human-readable clinical report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces BMD trajectory projections, 10-year fracture probability estimates, risk categories, and treatment guidance for clinician review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
