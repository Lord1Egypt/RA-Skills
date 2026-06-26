## Description: <br>
Configure AIsa as a first-class model provider for OpenClaw, enabling production access to major Chinese AI models such as Qwen, DeepSeek, Kimi K2.5, and Doubao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw for AIsa API access, choose Chinese LLM models, compare model pricing, and troubleshoot provider setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AISA_API_KEY is required and could be exposed if pasted into shell history, chat logs, or command-line arguments. <br>
Mitigation: Set AISA_API_KEY through an environment variable or OpenClaw's interactive onboarding flow, and avoid passing the key directly as a command-line argument. <br>
Risk: The skill routes prompts to AIsa and downstream model providers, so confidential prompts depend on provider privacy terms. <br>
Mitigation: Review AIsa and provider privacy terms before sending confidential data, especially for privacy-sensitive or regulated workloads. <br>
Risk: Applying the provided configuration can change OpenClaw's default model provider or model selection. <br>
Mitigation: Review default-model and fallback changes before applying them to an existing OpenClaw configuration. <br>
Risk: Kimi K2.5 accepts only temperature=1.0, so incompatible temperature settings can cause request failures. <br>
Mitigation: Use the model's default temperature or configure Kimi K2.5 with temperature=1.0. <br>
Risk: Pricing and model availability are time-sensitive and may differ from the reference documentation. <br>
Mitigation: Check the AIsa marketplace pricing page and model endpoint before making cost or deployment decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xjordansg-yolo/openclaw-aisa-chinese-llm-models) <br>
- [AIsa Marketplace](https://marketplace.aisa.one) <br>
- [AIsa Pricing](https://marketplace.aisa.one/pricing) <br>
- [AIsa Provider Configuration Examples](artifact/references/config-examples.md) <br>
- [AIsa Pricing Reference](artifact/references/pricing.md) <br>
- [AIsa Chinese Usage Guide](artifact/references/guide-zh-CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces provider setup steps, model IDs, pricing references, and troubleshooting guidance for OpenClaw.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
