## Description: <br>
Transform natural language image requests into optimized structured prompts for Gemini image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minilozio](https://clawhub.ai/user/minilozio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to turn natural language image requests into structured Gemini image prompts with style, composition, camera, rendering, and negative-prompt details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a Gemini API key and a helper workflow that may expose credentials if handled carelessly. <br>
Mitigation: Keep GEMINI_API_KEY in the environment, avoid logging or committing it, and use a trusted Gemini generator helper. <br>
Risk: Generated image filenames, output paths, or reference images may expose sensitive data or affect unintended files. <br>
Mitigation: Use simple agent-constructed filenames, avoid unsanitized user input in paths, and be deliberate when using sensitive reference images. <br>


## Reference(s): <br>
- [Structured Prompt Guide for Gemini Image Generation](references/prompt-guide.md) <br>
- [Nano Banana Prompting Skill on ClawHub](https://clawhub.ai/minilozio/nano-banana-prompting) <br>
- [Gemini API Key Setup](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured JSON prompt examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to produce image files through a trusted Gemini image generation helper.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
