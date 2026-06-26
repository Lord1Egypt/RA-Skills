## Description: <br>
LLM Key Pool helps agents route LLM requests across tiered provider API keys with round-robin selection, cooldowns, and failover. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chatgpt34993](https://clawhub.ai/user/chatgpt34993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage multiple LLM provider API keys, reduce single-key rate-limit failures, and keep model calls available through tiered failover. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured provider API keys can be exposed if llm_config.yaml is committed, shared, or stored with broad file permissions. <br>
Mitigation: Keep llm_config.yaml private, restrict file permissions, and do not commit or share the file. <br>
Risk: Automatic failover can route prompts or data to any configured provider. <br>
Mitigation: Configure only providers approved for the data being sent, especially for regulated, proprietary, or secret content. <br>
Risk: Multi-provider key rotation can increase quota usage or billing across several accounts. <br>
Mitigation: Monitor billing and quota for each configured provider and review tier settings before enabling broad failover. <br>


## Reference(s): <br>
- [Configuration Format](references/config_format.md) <br>
- [Supported Providers](references/supported_providers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text responses, JSON status objects, YAML configuration examples, and Markdown instructions with command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured provider APIs and may return provider, tier, model, key index, temperature, and token-limit metadata alongside the model response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
