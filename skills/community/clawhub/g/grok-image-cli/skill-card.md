## Description: <br>
Generate and edit images via Grok API from the command line with secure xAI API key storage, batch generation, aspect ratios, and style transfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberash-dev](https://clawhub.ai/user/cyberash-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and creative automation users use this skill to configure and run a command-line workflow for generating and editing images through xAI's Grok image API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI handles an xAI API key and can fall back to the XAI_API_KEY environment variable. <br>
Mitigation: Use a scoped key where possible, store it with the documented credential workflow, avoid committing environment files, and rotate the key when access is no longer needed. <br>
Risk: Image prompts, uploaded images, referenced image URLs, and generation requests are sent to xAI for the skill's stated purpose. <br>
Mitigation: Do not submit sensitive, regulated, or confidential content unless xAI processing is approved for that data. <br>
Risk: The source installation path runs package build and link commands from a cloned repository. <br>
Mitigation: Prefer the npm install path for normal use, or audit the source and install command before building from source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberash-dev/grok-image-cli) <br>
- [grok-image-cli source](https://github.com/cyberash-dev/grok-image-cli) <br>
- [xAI image generation documentation](https://docs.x.ai/docs/guides/image-generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include commands for installing grok-image-cli, storing an xAI API key, generating images, editing images, and selecting models or output directories.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
