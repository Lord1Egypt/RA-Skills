## Description:

Runs local image OCR on Windows with GLM-OCR and llama.cpp Vulkan to extract text from images, scanned documents, screenshots, receipts, invoices, tables, business cards, IDs, and mixed Chinese/English content without cloud API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violet17](https://clawhub.ai/user/violet17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to set up a local Windows OCR workflow and extract readable text or structured fields from image-based documents. It is suited to local document digitization tasks where cloud OCR is not desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can install and run third-party executables and broad PowerShell commands.

Mitigation: Install only after reviewing the setup steps; prefer manual installation or verify downloaded hashes and signatures where available.

Risk: The skill downloads large third-party model and tooling files before first use.

Mitigation: Confirm the download with the user, ensure adequate disk space and network trust, and use manual download fallback when automatic download behavior is not acceptable.

Risk: OCR inputs and outputs may contain sensitive IDs, contracts, financial documents, or other confidential text.

Mitigation: Avoid highly sensitive documents unless local storage and output handling are understood and acceptable for the user's policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/violet17/skills/image-ocr-local-aipc)
- [GLM-OCR GGUF](https://huggingface.co/ggml-org/GLM-OCR-GGUF)
- [llama.cpp Releases](https://github.com/ggml-org/llama.cpp/releases)
- [Miniforge Releases](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Plain text OCR results, Markdown tables, JSON field extraction, and PowerShell setup commands depending on the user request.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR results may preserve layout or be reorganized into task-specific fields for invoices, receipts, tables, business cards, IDs, screenshots, and documents.]

## Skill Version(s):

1.0.0 (source: release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
