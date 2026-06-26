## Description: <br>
Generate and edit images via OpenAI gpt-image-2 with an agent-agnostic CLI that supports configurable API endpoints and credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jancong](https://clawhub.ai/user/jancong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can call the bundled CLI to generate new images from prompts or edit existing images through an OpenAI-compatible image API. The skill is useful when an agent needs a repeatable shell workflow for image generation, image editing, and credential-aware configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured custom or relay API endpoints may receive prompts, source images, generated images, and bearer tokens. <br>
Mitigation: Use the default OpenAI endpoint or only configure a relay endpoint whose operator you trust. <br>
Risk: API credentials can be exposed through plaintext config files, shell history, process listings, or loose file permissions. <br>
Mitigation: Prefer environment-variable based configuration, keep config files owner-readable only, avoid the --api-key flag for routine use, and rotate keys if exposure is suspected. <br>
Risk: Prompts and input images may contain sensitive or regulated content that is sent to the configured image API. <br>
Mitigation: Review prompts and source images before use and follow the user's or organization's data handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jancong/gpt-image-2-api) <br>
- [OpenAI API base URL](https://api.openai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [CLI stdout, generated image files, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+, curl, and an OpenAI-compatible image API key; generated image count and output format are controlled by CLI options.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
