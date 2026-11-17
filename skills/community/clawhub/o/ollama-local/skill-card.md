## Description:

Manage and use local Ollama models for model management, chat and completion requests, embeddings, tool-use workflows, and OpenClaw sub-agent integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timverhoogt](https://clawhub.ai/user/timverhoogt)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to interact with local or trusted remote Ollama servers, manage installed models, run prompts and embeddings, test tool-calling behavior, and configure Ollama-backed sub-agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, embedding text, and tool-use messages are sent to the configured Ollama host.

Mitigation: Keep OLLAMA_HOST on localhost for private work, or use only a trusted remote Ollama server with appropriate transport protections.

Risk: Sensitive data could be exposed through prompts or embedding requests.

Mitigation: Avoid sending secrets or confidential text in prompts, embedding input, or tool-call messages.

Risk: The remove-model command deletes a local Ollama model.

Mitigation: Verify the target model name before using rm.

## Reference(s):

- [Model Guide](artifact/references/models.md)
- [ClawHub Skill Page](https://clawhub.ai/timverhoogt/skills/ollama-local)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, JSON examples, and text responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send prompts, embedding text, and tool-call messages to the configured OLLAMA_HOST. Model removal commands delete local Ollama models.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
