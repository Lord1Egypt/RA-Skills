## Description: <br>
Helps agents recommend, configure, and test OpenAI-compatible access to Chinese AI API providers such as MiMo, DeepSeek, Qwen, GLM, and related gateway setups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to compare Chinese AI API providers, select low-cost or free model endpoints, generate OpenAI-compatible code and configuration, and troubleshoot routing, quota, and connectivity issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and API requests may be sent to third-party AI providers. <br>
Mitigation: Use only providers whose logging, retention, pricing, and quota policies are acceptable for the data being processed. <br>
Risk: API keys may be exposed or reused unsafely in generated gateway configuration. <br>
Mitigation: Store real keys in environment variables or a secret manager and avoid committing credentials to source files. <br>
Risk: A self-hosted gateway exposed publicly could allow unauthorized use of configured provider accounts. <br>
Mitigation: Add authentication and firewall or private-network controls before exposing the gateway outside a trusted environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/mimo-china-api-gateway) <br>
- [中国AI API统一网关 - 详细内容](references/details.md) <br>
- [中国AI平台注册与API获取指南](references/platforms.md) <br>
- [MiMo platform](https://platform.xiaomimimo.com) <br>
- [DeepSeek platform](https://platform.deepseek.com) <br>
- [Alibaba Bailian console](https://bailian.console.aliyun.com) <br>
- [Zhipu AI Open Platform](https://open.bigmodel.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python, curl, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider recommendations, API key setup steps, local gateway commands, and fallback or troubleshooting advice.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
