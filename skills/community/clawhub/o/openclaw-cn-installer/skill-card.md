## Description: <br>
OpenClaw Chinese installation helper that checks the local environment, configures DeepSeek, Zhipu GLM, and Alibaba Qwen providers, and tests API connections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users, especially Chinese-language users, use this skill to check their local Node.js environment, configure supported domestic AI providers, and verify API connectivity before running OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script stores AI provider API keys in ~/.openclaw/.env on the local machine. <br>
Mitigation: Use revocable API keys, restrict access to ~/.openclaw/.env, and rotate keys if the skill is removed or the local machine is no longer trusted. <br>
Risk: Diagnostic scripts run locally and make outbound API calls to configured providers. <br>
Mitigation: Install only from a trusted publisher, review commands before execution, and avoid sharing logs or screenshots that may include configuration or secret material. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [DeepSeek Platform](https://platform.deepseek.com) <br>
- [Zhipu AI Platform](https://open.bigmodel.cn) <br>
- [Alibaba DashScope Console](https://dashscope.console.aliyun.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with command-line output and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [User-invoked scripts can create or update ~/.openclaw/.env and ~/.openclaw/config.json, then run outbound API connection checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
