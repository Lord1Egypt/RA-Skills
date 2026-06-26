## Description: <br>
Poe Connector lets an OpenClaw agent use Poe.com models for chat, media generation, file-based prompts, and model discovery through a configured Poe API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dzwalker](https://clawhub.ai/user/dzwalker) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to route selected prompts, optional local files, and media-generation requests to Poe.com models from OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected local files can be sent to Poe, including sensitive or regulated content if the user attaches it. <br>
Mitigation: Use a dedicated Poe API key and avoid sending secrets, private keys, confidential documents, or regulated data unless the user explicitly intends to share them with Poe. <br>
Risk: Generated media URLs can be auto-downloaded from model responses. <br>
Mitigation: Review downloaded media before redistributing it and treat model-returned URLs as untrusted content. <br>
Risk: The Poe API key is read from the OpenClaw configuration file. <br>
Mitigation: Protect the OpenClaw configuration file and rotate the Poe API key if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dzwalker/poe-connector) <br>
- [Poe API keys](https://poe.com/api/keys) <br>
- [Poe API endpoint](https://api.poe.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown, shell command output, JSON-capable model listings, and downloaded media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, bash, the openai Python package, and a configured POE_API_KEY in OpenClaw skill config.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
