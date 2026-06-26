## Description: <br>
Helps deploy MiGPT on Xiaomi and Redmi smart speakers, configure a custom LLM-powered voice assistant, and troubleshoot MIoT, MiNA, latency, wake-word, and device-specific setup issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuituijcb](https://clawhub.ai/user/tuituijcb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and smart-home operators use this skill to set up a MiGPT-based voice assistant on supported Xiaomi or Redmi speakers and to generate setup guidance, configuration, shell commands, and targeted patch instructions. It is especially relevant when resolving MIoT login loops, model-specific TTS behavior, stream-response hangs, native assistant race conditions, and response-latency tuning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes high-risk guidance for bypassing Xiaomi account security checks with browser cookies and cached MIoT tokens. <br>
Mitigation: Prefer supported Xiaomi login and recovery flows; only use cookie or token injection when the user understands the account-takeover risk and can protect the resulting credentials. <br>
Risk: Configuration files such as .env, .migpt.js, and .mi.json can contain Xiaomi credentials, LLM API keys, browser cookies, service tokens, or voice-assistant secrets. <br>
Mitigation: Keep these files out of git, restrict local file permissions, use a dedicated Xiaomi account where possible, and rotate any exposed keys or sessions. <br>
Risk: The deployment may send voice transcripts or assistant prompts to the configured OpenAI-compatible LLM provider. <br>
Mitigation: Choose an LLM provider appropriate for the user's privacy requirements and avoid sending sensitive speech content unless the provider and configuration are acceptable. <br>
Risk: The skill asks users to patch files in node_modules, which can alter dependency behavior and may be overwritten by future installs. <br>
Mitigation: Review dependency patches before applying them, keep them reproducible with patch-package or a postinstall step, and re-check behavior after npm install or dependency updates. <br>


## Reference(s): <br>
- [MiGPT](https://github.com/idootop/mi-gpt) <br>
- [MiGPT Issues](https://github.com/idootop/mi-gpt/issues) <br>
- [MIoT Specification](https://home.miot-spec.com/) <br>
- [mi-service-lite](https://www.npmjs.com/package/mi-service-lite) <br>
- [MiGPT Configuration Template](references/config-template.md) <br>
- [MIoT Authentication Bypass](references/miot-auth-bypass.md) <br>
- [Required Code Patches](references/patches.md) <br>
- [End-to-End Latency Analysis](references/latency-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash, JavaScript, JSON, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local dependency patch instructions and credential-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
