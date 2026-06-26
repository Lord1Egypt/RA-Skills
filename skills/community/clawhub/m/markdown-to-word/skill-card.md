## Description: <br>
Convert a Markdown file or raw Markdown string into a polished Word DOCX document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mutour](https://clawhub.ai/user/mutour) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and agents use this skill to convert Markdown files or raw Markdown strings into Word DOCX documents with built-in or custom reference templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes to a user-selected DOCX output path and could overwrite an important file if that path is chosen incorrectly. <br>
Mitigation: Review the output path before running the conversion. <br>
Risk: The skill reads user-provided Markdown, template, metadata, and resource paths. <br>
Mitigation: Use trusted Markdown and templates when possible and provide only the files needed for the conversion. <br>
Risk: The converter depends on pandoc being installed and available on PATH. <br>
Mitigation: Confirm pandoc is installed before invoking the conversion command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mutour/markdown-to-word) <br>
- [Example Markdown](assets/examples/sample.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated DOCX file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local Markdown, template, metadata, and resource paths provided by the user and writes the chosen DOCX output path.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
