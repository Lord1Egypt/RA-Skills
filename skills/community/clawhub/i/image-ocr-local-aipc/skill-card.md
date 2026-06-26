## Description: <br>
Provides local Windows image OCR using GLM-OCR and llama.cpp Vulkan to extract text from images, including mixed Chinese and English content, without cloud API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[violet17](https://clawhub.ai/user/violet17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to run on-device OCR for screenshots, scanned documents, invoices, receipts, business cards, IDs, tables, and other image text extraction tasks on Windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-use setup may download third-party binaries, Python tooling, and large model files. <br>
Mitigation: Use a dedicated OCR directory, review download sources before proceeding, and confirm available disk space before setup. <br>
Risk: The skill processes local image content that may contain sensitive information. <br>
Mitigation: Avoid highly sensitive images unless the local runtime and model installation are acceptable for the user's environment. <br>
Risk: OCR quality can be poor on blurry, low-resolution, or unsupported images. <br>
Mitigation: Ask the user to provide a clearer image or rescan before relying on extracted text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/violet17/image-ocr-local-aipc) <br>
- [llama.cpp releases](https://github.com/ggml-org/llama.cpp/releases) <br>
- [GLM-OCR GGUF model](https://huggingface.co/ggml-org/GLM-OCR-GGUF) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text, Markdown tables, JSON snippets, and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May preserve original image layout or return structured fields for receipts, tables, business cards, IDs, and documents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
