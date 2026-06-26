## Description: <br>
Helps OpenClaw users switch between configured AI models, add provider configurations, and update local OpenClaw settings through bundled Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwg2025](https://clawhub.ai/user/williamwg2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers who run OpenClaw use this skill to switch among local model presets, add new model providers, and update the active model configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit ~/.openclaw/openclaw.json and the bundled models.json, changing the active OpenClaw model configuration. <br>
Mitigation: Back up configuration before use and verify the active model after switching. <br>
Risk: Provider API keys may be stored in plaintext in ~/.openclaw/openclaw.json. <br>
Mitigation: Restrict file permissions, avoid committing the file to source control, and use external secret management where required. <br>
Risk: Switching models can restart the OpenClaw gateway and briefly interrupt service. <br>
Mitigation: Run switches during an acceptable maintenance window and confirm gateway status after restart. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/williamwg2025/openclaw-model-switch-2) <br>
- [README](artifact/README.md) <br>
- [English README](artifact/README_EN.md) <br>
- [Google AI Studio API keys](https://makersuite.google.com/app/apikey) <br>
- [OpenAI API keys](https://platform.openai.com/api-keys) <br>
- [Anthropic API keys](https://console.anthropic.com/settings/keys) <br>
- [DashScope API keys](https://dashscope.console.aliyun.com/apiKey) <br>
- [Moonshot platform](https://platform.moonshot.cn) <br>
- [MiniMax platform](https://platform.minimaxi.com) <br>
- [Zhipu GLM platform](https://open.bigmodel.cn) <br>
- [DeepSeek platform](https://platform.deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with shell commands and JSON configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify ~/.openclaw/openclaw.json and artifact/config/models.json, create backups, and restart the OpenClaw gateway.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
