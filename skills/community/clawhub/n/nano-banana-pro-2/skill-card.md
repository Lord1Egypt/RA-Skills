## Description:

Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dycathecorde](https://clawhub.ai/user/dycathecorde)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate new images, edit a source image, or compose multiple images through Gemini 3 Pro Image from a prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images are sent to Google's Gemini API.

Mitigation: Use the skill only with prompts and images that are appropriate to send to Google Gemini.

Risk: A Gemini API key can be exposed if passed directly on the command line.

Mitigation: Prefer GEMINI_API_KEY or another protected secret mechanism, and keep the key restricted and revocable.

Risk: The script writes the requested PNG to the configured output path.

Mitigation: Choose a non-sensitive output path and review generated files before sharing them.

## Reference(s):

- [Google AI Developer Documentation](https://ai.google.dev/)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG image file plus terminal text reporting the saved path and MEDIA line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; supports 1K, 2K, and 4K output resolutions and up to 14 input images.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
