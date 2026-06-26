## Description: <br>
Use when tasks need the NanoGPT API for text, image, or video generation through the local `nano-gpt` CLI and bundled wrapper scripts for OpenClaw or ClawHub workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icework](https://clawhub.ai/user/icework) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call NanoGPT from a local terminal for text prompts, interactive chat, model discovery, image generation, and video generation. It is intended for workflows where the user has a NanoGPT API token and wants wrapper scripts or the `nano-gpt` CLI to manage the API interaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens may be stored in local user configuration when `nano-gpt config set api-key` is used. <br>
Mitigation: Prefer setting `NANO_GPT_API_KEY` in the environment and keep secrets out of prompts and logs. <br>
Risk: Prompts and explicitly provided image or video files are sent to the configured NanoGPT endpoint. <br>
Mitigation: Only pass local media paths when the user intends those files to be uploaded, and avoid sensitive files unless upload is explicitly requested. <br>


## Reference(s): <br>
- [NanoGPT Documentation](https://docs.nano-gpt.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/icework/nano-gpt-cli) <br>
- [NanoGPT CLI Reference](references/cli.md) <br>
- [NanoGPT Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [CLI text or JSON output, with optional generated image or video files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the selected NanoGPT model and may include locally written media files when --output is used.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
