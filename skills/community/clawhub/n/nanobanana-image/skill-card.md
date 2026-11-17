## Description:

Generates and edits images with Google Gemini native image generation, including text-to-image, reference-image editing, multi-image composition, search-grounded generation, YouTube video-to-image workflows, and up to 4K output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fackee](https://clawhub.ai/user/fackee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to invoke a Gemini-backed command-line workflow for generating new images, editing or composing reference images, and producing visual assets from prompts, search grounding, or supported video inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, input images, video URLs, and .env-provided credentials are used with Google services.

Mitigation: Do not submit confidential prompts, images, URLs, or .env content unless sharing that content with Google services is acceptable.

Risk: The skill installs and runs third-party Python dependencies.

Mitigation: Install in a dedicated virtual environment and pin or review dependency versions before operational use.

Risk: Search-grounded and video-based generation can rely on live external content.

Mitigation: Review prompts, generated outputs, and any printed search sources before using results in production materials.

## Reference(s):

- [Nano Banana Models and Parameters Quick Reference](references/models-and-params.md)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Generative AI Use Policy](https://policies.google.com/terms/generative-ai/use-policy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; the bundled Python script saves PNG image files and may print model descriptions or search source metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9+, google-genai, Pillow, and GEMINI_API_KEY; generated image paths depend on the --output argument.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
