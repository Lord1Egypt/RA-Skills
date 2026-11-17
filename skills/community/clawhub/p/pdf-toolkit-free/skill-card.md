## Description: <br>
Pdf Toolkit Free helps agents perform common PDF tasks such as creating, editing, converting, merging, splitting, compressing, encrypting, OCR extraction, and table extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through everyday PDF processing tasks, including text extraction, watermarking, conversion, encryption, and single-file workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to run shell commands and write PDF output files. <br>
Mitigation: Use it only when shell execution and file writing are acceptable, keep outputs in a specific folder, and require confirmation before overwriting or deleting files. <br>
Risk: The optional callback_url parameter can send processing notifications or data to an external destination. <br>
Mitigation: Use callback_url only with destinations you control, and avoid it for sensitive documents. <br>
Risk: The server security verdict is suspicious because file, shell, and callback capabilities are under-scoped. <br>
Mitigation: Review the skill before installation and restrict execution to the intended PDF workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pdf-toolkit-free) <br>
- [SkillHub homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and inline Python or shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce PDF output files and structured JSON-style execution results when the agent runs the proposed workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
