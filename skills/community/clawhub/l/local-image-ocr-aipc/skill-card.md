## Description: <br>
Extracts text from images, scanned documents, invoices, receipts, contracts, tables, business cards, IDs, screenshots, and other documents locally on Windows with GLM-OCR and llama.cpp Vulkan, prioritizing Intel iGPU inference without cloud API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[violet17](https://clawhub.ai/user/violet17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and end users can use this skill to set up a local Windows OCR workflow and extract or structure text from images, receipts, invoices, business cards, IDs, screenshots, and documents without calling a cloud OCR API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup modifies the user's Python environment and may install packages or Miniforge with the user's privileges. <br>
Mitigation: Run setup in an isolated Python environment and confirm before allowing automatic installers or pip package installation. <br>
Risk: The skill downloads and executes llama.cpp binaries from GitHub releases. <br>
Mitigation: Install only after reviewing and trusting the GitHub release source, and prefer verified or pinned downloads where operational policy requires it. <br>
Risk: The workflow downloads large model files from HuggingFace or ModelScope. <br>
Mitigation: Verify the intended model source and ensure enough disk space before starting setup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/violet17/local-image-ocr-aipc) <br>
- [violet17 publisher profile](https://clawhub.ai/user/violet17) <br>
- [llama.cpp releases](https://github.com/ggml-org/llama.cpp/releases) <br>
- [GLM-OCR GGUF model](https://huggingface.co/ggml-org/GLM-OCR-GGUF) <br>
- [Miniforge releases](https://github.com/conda-forge/miniforge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and OCR text output; structured JSON or Markdown tables may be produced when the user asks for extracted fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local llama-server HTTP process for inference, then returns recognized text or user-requested structured summaries.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
