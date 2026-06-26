## Description: <br>
Access high-performance open-source models through OpenRouter-compatible endpoints for a free GPT-5.5-like chat experience that requires an API key. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[leic8959-sudo](https://clawhub.ai/user/leic8959-sudo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI experimenters can use this skill to send prompts to OpenRouter-compatible free model endpoints for lightweight chat demos and evaluation while supplying their own API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and included context are sent to OpenRouter or the configured external LLM endpoint. <br>
Mitigation: Do not submit secrets, regulated data, or private customer information unless the provider's privacy and retention terms have been reviewed. <br>
Risk: The skill requires a sensitive API key and allows a custom API endpoint. <br>
Mitigation: Store credentials in environment variables, use only trusted endpoints, and rotate keys if they are exposed. <br>
Risk: Free model tiers may have rate limits and may not match an official GPT-5.5 service. <br>
Mitigation: Use the skill for demos and lightweight evaluation, validate important responses independently, and avoid high-concurrency production workloads. <br>


## Reference(s): <br>
- [Artifact overview](docs/overview.md) <br>
- [OpenRouter](https://openrouter.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JavaScript snippets; runtime chat responses are plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and sends prompts to OpenRouter or the configured OpenAI-compatible API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
