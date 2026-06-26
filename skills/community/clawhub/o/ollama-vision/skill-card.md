## Description: <br>
Ollama Vision uses a local Ollama qwen3-vl:4b vision model to describe images, extract text with OCR, and return custom image analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LZM2023](https://clawhub.ai/user/LZM2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to analyze local image files through Ollama while keeping the primary conversation model separate. It is useful for image description, OCR, and targeted extraction from screenshots, documents, and photos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image analysis may involve confidential local images and local Ollama behavior outside the skill package. <br>
Mitigation: Use the skill only with images appropriate for the local Ollama installation, its logging or retention behavior, and other users or processes on the same machine. <br>
Risk: First use may download a multi-gigabyte qwen3-vl:4b model and depends on local Ollama availability. <br>
Mitigation: Confirm Ollama is installed, running, and approved for local model downloads before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LZM2023/ollama-vision) <br>
- [Publisher profile](https://clawhub.ai/user/LZM2023) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may contain image descriptions, OCR text, or custom extracted information; images larger than 2 MB may be compressed before analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
