## Description:

MLX Swift LM - Run LLMs and VLMs on Apple Silicon using MLX. Covers local inference, streaming, tool calling, LoRA fine-tuning, and embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ronaldmannak](https://clawhub.ai/user/ronaldmannak)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to get Swift-oriented guidance, code examples, and configuration patterns for local LLM, VLM, embedding, tool-calling, and LoRA workflows with MLX on Apple Silicon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may trigger outbound downloads from Hugging Face and cache large model files locally.

Mitigation: Use trusted model IDs, pin revisions when reproducibility or supply-chain control matters, and review downloaded artifacts before deployment.

Risk: Prompt caches, adapter checkpoints, and training datasets can contain sensitive or proprietary data.

Mitigation: Store generated artifacts in approved locations, restrict access, and avoid sharing caches or checkpoints that may encode sensitive inputs.

## Reference(s):

- [ModelContainer & Model Loading](references/model-container.md)
- [KV Cache System](references/kv-cache.md)
- [Concurrency Patterns](references/concurrency.md)
- [Tool Calling](references/tool-calling.md)
- [Tokenizer & Chat Messages](references/tokenizer-chat.md)
- [Supported Models](references/supported-models.md)
- [LoRA Adapters](references/lora-adapters.md)
- [LoRA Training](references/training.md)
- [Embedding Models](references/embeddings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Swift code blocks and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model IDs, cache and checkpoint handling notes, and Swift API usage patterns.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
