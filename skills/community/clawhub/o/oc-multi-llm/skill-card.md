## Description:

Provides a Python and CLI adapter for OpenAI, Anthropic, and Ollama chat, streaming, response comparison, and priority fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and call supported LLM providers through one interface, compare model responses, stream replies, and fall back by provider priority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, responses, API keys, and tool definitions may be sent to configurable provider endpoints.

Mitigation: Use trusted provider configuration, avoid custom base URLs unless you control the endpoint, and do not include secrets or private data in prompts.

Risk: The artifact documentation advertises Gemini, LiteLLM, load balancing, and cost tracking features that are not supported by the included code.

Mitigation: Rely only on implemented OpenAI, Anthropic, Ollama, streaming, comparison, and priority fallback behavior until matching code and documentation are added.

Risk: Dependencies are specified as version ranges and no lock file is included.

Mitigation: Pin and review dependencies in the deployment environment before installation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with CLI commands, Python snippets, configuration examples, and optional JSON comparison output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route prompts, responses, API keys, and tool definitions to configured provider endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
