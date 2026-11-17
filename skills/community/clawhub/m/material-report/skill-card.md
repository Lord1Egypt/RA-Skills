## Description:

Analyze ad material videos and produce a markdown report with framework, material traits, and acquisition keywords, then propose new material production frameworks and detailed storyboard tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fevolq](https://clawhub.ai/user/fevolq)

### License/Terms of Use:


## Use Case:

Marketing creatives, growth teams, and agents use this skill to analyze performance-ad videos, identify their creative structure and material traits, and draft new storyboard-ready ad concepts for the same category and target platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read a user-provided video and create extracted frame images in the current working directory using ffmpeg.

Mitigation: Use the skill only on video assets appropriate for local analysis and confirm file-system permissions before frame extraction.

Risk: The bundled report template is Chinese by default.

Mitigation: Adapt the final report language to the user's requested language or clearly confirm the preferred language before delivery.

## Reference(s):

- [Report Template](references/report_template.md)
- [ClawHub Skill Page](https://clawhub.ai/fevolq/skills/material-report)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with structured analysis, keyword lists, creative frameworks, and storyboard tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create extracted frame images in a folder named after the source video when frame extraction is needed.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
