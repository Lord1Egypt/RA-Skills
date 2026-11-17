## Description:

Extracts structured Apple Watch pool-swim workout data from screenshots, saves local training records, and generates trend analysis and personalized swim-training guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zygzzp](https://clawhub.ai/user/zygzzp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Apple Watch pool-swim screenshots into structured workout history, recent trend comparisons, and concise training recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal swim workout and heart-rate history locally.

Mitigation: Use it only in a workspace where local fitness data storage is acceptable, and avoid sharing generated history files unless intended.

Risk: Weak date and path validation can allow JSON files to be read or written outside the intended swim_data folder.

Mitigation: Review or strengthen date validation before using the skill with untrusted screenshots or direct JSON input.

Risk: Same-day records are overwritten rather than versioned.

Mitigation: Back up existing records or add versioning if preserving multiple same-day entries matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zygzzp/skills/iwatch-swim-tracker)
- [Swimming Workout Data Schema](artifact/references/data_schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown summary with structured JSON records, shell commands, and locally stored JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include personal workout metrics such as swim distance, pace, stroke distribution, calories, and heart-rate data.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
