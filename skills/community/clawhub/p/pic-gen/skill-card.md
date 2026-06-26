## Description: <br>
pic-gen helps users turn plain-language image ideas into optimized prompts, choose among Qwen Wanxiang, Banana/Flux, and DALL-E 3, and optionally call configured image-generation APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aoturlab](https://clawhub.ai/user/aoturlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to optimize image prompts, manage model configuration, and generate images through configured Qwen Wanxiang, Banana/Flux, or DALL-E 3 providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys can be exposed if real credentials are saved in config/models.yaml or shared with the skill artifact. <br>
Mitigation: Prefer DASHSCOPE_API_KEY, BANANA_API_KEY, OPENAI_API_KEY, and BANANA_MODEL_KEY environment variables; avoid sharing config/models.yaml after adding real keys. <br>
Risk: Unpinned Python dependencies can change behavior between installations. <br>
Mitigation: Install the skill in an isolated environment and pin reviewed dependency versions before regular use. <br>
Risk: Image generation sends prompts and credentials to configured external providers. <br>
Mitigation: Use only approved provider accounts and review prompt content before sending requests to Qwen Wanxiang, Banana/Flux, or DALL-E 3 APIs. <br>


## Reference(s): <br>
- [DALL-E 3 prompt format reference](artifact/references/dalle.md) <br>
- [Flux prompt format reference](artifact/references/flux.md) <br>
- [Midjourney prompt format reference](artifact/references/midjourney.md) <br>
- [Stable Diffusion / ComfyUI prompt format reference](artifact/references/stable-diffusion.md) <br>
- [OpenAI Images guide](https://platform.openai.com/docs/guides/images) <br>
- [OpenAI Images API reference](https://platform.openai.com/docs/api-reference/images-create) <br>
- [Black Forest Labs Flux](https://blackforestlabs.ai/flux/) <br>
- [Banana documentation](https://docs.banana.dev/banana-docs) <br>
- [Midjourney parameter documentation](https://docs.midjourney.com/docs/parameter-simplified) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown and command-line output containing optimized prompts, configuration guidance, API result JSON, image URLs, and optional downloaded image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied provider credentials for image API calls; prompt optimization can run without generating images.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
