## Description: <br>
Nanobanana Image helps agents generate and edit images with Google Gemini native image generation, including text-to-image, reference-based edits, multi-image composition, search-grounded generation, YouTube video inputs, and up to 4K output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fackee](https://clawhub.ai/user/fackee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate new images, edit supplied images, compose multiple references, and create search- or video-informed visuals through a Gemini-backed CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, selected reference images, and video or search requests to Google services. <br>
Mitigation: Use it only for inputs appropriate for Google-hosted processing, and avoid sensitive personal or confidential images unless that matches the intended use. <br>
Risk: A Gemini API key is required and may be loaded from the environment or a .env file. <br>
Mitigation: Keep the API key private and scoped, and review any .env file before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fackee/skills/nanobanana-image) <br>
- [Nano Banana Models and Parameters Quick Reference](references/models-and-params.md) <br>
- [Google AI Studio API key setup](https://aistudio.google.com/apikey) <br>
- [Google Generative AI Use Policy](https://policies.google.com/terms/generative-ai/use-policy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline bash code blocks and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY; the CLI may save multiple generated images, optional thought images, model text, and search source output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
