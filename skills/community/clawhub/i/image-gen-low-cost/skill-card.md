## Description: <br>
Low-cost AI image generation CLI for text-to-image generation and image editing with OpenAI-compatible API endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enihsago](https://clawhub.ai/user/enihsago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a command-line image generation workflow for text-to-image generation, image editing, model selection, token configuration, and saving or printing generated image outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and credentials may be sent to the configured API provider, and the security evidence notes that a third-party default endpoint can receive an existing OpenAI API key. <br>
Mitigation: Set IMGEN_TOKEN explicitly, verify IMGEN_API_URL before use, and avoid running the skill where OPENAI_API_KEY is set unless that key is intended for this tool. <br>
Risk: Generated image URLs may be temporary or externally hosted. <br>
Mitigation: Save required image outputs promptly and review generated files before reuse or distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/enihsago/image-gen-low-cost) <br>
- [Laozhang API registration](https://api.laozhang.ai/register/?aff_code=lfa0) <br>
- [Default OpenAI-compatible API endpoint](https://api.laozhang.ai/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown or CLI text with image file paths, image URLs, data URLs, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved to the configured output path or generated-images directory unless URL-only output is requested.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
