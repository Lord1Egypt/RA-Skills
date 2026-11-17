## Description:

Manage and control local LLM services like Ollama and vLLM, including starting services, pulling models, and querying APIs through a unified interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check, start, and query local LLM services such as Ollama, vLLM, and OpenAI-compatible endpoints from a unified command interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and an optional OPENAI_API_KEY can be sent to the endpoint named by OPENAI_BASE_URL.

Mitigation: Use only trusted HTTPS endpoints, review OPENAI_BASE_URL and OPENAI_API_KEY before use, and avoid sensitive prompts.

Risk: The skill can start Ollama and pull models through local commands.

Mitigation: Run it only in environments where starting local services and downloading models are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/llm-service-manager)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command responses and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include model output returned by a local or configured LLM service.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
