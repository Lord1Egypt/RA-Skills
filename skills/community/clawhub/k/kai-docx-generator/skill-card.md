## Description: <br>
Generate professional .docx documents from Markdown text or fill data into .docx templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaisersong](https://clawhub.ai/user/kaisersong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and document workflow users use this skill to convert Markdown into styled Word documents, fill existing .docx templates with structured data, and validate generated .docx structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Word templates, DOCX files, and embedded images from unknown sources can carry normal local file parsing risks. <br>
Mitigation: Process only trusted inputs where possible, keep dependencies patched, and prefer a lockfile for reproducible dependency versions. <br>
Risk: Broad document-related triggers may route unrelated document tasks to this skill. <br>
Mitigation: Invoke the skill only for Word/DOCX generation, template filling, or DOCX validation tasks. <br>
Risk: Template filling may leave placeholders unresolved when input data is incomplete. <br>
Mitigation: Use strict template filling or run the validation command before relying on generated documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaisersong/kai-docx-generator) <br>
- [Style presets reference](references/style-presets.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands that produce .docx files and validation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts are Word .docx files; validation may report document structure, XML parseability, file size, and unreplaced template placeholders.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
