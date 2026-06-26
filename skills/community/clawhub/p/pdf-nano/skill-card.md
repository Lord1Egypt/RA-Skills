## Description: <br>
Provides PDF processing guidance and helper scripts for reading, extracting, combining, splitting, rotating, creating, filling, encrypting, decrypting, image extraction, and OCR workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[climbkim](https://clawhub.ai/user/climbkim) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, engineers, and document automation users use this skill to inspect, extract, transform, generate, and fill PDF documents through Python snippets, helper scripts, and command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A form-filling path can make persistent font and font-cache changes on the host system. <br>
Mitigation: Review or disable the annotation form-filling font behavior before use, and run the skill without elevated privileges. <br>
Risk: PDF workflows may overwrite outputs, alter documents, or decrypt files. <br>
Mitigation: Work on copies of important PDFs and only decrypt documents you are authorized to access. <br>


## Reference(s): <br>
- [PDF Processing Guide](artifact/SKILL.md) <br>
- [PDF Forms Workflow](artifact/forms.md) <br>
- [PDF Processing Advanced Reference](artifact/reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/climbkim/pdf-nano) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, JavaScript, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to create or modify local PDF, image, text, JSON, spreadsheet, and validation files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
