## Description: <br>
Intelligent model router for OpenClaw that reads local configuration, classifies available models into Premium, Balanced, and Economy tiers, and routes tasks to a suitable active model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forrestinfo](https://clawhub.ai/user/forrestinfo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to choose an available LLM for coding, writing, reasoning, agent, long-context, and quick-query tasks based on local provider configuration and tier preference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local OpenClaw configuration and provider availability to decide which models are active. <br>
Mitigation: Install only if this local inspection is acceptable, and review the configuration paths, provider keys, and diagnostic script behavior before use. <br>
Risk: Routing decisions can affect cost and which provider receives user prompts. <br>
Mitigation: Review tier defaults and use manual model overrides or an allowlist when strict cost or provider control is required. <br>


## Reference(s): <br>
- [OpenClaw LLM Router ClawHub Page](https://clawhub.ai/forrestinfo/openclaw-llm-router) <br>
- [OpenClaw LLM Router Homepage](https://clawhub.ai/skills/openclaw-llm-router) <br>
- [Model Tiers Reference](references/model-tiers.md) <br>
- [OpenClaw Config Format](references/openclaw-config-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style routing guidance with model recommendations and occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes within the user's active OpenClaw providers and optional model allowlist.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
