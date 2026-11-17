## Description:

Handwriting Analysis is a Chinese-language graphology skill that guides an agent to review handwriting features and produce personality, mental-state, behavioral, signature, comparison, and forensic-style observations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhanchao883](https://clawhub.ai/user/wangzhanchao883)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to review handwriting images, identify visible handwriting features, and draft a structured analysis report. The skill should be limited to non-consequential educational exploration and should not be used to judge honesty, mental health, criminal propensity, hiring suitability, or legal responsibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to make unsupported personality, mental-state, and criminal-risk judgments from handwriting.

Mitigation: Use only for non-consequential educational exploration; do not use outputs for hiring, legal responsibility, mental-health assessment, honesty judgments, or criminal-propensity decisions.

Risk: Forensic handwriting questions may be mistaken for qualified document examination.

Mitigation: Treat outputs as informal observations only and refer forensic or legal matters to qualified document examiners supported by independent evidence.

## Reference(s):

- [Personality traits reference table](references/personality-traits.md)
- [Forensic handwriting guide](references/forensic-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured report with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include handwriting feature descriptions, confidence ratings, limitations, and cautions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
