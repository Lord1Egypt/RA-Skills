## Description: <br>
Configure AIsa as a first-class model provider for OpenClaw, enabling production access to major Chinese AI models including Qwen, DeepSeek, Kimi K2.5, and Doubao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIsaDocs](https://clawhub.ai/user/AIsaDocs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure AIsa API access, select Chinese LLMs, compare provider pricing, and troubleshoot AIsa model-provider setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys can be exposed if pasted directly into shell history, logs, or shared configuration. <br>
Mitigation: Use interactive onboarding, environment-variable indirection, or a secure secret store, and avoid placing real AIsa API keys directly in command history. <br>
Risk: Changing the default OpenClaw model to AIsa may route future prompts through AIsa and create usage charges. <br>
Mitigation: Confirm the intended provider and model before making AIsa the default, and verify current pricing before sustained use. <br>
Risk: Pricing, privacy, and Zero Data Retention terms for model access can change over time. <br>
Mitigation: Check the current AIsa pricing and provider terms before relying on quoted rates or privacy claims for production workloads. <br>
Risk: Kimi K2.5 rejects temperature settings other than 1.0. <br>
Mitigation: Use the model default or set temperature to 1.0 when selecting Kimi K2.5. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIsaDocs/openclaw-aisa-leading-chinese-llm) <br>
- [AIsa marketplace](https://marketplace.aisa.one) <br>
- [AIsa pricing](https://marketplace.aisa.one/pricing) <br>
- [AIsa models endpoint](https://api.aisa.one/v1/models) <br>
- [Pricing reference](artifact/pricing.md) <br>
- [Chinese usage guide](artifact/guide-zh-CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API key setup steps, provider configuration, pricing comparisons, model selection guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
