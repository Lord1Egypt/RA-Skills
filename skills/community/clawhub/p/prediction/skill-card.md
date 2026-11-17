## Description:

Forecast uncertain outcomes with base rates, reference classes, calibration loops, and explicit scorekeeping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn uncertain business, product, technical, operational, policy, sports, market, or personal planning questions into auditable forecasts with resolution rules, probabilities, review triggers, and scorekeeping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent forecasting notes under ~/prediction/ may contain sensitive forecasts or planning context if users store more than intended.

Mitigation: Store only durable forecasting defaults, open forecasts, scorecards, reference classes, and assumptions; avoid sensitive personal, medical, legal, credential, financial, or unreleased company details.

Risk: Forecast outputs can be misleading when questions lack a clear deadline, threshold, or resolution source, or when evidence is too thin for a responsible estimate.

Mitigation: Define a resolvable question before assigning odds, use base rates and reference classes, cap confidence when assumptions are weak, and abstain or hold a low-confidence view when critical evidence is missing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/prediction)
- [Skill Homepage](https://clawic.com/skills/prediction)
- [Skill Definition](artifact/SKILL.md)
- [Setup - Prediction](artifact/setup.md)
- [BRACE Forecast Loop](artifact/forecast-loop.md)
- [Forecastable Question Design](artifact/question-design.md)
- [Calibration and Confidence](artifact/calibration.md)
- [Scoring and Review](artifact/scoring-and-review.md)
- [Memory Template - Prediction](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with structured forecast fields and optional bash setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local notes under ~/prediction/ when the user permits persistent forecasting memory.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
