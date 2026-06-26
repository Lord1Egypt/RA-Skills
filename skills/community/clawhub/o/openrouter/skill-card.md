## Description: <br>
OpenRouter API gateway skill that helps agents use a single OpenAI-compatible API key to access many model providers with unified billing, fallback routing, provider controls, and BYOK support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure OpenRouter credentials, call OpenRouter's OpenAI-compatible endpoints, compare model and routing options, and understand operational constraints such as billing, provider policies, and rate limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a paid OpenRouter API key, so agent use can spend account credits. <br>
Mitigation: Use a dedicated revocable key and configure spending limits before enabling live API calls. <br>
Risk: Prompts and completions may be routed to external model providers through OpenRouter. <br>
Mitigation: Review provider routing and privacy settings, use provider allowlists for sensitive workflows, and enable ZDR where appropriate. <br>
Risk: The :online model variant can introduce web search data flow for prompts. <br>
Mitigation: Avoid :online for sensitive prompts unless the additional web search data flow is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jononovo/openrouter) <br>
- [OpenRouter Homepage](https://openrouter.ai) <br>
- [OpenRouter Documentation](https://openrouter.ai/docs) <br>
- [OpenRouter Models](https://openrouter.ai/models) <br>
- [OpenRouter API Base](https://openrouter.ai/api/v1) <br>
- [OpenRouter Status](https://status.openrouter.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, API examples, Python code, configuration notes, and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY for live API use; examples target OpenRouter's OpenAI-compatible API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
