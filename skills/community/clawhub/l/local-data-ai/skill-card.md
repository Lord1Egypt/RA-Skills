## Description:

LocalDataAI helps agents parse and analyze local private files with offline models, including WPS, PDF, Excel, image OCR, and WeChat cache files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise teams use this skill to build local document-processing workflows that parse private files, answer questions, summarize content, extract entities, and search across documents without relying on cloud inference at runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security, sandboxing, offline, and audit claims may exceed the protections actually enforced by the artifact.

Mitigation: Review the implementation before sensitive use, restrict file access, and treat sandbox and compliance behavior as application code rather than certified isolation or audit control.

Risk: The skill depends on large external model and package downloads during setup.

Mitigation: Use a disposable virtual environment and pin, verify, and stage dependencies and model files before deployment.

Risk: Private or regulated documents may be exposed if path validation, output handling, or audit-key management is incomplete.

Mitigation: Avoid highly sensitive documents until those controls are reviewed and fixed for the target environment.

## Reference(s):

- [LocalDataAI ClawHub Skill Page](https://clawhub.ai/kaiyuelv/skills/local-data-ai)
- [Qwen2.5-3B-Instruct GGUF model asset](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf)
- [BGE-M3 embedding model asset](https://huggingface.co/BAAI/bge-m3/resolve/main/model.safetensors)
- [PaddleOCR v4 recognition model archive](https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_rec_infer.tar)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Natural-language text with Python snippets, shell commands, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce answers, summaries, extracted entities, search results, audit guidance, and local setup instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
