## Description: <br>
Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wingchiu](https://clawhub.ai/user/wingchiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate new images, edit a single image, or compose up to 14 images through Google's Gemini image API from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and uploaded or reference images are sent to Google Gemini for generation or editing. <br>
Mitigation: Avoid private documents, faces, credentials, sensitive photos, or other confidential inputs unless the user trusts the provider's data handling. <br>
Risk: The skill requires a Gemini API key and can also accept an API key through a command-line argument. <br>
Mitigation: Prefer environment or agent configuration for GEMINI_API_KEY and avoid exposing keys in shell history, logs, or shared transcripts. <br>


## Reference(s): <br>
- [Google AI for Developers](https://ai.google.dev/) <br>
- [ClawHub Skill Page](https://clawhub.ai/wingchiu/nano-banana-2-fal) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and saved image path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script saves PNG image files and emits a MEDIA line for supported chat providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
