## Description:

Convert a scientific paper into a presentation deck (PPTX). Generates structured Chinese or bilingual slides for journal clubs, group meetings, or conference talks. Trigger when user wants to make slides from a paper or present research findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1bai](https://clawhub.ai/user/yang1bai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, presenters, and students use this skill to turn scientific papers into structured slide outlines, optional PPTX decks, presenter notes, and discussion questions for journal clubs, group meetings, or conference talks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic presentation requests may invoke this skill when the user does not intend paper-to-slide conversion.

Mitigation: Confirm the user is working from a scientific paper or research findings before applying the skill.

Risk: Optional PPTX export relies on a local script path referenced by the artifact.

Mitigation: Use the default Markdown outline unless the local export script is present, reviewed, and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1bai/skills/nature-paper2ppt)
- [Publisher profile](https://clawhub.ai/user/yang1bai)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown slide outline with presenter notes; optional PPTX file when requested and dependencies are available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is a slide-by-slide outline; optional PPTX export depends on python-pptx and a trusted local export script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
