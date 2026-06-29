## Description: <br>
Potaco helps agents generate images from text prompts, edit existing images, perform inpainting or outpainting, configure supported image providers, discover models, and troubleshoot Potaco CLI failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncxton](https://clawhub.ai/user/ncxton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate the Potaco CLI for image generation, image editing, provider setup, model discovery, configuration, and troubleshooting. It is intended for workflows using OpenAI, fal, Vercel AI Gateway, or trusted custom OpenAI-compatible image providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, input images, masks, model names, and generated content may be sent to external or custom providers. <br>
Mitigation: Use only trusted providers and avoid sensitive personal, biometric, proprietary, or otherwise confidential images unless the selected provider's privacy and retention terms are acceptable. <br>
Risk: API keys supplied through command flags or environment variables can leak through shell history, process listings, or logs. <br>
Mitigation: Prefer interactive credential setup and encrypted stored credentials; use non-interactive credential setup only when explicitly approved. <br>
Risk: Installation uses a GitHub release installer when the CLI is missing. <br>
Mitigation: Install only after approval and only if the user trusts the Potaco release installer; build from source when maximum installation scrutiny is required. <br>


## Reference(s): <br>
- [ClawHub Potaco Listing](https://clawhub.ai/ncxton/skills/potaco) <br>
- [Commands](references/commands.md) <br>
- [Configuration](references/configuration.md) <br>
- [Image Editing Modes](references/editing.md) <br>
- [Providers](references/providers.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON command-output options, and generated or edited image files from the Potaco CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce image files, raw image bytes through stdout, or JSON metadata when Potaco commands are run with the corresponding flags.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
