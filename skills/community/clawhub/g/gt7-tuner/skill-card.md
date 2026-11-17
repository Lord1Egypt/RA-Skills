## Description:

This skill helps Gran Turismo 7 players turn a settings screenshot into a complete optimized tune using the GT Pro Tune calculator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamstevebot](https://clawhub.ai/user/iamstevebot)

### License/Terms of Use:

MIT-0

## Use Case:

External Gran Turismo 7 players use this skill to extract tuning values from screenshots, automate GT Pro Tune form entry, and receive suspension, transmission, and differential settings to test in game.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may require a GT Pro Tune account and may upload GT7 screenshots to that third-party service.

Mitigation: Confirm with the user before login or upload, and keep credentials secure without logging, echoing, or displaying them.

Risk: OCR or image analysis can misread GT7 settings and produce an unsuitable tune.

Mitigation: Confirm extracted values with the user before form entry, ask for a clearer image when confidence is low, and recommend testing calculated tunes in game.

## Reference(s):

- [GT7 Tuning Knowledge Base](artifact/references/gt7-tuning-knowledge.md)
- [GT Pro Tune](https://app.gtprotune.com/)
- [GT Pro Tune Registration](https://app.gtprotune.com/register)
- [ClawHub Skill Page](https://clawhub.ai/iamstevebot/skills/gt7-tuner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tuning settings, confirmation prompts, and inline browser automation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OCR-derived values, GT Pro Tune form-entry steps, and tune tables for suspension, transmission, and differential settings.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
