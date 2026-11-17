## Description:

PREGNA-RISK calculates a weighted composite risk score for adverse pregnancy outcomes in patients with SLE and/or APS and returns risk categories, uncertainty estimates, and monitoring recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptoreumd](https://clawhub.ai/user/cryptoreumd)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, medical developers, and reviewers can use this skill to inspect or run a pregnancy-risk stratification calculator for SLE/APS scenarios and produce risk scores, categories, uncertainty intervals, and monitoring-oriented guidance. Its outputs require qualified obstetric, maternal-fetal medicine, and rheumatology review before any clinical use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for validated medical decision support for pregnancy, medication, monitoring, hospitalization, or delivery decisions.

Mitigation: Use outputs only as informational risk-calculator results that require qualified obstetric, maternal-fetal medicine, and rheumatology review before any clinical decision.

Risk: The JSON mode may process patient identifiers or protected health information without explicit privacy safeguards.

Mitigation: Use de-identified inputs by default, and process real patient data only in environments with approved privacy controls and logging safeguards.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptoreumd/skills/pregna-risk)
- [Artifact skill documentation](artifact/SKILL.md)
- [PREGNA-RISK Python implementation](artifact/pregna_risk.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, plus plain-text or JSON calculator output when the script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The calculator accepts boolean clinical risk factors and an optional patient identifier in JSON mode, then emits a composite score, risk category, recommendation, and Monte Carlo uncertainty estimates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
