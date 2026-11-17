## Description:

Guides agents in advising photographers on light meter compensation for gray snow, backlit portraits, 18% gray card use, and high-contrast exposure decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchunhui](https://clawhub.ai/user/bianchunhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and photography-focused agents use this skill to answer exposure-compensation questions, including snow or sand rendering gray, backlit faces becoming too dark, 18% gray card use, and high-contrast metering choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect fully bilingual behavior although the artifact is mostly Chinese with English trigger support.

Mitigation: State the language posture clearly and translate or summarize guidance when responding in English.

Risk: Exposure advice may be applied outside the skill boundary, such as creative aperture and shutter choices or digital post-processing.

Mitigation: Route creative exposure-control, ISO, and post-processing questions to the appropriate adjacent guidance instead of using this skill alone.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/bianchunhui/nyip-photography-skills/tree/main/light-meter-compensation)
- [ClawHub skill page](https://clawhub.ai/bianchunhui/skills/light-meter-compensation)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown or plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English trigger support; no executable output.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
