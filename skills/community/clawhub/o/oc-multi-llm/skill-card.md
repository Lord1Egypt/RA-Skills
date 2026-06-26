## Description: <br>
Universal adapter for multiple LLM providers with a unified interface for OpenAI, Anthropic, Google Gemini, Ollama, and LiteLLM-backed providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to call, compare, and fail over across configured LLM providers through one Python and CLI interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, system messages, tool definitions, and provider API keys may be sensitive when sent to configured LLM providers. <br>
Mitigation: Use dedicated provider API keys, avoid secrets in prompts and tool schemas, and route sensitive work only to approved providers. <br>
Risk: Automatic fallback, load balancing, and compare modes can send the same content to more than one provider. <br>
Mitigation: Disable auto or compare modes for sensitive data and select the intended provider explicitly. <br>
Risk: Dependencies are declared with open lower bounds, which can change runtime behavior over time. <br>
Mitigation: Pin and scan dependencies before production or regulated use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/oc-multi-llm) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON responses, with Markdown-oriented command and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports streaming responses, provider comparison output, and optional provider/model usage metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version text) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
