## Description: <br>
Uses miaoda-studio-cli image-understanding to describe, question, analyze, and extract information from local image files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nice1234-h](https://clawhub.ai/user/nice1234-h) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need an agent to inspect a local image, answer targeted questions about it, extract visible text, or return image-analysis results in text or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images submitted for analysis may contain confidential screenshots, IDs, documents, or private photos and are processed through an external AI CLI. <br>
Mitigation: Use only intentionally selected images and avoid sensitive content unless that external image processing is acceptable. <br>
Risk: Vague prompts or mismatched document inputs can produce unhelpful or incorrect analysis. <br>
Mitigation: Ask specific image-focused questions and use a document parsing workflow for PDF or Word files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nice1234-h/miaoda-image-understanding) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI output can be text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local image path and can accept an optional prompt and output format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
