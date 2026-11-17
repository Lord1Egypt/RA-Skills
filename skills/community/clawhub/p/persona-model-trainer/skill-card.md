## Description:

Fine-tune any HuggingFace instruction-tuned model (Gemma 4, Qwen 3, Llama, Phi, Mistral, and more) on persona data from anyone-skill. Produces a self-contained, locally runnable persona model - no cloud API required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neiljo-gy](https://clawhub.ai/user/neiljo-gy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to fine-tune persona models from anyone-skill or persona-knowledge training data, then evaluate and export local adapters or runtime packages for Ollama, llama.cpp, vLLM, MLX, or ONNX.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe paths that can execute untrusted HuggingFace code.

Mitigation: Review or patch scripts before installation, use trusted and pinned HuggingFace models, and isolate any custom model repositories.

Risk: The security evidence reports paths that can delete or write files outside the intended model folder.

Mitigation: Use simple alphanumeric slugs and version labels, review output paths before execution, and run preview or dry-run modes where available.

Risk: Persona training data can encode sensitive personal information into model weights, and Colab or data upload modes may expose training material to third-party services.

Mitigation: Keep persona data local when possible, manually review and redact training/raw and conversations.jsonl before training, check PII scan outputs, and avoid --include-data or Colab unless sharing the data is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neiljo-gy/skills/persona-model-trainer)
- [End-to-End Pipeline Guide](references/pipeline-guide.md)
- [Model Registry](references/model-registry.md)
- [Model Selection Guide](references/model-selection.md)
- [QLoRA Hyperparameter Guide](references/qlora-guide.md)
- [GGUF Quantization Guide](references/quantization.md)
- [Privacy & Data Handling Guide](references/privacy.md)
- [Autoresearch Integration](references/autoresearch-integration.md)
- [Pack Integration & Usage](references/pack-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated files or configuration when scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce prepared datasets, LoRA or QLoRA adapter weights, evaluation JSON, GGUF/Ollama/vLLM/MLX/ONNX exports, model cards, dataset cards, and persona pack integration files.]

## Skill Version(s):

0.3.3 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
