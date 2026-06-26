## Description: <br>
Uses Ollama's local vision/OCR models to recognize text from images without relying on cloud APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to extract text from local image files, screenshots, and sensitive images through a locally controlled Ollama vision model instead of a cloud OCR service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images are sent to the configured local HTTP Ollama endpoint. <br>
Mitigation: Confirm that 172.17.0.2:11434 reaches a trusted local Ollama instance before processing sensitive images. <br>
Risk: Model tags such as latest can change behavior over time. <br>
Mitigation: Pin trusted model versions when repeatable OCR behavior is required. <br>
Risk: OCR output can be inaccurate or repetitive depending on the selected vision model and image quality. <br>
Mitigation: Review extracted text before using it in downstream decisions or records. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Plain text OCR results, with optional Markdown guidance and Python or shell examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running local Ollama endpoint and a downloaded vision/OCR model; the bundled helper uses a 120 second request timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
