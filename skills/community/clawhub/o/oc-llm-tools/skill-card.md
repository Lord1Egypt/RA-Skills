## Description:

Universal tool definition system for LLM function calling that defines tools once and converts them for providers such as OpenAI, Anthropic, Gemini, Ollama, Mistral, and Cohere.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define LLM-callable tools in one JSON Schema-based format, validate tool calls, and convert those definitions for multiple LLM providers. It also provides a small CLI for converting, validating, and listing tool definitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and exec authority.

Mitigation: Review before installing, prefer sandboxed environments, and remove or constrain exec permission when it is not required.

Risk: The artifact includes unsafe integration examples such as an eval-based handler.

Mitigation: Do not copy those examples into production; replace them with bounded handlers that validate inputs and avoid dynamic code execution.

Risk: File-reading handler examples could expose unintended paths if copied directly.

Mitigation: Constrain file access to approved directories and validate paths before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/michealxie001/skills/oc-llm-tools)
- [Artifact Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [code, configuration, shell commands, guidance]

**Output Format:** [Markdown with Python, JSON, and bash examples; CLI commands can emit JSON tool definitions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports JSON Schema-style tool parameters and provider-specific conversions for OpenAI, Anthropic, Gemini, and Ollama.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
