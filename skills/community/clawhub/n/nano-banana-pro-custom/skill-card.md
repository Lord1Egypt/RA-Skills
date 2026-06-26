## Description: <br>
Generate or edit images using OpenAI-compatible API. Supports multi-image input, fine-tuned models, and multiple configuration sources (env vars, openclaw.json, config.json). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CHENXCHEN](https://clawhub.ai/user/CHENXCHEN) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate new images, edit images, or compose multiple input images through a configured OpenAI-compatible image API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to the configured OpenAI-compatible API provider. <br>
Mitigation: Use a trusted provider and avoid sending sensitive personal or proprietary images unless that provider's data practices are acceptable. <br>
Risk: API keys may be exposed if configuration files or environment values are committed or shared. <br>
Mitigation: Use a dedicated or limited API key and keep config files containing secrets out of version control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CHENXCHEN/nano-banana-pro-custom) <br>
- [Publisher profile](https://clawhub.ai/user/CHENXCHEN) <br>
- [OpenAI-compatible API base URL example](https://api.openai.com/v1) <br>
- [OpenRouter API base URL example](https://openrouter.ai/api/v1) <br>
- [Azure OpenAI deployment URL example](https://your-resource.openai.azure.com/openai/deployments/your-deployment) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the script saves PNG image files and prints MEDIA paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, Python >=3.10, NANO_API_KEY, a configured OpenAI-compatible base URL, and a compatible image model.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
