## Description: <br>
Calls a configured OpenAI-compatible image generation API to generate images and save the returned PNG files locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoanCo](https://clawhub.ai/user/zuoanCo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate images through a chosen third-party provider after configuring the image API URL, API key, and optional model ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts to a user-configured third-party image API, so prompt content and API keys depend on the configured provider. <br>
Mitigation: Use only approved providers, verify IMAGE_API_URL before running, use a scoped API key, and avoid confidential or regulated prompt content unless the provider is approved. <br>
Risk: Generated or downloaded PNG files are written to the current working directory. <br>
Mitigation: Run the skill from a directory where generated files are expected and review outputs before using or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zuoanCo/image-generator-custom) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration guidance] <br>
**Output Format:** [PNG image files with terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMAGE_API_URL and IMAGE_API_KEY; IMAGE_MODEL_ID can be supplied by environment variable or command-line argument.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
