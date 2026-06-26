## Description: <br>
Drives the local nano-img Gemini image CLI for image generation, model selection, saved defaults, reference-image workflows, and output sizing or format conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dishant0406](https://clawhub.ai/user/dishant0406) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate images with the local nano-img or nano-image CLI, inspect and configure saved defaults, manage reference images, and troubleshoot CLI behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide local command execution for the nano-img CLI, which may create files or change saved defaults. <br>
Mitigation: Review proposed commands before running them and prefer the CLI's inspection commands, such as nano-img config --json and nano-img refs --json, to confirm state changes. <br>
Risk: Using the CLI may consume Gemini API quota or billing through NANO_IMAGE_API_KEY. <br>
Mitigation: Verify the API key, quota, and billing expectations before image generation. <br>
Risk: Saved defaults and reference images under ~/.nano-img can affect later generations and may include sensitive content. <br>
Mitigation: Review ~/.nano-img/config.json, ~/.nano-img/INSTRUCTION.md, ~/.nano-img/STYLE.md, and ~/.nano-img/assets before sensitive generations or persistent configuration changes. <br>
Risk: The skill depends on the local nanobana/nano-img binary being trustworthy. <br>
Mitigation: Install or run the binary only from a trusted source and validate the command surface with nano-img help before relying on flags. <br>


## Reference(s): <br>
- [Nano Img CLI Skill](SKILL.md) <br>
- [Command Reference](references/command-reference.md) <br>
- [Defaults And Files](references/defaults-and-files.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dishant0406/nano-img-cli) <br>
- [Publisher Profile](https://clawhub.ai/user/dishant0406) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated file paths, saved model names, output directory settings, or JSON inspection results when relevant.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
