## Description: <br>
GPU-accelerated document parsing and OCR via PaddleOCR-VL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessy-huang](https://clawhub.ai/user/jessy-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to OCR image files, parse screenshots and document images, and extract text or layout-aware document content through a local MCP server backed by PaddleOCR-VL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Docker container receives broad local and network access. <br>
Mitigation: Review before installing and prefer a revised version that disables host networking, avoids root, and mounts only the target file read-only. <br>
Risk: OCR runs on user-provided local file paths. <br>
Mitigation: Use only trusted file paths and avoid files with unusual or attacker-controlled filenames. <br>
Risk: The skill depends on external Docker images for local execution. <br>
Mitigation: Use only trusted images and verify the pulled image before processing sensitive documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jessy-huang/paddle-ocr-vl) <br>
- [Publisher profile](https://clawhub.ai/user/jessy-huang) <br>
- [Homepage](https://github.com/user/paddle-ocr-vl-skill) <br>
- [PaddleOCR-VL documentation](https://www.paddleocr.ai/latest/version3.x/pipeline_usage/PaddleOCR-VL.html) <br>
- [PaddleOCR-VL Blackwell documentation](https://www.paddleocr.ai/latest/version3.x/pipeline_usage/PaddleOCR-VL-NVIDIA-Blackwell.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown setup guidance and JSON-formatted OCR results from MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Docker-based OCR and returns environment checks, setup guidance, demo results, or extracted text.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
