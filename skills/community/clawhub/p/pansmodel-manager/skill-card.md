## Description: <br>
PanSclaw model manager for adding, deleting, switching, and listing custom model provider configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw/PanSclaw users use this skill to manage custom model access, switch the default model, and maintain configured providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store API keys in local OpenClaw/PanSclaw model configuration. <br>
Mitigation: Use it only where plaintext local key storage is acceptable, avoid production API keys when that is not acceptable, and restrict local file permissions. <br>
Risk: The skill can change or delete configured model providers. <br>
Mitigation: Back up ~/.openclaw-pansclaw/openclaw.json before switching or deleting providers and double-check provider names before running commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or terminal text with command examples and local JSON configuration updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update ~/.openclaw-pansclaw/openclaw.json when the bundled script is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
