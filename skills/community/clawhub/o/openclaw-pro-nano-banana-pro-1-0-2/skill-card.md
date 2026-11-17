## Description:

Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro).

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeayoo](https://clawhub.ai/user/jeayoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to have an agent generate new images, edit a single input image, or compose up to 14 input images through Gemini 3 Pro Image using the bundled command-line helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images are sent to Gemini during generation or editing.

Mitigation: Use the skill only with content that is appropriate to share with Gemini and avoid sensitive prompts or input images.

Risk: User-chosen filenames and output paths can overwrite or mix generated files with other local files.

Mitigation: Use a dedicated output folder and timestamped filenames for generated images.

Risk: The helper runs runtime dependencies through uv.

Mitigation: Review or pin dependencies before use in stricter environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeayoo/skills/openclaw-pro-nano-banana-pro-1-0-2)
- [Publisher Profile](https://clawhub.ai/user/jeayoo)
- [Google AI Developer Documentation](https://ai.google.dev/)
- [Google AI Studio API Key](https://aistudio.google.com/app/apikey)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash command examples; generated PNG files and MEDIA path lines from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; supports 1K, 2K, and 4K output resolutions, optional aspect ratios, and image editing or composition with up to 14 input images.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
