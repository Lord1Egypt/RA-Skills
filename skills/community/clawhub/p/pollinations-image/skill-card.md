## Description: <br>
Generate detailed images from text prompts using Pollinations.ai models with optional configuration, model selection, and advanced settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aprilox](https://clawhub.ai/user/Aprilox) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to generate image files from text prompts through Pollinations.ai, choose free or paid models, set persistent defaults, and inspect model options from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shell script can run unintended local commands through unsafe evaluation and config loading. <br>
Mitigation: Remove eval, call curl with quoted arguments, load only intended skill-local environment files, and parse user configuration as data instead of sourcing it as shell code. <br>
Risk: The API key can be exposed in configuration output or local files. <br>
Mitigation: Mask API keys in displayed configuration, keep .env files out of shared artifacts, and avoid logging secrets. <br>
Risk: Prompts and generated-image requests are sent to Pollinations.ai. <br>
Mitigation: Do not include secrets, personal data, or confidential prompts in image-generation requests. <br>


## Reference(s): <br>
- [Pollinations.ai](https://pollinations.ai) <br>
- [Pollinations API key portal](https://enter.pollinations.ai) <br>
- [ClawHub skill page](https://clawhub.ai/Aprilox/pollinations-image) <br>


## Skill Output: <br>
**Output Type(s):** [Image files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [PNG or JPEG image files with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports prompt, model, dimensions, seed, filename, watermark, and prompt-enhancement options; may use a Pollinations API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
