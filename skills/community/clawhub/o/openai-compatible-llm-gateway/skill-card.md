## Description: <br>
OpenAI-compatible LLM gateway for AI agents that lets OpenAI clients use a drop-in base_url for chat completions across listed model families, with USDC pay-per-call or funded-key payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colinhughes2121](https://clawhub.ai/user/colinhughes2121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to configure OpenAI-compatible clients for third-party LLM chat completions through gocreativeai.com. It is useful when a workflow needs pay-per-call USDC access, a funded key, or a single OpenAI-style base URL for multiple model families. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, messages, and payment-related API activity are routed through a third-party gateway. <br>
Mitigation: Review the provider's privacy, retention, logging, payment, and downstream model-provider terms before sending secrets, regulated data, customer data, or internal business context. <br>
Risk: Agents with broad HTTP access could call unintended endpoints or tiers. <br>
Mitigation: Restrict network or tool access to the intended LLM endpoints and model tiers before deployment. <br>
Risk: Pay-per-call and funded-key usage can create spend exposure. <br>
Mitigation: Use spending controls, funded-key limits, and review steps appropriate for the agent workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/colinhughes2121/openai-compatible-llm-gateway) <br>
- [Gateway API base URL](https://api.gocreativeai.com/v1) <br>
- [OpenAI-compatible chat completions endpoint](https://api.gocreativeai.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce HTTP request examples and OpenAI client base_url configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
