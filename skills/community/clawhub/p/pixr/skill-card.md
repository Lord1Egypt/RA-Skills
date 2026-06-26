## Description: <br>
Drives the local pixr Gemini image CLI for generation, editing, variations, model selection, saved defaults, profile-based defaults, reference-image workflows, and output sizing or format conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dishant0406](https://clawhub.ai/user/dishant0406) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate the local pixr CLI for image generation, editing, variation workflows, model selection, saved defaults, profiles, reference images, and output sizing or format conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide local pixr configuration changes, including model, profile, and save-directory updates. <br>
Mitigation: Review state-changing requests before running commands and confirm the resulting configuration with pixr JSON inspection commands. <br>
Risk: Prompts, shared configuration files, and image references may contain API keys or sensitive images. <br>
Mitigation: Avoid placing API keys or sensitive image content in prompts or shared files, and install the skill only when the local pixr CLI is intended and trusted. <br>


## Reference(s): <br>
- [ClawHub Pixr Skill Page](https://clawhub.ai/dishant0406/pixr) <br>
- [Command Reference](artifact/references/command-reference.md) <br>
- [Defaults And Files](artifact/references/defaults-and-files.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report resolved pixr configuration, reference-image state, or generated output paths when relevant.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
