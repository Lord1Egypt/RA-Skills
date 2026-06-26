## Description: <br>
MLX Swift LM - Run LLMs and VLMs on Apple Silicon using MLX. Covers local inference, streaming, tool calling, LoRA fine-tuning, and embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ronaldmannak](https://clawhub.ai/user/ronaldmannak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill for Swift guidance on running LLMs, VLMs, embeddings, tool calling, streaming generation, and LoRA fine-tuning on Apple Silicon with MLX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may download or load remote Hugging Face models and media URLs. <br>
Mitigation: Pin trusted model revisions where practical and restrict remote media URLs before using examples in production workflows. <br>
Risk: Tool-calling examples can connect model outputs to actions with external effects. <br>
Mitigation: Require validation or confirmation before connecting model tool calls to file changes, account actions, payments, or public posting. <br>
Risk: Credentials such as Hugging Face tokens could be exposed if copied directly into source code. <br>
Mitigation: Keep tokens out of source code and use environment or secret-management mechanisms. <br>


## Reference(s): <br>
- [MLX Swift LM ClawHub release](https://clawhub.ai/ronaldmannak/mlx-swift-lm) <br>
- [Model Container & Model Loading](references/model-container.md) <br>
- [KV Cache](references/kv-cache.md) <br>
- [Concurrency Patterns](references/concurrency.md) <br>
- [Tool Calling](references/tool-calling.md) <br>
- [Tokenizer & Chat Templates](references/tokenizer-chat.md) <br>
- [Supported Models](references/supported-models.md) <br>
- [LoRA Adapters](references/lora-adapters.md) <br>
- [Training](references/training.md) <br>
- [Embedding Models](references/embeddings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with Swift code examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; security evidence reports clean scanner results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
