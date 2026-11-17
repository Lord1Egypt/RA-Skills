## Description:

Python skill using LangChain to manage conversation memory and chains, enabling context-aware, concise Vietnamese replies with customizable prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[s0nocean](https://clawhub.ai/user/s0nocean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route Vietnamese LangChain-style queries through a Python assistant interface for conversational answers, with documented plans for memory, PDF RAG, tool calling, and model-provider backends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation describes broad capabilities such as reading files, retaining chat memory, processing PDFs, and using model-provider API keys, while the shipped code is only a prototype stub.

Mitigation: Treat the skill as a prototype before installation, keep secrets in environment variables or a secret manager, and review any future implementation before allowing local file access or memory retention.

Risk: User-provided PDFs, files, and chat history may be processed by the selected model provider if those documented features are later implemented.

Mitigation: Only provide content that is appropriate for the chosen provider and confirm data-handling expectations before enabling RAG, file reading, or long-term memory.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/s0nocean/skills/langchain-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/s0nocean)

## Skill Output:

**Output Type(s):** [Text, Guidance, Code]

**Output Format:** [Plain text response string from a Python function, with Markdown-style usage examples in the documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The shipped code is a small stub; documented memory, RAG, and tool-calling behavior is not implemented in the included Python file.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
