## Description:

Configures AIsa as an OpenClaw model provider for Chinese LLMs including Qwen, DeepSeek, Kimi K2.5, and Doubao, with setup, pricing comparison, model switching, and troubleshooting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure AIsa API access, choose Chinese LLM model IDs, compare reference pricing, and troubleshoot provider setup. It is intended for production model-routing workflows that require AISA_API_KEY access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AISA_API_KEY can be exposed if passed as a command-line argument or printed in shared terminals or logs.

Mitigation: Prefer interactive onboarding or a protected secret store, and avoid commands that echo or log the key.

Risk: Prompts and outputs are routed through AIsa and upstream model providers.

Mitigation: Review AIsa and Moonshot privacy terms before sending regulated or highly sensitive data.

Risk: The artifact makes strong privacy claims for an external model provider.

Mitigation: Treat privacy claims as requiring independent review before relying on the skill for sensitive workloads.

Risk: Kimi K2.5 requests fail when temperature is set to a value other than 1.0.

Mitigation: Use the model default or set temperature to 1.0 for Kimi K2.5 configurations.

## Reference(s):

- [AIsa Provider Configuration Examples](artifact/references/config-examples.md)
- [AIsa Pricing Reference](artifact/references/pricing.md)
- [AIsa Chinese User Guide](artifact/references/guide-zh-CN.md)
- [AIsa Marketplace](https://marketplace.aisa.one)
- [AIsa Pricing](https://marketplace.aisa.one/pricing)
- [AIsa Models API](https://api.aisa.one/v1/models)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw provider configuration snippets, model IDs, pricing notes, and API-key setup guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
