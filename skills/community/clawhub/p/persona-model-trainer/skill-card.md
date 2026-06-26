## Description: <br>
Fine-tune any HuggingFace instruction-tuned model (Gemma 4, Qwen 3, Llama, Phi, Mistral, and more) on persona data from anyone-skill. Produces a self-contained, locally runnable persona model - no cloud API required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neiljo-gy](https://clawhub.ai/user/neiljo-gy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to convert persona training exports from anyone-skill or persona-knowledge into fine-tuned local persona models. It guides data preparation, LoRA or QLoRA training, evaluation, export, version management, and persona pack integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Arbitrary Hugging Face model choices can execute repository code locally during model loading. <br>
Mitigation: Use trusted and pinned model repositories, review model code before use, or remove trust_remote_code where compatible. <br>
Risk: Persona training data, generated adapters, and derived model artifacts can contain sensitive personal information. <br>
Mitigation: Review and redact training files before preparation, keep generated adapters private, and share artifacts only when the data owner intentionally approves it. <br>
Risk: Colab or Hugging Face push workflows can move persona material or derived model artifacts off the local machine. <br>
Mitigation: Use those workflows only when remote processing or publication is intended, and prefer private repositories for sensitive personas. <br>


## Reference(s): <br>
- [End-to-End Pipeline Guide](references/pipeline-guide.md) <br>
- [Model Selection Guide](references/model-selection.md) <br>
- [Model Registry](references/model-registry.md) <br>
- [QLoRA Hyperparameter Guide](references/qlora-guide.md) <br>
- [GGUF Quantization Guide](references/quantization.md) <br>
- [Privacy & Data Handling Guide](references/privacy.md) <br>
- [Pack Integration & Usage](references/pack-integration.md) <br>
- [Autoresearch Integration](references/autoresearch-integration.md) <br>
- [ClawHub skill page](https://clawhub.ai/neiljo-gy/persona-model-trainer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python commands; generated local configuration, evaluation summaries, and model artifact files when the bundled scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for preparing persona data, training adapters, evaluating voice fidelity, exporting GGUF/Ollama/vLLM/ONNX formats, and integrating generated artifacts into persona packs.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
