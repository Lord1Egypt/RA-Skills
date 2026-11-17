## Description:

Convert PDF, DOC, DOCX, and PPTX office documents to Markdown with legacy .doc text extraction and basic formatting preservation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkyyyy320](https://clawhub.ai/user/lkyyyy320)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to convert office documents into Markdown for reading, analysis, and downstream agent workflows. It is most relevant when extracting text from PDFs, Word documents, legacy .doc files, or PowerPoint presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PPTX conversion may run shell commands from crafted filenames.

Mitigation: Convert only trusted PPTX files in a constrained workspace, normalize filenames before conversion, and do not run the skill with privileged accounts.

Risk: The skill may install Python packages automatically during conversion.

Mitigation: Install dependencies explicitly in a controlled environment before use and restrict unexpected package installation during conversion.

Risk: Converted Markdown, previews, logs, or agent responses may expose source document content.

Mitigation: Avoid confidential files unless logs and agent responses are controlled, and handle generated Markdown as document content.

Risk: Generated .md files may collide with existing Markdown files beside the source document.

Mitigation: Check for existing .md output paths before conversion and run the skill in a workspace where overwrites can be reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lkyyyy320/skills/office-to-md-v2)
- [OpenClaw Office to Markdown documentation](https://docs.openclaw.ai/skills/office-to-md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown files with console text and structured conversion status objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a .md file next to the input document; the wrapper can also return converted Markdown, a preview, file type, and line, character, and word statistics.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
