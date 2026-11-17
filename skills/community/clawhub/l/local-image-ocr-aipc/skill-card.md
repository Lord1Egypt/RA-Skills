## Description:

This skill guides an agent to set up and run local GLM-OCR image text extraction on Windows AI PCs using llama.cpp Vulkan, with no cloud API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violet17](https://clawhub.ai/user/violet17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to configure a local OCR environment and extract text from images, documents, screenshots, receipts, invoices, business cards, IDs, and tables. It is intended for local Windows AI PC workflows that avoid cloud OCR APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can download and run third-party executables and unpinned Python packages without integrity checks.

Mitigation: Use the manual or step-by-step setup path, review each command before execution, and verify upstream hashes or signatures where possible.

Risk: Autonomous installation in sensitive environments may introduce unreviewed binaries, model files, or Python dependencies.

Mitigation: Avoid autonomous setup unless the deployment environment trusts ggml-org, conda-forge, HuggingFace, ModelScope, and the Python package dependency chain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/violet17/skills/local-image-ocr-aipc)
- [llama.cpp Releases](https://github.com/ggml-org/llama.cpp/releases)
- [GLM-OCR GGUF](https://huggingface.co/ggml-org/GLM-OCR-GGUF)
- [Miniforge](https://github.com/conda-forge/miniforge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime OCR results as plain text, JSON, or Markdown tables depending on user request.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local llama-server process and returns recognized text; post-processing may structure OCR results for receipts, invoices, tables, business cards, IDs, or documents.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
