## Description: <br>
Generates images from text prompts with the WellAPI gpt-image-2 endpoint and saves decoded image files locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laolujava](https://clawhub.ai/user/laolujava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn natural-language image requests into generated image files through WellAPI. It is intended for text-to-image generation workflows where the agent can collect or load a WellAPI API key, call the endpoint, and report saved output paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and API usage to WellAPI using a user-provided API key. <br>
Mitigation: Install only if you trust WellAPI for the prompts you submit, avoid confidential prompts, and use a dedicated revocable API key. <br>
Risk: The WellAPI key may be saved in the user's local configuration file. <br>
Mitigation: Rely on the skill's 0600 file permissions where supported and delete or rotate the saved key when it is no longer needed. <br>
Risk: Generated image files are written to local disk. <br>
Mitigation: Review saved files and output paths before sharing, committing, or reusing the generated images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laolujava/gpt-image-2-generation) <br>
- [WellAPI](https://wellapi.ai) <br>
- [WellAPI image generation endpoint](https://wellapi.ai/v1/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Image files saved locally with text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a WellAPI API key and supports prompt, size, quality, format, count, output path, and timeout options.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
