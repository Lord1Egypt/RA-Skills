## Description:

Generate or edit images using Google Gemini API through the nanobanana tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiskyer](https://clawhub.ai/user/feiskyer)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to have an agent generate new images or edit provided images with Google Gemini, selecting prompts, output paths, aspect ratios, resolution, and model choice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images are sent to Google Gemini.

Mitigation: Avoid submitting secrets, private documents, sensitive personal images, or data that is not approved for third-party processing.

Risk: Dependencies are listed without pinned versions.

Mitigation: Install in a virtual environment and pin or review dependency versions before operational use.

Risk: The script enables Google Search during Gemini calls.

Mitigation: Review whether Google Search is acceptable for the intended workflow before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feiskyer/skills/nanobanana-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY and may produce PNG image files from Gemini responses.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
