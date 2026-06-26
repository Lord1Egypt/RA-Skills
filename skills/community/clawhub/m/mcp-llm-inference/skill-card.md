## Description: <br>
Anonymous LLM inference via L402 micropayments for chat completions, text generation, and model discovery without API keys or account signup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haveblue997](https://clawhub.ai/user/haveblue997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this MCP skill to call remote LLM chat, text generation, and model-listing endpoints through L402 micropayments. It is intended for workflows that need LLM access without managing provider API keys or billing accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and chat history are sent to a configured external LLM service. <br>
Mitigation: Use only with data suitable for the configured provider, and avoid sending secrets, regulated data, or sensitive conversation history unless that endpoint is approved. <br>
Risk: The declared environment variable in SKILL.md differs from the variable used by the code. <br>
Mitigation: Configure and review NAUTDEV_BASE_URL for endpoint control; do not assume L402_API_BASE_URL changes runtime behavior. <br>
Risk: Installation examples and package metadata name different npm package scopes. <br>
Mitigation: Verify the exact npm package before installation and pin the reviewed package version. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haveblue997/mcp-llm-inference) <br>
- [Publisher profile](https://clawhub.ai/user/haveblue997) <br>
- [Configured L402 API endpoint](https://api.nautdev.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, configuration, guidance] <br>
**Output Format:** [JSON responses returned as MCP text content, plus setup guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote LLM responses depend on the configured endpoint, selected model, prompt, and paid L402 request flow.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
