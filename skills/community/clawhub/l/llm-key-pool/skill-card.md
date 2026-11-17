## Description:

Manages multiple LLM provider API keys with tiered rotation, failover, cooldown handling, and a unified client interface for OpenAI-compatible and Anthropic-style calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chatgpt34993](https://clawhub.ai/user/chatgpt34993)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route LLM prompts across configured provider keys, reduce disruption from rate limits, and fail over between primary, daily, and fallback provider tiers. It is most relevant when an agent needs a local configuration-driven client for high-availability model calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores live LLM provider API keys in a local YAML configuration file.

Mitigation: Use restrictive file permissions for llm_config.yaml, keep it out of version control, and never share configs containing real keys.

Risk: Prompts and responses are routed through whichever third-party LLM providers are configured.

Mitigation: Use trusted HTTPS endpoints, avoid custom or shared configs, and test with non-sensitive prompts before operational use.

Risk: Provider usage can create unexpected billing or quota consumption.

Mitigation: Monitor provider dashboards, configure cooldown and retry settings conservatively, and review usage after failover events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chatgpt34993/skills/llm-key-pool)
- [Configuration format](references/config_format.md)
- [Supported providers](references/supported_providers.md)
- [Quickstart](assets/QUICKSTART.md)
- [Platform setup guide](assets/PLATFORM_SETUP_GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance, command-line output, YAML configuration, and Python call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include provider, tier, model, and key-index metadata for completed calls.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
